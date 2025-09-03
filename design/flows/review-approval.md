## Flow: Design Review & Approval

### Goal
Ensure quality gates pass for design tokens, components, and accessibility before merge.

### Flow Diagram
```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> InReview: PR created
  InReview --> ChangesRequested: Reviewer requests changes
  ChangesRequested --> Draft: Designer updates
  InReview --> Approved: All checks pass
  Approved --> Merged
```

### Quality Gates
- AA contrast verified (light/dark)
- Keyboard navigation validated
- Component states covered
- Preview build links included

