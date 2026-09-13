# Reconciling Conflicting Framework Requirements

Where two in-scope frameworks require different things of the same control, this document sets the
rule for what the enterprise does. Without a written rule the decision gets made per audit, by
whoever is in the room, and the enterprise ends up with a control that satisfies neither framework
and an evidence set that contradicts itself across two reports.

All examples are synthetic.

## 1. The four kinds of conflict

Most apparent conflicts are one of these, and the resolution differs for each. Misclassifying the
conflict is how programs end up over-engineering a control to satisfy a requirement that never
applied to that system.

| Type | Description | Resolution principle |
| --- | --- | --- |
| **Stringency** | Both frameworks require the same control; one is stricter (interval, coverage, retention) | Implement the strictest, apply it to the union of scopes, evidence once |
| **Scope** | The same control is required, but over different populations | Implement to the strictest standard over each population separately; do not average |
| **Direct** | The frameworks require incompatible behaviours | Escalate; cannot be resolved by an engineer or a compliance analyst |
| **Apparent** | The requirements look different because the frameworks use different vocabularies for the same outcome | Map both to one control; document the reading |

Apparent conflicts are the most common by volume and the least consequential. Direct conflicts are
rare and consume disproportionate senior time, which is exactly why the escalation path has to be
pre-agreed.

## 2. Stringency conflicts: adopt the strictest, once

**Rule.** Where multiple frameworks impose the same control at different strictness, the enterprise
standard is the strictest, applied across the union of in-scope populations, unless the cost of
extending it beyond the demanding population exceeds the cost of maintaining two standards — in
which case the split is documented in the control's scope statement rather than left implicit.

**Worked example — audit log retention.**

| Source | Requirement | Population |
| --- | --- | --- |
| HIPAA 164.316(b)(2)(i) | Retain documentation 6 years | Systems processing protected health information |
| SOX ITGC practice | Retention through the audit cycle, typically 12 months of detailed logs | Financially relevant systems |
| FedRAMP Moderate AU-11 | 90 days online, 1 year total, with defined parameter values | SaaS platform authorization boundary |
| NERC CIP-007-6 R4.3 | 90 days of logs retained | Cyber systems within CIP scope |
| GDPR Art. 5(1)(e) | Retain no longer than necessary for the purpose | Logs containing personal data |

Note the last row points the opposite way to the first four. This is the case that makes "adopt the
strictest" insufficient on its own: maximum-retention obligations and minimum-retention obligations
are both real, and the resolution is scope separation, not a single number.

**Resolution adopted.** Retention is set per log class, not per system: security audit records (6
years, the HIPAA-driven maximum applied across the estate because per-system separation of log
pipelines cost more than the storage); operational logs containing personal data (13 months, with a
documented necessity argument); and access logs within the industrial boundary (6 years, exceeding
CIP's 90 days because the same pipeline serves both and splitting it would create two evidence
trails). The GDPR necessity argument is documented once, in the records of processing, and cited by
the control rather than restated.

**Cost of the decision.** Storage cost approximately tripled against a 13-month baseline. Accepted
because the alternative — per-system retention policies — would require the log platform to be
scope-aware, which is a permanent engineering burden and a permanent source of misconfiguration.

## 3. Scope conflicts: separate populations, never average

**Rule.** When a control must be stronger for a subset, implement two documented tiers with an
explicit population boundary. Applying an intermediate standard to everything satisfies the
demanding framework nowhere and wastes effort everywhere.

**Worked example — multi-factor authentication.** FedRAMP Moderate requires phishing-resistant
authentication for privileged access within the authorization boundary. NERC CIP-005-6 R2.3
requires multi-factor for interactive remote access to the industrial environment. HIPAA treats
person-or-entity authentication as required but does not specify a factor count. ISO 27001 A.8.5
requires secure authentication proportionate to risk.

**Resolution.** Three tiers with a named population each: phishing-resistant factors for all
privileged and authorization-boundary access; multi-factor for all interactive remote access
including industrial; multi-factor for all other interactive human access, with registered,
expiring exemptions. The populations are defined by system inventory attributes, so the coverage
denominator is computable rather than negotiated — which is the part that makes the tiering
enforceable instead of aspirational.

**What was rejected.** A single enterprise "MFA everywhere" standard. It reads better in a policy
and it produces an unfalsifiable coverage number, because the denominator quietly becomes "systems
where MFA is possible."

## 4. Required, addressable, and the HIPAA trap

HIPAA distinguishes **required** implementation specifications from **addressable** ones.
Addressable does not mean optional. It means the covered entity must assess whether the
specification is reasonable and appropriate and, if not, document why and implement an equivalent
alternative.

The failure mode is treating addressable specifications as a discretionary list. The enterprise
rule here:

1. Every addressable specification receives a documented assessment, whether or not it is
   implemented.
