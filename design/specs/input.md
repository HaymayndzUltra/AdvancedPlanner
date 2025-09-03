## Component Spec: Text Input

### Purpose
Capture short-form textual data with validation feedback and clear labeling.

### Variants
- default, password, withIcon, invalid

### Sizes
- sm, md, lg

### Props (contract)
```json
{
  "component": "Input",
  "props": {
    "id": {"type": "string", "required": true},
    "type": {"type": "'text'|'email'|'password'", "default": "text"},
    "value": {"type": "string", "required": true},
    "placeholder": {"type": "string", "required": false},
    "size": {"type": "'sm'|'md'|'lg'", "default": "md"},
    "disabled": {"type": "boolean", "default": false},
    "required": {"type": "boolean", "default": false},
    "invalid": {"type": "boolean", "default": false},
    "ariaDescribedBy": {"type": "string | null", "default": null}
  }
}
```

### States
- default, focus, disabled, invalid

### Visual and Tokens
- Border: `{modes.light.color.role.border}`; Focus ring: `{a11y.focus.ring_color_light}`
- Radius: `{radii.sm}`; Spacing for padding: `{spacing.scale_px}`

### Accessibility
- Label must be associated via `<label for>` and matching `id`
- `aria-invalid=true` when invalid; helper text tied via `aria-describedby`
- Ensure programmatic name is present via label or `aria-label`

### Keyboard
- Typing inserts characters; Enter submits in forms; Esc clears if implemented

### Interaction Spec (JSON)
```json
{
  "component": "Input",
  "states": ["default","focus","disabled","invalid"],
  "keyboard": {"Tab":"focus next","Shift+Tab":"focus prev","Enter":"submit form"},
  "aria": {"role":"textbox","aria-invalid":"reflects invalid","aria-required":"reflects required"},
  "timings_ms": {"focus":0},
  "tokens": {"focus_ring":"{a11y.focus.ring_color_light}","radius":"{radii.sm}"}
}
```

### Validation Messaging
- Error text appears below input; color uses `{modes.light.color.palette.semantic.error}`; announce via ARIA live polite

