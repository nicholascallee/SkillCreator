---
description: Categorize uncategorized Actual Budget transactions using Claude's judgment
argument-hint: [--dry-run] [--limit N]
---

# Categorize Transactions

Categorize uncategorized transactions in Actual Budget. You (Claude) analyze each transaction and assign the best matching category from the user's existing categories.

## Variables

ARGS: $ARGUMENTS
SCRIPT_PATH: C:/Development/2026/ActualBudget/scripts/categorize-transactions.mjs
MAPPINGS_FILE: C:/Development/2026/ActualBudget/scripts/.last-categorization.json
DRY_RUN: (check if --dry-run is in ARGS)
LIMIT: (extract N from --limit N in ARGS, default 100)

## Workflow

### Step 1: Pre-flight Checks
- Parse ARGS for --dry-run flag and --limit N value
- Verify the script exists at SCRIPT_PATH. If not, tell the user: "Script not found. Run `cd C:/Development/2026/ActualBudget/scripts && npm install` first."
- Verify `C:/Development/2026/ActualBudget/scripts/.env` exists. If not, tell the user to create it with ACTUAL_SERVER_URL, ACTUAL_PASSWORD, and ACTUAL_SYNC_ID.

### Step 2: Fetch Transactions
- Run: `node SCRIPT_PATH fetch --limit LIMIT`
- Capture the stdout output as JSON
- If the command fails, show the error and stop
- If transactions array is empty, say "No uncategorized transactions found. Nothing to do." and stop
- Parse the JSON to get `categories` and `transactions` arrays

### Step 3: Analyze and Categorize
For each transaction in the list:
- Look at the `payee` name, `imported_payee` (raw bank description), `amount` (in cents, negative = expense, positive = income), `date`, and `notes`
- Select the single best matching category from the `categories` array
- Use common sense about merchant names, amounts, and patterns:
  - Grocery stores -> look for a groceries/food category
  - Restaurants -> dining/eating out category
  - Gas stations -> transportation/gas category
  - Streaming services -> subscriptions/entertainment
  - Payroll/salary -> income category
  - etc.
- If you truly cannot determine a category, mark it as skipped with a reason

Build two lists:
- `mappings`: array of `{"transactionId": "...", "categoryId": "..."}`
- `skipped`: array of `{"transactionId": "...", "payee": "...", "reason": "..."}`

### Step 4: Preview Table
Print a markdown table showing your proposed assignments:

| Date | Payee | Amount | -> Category | Reason |
|------|-------|--------|-------------|--------|

Format amounts as dollars (divide by 100, add $ sign, negative = expense).

If any transactions were skipped, list them separately.

If totalUncategorized > LIMIT, print:
"Note: Showing LIMIT of totalUncategorized uncategorized transactions. Run again to process more."

### Step 5: Dry Run Check
If DRY_RUN is true, print "DRY RUN: No changes applied." and stop here.

### Step 6: Confirm with User
Ask the user: "Apply these N categorizations? (yes/no)"
Wait for their response. If not "yes" or "y", print "Cancelled. No changes made." and stop.

### Step 7: Write Mappings File
Write the mappings JSON to MAPPINGS_FILE:
```json
{"mappings": [{"transactionId": "...", "categoryId": "..."}, ...]}
```

### Step 8: Apply
Run: `node SCRIPT_PATH apply MAPPINGS_FILE`
If it fails, show the error and tell the user the mappings file is saved at MAPPINGS_FILE for manual retry.

### Step 9: Report
Print a summary:
```
Categorization complete!
  Applied:  N transactions categorized
  Skipped:  N transactions (couldn't determine category)
  Tagged:   All categorized transactions tagged with #claude-code
  File:     MAPPINGS_FILE (saved for reference)
```
