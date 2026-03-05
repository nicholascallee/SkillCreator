---
name: browser-automation-creator
description: Create Bowser workflow command files in /home/openclaw/tools/bowser/.claude/commands/bowser from a single natural-language browser automation prompt. Use when user asks to make a Bowser command/workflow that runs through hop-automate. Defaults generated commands to playwright-bowser (playwright agent stack).
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: >-
            uv run /root/.openclaw/Workspace/skills/skill_browser-automation-creator/hooks/validators/validator_markdown_required_sections.py
---

# Browser Automation creator

## Purpose
- to create a command for hop-automate to use that is a specific set of browser automation steps. This skill creates these commands in a very particular way to achieve a reusable browser automation skill that works.

## Instructions
- read the users command, understand and ask questions if needed, then review reference info on skill creation so you can create the skill precicly in the required format. Then create the skill, run, and fix if it does not work. work fixes until completion and then report the skill name and steps in the command.

## Trigger and non-trigger conditions

Trigger when:
- User asks to create a Bowser browser automation command/workflow.

Do not trigger when:
- User only asks to run an existing Bowser command.
- User asks for non-Bowser skill package generation.

## Inputs and outputs

Inputs:
- required: one natural-language browser objective prompt
- optional: filename slug override

Outputs:
- you will have ran the skill by starting a new terminal and calling: 
  "cd /home/openclaw/tools/bowser && claude --dangerously-skip-permissions /hop-automate [insert name of new command here]"
- one new command markdown file in `/home/openclaw/tools/bowser/.claude/commands/bowser`
- format compatible with `/home/openclaw/tools/bowser/.claude/commands/bowser/hop-automate.md`
- default skill being used (mentioned in the command itself after generating on step 3) `/home/openclaw/tools/bowser/.claude/skills/playwright-bowser`

## Workflow (COMPLETE ALL STEPS)

1. read and review '/home/openclaw/tools/bowser/.claude/commands/bowser/hop-automate.md'
1. Fully understand the users prompt and Extract the request. If the request is unclear or you need more context, you can ask up to 3 questions to the user DURING THIS STEP ONLY.
2. Optionally extract command name if explicitly provided; otherwise auto-generate slug.
3. Run:

```bash
python3 /root/.openclaw/workspace/skills/bowser_automation_creator/scripts/generate_bowser_command.py --prompt "<objective>" --name "<slug>"
```

4. Read generated file and verify:
- frontmatter exists with `description`, `argument-hint`, and `defaults`
- defaults include:
  - `skill: playwright-bowser`
  - `mode: headed`
  - `vision: false`
- includes `{PROMPT}` placeholder in workflow steps

5. read and review the specifics for and example of a correctly created skill at: `/root/.openclaw/Workspace/skills/bowser_automation_creator/references/bowser-command-format.md`
6. plan out a concise set of steps you believe will solve the job.
7. create the command md file with the correct formatting and the steps you just determined would do the job.
8. run: `/hop-automate [insert name of new command here]`
9. verify the ran command completes as expected
10. if the command did not complete the full set of steps you wrote, brainstorm a solution and fix it, then retest and continue fixing until it works.
11. validate the creation of the command with `/root/.openclaw/Workspace/skills/bowser_automation_creator/tests/smoke-checklist.md`
12. Return created file path and the set of steps you generated in the file


## Failure handling

- If target directory is missing, create it.
- If prompt is empty, stop and ask the user for a prompt.
- If failures occur During step 8,9, and 10, always investigate why and attempt to resolve the issue
- If the run on step 8 does not get to the intended page or perform the intended set of steps in the command being ran, investigate why and attempt to resolve the issue, then reattempt, and solve any remaining issues until it works.
- If the workflow requires the user to be logged into an account, ask them to log in once, then use that login to perform the command.

## Validation

- Run `/root/.openclaw/Workspace/skills/bowser_automation_creator/tests/smoke-checklist.md` before finalizing.
- Output must be a `.md` command file inside `/root/.openclaw/Workspace/commands/bowser`.