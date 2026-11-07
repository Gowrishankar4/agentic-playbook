# Walkthrough — one feature, end to end

Meera is a developer on an e-commerce team. Repos: `web` (React) and `api` (Node). Her team also keeps issues in Jira. Her team uses Claude Code; her teammate Arun uses Cursor. Product lead Ravi approves plans.

Her intent: **"Customers should be able to request a refund from their order page."**

---

## 0. Install (once)

```bash
/plugin marketplace add Gowrishankar4/agentic-playbook
/plugin install agentic-playbook@agentic-playbook
```

Arun, on Cursor: `git clone …/agentic-playbook && ./install.sh --agent cursor`.

---

## Day 1 — intent → approved plan

### Start

```text
Meera: /playbook new — customers should be able to request a refund from their order page
```

### Step 1 · First-run setup (only the first time ever)

No config exists, so the playbook asks once:

```text
Claude: First run — quick setup (say "skip" for defaults).
        1. Where should playbooks live?            [~/playbooks]
        2. Preset?                                  feature / program / regulated
        3. Progress is tracked from git — nothing to set up.
           I can see these in this session — use them?
           interview → /prompt · code-analysis → code-graph · verify → /verify · commit → /commit
Meera:  ~/work/playbooks · feature · yes
```

Written to `~/.config/playbook/config.yml`:

```yaml
root: ~/work/playbooks
preset: feature
capabilities:
  interview:     [skill:prompt, builtin]
  code-analysis: [skill:code-graph, builtin]
  verify:        [command:/verify]
  commit:        [command:/commit]
```

Her team mirrors progress to Jira, so she adds two of the team's own skills on events, plus a review rule:

```yaml
capabilities:
  issue-create:  [skill:jira-create]
  issue-tracker: [skill:jira-comment]
rules:
  - id: jira-create
    on_event: [after_approval, task_added]
    use: issue-create
    instruction: Ask first; create one SHOP issue per task; append the key to Evidence.
  - id: jira-comment
    on_event: [task_done]
    use: issue-tracker
    instruction: Post a solution report on the task's issue. Never change its status.
  - id: payments-review
    on_event: [task_done]
    when: { paths: ["api/src/payments/**"] }
    mode: required
    ask: Payments code changed — who reviewed it, and when?
```

### Step 2 · Name and settings (every new playbook)

```text
Claude: Name? Repos? Approver? Optional modules (API contract, test cases)?
Meera:  refund-requests · web, api · Ravi · API contract
```

→ `~/work/playbooks/refund-requests-playbook/` is created from the templates; plan header `DRAFT — requirements pending`.

### Step 3 · Requirement interview → `00-REQUIREMENTS.md`

The mapped `/prompt` skill runs. It classifies the request as technical, reads `web` and `api` first, then asks only what the code and intent don't answer — one question at a time:

```text
Claude: Classified: technical. I found orders in api/src/orders/, payments via
        api/src/payments/gateway.ts (supports refund()), order page web/src/pages/Order.tsx.
        1. Which orders can be refunded — any delivered order, or within a time window?
Meera:  delivered, within 30 days
Claude: 2. Full refunds only, or partial (per item)?
Meera:  per item
Claude: 3. Automatic, or does someone approve each refund?
Meera:  automatic under ₹5,000 — above that, not sure, Ravi decides
Claude: 4. How should the customer hear about it?
Meera:  you decide
```

Draft spec shown for approval (abridged):

```xml
<task>Let customers request a per-item refund for delivered orders within 30 days.</task>
<requirements>
  <requirement id="R1">Refund button on delivered orders ≤ 30 days old. Default: refunds.window_days = 30</requirement>
  <requirement id="R2">Customer selects items and a reason.</requirement>
  <requirement id="R3">Refunds under ₹5,000 are issued automatically via gateway.refund(). Default: refunds.auto_limit = 5000</requirement>
  <requirement id="R4">Refunds ≥ ₹5,000: <TBD: auto or manual? → ask Ravi></requirement>
  <requirement id="R5">Customer is notified of the outcome.</requirement>
</requirements>
<acceptance_criteria>
  <criterion id="AC1" covers="R1">Button hidden for orders older than 30 days or not delivered.</criterion>
  <criterion id="AC3" covers="R3">₹4,999 refund → gateway.refund called once; order item marked refunded.</criterion>
  …
</acceptance_criteria>
<assumptions>Notification by email using the existing order-email template.</assumptions>
<open_questions><TBD: refunds ≥ ₹5,000 — auto or manual review? → ask Ravi></open_questions>
```

```text
Meera: approved
```

