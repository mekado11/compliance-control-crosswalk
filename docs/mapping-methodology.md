# Mapping Methodology

How a control in `library/control-library.csv` is mapped to framework requirements, what each
mapping strength means, and what this crosswalk deliberately refuses to claim.

All content is synthetic and illustrative. Framework identifiers are drawn from the public
catalogues named in `README.md`; the mappings themselves are editorial judgements made under the
rules below, and they are the part a reviewer should challenge.

## 1. The unit of mapping

The unit is **one enterprise control to one framework requirement identifier**, not framework to
framework. Framework-to-framework crosswalks — mapping ISO A.8.8 to SP 800-53 SI-2 directly — look
efficient and fail in practice for two reasons:

1. They produce an N×N problem. Eleven frameworks is 55 pairwise mappings, each maintained
   separately, each drifting at a different rate.
2. They have no implementation anchor. Two requirements can be semantically similar and satisfied
   by entirely different controls in a given enterprise, and it is the enterprise's control that
   produces the evidence an auditor tests.

Mapping through a single internal control library makes the problem 11 one-way mappings from a
stable centre, and every mapping terminates in something that actually exists and produces
evidence.

```
                    ┌──────────────────────────┐
  NIST SP 800-53 ◄──┤                          ├──► HIPAA Security Rule
  NIST CSF 2.0   ◄──┤   Enterprise control     ├──► FedRAMP Moderate
  SOC 2          ◄──┤   library (60 controls)  ├──► CMMC Level 2
  ISO 27001:2022 ◄──┤   owner · evidence ·     ├──► ISA/IEC 62443
  SOX ITGC       ◄──┤   test · automation      ├──► NERC CIP
                    └──────────────────────────┘──► GDPR
```

## 2. What makes something a control in this library

A row qualifies only if all four are true:

| Criterion | Why it is a criterion |
| --- | --- |
| It describes something the enterprise **does**, not something it must achieve | "Protect confidentiality" is an objective; "encrypt regulated data at rest with approved algorithms, with key access separated from data access" is a control |
| It has a **single accountable owner role** | A control with two owners has none. Where two functions genuinely share work, the control is split into two controls |
| It produces **evidence that exists independently of the assertion** | A control whose only evidence is someone saying it operates is a policy statement, not a control |
| It has a **test procedure that can fail** | If no realistic execution of the test produces a finding, the test is theatre and the control is unverifiable |

The last criterion removes more candidate controls than the other three combined. It is the reason
this library has 60 controls rather than 400: most framework requirements decompose into a small
number of enterprise controls plus a large number of scope statements.

## 3. Mapping strength

Every crosswalk row carries one of three strengths. The distinction is the substance of the whole
artifact — a crosswalk without it is a claim that everything maps to everything.

| Strength | Definition | Credit toward the obligation | Typical case |
| --- | --- | --- | --- |
| **full** | Operating this control as written satisfies the framework requirement within the declared scope, with no material element left unaddressed | 1.0 | DP-01 → HIPAA 164.312(e)(2)(ii): the requirement is encryption in transit, and the control is exactly that |
| **partial** | The control satisfies a material portion; at least one other control is required to complete it | 0.5 | AC-01 → 45 CFR 164.308(a)(4)(ii)(B): account lifecycle covers provisioning and revocation, but the authorization-policy element requires AC-02 |
| **supporting** | The control produces evidence relevant to the requirement or enables another control to satisfy it, but does not satisfy any element itself | 0.0 | AU-04-class time synchronization toward incident-response requirements: necessary for correlation, satisfying nothing on its own |

**Supporting maps are scored at zero on purpose.** Their value is investigative — they tell you
which other controls an auditor will pull when testing an obligation — and letting them accumulate
credit is how a crosswalk manufactures compliance that does not exist. The scoring test
`test_supporting_mapping_never_closes_an_obligation` exists so this cannot be quietly changed.

## 4. Scoring an obligation

`scripts/gap_report.py` computes, for each (framework, requirement) pair in the declared scope:

```
credit(control, obligation) = implementation_credit(control) × strength_credit(mapping)

implementation_credit:  implemented 1.0 · partial 0.5 · planned 0.0 · not-implemented 0.0
                        not-applicable → obligation excluded from the denominator entirely
strength_credit:        full 1.0 · partial 0.5 · supporting 0.0

obligation_credit = max over all mapped controls
state             = met (≥1.0) · partial (>0) · gap (0)
```

Two properties of this formula are deliberate and both are contestable:

- **Maximum, not sum.** Two partially implemented controls at 0.5 each do not add up to a met
  obligation. Summing would let a program accumulate credit from half-built controls and report
  coverage it cannot demonstrate in a test. The cost of this choice is that a genuine case of two
  complementary partial controls fully covering a requirement is under-reported, and the reviewer
  has to resolve it by hand. Under-reporting is the safer direction of error in an audit artifact.
- **Partial implementation halves full mappings.** A perfectly mapped control that only operates in
  half the estate cannot be reported as met. This makes scope the enemy of the score, which is
  correct: partial-scope implementation is the single most common reason a control that "exists"
  fails a test.

