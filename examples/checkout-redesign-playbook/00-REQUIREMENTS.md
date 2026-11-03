# 00 — Requirements

Source: "Checkout v2 PRD", 2026-10-20, Product. Numbers are quoted from the source. Gathered and refined with `/playbook interview`. Defaults live in app config — the `Default` column names the config key.

## Checkout

| ID | Requirement | Acceptance criteria | Default | Source |
|---|---|---|---|---|
| C1 | Shipping, payment and review on one page | e2e: happy path completes without a page change | — | PRD §2 |
| C2 | Totals recalculate within 300 ms of a cart or address change | load test p95 < 300 ms; contract test returns subtotal, tax, shipping, total | `checkout.totals_timeout_ms = 300` | PRD §3, interview 2026-10-28 |
| C3 | Draft order saved so a refresh keeps the form | api test: draft restored after reload within TTL | `checkout.draft_ttl_hours = 24` | PRD §3 |
| C5 | Emit `checkout_started` and `checkout_completed` events | api test asserts both events with order ID | — | interview 2026-10-30 (added 2026-10-30, source: Product lead) |
| C4 | Guest checkout supported | e2e: guest path completes | <TBD: keep guest checkout? → D-02> | PRD §4 |

## Invariants — never break these

| ID | Invariant |
|---|---|
| I1 | Totals equal the pricing service's result for the same cart, to the cent (parity test on 50 fixture carts) |

## Constraints

- `api/src/pricing/totals.ts` is reused unchanged (interview 2026-10-28)

## Assumptions — confirm with Product lead

- Debounce lives in the client, not the API (DD-01)

## Out of scope

- Saved payment methods (separate program)

## Interview record

Approved interview specs, newest first. Never edit an old record; add a new one.

### 2026-10-28 — CO-02 — APPROVED (Tech lead)

```xml
<context>The web client needs live totals; api/src/pricing/totals.ts already computes them for step 4.</context>
<task>Expose POST /checkout/totals returning the same totals as the pricing service.</task>
<requirements>
  <requirement id="R1">Accepts a draft order ID; returns subtotal, tax, shipping, total. → C2</requirement>
  <requirement id="R2">Uses pricing/totals.ts unchanged. → I1</requirement>
</requirements>
<constraints>p95 under 300 ms (checkout.totals_timeout_ms). No change to pricing/totals.ts.</constraints>
<acceptance_criteria>
  <criterion id="AC1" covers="R1">Contract test returns all four fields for a fixture draft.</criterion>
  <criterion id="AC2" covers="R2">Parity test: 50 fixture carts equal the pricing service to the cent.</criterion>
</acceptance_criteria>
<references>api/src/pricing/totals.ts; DD-01</references>
<output_format>PR to api with endpoint, tests, OpenAPI entry.</output_format>
<assumptions>Debounce lives in the client (DD-01).</assumptions>
<open_questions>None</open_questions>
```

### 2026-10-24 — program — APPROVED (Product lead)

Initial interview on the PRD: goal, repos (`web`, `api`), approver, modules (none). Requirements C1–C4 and I1 above; open questions → D-01, D-02.