Saved — **not executed** — into `00-REQUIREMENTS.md`:

```markdown
| ID | Requirement                                   | Acceptance criteria                         | Default                     |
|----|-----------------------------------------------|---------------------------------------------|-----------------------------|
| R1 | Refund button on delivered orders ≤ 30 days   | hidden when > 30 days or not delivered      | refunds.window_days = 30    |
| R3 | Under ₹5,000 refunded automatically           | ₹4,999 → one gateway.refund call            | refunds.auto_limit = 5000   |
| R4 | ₹5,000 and above                              | —                                           | <TBD: auto or manual? → D-01> |
| R5 | Customer notified of the outcome              | email sent with refund status               | —                           |

## Assumptions — confirm with Ravi
- Notification by email using the existing order-email template

## Interview record
### 2026-11-04 — program — APPROVED (Meera)
<the full spec>
```

…and `D-01` appears in `03-DECISIONS.md`:

```markdown
| ID   | Req | Question                              | Recommendation                 | Blocks | Status |
|------|-----|---------------------------------------|--------------------------------|--------|--------|
| D-01 | R4  | Refunds ≥ ₹5,000: auto or manual?     | Manual review queue (fraud)    | RF-04  | ⬜     |
```

### Step 4 · Analysis → `01-ANALYSIS.md`

code-graph maps the code: reuse `gateway.refund()` and the order-email template; gap — no `refunds` table; ambiguity `A-01` "partial refund of a discounted item — refund paid price or list price?" → proposed reading "paid price", raised as `D-02`.

### Step 5–6 · Plan, then stop

```text
Claude: Plan ready — DRAFT, awaiting approval
        ~/work/playbooks/refund-requests-playbook/
        5 requirements · 5 tasks · 2 open decisions

        Phase 1 — API   RF-01 refunds table + model · RF-02 POST /refunds · RF-04 large-refund handling
        Phase 2 — Web   RF-03 refund form on order page
        Phase 3 — Notify RF-05 refund outcome email

        Blocking: D-01 (blocks RF-04) · D-02 (blocks RF-02)
        Approve?
Meera:  Ravi approved. D-02: paid price.
```

In one sweep:
- `02-PLAN.md` → `**Status:** APPROVED 2026-11-04 (Ravi)`
- `D-02` → `✅ → DD-01` ("Refund the price paid." — Ravi, relayed by Meera); RF-02 unblocked
- `after_approval` fires → her `jira-create` rule asks, then creates `SHOP-211 … SHOP-215`; the keys are appended to each task's Evidence
- `git init` + first commit of the playbook folder (asked first)

`PROGRESS.md` now:

```markdown
**Stage:** APPROVED — in delivery
**Current phase:** Phase 1 — API, not started
**Next action:** RF-01 refunds table + model (Meera)

| Task  | Status | Repo / branch | Blocked by | Evidence |
|-------|--------|---------------|------------|----------|
| RF-01 | ⬜ | api | — | SHOP-211 |
| RF-02 | ⬜ | api | RF-01 | SHOP-212 |
| RF-03 | ⬜ | web | RF-02 | SHOP-213 |
| RF-04 | ⏸ | api | D-01 | SHOP-214 |
| RF-05 | ⬜ | api | RF-02 | SHOP-215 |
```

---

## Day 2 — delivery

### The agent implements a task end to end

```text
Meera: /playbook work RF-01
Claude: RF-01 can start (plan approved, nothing blocking). Loaded R1–R3 and acceptance criteria.
        → 🟡 started, branch feat/refunds-table
        … migration api/migrations/2026_11_05_refunds.sql, model api/src/refunds/model.ts, tests …
        /verify → PASS (jest 14/14). Commit via /commit? 
Meera:  yes
Claude: RF-01 ✅ — api `9f3c2e1` (feat/refunds-table, not pushed); verify PASS; jest 14/14; SHOP-211.
        jira-comment rule: post the solution report on SHOP-211? → yes, posted.
        Unblocked: RF-02. Next action: RF-02 POST /refunds.
```

### A teammate's work, recorded in plain words

Arun built RF-02 himself in Cursor:

```text
Arun (Cursor): RF-02 is done, b71d0aa on feat/refund-endpoint, pushed, verify passed, PR #88
Claude: payments-review rule: payments code changed (api/src/payments/gateway.ts) — who reviewed it, and when?
Arun:   Meera, today
Claude: RF-02 ✅ — api `b71d0aa` (feat/refund-endpoint, pushed); PR #88; verify PASS; reviewed by Meera 2026-11-05.
        Updated: PROGRESS row + log · traceability R2, R3 → ✅ · RF-03 and RF-05 unblocked ·
        next action → RF-03 (web).
```

