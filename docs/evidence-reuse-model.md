# Evidence Reuse Model

Control design is cheap and evidence is expensive. This document sets out how one artifact is made
to satisfy obligations across several frameworks, what that saves, and where reuse stops working.

All figures are synthetic and illustrative.

## 1. The problem reuse solves

In a program with per-framework control sets, the same underlying fact — "privileged access is
reviewed quarterly by an accountable reviewer" — is evidenced separately for each audit. Each
collection is a request to the same engineer, a fresh export with a slightly different date range,
a different naming convention, and an independent chance of contradicting the last one.

Illustrative cost in the reference organization before consolidation:

| | Per-framework collection | Consolidated collection |
| --- | --- | --- |
| Distinct evidence requests per year | 412 | 147 |
| Engineer hours servicing requests | ~980 | ~350 |
| Compliance analyst assembly hours | ~1,150 | ~520 |
| Instances of two frameworks receiving inconsistent evidence for the same control | 9 (found) | 0 (found) |

The last row is the one that matters. Inconsistent evidence across two audits is not an efficiency
problem, it is a credibility problem, and the finding it produces is about the control environment
rather than the control.

## 2. The reuse mechanism

```
   Control (one owner, one test procedure)
        │
        ├── produces ──► Evidence artifact (one collection, one timestamp, one scope statement)
        │                       │
        │                       ├──► satisfies HIPAA 164.308(a)(4)(ii)(C)
        │                       ├──► satisfies SOC 2 CC6.2, CC6.3
        │                       ├──► satisfies SP 800-53 AC-2(j) / FedRAMP (M)
        │                       ├──► satisfies ISO 27001 A.5.18
        │                       └──► satisfies internal SOX ITGC-ACC-03
        │
        └── tested once, on the control's own cadence, not once per audit
```

Three conditions make this work, and all three fail in practice more often than the model does:

1. **The artifact's scope must be stated explicitly.** "Access review evidence" is unusable. "Access
   certification campaign covering all entitlements to the 14 systems in the financially relevant
   population, executed 2026-07-01 to 2026-07-31, 100% decision coverage, 41 revocations of which 41
   were verified complete by 2026-08-07" is reusable across every framework that asks about access
   review — because each auditor can determine whether their population is inside the scope.
2. **The collection cadence must be at least as frequent as the most demanding framework.** One
   framework requiring quarterly and another annual means quarterly, not an annual artifact with
   three retrospective assertions.
3. **The artifact must be immutable once collected.** Regenerating an export at audit time produces
   a current-state document that cannot evidence a past period, and an auditor who notices this
   discounts every other artifact in the set.

## 3. What the current library achieves

From `scripts/gap_report.py` §5 against the core scope profile (7 frameworks, 57 in-scope controls):

| Measure | Value |
| --- | --- |
| Evidence-producing controls in scope | 57 |
| Framework obligation references satisfied | 611 |
| Reuse ratio | 10.7 obligation references per evidence artifact |
| Highest-reuse single controls | AM-03, SA-04, SR-01 and SR-02, each carrying 14 references across all 7 frameworks |

Reuse ratio is a planning number, not a cost saving. It says that if the enterprise collected
evidence per framework instead, the collection count would be roughly ten times higher; it does
not say the compliance function would be ten times cheaper, because assembly and audit liaison
do not scale linearly with artifact count. A defensible claim from this data is a 55–65% reduction
in collection effort, which is what the table in §1 shows.

## 4. The highest-reuse artifacts

Where a compliance program should invest its automation budget first, in this order.

| Artifact | Produced by | Frameworks touched | Collection cost | Automation rating |
| --- | --- | --- | --- | --- |
| Access certification campaign record | AC-03 | 6 | Medium | 4 |
| Vendor register with tier, assessment date and findings | SR-01 | 7 | High | 2 |
| Change records with approver and test evidence | CM-02 | 6 | Low | 4 |
| Audit log configuration and source inventory | AU-01 | 5 | Low | 4 |
| Backup and verified restore records | CP-01 | 6 | Medium | 3 |
| Encryption state per data store | DP-02 | 5 | Very low | 5 |
| Vulnerability coverage and aging report | VM-01, VM-02 | 5 | Very low | 5 |
| Incident records with timeline and notification assessment | IR-02, IR-03 | 6 | Medium | 3 |

