"""PROJECT_LOG 事件格式的共享解析器；不读取文件或终止调用方进程。"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


ENTRY_RE = re.compile(
    r"^## \[(?P<date>\d{4}-\d{2}-\d{2})\]\s+(?P<type>[^|\n]+?)\s*\|\s*(?P<summary>[^\n]+)$",
    re.MULTILINE,
)

class LogFormatError(ValueError):
    def __init__(self, source_file: str, source_line: int) -> None:
        self.source_file = source_file
        self.source_line = source_line
        super().__init__(f"{source_file}:{source_line} 日志事件格式错误：应使用 ## [日期] 类型 | 摘要")


@dataclass(frozen=True)
class Entry:
    event_date: str
    event_type: str
    summary: str
    content: str
    source_file: str
    source_line: int

    @property
    def entry_hash(self) -> str:
        return hashlib.sha256(self.content.encode("utf-8")).hexdigest()


def parse_entries(text: str, source_file: str) -> tuple[str, list[Entry]]:
    for line_number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^(?:#{1,6}\s*)?\[\d{4}-\d{2}-\d{2}\].*\|", line) and not ENTRY_RE.fullmatch(line):
            raise LogFormatError(source_file, line_number)
    matches = list(ENTRY_RE.finditer(text))
    if not matches:
        return text.rstrip() + "\n", []

    preamble = text[: matches[0].start()].rstrip() + "\n"
    entries: list[Entry] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[match.start() : end].strip() + "\n"
        entries.append(
            Entry(
                event_date=match.group("date"),
                event_type=match.group("type").strip().lower(),
                summary=match.group("summary").strip(),
                content=content,
                source_file=source_file,
                source_line=text.count("\n", 0, match.start()) + 1,
            )
        )
    return preamble, entries
