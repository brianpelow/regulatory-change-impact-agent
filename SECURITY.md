# Security Policy

## Reporting a vulnerability

Open a [security advisory](https://github.com/brianpelow/regulatory-change-impact-agent/security/advisories/new) rather than a public issue.

Expect an initial response within seven days.

## Scope

This tool reads local files only. It does not fetch regulatory documents, transmit your system inventory anywhere, or execute analyzed content.

If `OPENROUTER_API_KEY` is set, the summary narrative is generated remotely. That request includes the document name, obligation counts, control domains, system identifiers, and gap list -- not the source document and not your full inventory. Leave the variable unset to keep the tool entirely offline.

## A note on output

Assessments are an engineering planning aid, not legal advice. A clean assessment means no gap against the encoded taxonomy, not that your institution is compliant.