# docs-governance

> A documentation-governance plugin for Claude Code, Codex, and ChatGPT. It keeps long-running AI-assisted projects understandable by separating project rules, structure, current state, and history—and by checking that those documents do not silently drift from the codebase.

[中文 README](README.md) · [Usage guide](使用说明.md) · [Contributing](CONTRIBUTING.md)

## Try it in three minutes

Install it in Claude Code:

```text
/plugin marketplace add Seekers2001/docs-governance
/plugin install docs-governance@docs-governance
```

Then open an existing project and run a read-only audit:

```text
/governance-audit
```

Or in Codex / ChatGPT:

```text
$docs-governance audit the current project in read-only mode and recommend the smallest useful next step
```

The first output is a report, not an automatic rewrite. Confirm the findings before using `/governance` or a focused skill to change project documents.

## What it provides

### A thin documentation spine

| Document | Single responsibility |
| --- | --- |
| `CLAUDE.md` | durable rules and entry points |
| `CLAUDE_MAP.md` | non-obvious structure, dependency directions, and traps |
| `PROJECT_STATUS.md` | current health, risks, and priorities |
| `PROJECT_LOG.md` | append-only project history |

The point is not to create four documents in every repository. Use them progressively: a small project can stay small, while a long-running project gains a stable handoff surface for humans and agents.

### Focused workflows

- **Living documentation**: initialize, audit, and synchronize the documentation spine.
- **Context and decisions**: keep stable domain language in `CONTEXT.md`; record high-cost-to-reverse decisions as ADRs.
- **Change impact**: inspect code, data, contracts, tests, docs, deployment, and rollback before and after a risky change.
- **Contract-first collaboration**: use one machine-readable-friendly `CONTRACT.md` as the shared source of truth for frontend/backend or multi-service work.
- **Test collaboration**: register requirements, risks, and fixed bugs as TEST-IDs with durable evidence.
- **Module regression**: maintain downstream consumers and executable regression commands for modules that can break each other.

## Why it exists

AI makes code cheap to regenerate, but project intent and verification evidence become easier to lose. A README can become stale, an architecture decision can lose its rationale, and a new agent can repeatedly rediscover the same structure.

docs-governance treats project documentation as a small system with one owner per fact, graded reading instead of loading everything every session, and read-only checks before edits.

## Evidence and safety boundaries

- Audits are read-only by default.
- The plugin does not require a database for ordinary projects. Markdown stays the source of truth; the optional SQLite index is rebuildable and gitignored.
- Task assignment and schedules stay in the repository's existing tracker (for example GitHub Issues or Linear), rather than being copied into governance documents.
- The repository is dogfooded on real projects and its own structure check runs via `bash scripts/verify.sh`.

## Development

```bash
bash scripts/verify.sh
```

Run this before submitting a change. The check validates manifests, references, hooks, Python syntax, and unit tests.

## License

[MIT](LICENSE) · [Seekers2001](https://github.com/Seekers2001)
