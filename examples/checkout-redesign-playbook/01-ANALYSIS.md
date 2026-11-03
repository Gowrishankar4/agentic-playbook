# 01 — Analysis

## 1. Summary
The 4-step flow lives in `web/src/checkout/steps/`; totals come from `api/src/pricing/totals.ts`, which is reusable.

## 2. What exists (reuse)

| Repo | Path | What it gives us |
|---|---|---|
| api | `src/pricing/totals.ts` | Canonical totals calculation |
| web | `src/checkout/address/AddressForm.tsx` | Address validation |

## 3. Gaps
No draft-order persistence; totals are only computed at step 4.

## 4. Ambiguities

| ID | Ambiguity | Reading proposed | Confirm in |
|---|---|---|---|
| A-01 | "Fast totals" — server or client? | Server, debounced from the client | D-01 → DD-01 |

## 5. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Totals drift from pricing service | Wrong charges | Parity test on fixture carts (I1) |
