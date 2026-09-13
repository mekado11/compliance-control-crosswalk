# Compliance Control Crosswalk

A single enterprise control library crosswalked across eleven security and privacy frameworks, with
per-control evidence requirements, test procedures and automation ratings, plus a gap-report
generator that runs against any declared set of in-scope frameworks.

All content is synthetic. The control library, implementation status data, scope profiles and
generated reports describe a fictional composite organization and contain no real findings,
architecture or assessment results from any organization.

## What this demonstrates

- **Assess** — 60 controls scored against a declared framework scope, with obligation-level
  coverage states derived from mapping strength and implementation status rather than asserted.
- **Secure** — control statements written as things an enterprise does, each with a single
  accountable owner role and a scope that can be tested.
- **Detect** — logging, monitoring and detection-content controls mapped across frameworks that
  express the same requirement in four different vocabularies.
- **Respond** — incident, notification and post-incident controls carrying the regulatory clocks
  that differ per regime, with the clock reconciliation documented rather than averaged.
- **Govern** — a written methodology for mapping strength, a rule set for reconciling conflicting
  framework requirements, and an evidence-reuse model that makes multi-framework compliance
  affordable at fixed headcount.

## Scope and boundaries

**In scope.** A representative control library spanning nineteen families; crosswalk mappings to
eleven frameworks with explicit strength ratings; a working gap-report generator with three example
scope profiles; methodology documentation covering mapping, conflict reconciliation and evidence
reuse; a test suite covering data integrity and scoring behaviour.

**Out of scope.** This is not a compliance product and not a substitute for a GRC platform. The
mappings are editorial judgements, not authoritative interpretations, and no framework body has
reviewed them. Control inheritance from cloud service providers is not modelled, which materially
understates the effort profile of any authorization pursuit. Assessment objectives, parameter
values and organization-defined values are referenced in mapping notes but not encoded. Nothing
here constitutes legal advice.

**Not claimed.** The library is representative, not exhaustive: it covers the requirements a
mid-size regulated enterprise meets in practice, not every requirement in every catalogue. Coverage
percentages in generated reports are a function of the synthetic status data and mean nothing
outside this repository.

## Standards implemented

| Standard | Version | How it is used here |
| --- | --- | --- |
| NIST SP 800-53 | Rev 5 | Primary reference catalogue; control and enhancement identifiers, mapped at enhancement level where the enhancement carries a distinct obligation |
| NIST Cybersecurity Framework | 2.0 | Outcome-level mapping at subcategory granularity; the Govern function carries the program-level controls |
| SOC 2 | TSC 2017 (rev. 2022) | Trust services criteria points, including privacy series criteria |
| HIPAA Security Rule | 45 CFR 164 subpart C | CFR citations; required and addressable specifications handled per `docs/conflict-reconciliation.md` §4 |
| FedRAMP | Moderate baseline | 800-53 identifiers with baseline annotation; parameters noted, not encoded |
| CMMC | 2.0 Level 2 | Practice identifiers tracking NIST SP 800-171 |
| ISO/IEC 27001 | 2022 | Annex A controls plus management-system clause references where the obligation lives in the clauses |
| ISA/IEC 62443 | ‑2‑1, ‑2‑3, ‑3‑2, ‑3‑3, ‑4‑1 | System and lifecycle requirements; zone/conduit and security-level reasoning |
| NERC CIP | current standard versions as cited per requirement | Prescriptive requirements; gaps route to the standard's own deviation mechanism, never to enterprise risk acceptance |
| SOX ITGC | PCAOB AS 2201 framing | Internal key control identifiers; there is no external SOX control catalogue and the reports say so |
| GDPR | Regulation (EU) 2016/679 | Article-level obligations, predominantly Art. 5, 30, 32, 33–35 and the data subject rights articles |
| CycloneDX / SPDX | 1.7 (ECMA-424 2nd Ed.) / 3.0.1 | SBOM format requirements referenced by control AM-04 |

## Repository structure

```
compliance-control-crosswalk/
  README.md
  DECISIONS.md
  LICENSE
  .gitignore
  library/
    build_library.py            Single source of truth; emits the library and the crosswalk
    control-library.csv         60 controls: statement, owner role, evidence, test, automation rating
  crosswalk/
    crosswalk.csv               879 mappings: control to framework requirement, with strength
    crosswalk-matrix.md         Generated coverage matrix, controls by framework
  scripts/
    gap_report.py               Gap report generator; stdlib only, markdown output
    test_gap_report.py          14 tests covering data integrity, scoring and end-to-end rendering
  examples/
    implementation-status.csv   Synthetic implementation status for all 60 controls
    scope-profile-core.json     Enterprise obligations today
    scope-profile-fedramp-pursuit.json   Adds FedRAMP Moderate and CMMC L2 for the SaaS boundary
    scope-profile-ot-division.json       NERC CIP and ISA/IEC 62443 for the industrial estate
  docs/
    mapping-methodology.md      Unit of mapping, strength definitions, scoring algebra, maintenance
    conflict-reconciliation.md  Four conflict types, worked resolutions, prescriptive vs risk-based
    evidence-reuse-model.md     One artifact, N obligations: mechanism, limits, metadata standard
  reports/
    gap-report-core.md          Generated output for each example profile
    gap-report-fedramp-pursuit.md
    gap-report-ot-division.md
```

## How to use this

Requires Python 3.9 or later. No third-party packages, by design — see `DECISIONS.md` ADR-004.

```
# regenerate the control library and crosswalk from the source data
python3 library/build_library.py

# run a gap report against a declared framework scope
python3 scripts/gap_report.py --scope examples/scope-profile-core.json

# write it to a file instead
python3 scripts/gap_report.py --scope examples/scope-profile-ot-division.json \
    --out reports/gap-report-ot-division.md

# pipeline use: non-zero exit if any in-scope obligation is in gap state
python3 scripts/gap_report.py --scope examples/scope-profile-core.json --fail-on-gap

# run the tests
python3 scripts/test_gap_report.py
```

To adapt this to a different organization: replace `examples/implementation-status.csv` with real
status data, write a scope profile naming the frameworks actually in scope and the controls
genuinely not applicable (with a written reason for each), then read
`docs/mapping-methodology.md` §8 before changing any mapping. The mappings are the part that
requires judgement; the tooling around them is deliberately simple so that the judgement stays
visible.

Read the generated report from the bottom up. Section 5 (evidence burden) and section 4
(highest-leverage remediations) drive resourcing decisions; section 1's headline percentages are
the least useful numbers in the document and are printed first only because that is where people
look.

## Related

Part of a set of security engineering and governance repositories: `security-program-blueprint`,
`product-security-program`, `ai-governance-framework`, `vulnerability-management-model`,
`identity-governance-reviews`, `ot-security-baseline`.
