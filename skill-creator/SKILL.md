---
name: skill-creator
description: Create or update Claude-style skills with a strict, repeatable structure. Use when a user asks to build a new skill, refactor an existing skill, add required sections, create references/tools/examples/subtasks, or validate that a skill conforms to the defined template and workflow.
argument-hint: PROMPT , SKILL_OUTPUT_LOCATION, SKILL_NAME
---

#  Skill Creator

## Purpose
- Act as a senior skill engineer that designs and builds high-quality skills with explicit structure, deterministic workflow, and validation. Use this skill when a user wants a new skill created, an existing skill improved, or a skill audited for format and execution clarity.

## Variables
PROMPT
SKILL_OUTPUT_LOCATION : `/root/[User Name]/workspace/skills/[SKILL_NAME]`
SKILL_NAME : [you decide if not provided]

## Instructions
- Read the request in `PROMPT`, design the smallest complete skill that solves it, and implement it with strict folder conventions, explicit workflow steps, and concrete expected outputs. Prefer clarity over verbosity. Create only the files required for execution quality (no placeholder docs, no unnecessary extras). If a workflow step is too large for reliable single-agent execution, split it into a constrained subtask file and explicitly instruct running it with a subagent.

## Workflow
1. Read and understand the guide on creating skills at `/references/skill_creation_guide.md`
2. Read `PROMPT` and infer target behavior, triggers, inputs, and outputs.
3. Ask the user 3 questions, 1 at a time, on how they want the skill made or on any ambiguities you want cleared up. Then take in and understand the responses.
4. Brainstorm possible ways to create this skill adhearing to the `/references/skill_creation_guide.md` and the answered questions
5. After reviewing possible options, determine the most precise and straightforward way to effectivly create the skill under the guidelines in the `/references/skill_creation_guide.md` and following the answered questions
6. Consider the size of each step in the workflow, think about if its so big or will require so many substeps that it may affect the quality of the agentic work you are doing due to context bloat. also think about if its such a large task that its somewhat unclear for any agent that would run it.
  - if either is true. brainstorm each of the steps needin substeps to come up with each subtask set of steps. then create the subtask md files under `root/[User Name]/workspace/skills/[skill name]/subtasks`.
7. Create skill directory at `SKILL_OUTPUT_LOCATION`.
8. Create only needed subfolders from this allowed set:
   - `references/` for docs/templates/schema/context loaded as needed.
   - `tools/` for executable scripts/utilities used by the skill workflow.
   - `examples/` for sample inputs/outputs if they improve reliability.
   - `subtasks/` for large isolated workflows delegated to subagents.
9. Create supporting files only when directly justified by workflow needs:
   - Add `references/*` for non-trivial domain constraints or policies.
   - Add `tools/*` only when deterministic execution is needed repeatedly.
   - Add `examples/*` only if they reduce ambiguity for future runs.
10. If subtasks need created:
   - Place files in `subtasks/`.
   - In the parent `SKILL.md`, reference exact subtask filename and full path.
   - Explicitly state: "when you reach this step spawn a subagent to run the subtask at [location of subagent file].
11. create the SKILL.md file in that folder adhearing to the `/references/skill_creation_guide.md`
12. verify that any workflow steps requiring a subtask clearly state to run the subtask steps with a SUBAGENT and reference the file name and location of the subtask md file.
13. verify the skill follows the guidelines at "/references/skill_creation_guide.md"
14. spawn a subagent to run a validation pass with pass/fail gates:
   - structure and section order correct,
   - frontmatter keys valid,
   - paths are absolute or clearly resolvable,
   - no contradictory folder rules,
   - all referenced files exist.
   - follows the guidelines of `/references/skill_creation_guide.md`
15. If validation fails, fix issues and re-run validation. 
16. Return a concise completion report: skill name, purpose, created files, and workflow summary.

## Expected Output
- a new skill folder in `root/[User Name]/workspace/skills`
- a SKILL.md file in that folder containing a skill that fits the format in the "[skill name]/references/skill_creation_guide.md"
- any code files or tools are contained in the [skill name]//tools folder
- any reference douments are contained in the [skill name]//references folder
- any subtask md files are contained in the [skill name]//subtasks folder
- the SKILL.md file contains all required subheaders from the "[skill name]/references/skill_creation_guide.md"
- if a subtask md file is present, it must be referenced in the correct workflow step within that skills SKILL.md file
- a returned response to the user that the skill has been created and explaining the steps it takes.

## Reference
- skill creation guide
  - reference this when creating a skill 
  - "/references/skill_creation_guide.md"