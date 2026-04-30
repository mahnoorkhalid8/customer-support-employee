# Incubation Phase - Source Code

This directory contains prototype code developed during the **Incubation Phase** (Hours 1-16).

## Purpose

Use this directory to:
- Experiment with agent responses
- Test different prompts and approaches
- Build quick prototypes
- Discover requirements and edge cases

## Structure

```
src/
├── channels/       # Channel integration prototypes
├── agent/          # Agent logic experiments
└── web-form/       # Web form prototypes
```

## Guidelines

1. **Iterate Quickly**: Don't worry about production quality here
2. **Document Discoveries**: Note what works and what doesn't
3. **Test Edge Cases**: Try unusual inputs and scenarios
4. **Capture Learnings**: Document findings in `specs/discovery-log.md`

## Transition to Production

Once you've validated your approach:
1. Document requirements in `specs/`
2. Implement production version in `production/`
3. Keep prototypes here for reference

## Example Workflow

```python
# src/agent/prototype_v1.py
# Quick experiment with agent responses

def handle_customer_query(query, channel):
    # Test different response styles
    if channel == "whatsapp":
        return f"Hi! {query[:50]}..."
    else:
        return f"Dear Customer,\n\n{query}\n\nBest regards"

# Test it
print(handle_customer_query("How do I reset password?", "email"))
print(handle_customer_query("How do I reset password?", "whatsapp"))
```

## Notes

- This code is **not** used in production
- Focus on learning and discovery
- Move validated code to `production/` directory
