# Admissibility vs Logs (production distinction)

Logs are forensic: they tell you what happened after the fact.
Admissibility is contractual: it tells you what was allowed at commit-time and why.

A system that only logs execution forces teams into archaeology during incidents and audits:
- constraints drift silently
- intent becomes implicit
- accountability becomes a reconstruction exercise

This repo enforces commit-time admissibility:
proposal → deterministic checks → admit/reject → decision record + snapshot
