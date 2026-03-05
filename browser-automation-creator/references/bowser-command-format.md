# Bowser Command Format Reference

Target location:
`/home/openclaw/tools/bowser/.claude/commands/bowser/`

Generated file must include:

1. YAML frontmatter:
- `description`
- `argument-hint`
- `defaults.skill = playwright-bowser`
- `defaults.mode = headed`
- `defaults.vision = false`

2. Markdown body sections:
- Title (`# ...`)
- Variables table
- Workflow numbered steps

3. Workflow compatibility:
- Must use `{PROMPT}` placeholder so `hop-automate` can inject runtime task details.
- Should be runnable as:
`/hop-automate <workflow-name> "<task details>"`

## EXAMPLE:

'''

    ---
    description: Search Amazon, add item(s) to cart, proceed to checkout, stop
    argument-hint: <item to search for>
    ---

    # Amazon Add to Cart

    Search Amazon for an item(s), add it/them to cart, and proceed to checkout without submitting the order.

    ## Variables

    | Variable | Value           | Description                                         |
    | -------- | --------------- | --------------------------------------------------- |
    | SKILL    | `playwright-bowser` | playwright browser |
    | MODE     | `headed`        | Visible browser                                     |

    ## Workflow

    1. Navigate to https://www.amazon.com
    2. Verify the homepage loads (look for the search bar)
    3. Search for: {PROMPT}
    4. Verify search results appear
    5. Click into the first relevant result
    6. Verify the product detail page loads with title, price, and "Add to Cart" button
    7. Click "Add to Cart"
    8. Verify the cart confirmation appears (look for "Added to Cart" or cart count increment)
    9. Click "Proceed to checkout" or navigate to the cart
    10. Verify the checkout page loads with the item visible
    11. STOP — do not submit the order
    12. Report: item name, price, and confirmation that it reached checkout

'''