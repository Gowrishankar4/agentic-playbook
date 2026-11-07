# 02 — Plan

**Status:** APPROVED 2026-10-27 (Product lead)

## Architecture
Web calls a new `POST /checkout/totals` (debounced 250 ms); API wraps `pricing/totals.ts`. Draft orders persist server-side.

## Phases

| Phase | Tasks | Exit criteria |
|---|---|---|
| 1 — API | CO-01, CO-02, CO-04 | Totals endpoint p95 < 300 ms; parity test green |
| 2 — Web | CO-03 | Single page live behind `checkout_v2` flag |

## Dependency graph

```
CO-01 ──► CO-02 ──► CO-03 (also waits on D-02)
CO-01 ──► CO-04
```

## Task list

| ID | Title | Repo | Type |
|---|---|---|---|
| CO-01 | Draft order model + persistence | api | api |
| CO-02 | Totals endpoint | api | api |
| CO-03 | Single-page checkout UI | web | ui |
| CO-04 | Checkout analytics events | api | api |
