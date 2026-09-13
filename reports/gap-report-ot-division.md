# Compliance gap report — Industrial and energy-services division

Generated 2026-09-13 03:20 by `scripts/gap_report.py` from `implementation-status.csv`. All data is synthetic and illustrative.

**Scope note.** CIP obligations are prescriptive. Where this report shows a gap against a CIP requirement, the response is a mitigation plan under the standard's own terms, not an enterprise risk acceptance - see docs/conflict-reconciliation.md.

## 1. Summary

60 controls in the library. 4 frameworks declared in scope. 284 distinct framework obligations are mapped from those controls.

- **Met** (a fully mapped, implemented control exists): 80 (28%)
- **Partial** (implemented but only partially mapped, or mapped but only partially implemented): 164 (58%)
- **Gap** (no implemented control contributes): 40 (14%)

Partial is the row that matters. A program reporting 'compliant' on a partially mapped obligation is making a claim the crosswalk does not support, and it is the claim an auditor tests first.

## 2. Coverage by framework

| Framework | Obligations mapped | Met | Partial | Gap | Met rate |
| --- | --- | --- | --- | --- | --- |
| N53 | 114 | 30 | 67 | 17 | 26% met |
| CSF | 65 | 17 | 40 | 8 | 26% met |
| IEC62443 | 60 | 18 | 32 | 10 | 30% met |
| CIP | 45 | 15 | 25 | 5 | 33% met |

## 3. Open gaps, by control

An obligation is attributed to the control that provides the most credit toward it. A control shown as `implemented` still appears here when its mapping to an obligation is partial or supporting: the control operates, but it does not close that obligation by itself. Those rows are where a second control has to be named, not where remediation is owed.

