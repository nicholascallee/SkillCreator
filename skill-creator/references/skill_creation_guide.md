# Guide to creating a claude code skill with a very specific and refined structure

## File Structure
- skills should always be created at: root/openclaw/workspace/skills
- each skill gets its own folder
- each skill contains a SKILL.md file
- any example files go in /examples
- any files that will get ran go in /tools
- any templates or documentation for reference go in /references
- subtasks can be created in the subtasks folder to isolate context for steps that are large or would degrade the context enough to impact the quality of the outcome
- example structure:
    ```
       [skill name goes here]/
        SKILL.md
        references/
        tools/
        subtasks/
        examples/
    ```

## Requirements
- a SKILL.md file has to have a yaml header that fits the specifications of a CLAUDE code Skill
    - example:
        '''
            ---
            name: [name with no spaces goes here]
            description: [description goes here].
            argument-hint: [list any variables here]
            ---
        '''
- a SKILL.md file should have follow this exact format (unless marked optional) in this exact order:
    -'''
        # <add the title here>

        ## Purpose
            <a short explaination of 1: who to act as to accomplish the task, 2: what the skill is for, and 3: when its used>
        ## Variables
            <any variables that the skill will take in. All caps and 1 variable per line>
        ## Prerequisites (optional)
            <any required data or anything needing done before starting. add any hard pre skill run validation checks here>
        ## Instructions
            <a paragraph style explanation of what the skill will do and how>
        ## Workflow
            <numbered steps the agent must perform in order. will include every detail on how to accomplish the task>
        ## Expected Output
            <a bulleted list of critical outcomes that can be used to validate the completion of the skill>
        ## Reference (optional)
            <any information or locations of files that need to be referenced during the workflow will be listed here>
        ## Troubleshooting (optional)
            <if statements which speficy how to resolve any issues that may arise during the workflow>
     '''

## Sub tasks
- when a single step in the workflow is large enough that the context will degrade the quality of the individual skill, a subtask file should be created and the step should specify to run the subtask with a new subagent.
- subtask files are markdown files that are structured the same way as a skill. they are essentially a subskill that is contained within the tools folder of the top level skill being created.
- subtasks should be heavily constrained and follow all the same guidelines as the skill that its being ran under.

## Composition rules
- A skill can orchestrate commands, subagents, tools, and output styles.
- Hooks are optional and should enforce policy and validation, not fuzzy reasoning.
- Keep orchestration explicit where order matters.