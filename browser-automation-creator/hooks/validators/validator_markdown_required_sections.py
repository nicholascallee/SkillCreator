# Use this validator on PostToolUse when generated markdown artifacts must include required sections like a title and workflow.
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = ["# ", "## Workflow"]


def heading_present(content: str, heading: str) -> bool:
    if heading == "# ":
        return any(line.startswith("# ") for line in content.splitlines())
    return heading in content


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path.endswith(".md"):
            sys.exit(0)

        p = Path(file_path)
        if not p.exists():
            sys.exit(0)

        content = p.read_text(encoding="utf-8", errors="ignore")
        missing = [h for h in REQUIRED_HEADINGS if not heading_present(content, h)]

        # Log every checked event
        log_dir = Path.cwd() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "post_tool_use_markdown_sections.json"
        try:
            existing = json.loads(log_path.read_text()) if log_path.exists() else []
        except Exception:
            existing = []
        existing.append(
            {
                "file": str(p),
                "tool": tool_name,
                "missing": missing,
                "status": "blocked" if missing else "pass",
            }
        )
        log_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")

        if missing:
            print(
                "BLOCKED: Markdown validation failed. Missing required sections: "
                + ", ".join(missing),
                file=sys.stderr,
            )
            sys.exit(2)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
