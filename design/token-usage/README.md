# Design Token Usage

This frontend uses a minimal token set defined in `src/frontend/src/styles/tokens.css` to ensure consistent theming and spacing.

- Colors: `--color-bg`, `--color-fg`, `--color-accent`
- Spacing: `--space-1`..`--space-4`
- Radius: `--radius-2`
- Font: `--font-base`

Usage example:

```css
.button-primary {
	background: var(--color-accent);
	border-radius: var(--radius-2);
	padding: var(--space-3) var(--space-4);
}
```

To switch to dark mode, set `data-theme="dark"` on the `html` element.