| Control | Title | Status | Affected obligations | Frameworks | Exception / acceptance | Owner role |
| --- | --- | --- | --- | --- | --- | --- |
| CM-01 | Secure configuration baselines | partial | 9 | CIP CSF IEC62443 N53 | **none** | Platform Engineering Lead |
| SR-01 | Vendor security assessment and tiering | partial | 8 | CIP CSF IEC62443 N53 | RA-2026-005 | Third-Party Risk Analyst |
| AU-01 | Audit log generation standard | partial | 7 | CIP CSF IEC62443 N53 | **none** | Security Engineer (Detection) |
| AU-03 | Security monitoring and detection content | not-implemented | 7 | CIP CSF IEC62443 N53 | RA-2026-001 | Security Engineer (Detection) |
| IR-02 | Incident detection, triage and escalation | partial | 7 | CIP CSF IEC62443 N53 | **none** | Incident Response Manager |
| PS-02 | Role-based security competence | partial | 7 | CIP CSF IEC62443 N53 | **none** | GRC Manager |
| SI-03 | Software authenticity and integrity verification | planned | 7 | CIP CSF IEC62443 N53 | **none** | Platform Engineering Lead |
| AC-04 | Privileged access brokering and session recording | partial | 6 | CIP IEC62443 N53 | EX-2026-0110 | Security Engineer (IAM) |
| AM-04 | Software bill of materials generation and maintenance | partial | 6 | CIP CSF IEC62443 N53 | **none** | Product Security Lead |
| CP-02 | Disaster recovery objectives and testing | partial | 6 | CIP CSF IEC62443 N53 | **none** | IT Operations Manager |
| IR-04 | Post-incident review and corrective action | partial | 6 | CIP CSF IEC62443 N53 | **none** | Incident Response Manager |
| SA-01 | Secure development lifecycle gates | partial | 6 | CSF IEC62443 N53 | **none** | Product Security Lead |
| DP-04 | Data retention and secure disposal | planned | 5 | CIP CSF IEC62443 N53 | **none** | Data Governance Lead |
| OT-01 | Zone and conduit segmentation | not-implemented | 5 | CIP CSF IEC62443 N53 | RA-2026-003 | OT Security Engineer |
| PE-02 | Media handling and removable media control | partial | 5 | CIP IEC62443 N53 | **none** | Security Engineer (Endpoint) |
| SI-01 | Endpoint protection and detection | partial | 5 | CIP CSF IEC62443 N53 | EX-2026-0077 | Security Engineer (Endpoint) |
| VM-01 | Vulnerability scanning coverage | partial | 5 | CIP CSF IEC62443 N53 | **none** | Security Engineer (Vulnerability) |
| AC-02 | Least privilege and role definition | partial | 4 | CIP IEC62443 N53 | **none** | Security Engineer (IAM) |
| AC-05 | Remote access control | implemented | 4 | CSF IEC62443 N53 | **none** | Network Engineer |
| AM-01 | Hardware asset inventory | partial | 4 | CSF IEC62443 N53 | EX-2026-0091 | IT Operations Manager |
| DP-02 | Encryption at rest | partial | 4 | CIP CSF N53 | **none** | Platform Engineering Lead |
| DP-03 | Cryptographic key management | partial | 4 | IEC62443 N53 | **none** | Security Engineer (Platform) |
| IA-01 | Multi-factor authentication | partial | 4 | CIP IEC62443 N53 | EX-2026-0033 | Security Engineer (IAM) |
| NW-01 | Boundary protection | implemented | 4 | CSF IEC62443 N53 | **none** | Network Engineer |
| OT-02 | Industrial remote and vendor access | partial | 4 | CIP N53 | **none** | OT Security Engineer |
| SI-02 | Patch management | partial | 4 | CIP CSF IEC62443 N53 | **none** | IT Operations Manager |
| SR-02 | Contractual security requirements and flow-down | implemented | 4 | CSF IEC62443 N53 | **none** | General Counsel |
| AC-01 | Account lifecycle management | implemented | 3 | CSF N53 | **none** | Security Engineer (IAM) |
| AM-02 | Software inventory and authorized software | partial | 3 | CSF IEC62443 N53 | **none** | IT Operations Manager |
| CP-01 | Backup and verified restore | implemented | 3 | CSF IEC62443 N53 | **none** | IT Operations Manager |
| GV-04 | Compliance obligation register | partial | 3 | CSF IEC62443 N53 | EX-2026-0142 | Compliance Manager |
| IA-03 | Non-human identity governance | planned | 3 | CIP IEC62443 N53 | **none** | Security Engineer (IAM) |
| RM-01 | Enterprise security risk assessment | implemented | 3 | CIP CSF | **none** | GRC Manager |
| RM-03 | System categorization and impact levels | partial | 3 | CSF IEC62443 N53 | **none** | Enterprise Architect |
| AC-03 | Periodic access certification | implemented | 2 | CSF IEC62443 | **none** | GRC Analyst |
| AC-06 | Separation of duties | partial | 2 | IEC62443 N53 | **none** | GRC Manager |
| AM-03 | Data inventory and classification | planned | 2 | CSF N53 | **none** | Data Governance Lead |
| AU-02 | Log retention, protection and integrity | implemented | 2 | IEC62443 N53 | **none** | Security Engineer (Detection) |
| CM-02 | Change management and approval | implemented | 2 | N53 | **none** | IT Operations Manager |
| DP-01 | Encryption in transit | implemented | 2 | CIP N53 | **none** | Network Engineer |
| GV-03 | Risk acceptance and exception governance | implemented | 2 | CIP CSF | **none** | GRC Manager |
| IA-02 | Authenticator management | implemented | 2 | CSF IEC62443 | **none** | Security Engineer (IAM) |
| IR-03 | Regulatory and contractual breach notification | implemented | 2 | CSF N53 | **none** | General Counsel |
| NW-02 | Egress control and data movement monitoring | not-implemented | 2 | IEC62443 N53 | RA-2026-004 | Network Engineer |
| OT-03 | Unsupported industrial system compensations | partial | 2 | CIP N53 | RA-2026-006 | OT Security Engineer |
| PS-01 | Personnel screening and access authorization | implemented | 2 | CSF N53 | **none** | HR Business Partner |
| SA-04 | Environment separation and non-production data | not-implemented | 2 | IEC62443 N53 | EX-2026-0156 | Platform Engineering Lead |
| SR-03 | Supplier component provenance | planned | 2 | CSF IEC62443 | **none** | Product Security Lead |
| VM-02 | Remediation within severity-based service levels | partial | 2 | CSF N53 | **none** | Security Engineer (Vulnerability) |
| VM-03 | Penetration testing | implemented | 2 | CIP N53 | **none** | Security Manager |
| GV-02 | Security roles, responsibilities and decision authority | implemented | 1 | N53 | **none** | CISO |
| IR-01 | Incident response plan and severity model | implemented | 1 | N53 | **none** | Incident Response Manager |
| PE-01 | Physical access control | implemented | 1 | N53 | **none** | Facilities Manager |
| RM-02 | Risk register and treatment tracking | implemented | 1 | CSF | **none** | GRC Manager |

**5 control(s) are unimplemented with no registered exception or acceptance: SI-03, DP-04, IA-03, AM-03, SR-03.** An unimplemented control without a record is not a risk decision, it is an undocumented deviation, and it is the finding an auditor writes up as a governance failure rather than a control failure.

## 4. Highest-leverage remediations

Ranked by the number of in-scope framework obligations closed by bringing one control to fully implemented. This is the ordering a resource-constrained program should work in, adjusted for the risk reduction each control delivers — which this script deliberately does not model, because obligation count and risk reduction are different quantities and collapsing them hides the trade-off.

