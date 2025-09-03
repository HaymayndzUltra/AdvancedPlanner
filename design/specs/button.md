## Component Spec: Button

### Purpose
Action trigger for primary and secondary operations with clear affordances and inclusive interaction.

### Variants
- primary, secondary, tertiary, destructive

### Sizes
- sm, md, lg

### Props (contract)
```json
{
  "component": "Button",
  "props": {
    "variant": {"type": "'primary'|'secondary'|'tertiary'|'destructive'", "default": "primary"},
    "size": {"type": "'sm'|'md'|'lg'", "default": "md"},
    "disabled": {"type": "boolean", "default": false},
    "loading": {"type": "boolean", "default": false},
    "iconLeading": {"type": "Icon | null", "default": null},
    "iconTrailing": {"type": "Icon | null", "default": null},
    "ariaLabel": {"type": "string | null", "default": null},
    "onClick": {"type": "(event) => void", "required": false}
  }
}
```

### States
- default, hover, focus, active, disabled, loading

### Visual and Tokens
- Background (primary): `{modes.light.color.palette.primary.500}`; text: `{modes.light.color.role.text_on_primary}`
- Focus ring: `{a11y.focus.ring_color_light}` width `{a11y.focus.ring_width}`
- Radii: `{radii.md}`; Motion durations: `{motion.duration_ms.base}`

### Accessibility
- Role: `button`; `aria-disabled` when disabled; `aria-busy` when loading
- Size: min touch target iOS 44pt / Android 48dp
- Focus visible at all times; focus order respects DOM

### Keyboard
- Tab / Shift+Tab: moves focus
- Enter / Space: activates press
- Escape: no-op (unless handled by container, e.g., closing a modal)

### Interaction Spec (JSON)
```json
{
  "component": "Button",
  "variants": ["primary","secondary","tertiary","destructive"],
  "sizes": ["sm","md","lg"],
  "states": ["default","hover","focus","active","disabled","loading"],
  "keyboard": {"Tab":"focus next","Shift+Tab":"focus prev","Enter":"activate","Space":"activate"},
  "aria": {"role":"button","aria-disabled":"reflects disabled","aria-busy":"reflects loading"},
  "timings_ms": {"hover":120,"press_in":80,"press_out":120},
  "tokens": {"focus_ring":"{a11y.focus.ring_color_light}","radius":"{radii.md}","motion":"{motion.duration_ms.base}"}
}
```

### States Matrix (visual guidance)
- Hover: elevate by `shadow.level_1`; Active: darken background by ~6% (primary)
- Disabled: 50% opacity text/icon; no elevation; cursor not-allowed
- Loading: show spinner, set `aria-busy=true`, keep width stable

### Contrast
- Ensure label to background ≥ 4.5:1 in light and dark; destructive variant follows same rule

### Traceability
- Tokens coverage: see `design/tokens/core.tokens.json` → `coverage_map.Button`
- PRD refs: AC-UX-1 (contrast, a11y), AC-UX-2 (keyboard navigation)