"today" was written as `2026-11-05` — never as a relative date.

### Work with no commit and no ticket

Meera asks the agent to add a small admin export nobody ticketed:

```text
Meera:  task add — CSV export of refunds for finance
Claude: (quick interview) Which columns? Who uses it? → saved as R6 (added 2026-11-05, source: Meera),
        task RF-06. jira-create rule: create a SHOP issue? 
Meera:  no issue for this one, and don't commit yet — just build it
```

After `work RF-06`, the row records what the agent did:

```markdown
| RF-06 | ✅ | api | — | agent-tracked 2026-11-05: refunds CSV export; files: api/src/refunds/export.ts, api/test/export.test.ts; tests: npm test export → 3/3 pass |
```

---

## Day 3 — decisions and directives

```text
Meera: Ravi answered D-01: anything ₹5,000 or more goes to a manual review queue
```

One sweep:
- `D-01` → `✅ → DD-02`, Decided row quotes Ravi, dated 2026-11-06
- `R4` in `00-REQUIREMENTS.md`: `<TBD → D-01>` replaced with "≥ ₹5,000 → manual review queue", acceptance criterion added
- RF-04 `⏸` → `⬜`, "Blocked by" cleared; next action unchanged (RF-03 still first)

Ravi then sets a standing rule:

```text
Meera: directive from Ravi — "No refund may be issued for an order with an open chargeback."
```

→ `05-DIRECTIVES.md` `DIR-01` (verbatim, dated, by Ravi; lands in R7, RF-02, RF-04). It overrides the plan: RF-02 is already ✅, so it gets `⚠️ DIR-01: add chargeback check` and a new requirement `R7` plus task `RF-07` (Phase 1) are proposed and added.

### Refining requirements for one task

```text
Meera: /playbook interview RF-03
Claude: (reads R1–R2, Order.tsx) 3 questions: max reason length? show refund history on the page? mobile layout?
```

Approved → new acceptance criteria on R2, a dated `RF-03` interview record in `00-REQUIREMENTS.md`, traceability `Test` updated.

---

## Day 4 — another agent, another day

Arun opens Cursor. The playbook's `AGENTS.md` tells it to read `PROGRESS.md` first.

```text
Arun: /playbook resume refund-requests
Claude: Phase 1 — API: 3/5 done (RF-04, RF-07 not started).
        Next: RF-03 refund form (web).
        In progress: none. Blockers: none.
        Open decisions: none. New: DIR-01 — RF-07 chargeback check (⬜).
        Stale: none.
```

### Git check

Evidence comes straight from git, so a stale row is easy to catch:

```text
Arun: has RF-01 been pushed yet?
Claude: git branch -r --contains 9f3c2e1 → origin/feat/refunds-table. Pushed.
        RF-01 evidence updated: (feat/refunds-table, pushed).
```

### Audit

```text
Meera: /playbook audit
Claude: warn (3)
          PROGRESS.md      phase "1 — API" still ⬜ while 3 of its tasks are ✅ → should be 🟡
          PROGRESS.md      next action names RF-02, which is already done
          00-REQUIREMENTS  R6 has no acceptance criteria — run /playbook interview RF-06
        Fix these?
Meera: yes
```

### All playbooks at a glance

```text
Meera: /playbook status
refund-requests  · Phase 1 API · 3/7 tasks · 0 open D · next: RF-03 · last log 2026-11-07
checkout-v2      · Phase 2 Web · 6/9 tasks · 1 open D · next: CO-07 · last log 2026-10-29 (stale)
```

---

## Day 9 — close

All tasks ✅, released.

```text
Meera: /playbook close
Claude: audit clean. Summary written to PROGRESS.md:
        Outcome: refunds live 2026-11-12; 7/7 tasks; 2 decisions; 1 directive.
        Lessons → add to your config?
          • red flag: "Payments task done — skip the chargeback check" → "DIR-01 applies to every payments task"
Meera:  yes
```

→ PROGRESS `Stage` and the plan header both `CLOSED 2026-11-13`; playbook archived under `~/work/playbooks/archive/` (asked first); the new red flag is added to Meera's config, so every future playbook catches it.

---

## What Meera never did

- edit `PROGRESS.md`, traceability or the phase table by hand
- re-explain the feature to a new session or to Arun's agent
- guess a requirement — every one came from the interview or a recorded decision
- lose track of work with no commit or ticket (`agent-tracked`)
- configure a tracker — progress came from git; Jira was kept in step by her own skills on events, which never change an issue's status