| Control | Title | Current status | Obligations closed | Frameworks touched | Which | Automation rating |
| --- | --- | --- | --- | --- | --- | --- |
| OT-01 | Zone and conduit segmentation | not-implemented | 9 | 4 | CIP CSF IEC62443 N53 | 3 |
| OT-03 | Unsupported industrial system compensations | partial | 9 | 4 | CIP CSF IEC62443 N53 | 3 |
| AC-04 | Privileged access brokering and session recording | partial | 8 | 4 | CIP CSF IEC62443 N53 | 4 |
| AU-03 | Security monitoring and detection content | not-implemented | 8 | 4 | CIP CSF IEC62443 N53 | 3 |
| CM-01 | Secure configuration baselines | partial | 8 | 4 | CIP CSF IEC62443 N53 | 5 |
| IR-02 | Incident detection, triage and escalation | partial | 8 | 4 | CIP CSF IEC62443 N53 | 3 |
| OT-02 | Industrial remote and vendor access | partial | 8 | 4 | CIP CSF IEC62443 N53 | 4 |
| SI-03 | Software authenticity and integrity verification | planned | 8 | 4 | CIP CSF IEC62443 N53 | 4 |
| SR-01 | Vendor security assessment and tiering | partial | 8 | 4 | CIP CSF IEC62443 N53 | 2 |
| SR-03 | Supplier component provenance | planned | 8 | 4 | CIP CSF IEC62443 N53 | 4 |
| AU-01 | Audit log generation standard | partial | 7 | 4 | CIP CSF IEC62443 N53 | 4 |
| CP-02 | Disaster recovery objectives and testing | partial | 7 | 4 | CIP CSF IEC62443 N53 | 2 |
| NW-02 | Egress control and data movement monitoring | not-implemented | 7 | 4 | CIP CSF IEC62443 N53 | 4 |
| PS-02 | Role-based security competence | partial | 7 | 4 | CIP CSF IEC62443 N53 | 4 |
| SA-01 | Secure development lifecycle gates | partial | 7 | 3 | CSF IEC62443 N53 | 3 |

## 5. Evidence burden and reuse

56 evidence-producing controls are in scope. They carry 380 obligation references across 4 frameworks — a reuse ratio of **6.8 obligations satisfied per evidence artifact**. Collecting the same artifact once per framework instead would multiply the collection cost by roughly that factor. See `docs/evidence-reuse-model.md`.

| Control | Title | Frameworks | Obligation refs | Test frequency | Automation |
| --- | --- | --- | --- | --- | --- |
| AC-04 | Privileged access brokering and session recording | 4 | 9 | Quarterly | 4 |
| CM-01 | Secure configuration baselines | 4 | 9 | Monthly | 5 |
| OT-01 | Zone and conduit segmentation | 4 | 9 | Semi-annual | 3 |
| OT-02 | Industrial remote and vendor access | 4 | 9 | Quarterly | 4 |
| OT-03 | Unsupported industrial system compensations | 4 | 9 | Quarterly | 3 |
| AC-05 | Remote access control | 4 | 8 | Quarterly | 4 |
| SI-03 | Software authenticity and integrity verification | 4 | 8 | Quarterly | 4 |
| AU-02 | Log retention, protection and integrity | 4 | 8 | Annual | 4 |
| AU-03 | Security monitoring and detection content | 4 | 8 | Monthly | 3 |
| IR-02 | Incident detection, triage and escalation | 4 | 8 | Quarterly | 3 |
| CP-01 | Backup and verified restore | 4 | 8 | Quarterly | 3 |
| SR-01 | Vendor security assessment and tiering | 4 | 8 | Annual | 2 |

Automation feasibility distribution across in-scope controls (5 = evidence generated by machine, 1 = manual by nature):

| Rating | Controls | Share |
| --- | --- | --- |
| 5 | 10 | 18% |
| 4 | 20 | 36% |
| 3 | 14 | 25% |
| 2 | 9 | 16% |
| 1 | 3 | 5% |

12 in-scope controls rate 2 or below, meaning their evidence will be assembled by a human every cycle regardless of tooling investment. Any automation business case that promises to eliminate the compliance calendar has mis-scoped these.

## 6. Testing calendar load

| Test frequency | Controls |
| --- | --- |
| Quarterly | 22 |
| Annual | 12 |
| Monthly | 12 |
| Semi-annual | 6 |
| Per release | 2 |
| Per incident | 1 |
| Per build | 1 |

## 7. Control implementation status

| Status | Controls | Share |
| --- | --- | --- |
| implemented | 21 | 35% |
| partial | 26 | 43% |
| planned | 5 | 8% |
| not-implemented | 4 | 7% |
| not-applicable | 4 | 7% |

---

Mapping strength credit: full 1.0, partial 0.5, supporting 0.0. Implementation credit: implemented 1.0, partial 0.5, planned and not-implemented 0.0. An obligation is **met** only at combined credit 1.0. The reasoning behind these weights is in `docs/mapping-methodology.md` §4.
