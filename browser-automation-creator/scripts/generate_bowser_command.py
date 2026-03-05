#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

TARGET_DIR = Path('/home/openclaw/tools/bowser/.claude/commands/bowser')


def slugify(text: str, max_words: int = 6) -> str:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())[:max_words]
    slug = "-".join(words).strip('-')
    return slug or 'web-task'


def to_title(slug: str) -> str:
    return ' '.join(w.capitalize() for w in slug.split('-'))


def unique_path(base_slug: str) -> Path:
    path = TARGET_DIR / f"{base_slug}.md"
    if not path.exists():
        return path
    i = 2
    while True:
        candidate = TARGET_DIR / f"{base_slug}-{i}.md"
        if not candidate.exists():
            return candidate
        i += 1


def build_command_markdown(title: str, description: str) -> str:
    return f"""---
description: {description}
argument-hint: <task details or target url>
defaults:
  skill: playwright-bowser
  mode: headed
  vision: false
---

# {title}

Run this workflow via `hop-automate`.

## Variables

| Variable | Value               | Description |
| -------- | ------------------- | ----------- |
| SKILL    | `playwright-bowser` | Default browser automation stack (playwright agent) |
| MODE     | `headed`            | Visible browser mode |

## Workflow

1. Interpret `{{PROMPT}}` as the target browser objective.
2. Open the required website(s) and verify page load before interacting.
3. Execute the objective step-by-step with clear checks after each action.
4. If blocked by auth/captcha/permissions, stop and report the blocker clearly.
5. Perform any requested state-changing actions if explicitly required by `{{PROMPT}}`.
6. Capture key evidence from the page (critical fields, confirmations, statuses).
7. Return a concise report: actions taken, final state, and any follow-up needed.
"""


def main():
    parser = argparse.ArgumentParser(description='Generate a Bowser workflow command markdown file.')
    parser.add_argument('--prompt', required=True, help='Natural language browser automation objective.')
    parser.add_argument('--name', default=None, help='Optional command filename slug (without .md).')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite if name exists.')
    args = parser.parse_args()

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    base_slug = slugify(args.name) if args.name else slugify(args.prompt)
    if args.overwrite:
        path = TARGET_DIR / f"{base_slug}.md"
    else:
        path = unique_path(base_slug)

    description = f"Automate browser task: {args.prompt.strip()}"
    title = to_title(path.stem)

    content = build_command_markdown(title, description)
    path.write_text(content, encoding='utf-8')

    print(str(path))


if __name__ == '__main__':
    main()
