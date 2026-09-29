# Retrospective: Forge Planning / Dispatch Process

Epic: What we are doing right and how we can improve overall our working?

This document captures findings from observing the Forge plan/approve/dispatch
loop in practice, including a live example of one of the friction points it
describes.

## What's working

- **The plan/approve/dispatch loop functions end-to-end.** An epic can be
  broken into a task, dispatched to a worker, and carried through to a
  completed, reviewable change without the process itself breaking down.
- **The Steward can correct a misread of scope mid-flow before wrong work
  ships.** When the worker's understanding of a task drifts from what the
  Steward intended, the Steward can intervene and redirect before any
  incorrect output is finalized, keeping wrong work from shipping.

## What to improve

1. **Per-call approval on read-only commands can stall a task entirely.**
   Commands like `ls`, `git log`, and `git status` are read-only and carry no
   risk of changing state, yet each invocation currently requires its own
   Steward approval. In practice this happened repeatedly on this very task: a
   plain `ls` was denied multiple times in a row, each with a distinct
   approval ID, before one attempt was finally approved. If the Steward is
   away or slow to respond, a task can stall completely on a command that
   could not have caused harm.

2. **The planner cannot tell a reflective/discussion epic from a
   buildable-feature epic before committing to a full task breakdown.**
   Epics like this one — "what are we doing right and how can we improve" —
   are open-ended analysis, not a feature to build. The planner currently has
   no signal to recognize this distinction up front, so it proceeds as if
   every epic will resolve into concrete, buildable tasks, even when the real
   output is a written reflection.

3. **The tasks/questions/assumptions JSON contract has no slot for
   open-ended analysis with no buildable output.** The planning contract is
   shaped around producing discrete tasks, clarifying questions, and stated
   assumptions — all oriented toward implementation work. There is no field
   for "this epic's output is a document/analysis, not a code change," which
   forces reflective epics to be awkwardly fitted into a schema built for
   feature work.

4. **Repeated near-identical prompts across turns don't carry forward the
   planner's prior open questions.** When a task is re-sent with only minor
   variation, the planner does not retain or resurface questions or
   clarifications it raised in a previous turn. This means clarification only
   happens if the Steward personally notices the gap and re-types the
   correction, rather than the system preserving and re-presenting
   previously identified open questions.
