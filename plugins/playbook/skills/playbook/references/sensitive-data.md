# Sensitive-data profiles

Enable with `sensitive_data: [...]`. `secrets` is always on. When any enabled kind appears in what the user gives you, stop and ask them to redact before writing it anywhere. Use the placeholders instead.

| Profile | Never store | Placeholders |
|---|---|---|
| `secrets` | passwords, API keys, tokens, private keys, connection strings with credentials | `<API_KEY>`, `<DB_PASSWORD>`, env var names (`$STRIPE_KEY`) |
| `pii` | real names tied to records, personal emails, phone numbers, addresses, government IDs | `<USER_NAME>`, `<EMAIL>`, `<PHONE>`, `<ADDRESS>`, `<GOV_ID>` |
| `phi` | patient names, DOB, MRN, insurance IDs, diagnoses tied to a person | `<PATIENT_NAME>`, `<DOB>`, `<MRN>`, `<INSURANCE_ID>` |
| `pci` | card numbers, CVV, bank account numbers | `<CARD_NUMBER>`, `<BANK_ACCOUNT>` |

Custom profile:

```yaml
sensitive_data:
  - secrets
  - id: customer-ids
    description: Internal customer account numbers
    patterns: ["\\bCUST-\\d{6,}\\b"]
    placeholder: "<CUSTOMER_ID>"
```

`audit` reports matches as `file:line (profile)` — never the value.
