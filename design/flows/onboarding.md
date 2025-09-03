## User Flow: New Project Onboarding

### Goal
Guide a user from starting a project to seeing first design preview.

### Flow Diagram
```mermaid
flowchart TD
  A[Landing: Start New Project] --> B[Select Project Type]
  B --> C[Name Project]
  C --> D[Choose Brand Theme]
  D --> E[Accessibility Preferences]
  E --> F[Generate Baseline Tokens]
  F --> G[Preview UI]
  G --> H{Approve?}
  H -- No --> D
  H -- Yes --> I[Save & Continue to Specs]
```

### Key UX Notes
- Autosave at each step; breadcrumbs for navigation
- Real-time contrast checks during theme selection
- Keyboard-only path validated for all steps

