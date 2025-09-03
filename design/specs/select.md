## Component Spec: Select (Listbox/Combobox)

### Purpose
Choose one option from a list with full keyboard and screen reader support.

### Variants
- native select, custom combobox (autocomplete), single-select listbox

### Props (contract)
```json
{
  "component": "Select",
  "props": {
    "id": {"type": "string", "required": true},
    "options": {"type": "Array<{label:string,value:string,disabled?:boolean}>", "required": true},
    "value": {"type": "string | null", "required": false},
    "placeholder": {"type": "string | null", "default": null},
    "disabled": {"type": "boolean", "default": false},
    "combobox": {"type": "boolean", "default": false}
  }
}
```

### States
- closed, open, focused, disabled

### Accessibility
- Native: `<select>` preferred when possible
- Custom: `role="combobox"` with `aria-expanded`, `aria-controls` to listbox; options as `role="option"`
- Use roving tabindex for listbox; announce selection changes via SR

### Keyboard (custom)
- Alt/ArrowDown or Enter opens; Esc closes
- ArrowUp/ArrowDown moves active option; Enter/Space selects
- Typeahead (letters jump to matching option)

### Interaction Spec (JSON)
```json
{
  "component": "Select",
  "variants": ["native","combobox","listbox"],
  "states": ["closed","opening","open","closing","disabled"],
  "keyboard": {"Alt+ArrowDown":"open","Enter":"open/select","Esc":"close","ArrowUp":"prev","ArrowDown":"next","Type":"typeahead"},
  "aria": {"role":"combobox","aria-expanded":"reflects open","aria-controls":"links listbox id"},
  "timings_ms": {"open":180,"close":120},
  "tokens": {"focus_ring":"{a11y.focus.ring_color_light}","radius":"{radii.sm}","motion":"{motion.duration_ms.quick}"}
}
```

