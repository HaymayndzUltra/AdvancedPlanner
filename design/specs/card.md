## Component Spec: Card

### Purpose
Container for grouped content with optional header, body, and footer actions.

### Structure
- Header (title, meta)
- Body (content)
- Footer (actions)

### Props (contract)
```json
{
  "component": "Card",
  "props": {
    "elevation": {"type": "'surface'|'raised'|'overlay'", "default": "raised"},
    "interactive": {"type": "boolean", "default": false}
  }
}
```

### Visual and Tokens
- Background: `{modes.light.color.role.surface}` with `shadow.level_1` for raised
- Radius: `{radii.lg}`; Spacing: `{spacing.scale_px}`

### Accessibility
- If interactive, render as `button` or link with correct role and keyboard handling
- Maintain 4.5:1 contrast for text and controls inside