2. A decision not to implement requires a named alternative measure and a named decision-maker.
3. The assessment is refreshed when the environment materially changes, not only at audit time.
4. Encryption at rest (164.312(a)(2)(iv)) is treated as **required in practice** in this program
   regardless of its addressable status, because the alternative-measure argument has become
   difficult to sustain and the cost of implementation is now lower than the cost of defending the
   assessment. That is a judgement, it is recorded as one, and it is revisited annually.

## 5. Direct conflicts: escalate, do not engineer around

Direct conflicts cannot be resolved by choosing the stricter option, because compliance with one
constitutes non-compliance with the other. Two synthetic examples:

**Log retention versus erasure.** A GDPR erasure request covers personal data in security audit
logs, while HIPAA and CIP require retention of those records. Resolution path: legal determines
whether an exemption applies (in most such cases the controller's legal obligation and the
establishment of legal claims are the relevant grounds), the determination is recorded against the
request, and the data subject receives a reasoned response. **The engineer does not resolve this by
deleting the record.** The control that matters is that the request reaches legal before anything is
deleted, which is why PR-02's test procedure checks refusals cite an exemption.

**Data residency versus centralized monitoring.** A transfer restriction conflicts with routing
telemetry to a single monitoring platform in another jurisdiction. Resolution path: assess whether
the telemetry contains personal data (frequently it does — usernames, IP addresses, device
identifiers), then choose between regional processing with federated alerting, a transfer mechanism
with supplementary measures, or field-level minimization at collection. All three are expensive; the
cheap option, moving the data and not documenting the assessment, is the one that produces a
supervisory-authority finding.

**Escalation path for any direct conflict:** control owner → Compliance Manager → General Counsel →
Security Steering Committee, with the committee deciding only where the resolution has material
cost or accepts regulatory exposure. Interim posture while unresolved: **the more restrictive
option**, because unwinding an over-restriction is a change request and unwinding an unlawful
transfer is a notification.

## 6. Risk-based versus prescriptive: the rule that matters most

| | Risk-based requirement | Prescriptive requirement |
| --- | --- | --- |
| Examples | ISO 27001 Annex A with 6.1.3 justification, CSF 2.0 outcomes, SOC 2 criteria, GDPR Art. 32 | NERC CIP requirements, FedRAMP baseline parameters, CMMC practices, HIPAA required specifications |
| Is a documented risk acceptance a valid response to a gap? | **Yes**, if it follows the enterprise acceptance process and the residual is within appetite | **No**. Never |
| What is the correct response to a gap? | Treat, accept with a record, or transfer | Remediate, or follow the standard's own deviation mechanism (for example a CIP mitigation plan with its evaluation cycle), and self-report where required |
| Who decides | Risk owner at the authority tier for the exposure | Compliance and Legal, not the security program |

**The most damaging single error in multi-framework compliance is using an enterprise risk
acceptance to close a gap against a prescriptive requirement.** It feels like governance — there is
a record, an accepter, an expiry, compensating controls — and it produces a self-documented
violation with an audit trail proving the enterprise knew. Worked example in the sibling repository
`security-program-blueprint`: the unsupported-industrial-system acceptance explicitly carves out
the two systems within the prescriptive regulatory boundary and routes them to a mitigation plan
under the standard's own terms.

## 7. Reconciliation register

Every resolved conflict is recorded, because the reasoning is needed again — at the next audit, by
the next analyst, and by whoever inherits the control.

| Field | Purpose |
| --- | --- |
| Conflict ID | Stable reference cited from the affected controls |
| Frameworks and requirement identifiers | Exactly what conflicts |
| Conflict type | Stringency, scope, direct, apparent (§1) |
| Affected controls | Library control IDs |
| Resolution and standard adopted | What the enterprise actually does |
| Reasoning | Why, including the cost comparison where one drove the decision |
| Decision authority and date | Who decided and when |
| Review trigger | What would reopen it — usually a framework revision or a scope change |

Illustrative extract:

| ID | Frameworks | Type | Controls | Resolution |
| --- | --- | --- | --- | --- |
| CR-001 | HIPAA 164.316(b)(2)(i) · FedRAMP AU-11 · CIP-007-6 R4.3 · GDPR Art.5(1)(e) | Stringency + direct | AU-02 | Retention set per log class; 6 years for security audit records, 13 months for operational logs containing personal data with a documented necessity argument |
| CR-002 | FedRAMP IA-2(1) · CIP-005-6 R2.3 · HIPAA 164.312(d) | Scope | IA-01 | Three-tier factor standard with populations defined by inventory attributes |
| CR-003 | GDPR Art.17 · HIPAA 164.316 · CIP-007-6 R4.3 | Direct | PR-02, AU-02 | Erasure requests touching audit records route to legal for an exemption determination before any deletion; determination recorded against the request |
| CR-004 | CMMC AC.L2-3.1.5 · ISO A.8.2 | Apparent | AC-02 | Single least-privilege control; both mapped full. No separate implementation |
| CR-005 | SOX ITGC change approval · CIP-010-4 R1.2 | Stringency | CM-02 | Single change process at the CIP evidentiary standard for all in-scope systems; the incremental cost over the SOX standard was lower than maintaining two change workflows |
