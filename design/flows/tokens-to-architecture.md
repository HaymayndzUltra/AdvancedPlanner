## Flow: Tokens Handoff to Architecture & Implementation

### Goal
Deliver versioned tokens and component contracts to unblock Architecture/API and Implementation.

### Flow Diagram
```mermaid
flowchart LR
  A[Design Tokens v1.0.0] --> B[Validate AA Proofs]
  B --> C[Publish tokens JSON]
  C --> D[PR to integration branch]
  D --> E[Architecture consumes tokens]
  E --> F[Implementation consumes tokens]
  F --> G[Preview build (Storybook)]
  G --> H{Design Review Sign-off}
  H -- Changes --> A
  H -- Approved --> I[Tag version & release]
```

### Integration Notes
- Tokens path: `design/tokens/core.tokens.json`
- Contracts path: `design/specs/*.md`
- Preview link added in PR description