**Automation rating and reuse together give the priority order.** High reuse plus high automation
feasibility (DP-02, VM-01) is where the first engineering hour goes. High reuse plus low automation
feasibility (SR-01) is where headcount goes, and pretending otherwise produces a tooling purchase
that does not reduce the work. This is the substance of ADR-006 in `DECISIONS.md`.

## 5. Where reuse breaks

Reuse has hard boundaries, and a program that ignores them gets an audit finding rather than a
saving.

| Boundary | Why it breaks | What to do instead |
| --- | --- | --- |
| **Population mismatch** | The SOX population is 14 financially relevant systems; the HIPAA population is 61 systems processing protected health information. An artifact scoped to one does not evidence the other | Collect to the union population with a population field, or collect twice and say so |
| **Period mismatch** | An annual artifact cannot evidence a quarterly control | Collect at the most demanding cadence; sample from it for less demanding frameworks |
| **Independence requirements** | Some assurance engagements require evidence produced or observed by someone independent of the control operator | Identify these in advance; they are a small minority and cannot be satisfied by reuse |
| **Attestation requirements** | Some frameworks require a signed management assertion, not an artifact | Assertions are per-framework by nature; only the underlying evidence is reused |
| **Prescriptive format** | A regulator specifying a form or field set | Produce the required format; reuse the source data, not the document |
| **Point-in-time versus period-of-time** | A configuration export proves a moment; a period-of-time opinion needs evidence the state held throughout | Continuous configuration monitoring output, not a single export — this is the most frequently mishandled boundary in SOC 2 Type II engagements |

## 6. Evidence metadata standard

Every artifact carries these fields, without exception. An artifact missing any of them is not
reusable, because a second auditor cannot determine whether it covers their question.

| Field | Example |
| --- | --- |
| Artifact ID | `EV-2026-Q3-AC03-001` |
| Source control | `AC-03` |
| Collection date and period covered | Collected 2026-08-07; covers 2026-07-01 to 2026-07-31 |
| Population and scope statement | All entitlements to the 14 systems in the financially relevant population |
| Collection method | Export from the identity governance platform, campaign ID 2026-Q3-FIN |
| Collector | Named individual or the automated job identifier |
| Completeness assertion | 100% of in-scope entitlements received a decision |
| Known limitations | Two systems' entitlements were loaded manually; reconciliation record attached |
| Mapped obligations | The framework identifiers this artifact is offered against |
| Retention and location | 6 years, evidence repository path |

The **known limitations** field is the one that gets omitted, and it is the one that converts an
artifact from a liability into an asset. An auditor who finds an undisclosed limitation tests
everything else harder. An auditor handed the limitation up front tests the disclosed thing and
moves on.

## 7. Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| **Screenshot evidence** | No scope, no period, trivially staged, and unreproducible. Acceptable only where no export exists, and then with a named collector and a description of what is shown |
| **Regenerating evidence at audit time** | Proves current state, not the audit period. An auditor who spots one regenerated artifact discounts the set |
| **The evidence binder** | A single document assembled annually containing assertions rather than artifacts. It satisfies the appearance of an evidence request and collapses on sampling |
| **Reusing an artifact outside its stated scope** | The fastest route to a misrepresentation finding. If the scope statement does not cover the auditor's population, collect again |
| **Evidence with no linked control** | Cannot be maintained, because nobody knows what would make it stale |
| **One evidence owner for everything** | The compliance analyst becomes the single point of failure and the de facto owner of controls they do not operate — the pattern the RACI in the sibling repository exists to prevent |

## 8. Operating the model

| Activity | Cadence | Owner |
| --- | --- | --- |
| Collect evidence on each control's own test cadence, not per audit | Per control | Control owner |
| Verify metadata completeness on collection | Per artifact | GRC analyst |
| Reconcile the evidence index against the control library | Quarterly | Compliance Manager |
| Identify artifacts approaching staleness relative to the most demanding framework | Monthly, automated | GRC analyst |
| Review reuse ratio and collection-hour trend | Annually | Compliance Manager |
| Re-derive a 10% sample of mappings independently | Annually | Internal Audit |

The measure worth reporting upward is not the reuse ratio. It is **collection hours per audit
cycle**, trended. Reuse ratio can be improved by adding mappings on paper; collection hours only
fall when something real changed.
