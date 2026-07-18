# Illustrative regulation samples

**These are not real regulatory documents.**

Each file here is a synthetic composite written for demonstration and testing. They imitate the *structure* and *language patterns* of supervisory guidance -- numbered obligations, modal verbs, defined terms -- so the extraction pipeline can be exercised and tested. They do not reproduce, paraphrase, or represent the text of any actual agency publication, and they carry no regulatory authority.

To assess real guidance, download the actual document, save it as plain text, and pass it directly:

```bash
uv run rcia path/to/real-guidance.txt --inventory examples/inventory.yaml
```

The tool never fetches regulatory text on your behalf. Sourcing authoritative documents is deliberately left to the user.