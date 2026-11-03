# Interview spec format

The spec is drafted for approval, then saved into `00-REQUIREMENTS.md` (see `interview.md` step 7).

Default `spec_format: xml`. Sections in this order; omit none of the required three (`context`, `task`, `acceptance_criteria`). Custom sections from config go before `<references>`.

```xml
<context>
  Who this is for, the current state (with file paths for technical work), why it's needed now.
</context>

<task>
  One or two sentences: the outcome, stated as a deliverable.
</task>

<requirements>
  <requirement id="R1">Testable statement. Default: <value or config key>.</requirement>
  <requirement id="R2">…</requirement>
</requirements>

<constraints>
  Tech stack, compatibility, performance budgets, deadlines, things that must not change.
</constraints>

<acceptance_criteria>
  <criterion id="AC1" covers="R1">Observable check: given/when/then, or a command whose output proves it.</criterion>
</acceptance_criteria>

<references>
  Files read, docs, tickets, designs (links or paths). No sensitive values.
</references>

<output_format>
  What gets delivered: files changed, PR, document, report — and where.
</output_format>

<assumptions>
  Choices made on "you decide" or defaults — each one line.
</assumptions>

<open_questions>
  <TBD: what is missing → ask <owner>> — one per line.
</open_questions>
```

`<assumptions>` and `<open_questions>` are always present (write `None` if empty).

With `spec_format: markdown`, use the same section names as `##` headings and the same IDs.

Every `<criterion>` has `covers=` pointing at one or more requirement IDs; every requirement is covered by at least one criterion.
