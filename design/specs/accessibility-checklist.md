## Accessibility Checklist — WCAG 2.2 AA

### Scope
Applies to Button, Input, Select, Card, Modal.

### Principles & Success Criteria

- Perceivable
  - Text alternatives (1.1.1): All non-text content has `alt` or `aria-label`
  - Adaptable (1.3.x): Semantic landmarks; proper headings; labels associated to inputs
  - Distinguishable (1.4.x): Contrast ratios met; focus visible
    - Small text ≥ 4.5:1; large text ≥ 3:1; non-text UI ≥ 3:1
    - Motion respects prefers-reduced-motion (2.3.3)

- Operable
  - Keyboard accessible (2.1.x): All interactive elements operable with keyboard
  - Enough time (2.2.x): No unexpected timeouts; loading states indicated
  - Seizures & physical reactions (2.3.x): No flashing content
  - Navigable (2.4.x): Focus order logical; focus visible; descriptive titles and labels

- Understandable
  - Readable (3.1.x): Clear language; abbreviations expanded where needed
  - Predictable (3.2.x): No context changes on focus; explicit submit on forms
  - Input assistance (3.3.x): Error identification and suggestions provided

- Robust
  - Compatible (4.1.x): Valid HTML; ARIA roles/props/states accurate

### Component Mapping

- Button
  - Role `button`; `aria-disabled` when disabled; `aria-busy` when loading
  - Focus ring visible; min target sizes iOS 44pt / Android 48dp

- Input
  - Label associated via `for`/`id`; `aria-invalid` and error text linked via `aria-describedby`
  - Contrast for borders and placeholders sufficient

- Select
  - Prefer native `<select>`; for custom, `role="combobox"` and listbox semantics
  - Roving tabindex; typeahead; announcement of selections

- Card
  - If interactive, use `button` or link semantics; otherwise, structural container
  - Maintain contrast for text and embedded controls

- Modal
  - `role="dialog"`, `aria-modal=true`, `aria-labelledby` to title
  - Focus trap; return focus to invoker on close; ESC closes

### Testing Protocol
- Keyboard walk: Tab/Shift+Tab across full UI, verify order and traps
- Screen reader: NVDA/JAWS/VoiceOver smoke tests for roles and announcements
- Contrast audit: Automated + spot checks for dynamic states
- Motion: Verify durations and prefers-reduced-motion handling

### Acceptance Gate (Pass/Fail)
- AA contrast verified in light/dark
- Keyboard-only path complete for core flows
- Screen reader announcements for critical events (open modal, validation errors)
- No blocked tasks without pointer device

