# Requirement interview

How the playbook gathers requirements. Used by `new` (whole program), `interview [TASK]` (add or refine requirements, for the program or one task), `task add` (quick) and `work` (when a task's acceptance criteria are missing). The output always lands in **`00-REQUIREMENTS.md`** — normalized rows plus the approved spec as a record. Nothing is executed from the interview; the plan's approval gate governs when work starts.

To use your own interview skill instead (e.g. a `/prompt` skill), map it in config: `capabilities.interview: [skill:prompt, builtin]`. Whatever runs, its output must be saved into `00-REQUIREMENTS.md` as below.

## Settings (`interview:` in config)

| Key | Default | Meaning |
|---|---|---|
| `depth` | `standard` | `quick` (≤ 3 questions), `standard` (≤ 8), `deep` (no cap, every section probed). "quick"/"deep" in the request wins |
| `one_question_at_a_time` | `true` | `false` = batch questions in one message |
| `spec_format` | `xml` | `xml` or `markdown` for the saved record |
| `sections` | the 7 standard | add, remove or rename; `context`, `task`, `acceptance_criteria` cannot be removed |
| `extra_questions` | `[]` | always-asked questions, each with an optional `when:` (rule conditions) |

## Steps

1. **Read the request and the playbook.** Note what's already answered: the source document, `00-REQUIREMENTS.md`, `03-DECISIONS.md`, the analysis for the repo, and (for a task) its plan row.
2. **Classify** — *technical* (code, APIs, infra, data, bugs, architecture) or *general* (docs, research, planning, process, content). Mixed → technical. Say it in one line.
3. **Inspect before asking** (technical) — use the `code-analysis` capability: entry points, existing patterns, data model, tests, config. Never ask what the code answers; state what you found and ask only for confirmation where it matters.
4. **Interview** — questions from `interview-questions.md` for the type, at the configured depth, plus matching `extra_questions` (and, for `new`, the playbook questions at the end of that file).
   - skip anything already answered
   - one question at a time unless configured otherwise; offer 2–4 likely answers where you can
   - "you decide" / "default" → pick the clean standard option and record it as an assumption
   - a question only someone else can answer → don't block; it becomes a `D-NN`
   - stop when every required section can be filled; never pad
5. **Draft the spec** in the configured format (`interview-spec-format.md`). Unknowns are `<TBD: what → D-NN>`; assumptions listed, never hidden. No sensitive values — placeholders only (`<API_KEY>`, `<USER_EMAIL>`, `<PATIENT_NAME>`, `<MRN>`, `<INSURANCE_ID>`, `<CARD_NUMBER>`); if the user pastes any, ask them to redact first.
6. **Show it and ask for approval or edits.** Edits → revise and show again.
7. **Save into `00-REQUIREMENTS.md`** (on approval):

| Spec section | Lands in `00-REQUIREMENTS.md` | Also |
|---|---|---|
| `<requirements>` | rows in the matching group table — spec `R1` → playbook ID scheme (`C1`, `FR-01`); new rows for a task marked `added YYYY-MM-DD, source: <who>` | — |
| `<acceptance_criteria>` | `Acceptance` column of the requirement each criterion `covers` | traceability `Test` column |
| `<constraints>` | `## Constraints` (and `## Invariants` for must-never-break rules); defaults into the `Default` column with the config key | — |
| `<context>`, `<task>` | `## Interview record` entry (below) | README first paragraph / goal on `new` |
| `<references>` | `## Interview record` entry | source files into `references/` |
| `<output_format>` | `## Interview record` entry | plan task `Type` |
| `<assumptions>` | `## Assumptions` — each `confirm with <approver>` | Decided rows marked `assumed` in `03-DECISIONS.md` |
| `<open_questions>` | the requirement's `Default`/text as `<TBD → D-NN>` | Open `D-NN` rows in `03-DECISIONS.md` with recommendation and the tasks they block |

   Then append the full approved spec under `## Interview record` as `### YYYY-MM-DD — <program | TASK-ID> — APPROVED (<who>)` with the spec in a fenced block. The tables are the source of truth; the record is history — never edit an old record, add a new one.
8. **Fire `after_interview`** and run the ripple sweep (`Requirements changed` row).
