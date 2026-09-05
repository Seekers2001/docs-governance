import json
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dual-agent-review-loop.py"


class DualAgentReviewLoopTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name)
        (self.project / ".git").mkdir()
        self.document = self.project / "proposal.md"
        self.document.write_text("# 方案\n\n初始正文。\n", encoding="utf-8")
        self.bin_dir = self.project / "bin"
        self.bin_dir.mkdir()
        self.calls = self.project / "calls.log"
        self._write_fake("claude", "Claude 通过")
        self._write_fake("codex", "Codex 通过")

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_fake(self, name, message):
        path = self.bin_dir / name
        path.write_text(
            "#!/bin/sh\n"
            f"echo {name} >> \"$CALLS_FILE\"\n"
            f"printf 'VERDICT: PASS\\n{message}\\n'\n",
            encoding="utf-8",
        )
        path.chmod(0o755)

    def run_loop(self, *extra):
        env = os.environ.copy()
        env["CLAUDE_BIN"] = str(self.bin_dir / "claude")
        env["CODEX_BIN"] = str(self.bin_dir / "codex")
        env["CALLS_FILE"] = str(self.calls)
        env["REVIEW_DOCUMENT"] = str(self.document)
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.document), *extra],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_reviews_change_and_skips_unchanged_document(self):
        first = self.run_loop("--max-rounds", "2")
        self.assertEqual(first.returncode, 0, first.stderr)
        reviewed = self.document.read_text(encoding="utf-8")
        self.assertIn("## 双 Agent 自动评审", reviewed)
        self.assertIn("最终状态：**双方通过**", reviewed)
        self.assertEqual(self.calls.read_text(encoding="utf-8").splitlines(), ["claude", "codex"])

        second = self.run_loop()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("无正文变化", second.stdout)
        self.assertEqual(self.calls.read_text(encoding="utf-8").splitlines(), ["claude", "codex"])

        source = reviewed.replace("初始正文。", "正文已修改。")
        self.document.write_text(source, encoding="utf-8")
        third = self.run_loop()
        self.assertEqual(third.returncode, 0, third.stderr)
        self.assertEqual(
            self.calls.read_text(encoding="utf-8").splitlines(),
            ["claude", "codex", "claude", "codex"],
        )

        state = json.loads(
            (self.project / ".git" / "dual-agent-review-proposal.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["status"], "双方通过")

    def test_edit_during_review_is_preserved_and_retried(self):
        fake = self.bin_dir / "codex"
        fake.write_text(
            '#!/bin/sh\nprintf "# 用户保存的新正文\\n" > "$REVIEW_DOCUMENT"\n'
            'printf "VERDICT: PASS\\n通过\\n"\n', encoding="utf-8"
        )
        result = self.run_loop()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.document.read_text(encoding="utf-8"), "# 用户保存的新正文\n")
        self.assertIn("正文已变化", result.stderr)
        self.assertFalse((self.project / ".git/dual-agent-review-proposal.json").exists())
        self._write_fake("codex", "通过")
        retried = self.run_loop()
        self.assertEqual(retried.returncode, 0, retried.stderr)
        self.assertIn("# 用户保存的新正文", self.document.read_text(encoding="utf-8"))

    def test_document_deleted_during_review_is_not_recreated(self):
        (self.bin_dir / "codex").write_text(
            '#!/bin/sh\nrm "$REVIEW_DOCUMENT"\nprintf "VERDICT: PASS\\n通过\\n"\n',
            encoding="utf-8",
        )
        result = self.run_loop()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.document.exists())
        self.assertFalse((self.project / ".git/dual-agent-review-proposal.json").exists())


if __name__ == "__main__":
    unittest.main()