## 5. Unmapped requirements are a finding, not an omission

The crosswalk is built from controls outward, so it will never contain every requirement in every
framework. Two distinct situations arise and they must not be confused:

| Situation | What it means | Correct response |
| --- | --- | --- |
| A requirement exists in the framework and no control in the library maps to it | The library has a hole, or the requirement is out of scope for the assessment boundary | Add a control, or record an explicit applicability exclusion in the scope profile with a reason |
| A control maps to nothing in a declared framework | The control is either enterprise-specific (fine) or the mapping has not been researched (not fine) | Every control in this library maps to at least one framework; the test `test_every_control_maps_somewhere` enforces this |

Scope profiles carry `excluded_controls` with a written reason per exclusion, so the exclusions are
visible in the report rather than silently reducing the denominator. A compliance artifact that can
improve its own score by narrowing scope without saying so is not an assurance instrument.

## 6. Framework-specific mapping conventions

| Framework | Identifier convention used | Notes |
| --- | --- | --- |
| NIST SP 800-53 Rev 5 | Control and enhancement, e.g. `AC-6(9)` | Enhancements are mapped separately from their base control where the enhancement adds a distinct obligation |
| NIST CSF 2.0 | Subcategory, e.g. `PR.AA-05` | CSF is an outcome framework; most mappings are full at subcategory level and the Govern function carries the program controls |
| SOC 2 | Trust services criteria point, e.g. `CC6.2`, `P5.1` | Mapped to criteria, not to the service organization's own control numbers, which are entity-specific |
| HIPAA Security Rule | CFR citation, e.g. `164.312(a)(2)(iv)` | Addressable versus required is a property of the regulation, not of the mapping; the distinction is handled in `conflict-reconciliation.md` §4 |
| FedRAMP Moderate | 800-53 identifier plus `(M)` | FedRAMP inherits the 800-53 catalogue with parameter values and additional requirements; parameters are noted in the mapping note field, not encoded |
| CMMC Level 2 | Practice identifier, e.g. `AC.L2-3.1.5` | Level 2 practices track NIST SP 800-171; the mapping is to the practice, and assessment objectives are not modelled |
| ISO/IEC 27001:2022 | Annex A control, plus clause references where the obligation lives in the management system clauses, e.g. `6.1.3` | Clause-level obligations matter for governance controls and are missed by Annex-A-only crosswalks |
| ISA/IEC 62443 | Part plus requirement, e.g. `62443-3-3 SR 2.1`, `62443-4-1 SM-9` | Security level targets are an attribute of the zone, not of the control, and are set in the zone model rather than here |
| NERC CIP | Standard, version and requirement, e.g. `CIP-007-6 R2.3` | Prescriptive; see §7 |
| SOX ITGC | Internal identifier, e.g. `ITGC-ACC-03` | There is no external SOX control catalogue. These are the enterprise's own key control numbers under a PCAOB AS 2201 framing, and they are stated as internal in every report |
| GDPR | Article, e.g. `Art.32(1)(b)` | Articles state outcomes and obligations of the controller; most security mappings land on Art. 32 and are partial by nature |

## 7. Prescriptive versus risk-based frameworks

The frameworks in this crosswalk are not the same kind of object, and mapping them as if they were
is the defect that makes most crosswalks unusable in a regulated environment.

- **Risk-based** (ISO 27001, CSF 2.0, SOC 2, GDPR Art. 32): the requirement is to select and operate
  controls proportionate to assessed risk. The enterprise's own judgement is part of the standard.
  A documented, compensated deviation can still be conforming.
- **Prescriptive** (NERC CIP, FedRAMP baselines, CMMC, several HIPAA required specifications): the
  requirement names a control, an interval, or an artifact. The enterprise's risk judgement does not
  substitute for it. A deviation is a violation, not an accepted risk.

The crosswalk records the identifier in both cases, but the **consequence of a gap differs**, and
`docs/conflict-reconciliation.md` §2 sets out how a gap is handled in each. The gap report does not
attempt to encode this distinction in its scoring, because a single score that blends "we accepted
this risk" with "we are in violation of a mandatory standard" is worse than no score. It is stated
in the scope profile notes instead, where a human reads it.

## 8. Maintenance

| Trigger | Action | Owner |
| --- | --- | --- |
| Framework revision published | Re-map affected controls; record the previous identifier in the mapping note; do not delete history | Compliance Manager |
| New framework brought into scope | Map from the existing library first; add controls only where a genuine capability gap is found, not to mirror the new framework's structure | Compliance Manager |
| Control added or materially reworded | Map to all in-scope frameworks in the same change; a control with no mappings fails the test suite | Control owner |
| Audit challenges a mapping | Record the challenge and the resolution in the mapping note; a mapping that has survived a challenge is more valuable than one that has never been tested | Compliance Manager |
| Annual review | Sample 10% of full mappings and re-derive them independently; measure disagreement rate | Internal Audit |

The disagreement rate from that last row is the only real measure of crosswalk quality. A mapping
set nobody has ever independently re-derived has an unknown error rate, and unknown error rates in
compliance artifacts are discovered at the worst possible time.
