# Compliance gap report — Enterprise core obligations

Generated 2026-09-13 03:20 by `scripts/gap_report.py` from `implementation-status.csv`. All data is synthetic and illustrative.

**Scope note.** ISO 27001:2022 is used as a structural reference and gap-assessed only; no certification is being pursued. SOX identifiers are internal ITGC control numbers, not an external catalogue.

## 1. Summary

60 controls in the library. 7 frameworks declared in scope. 400 distinct framework obligations are mapped from those controls.

- **Met** (a fully mapped, implemented control exists): 115 (29%)
- **Partial** (implemented but only partially mapped, or mapped but only partially implemented): 225 (56%)
- **Gap** (no implemented control contributes): 60 (15%)

Partial is the row that matters. A program reporting 'compliant' on a partially mapped obligation is making a claim the crosswalk does not support, and it is the claim an auditor tests first.

## 2. Coverage by framework

| Framework | Obligations mapped | Met | Partial | Gap | Met rate |
| --- | --- | --- | --- | --- | --- |
| N53 | 121 | 30 | 73 | 18 | 25% met |
| CSF | 66 | 17 | 43 | 6 | 26% met |
| SOC2 | 37 | 14 | 20 | 3 | 38% met |
| HIPAA | 49 | 20 | 22 | 7 | 41% met |
| ISO | 61 | 18 | 32 | 11 | 30% met |
| SOX | 34 | 6 | 20 | 8 | 18% met |
| GDPR | 32 | 10 | 15 | 7 | 31% met |

## 3. Open gaps, by control

An obligation is attributed to the control that provides the most credit toward it. A control shown as `implemented` still appears here when its mapping to an obligation is partial or supporting: the control operates, but it does not close that obligation by itself. Those rows are where a second control has to be named, not where remediation is owed.

| Control | Title | Status | Affected obligations | Frameworks | Exception / acceptance | Owner role |
| --- | --- | --- | --- | --- | --- | --- |
| SR-01 | Vendor security assessment and tiering | partial | 14 | CSF GDPR HIPAA ISO N53 SOC2 SOX | RA-2026-005 | Third-Party Risk Analyst |
| PR-01 | Records of processing and lawful basis | partial | 11 | CSF GDPR HIPAA ISO N53 SOC2 | **none** | Data Protection Officer |
| CM-01 | Secure configuration baselines | partial | 10 | CSF ISO N53 SOC2 SOX | **none** | Platform Engineering Lead |
| AU-01 | Audit log generation standard | partial | 9 | CSF HIPAA ISO N53 SOX | **none** | Security Engineer (Detection) |
| CP-02 | Disaster recovery objectives and testing | partial | 9 | CSF HIPAA ISO N53 SOX | **none** | IT Operations Manager |
| DP-04 | Data retention and secure disposal | planned | 9 | CSF HIPAA ISO N53 SOC2 | **none** | Data Governance Lead |
| AC-02 | Least privilege and role definition | partial | 8 | GDPR HIPAA ISO N53 SOC2 SOX | **none** | Security Engineer (IAM) |
| IR-02 | Incident detection, triage and escalation | partial | 8 | CSF GDPR HIPAA ISO N53 | **none** | Incident Response Manager |
| PS-02 | Role-based security competence | partial | 7 | CSF GDPR HIPAA ISO N53 | **none** | GRC Manager |
| SA-01 | Secure development lifecycle gates | partial | 7 | CSF GDPR ISO N53 SOX | **none** | Product Security Lead |
| SR-02 | Contractual security requirements and flow-down | implemented | 7 | CSF GDPR ISO N53 SOX | **none** | General Counsel |
| AC-04 | Privileged access brokering and session recording | partial | 6 | HIPAA ISO N53 SOX | EX-2026-0110 | Security Engineer (IAM) |
| AC-05 | Remote access control | implemented | 6 | CSF HIPAA ISO N53 SOX | **none** | Network Engineer |
| AU-03 | Security monitoring and detection content | not-implemented | 6 | CSF ISO N53 | RA-2026-001 | Security Engineer (Detection) |
| IR-04 | Post-incident review and corrective action | partial | 6 | CSF ISO N53 SOC2 | **none** | Incident Response Manager |
| RM-03 | System categorization and impact levels | partial | 6 | CSF GDPR HIPAA ISO N53 SOX | **none** | Enterprise Architect |
| SA-03 | Product security postmarket obligations | partial | 6 | CSF ISO N53 | **none** | Product Security Lead |
| SA-04 | Environment separation and non-production data | not-implemented | 6 | GDPR HIPAA ISO N53 SOX | EX-2026-0156 | Platform Engineering Lead |
| SI-01 | Endpoint protection and detection | partial | 6 | CSF HIPAA ISO N53 SOC2 | EX-2026-0077 | Security Engineer (Endpoint) |
| SI-03 | Software authenticity and integrity verification | planned | 6 | CSF HIPAA N53 SOX | **none** | Platform Engineering Lead |
| AM-01 | Hardware asset inventory | partial | 5 | CSF ISO N53 SOX | EX-2026-0091 | IT Operations Manager |
| AM-04 | Software bill of materials generation and maintenance | partial | 5 | CSF ISO N53 | **none** | Product Security Lead |
| DP-02 | Encryption at rest | partial | 5 | CSF HIPAA N53 SOC2 | **none** | Platform Engineering Lead |
| GV-02 | Security roles, responsibilities and decision authority | implemented | 5 | GDPR ISO N53 SOC2 | **none** | CISO |
| GV-04 | Compliance obligation register | partial | 5 | CSF ISO N53 SOX | EX-2026-0142 | Compliance Manager |
| IA-01 | Multi-factor authentication | partial | 5 | HIPAA ISO N53 SOX | EX-2026-0033 | Security Engineer (IAM) |
| IR-03 | Regulatory and contractual breach notification | implemented | 5 | CSF HIPAA ISO N53 SOC2 | **none** | General Counsel |
| PE-02 | Media handling and removable media control | partial | 5 | HIPAA ISO N53 | **none** | Security Engineer (Endpoint) |
| PR-02 | Data subject rights fulfilment | implemented | 5 | GDPR N53 SOC2 | **none** | Data Protection Officer |
| PR-03 | Data protection impact assessment | partial | 5 | GDPR N53 SOC2 | **none** | Data Protection Officer |
| RM-01 | Enterprise security risk assessment | implemented | 5 | CSF GDPR ISO SOX | **none** | GRC Manager |
| VM-01 | Vulnerability scanning coverage | partial | 5 | CSF ISO N53 SOX | **none** | Security Engineer (Vulnerability) |
| AC-01 | Account lifecycle management | implemented | 4 | CSF HIPAA N53 | **none** | Security Engineer (IAM) |
| AC-06 | Separation of duties | partial | 4 | HIPAA N53 SOC2 SOX | **none** | GRC Manager |
| AM-02 | Software inventory and authorized software | partial | 4 | CSF ISO N53 SOX | **none** | IT Operations Manager |
| CP-01 | Backup and verified restore | implemented | 4 | CSF HIPAA N53 SOC2 | **none** | IT Operations Manager |
| GV-03 | Risk acceptance and exception governance | implemented | 4 | CSF ISO SOC2 SOX | **none** | GRC Manager |
| NW-01 | Boundary protection | implemented | 4 | CSF ISO N53 | **none** | Network Engineer |
| NW-02 | Egress control and data movement monitoring | not-implemented | 4 | ISO N53 | RA-2026-004 | Network Engineer |
| PE-01 | Physical access control | implemented | 4 | HIPAA ISO N53 SOX | **none** | Facilities Manager |
| RM-02 | Risk register and treatment tracking | implemented | 4 | CSF GDPR SOC2 SOX | **none** | GRC Manager |
| AM-03 | Data inventory and classification | planned | 3 | HIPAA ISO SOX | **none** | Data Governance Lead |
| AU-02 | Log retention, protection and integrity | implemented | 3 | GDPR N53 SOC2 | **none** | Security Engineer (Detection) |
| CM-02 | Change management and approval | implemented | 3 | HIPAA N53 | **none** | IT Operations Manager |
| DP-03 | Cryptographic key management | partial | 3 | N53 | **none** | Security Engineer (Platform) |
| GV-01 | Information security policy suite | implemented | 3 | GDPR SOC2 SOX | **none** | CISO |
| IR-01 | Incident response plan and severity model | implemented | 3 | ISO N53 SOC2 | **none** | Incident Response Manager |
| PS-01 | Personnel screening and access authorization | implemented | 3 | CSF GDPR N53 | **none** | HR Business Partner |
| SI-02 | Patch management | partial | 3 | CSF N53 SOX | **none** | IT Operations Manager |
| VM-03 | Penetration testing | implemented | 3 | ISO N53 SOC2 | **none** | Security Manager |
| IA-02 | Authenticator management | implemented | 2 | CSF SOX | **none** | Security Engineer (IAM) |
| IA-03 | Non-human identity governance | planned | 2 | N53 SOX | **none** | Security Engineer (IAM) |
| VM-02 | Remediation within severity-based service levels | partial | 2 | CSF N53 | **none** | Security Engineer (Vulnerability) |
| AC-03 | Periodic access certification | implemented | 1 | CSF | **none** | GRC Analyst |
| DP-01 | Encryption in transit | implemented | 1 | N53 | **none** | Network Engineer |
| SR-03 | Supplier component provenance | planned | 1 | CSF | **none** | Product Security Lead |

**5 control(s) are unimplemented with no registered exception or acceptance: DP-04, SI-03, AM-03, IA-03, SR-03.** An unimplemented control without a record is not a risk decision, it is an undocumented deviation, and it is the finding an auditor writes up as a governance failure rather than a control failure.

## 4. Highest-leverage remediations

Ranked by the number of in-scope framework obligations closed by bringing one control to fully implemented. This is the ordering a resource-constrained program should work in, adjusted for the risk reduction each control delivers — which this script deliberately does not model, because obligation count and risk reduction are different quantities and collapsing them hides the trade-off.

| Control | Title | Current status | Obligations closed | Frameworks touched | Which | Automation rating |
| --- | --- | --- | --- | --- | --- | --- |
| SR-01 | Vendor security assessment and tiering | partial | 14 | 7 | CSF GDPR HIPAA ISO N53 SOC2 SOX | 2 |
| AM-03 | Data inventory and classification | planned | 13 | 7 | CSF GDPR HIPAA ISO N53 SOC2 SOX | 3 |
| CP-02 | Disaster recovery objectives and testing | partial | 13 | 7 | CSF GDPR HIPAA ISO N53 SOC2 SOX | 2 |
| DP-04 | Data retention and secure disposal | planned | 12 | 6 | CSF GDPR HIPAA ISO N53 SOC2 | 3 |
| IR-02 | Incident detection, triage and escalation | partial | 12 | 6 | CSF GDPR HIPAA ISO N53 SOC2 | 3 |
| AC-04 | Privileged access brokering and session recording | partial | 11 | 6 | CSF HIPAA ISO N53 SOC2 SOX | 4 |
| NW-02 | Egress control and data movement monitoring | not-implemented | 11 | 6 | CSF GDPR HIPAA ISO N53 SOC2 | 4 |
| PR-01 | Records of processing and lawful basis | partial | 11 | 5 | CSF GDPR ISO N53 SOC2 | 2 |
| SA-04 | Environment separation and non-production data | not-implemented | 11 | 7 | CSF GDPR HIPAA ISO N53 SOC2 SOX | 4 |
| AC-02 | Least privilege and role definition | partial | 10 | 6 | CSF HIPAA ISO N53 SOC2 SOX | 3 |
| AU-01 | Audit log generation standard | partial | 10 | 6 | CSF HIPAA ISO N53 SOC2 SOX | 4 |
| CM-01 | Secure configuration baselines | partial | 10 | 5 | CSF ISO N53 SOC2 SOX | 5 |
| GV-04 | Compliance obligation register | partial | 10 | 7 | CSF GDPR HIPAA ISO N53 SOC2 SOX | 2 |
| IA-01 | Multi-factor authentication | partial | 10 | 6 | CSF HIPAA ISO N53 SOC2 SOX | 5 |
| AC-06 | Separation of duties | partial | 9 | 6 | CSF HIPAA ISO N53 SOC2 SOX | 3 |

## 5. Evidence burden and reuse

57 evidence-producing controls are in scope. They carry 611 obligation references across 7 frameworks — a reuse ratio of **10.7 obligations satisfied per evidence artifact**. Collecting the same artifact once per framework instead would multiply the collection cost by roughly that factor. See `docs/evidence-reuse-model.md`.

| Control | Title | Frameworks | Obligation refs | Test frequency | Automation |
| --- | --- | --- | --- | --- | --- |
| AM-03 | Data inventory and classification | 7 | 14 | Semi-annual | 3 |
| SA-04 | Environment separation and non-production data | 7 | 14 | Quarterly | 4 |
| SR-01 | Vendor security assessment and tiering | 7 | 14 | Annual | 2 |
| SR-02 | Contractual security requirements and flow-down | 7 | 14 | Annual | 2 |
| RM-01 | Enterprise security risk assessment | 7 | 13 | Annual | 2 |
| AC-01 | Account lifecycle management | 7 | 13 | Monthly | 4 |
| AC-04 | Privileged access brokering and session recording | 7 | 13 | Quarterly | 4 |
| AC-05 | Remote access control | 7 | 13 | Quarterly | 4 |
| CM-01 | Secure configuration baselines | 7 | 13 | Monthly | 5 |
| CP-02 | Disaster recovery objectives and testing | 7 | 13 | Annual | 2 |
| GV-02 | Security roles, responsibilities and decision authority | 7 | 12 | Annual | 1 |
| GV-03 | Risk acceptance and exception governance | 7 | 12 | Quarterly | 3 |

Automation feasibility distribution across in-scope controls (5 = evidence generated by machine, 1 = manual by nature):

| Rating | Controls | Share |
| --- | --- | --- |
| 5 | 10 | 18% |
| 4 | 19 | 33% |
| 3 | 14 | 25% |
| 2 | 11 | 19% |
| 1 | 3 | 5% |

14 in-scope controls rate 2 or below, meaning their evidence will be assembled by a human every cycle regardless of tooling investment. Any automation business case that promises to eliminate the compliance calendar has mis-scoped these.

## 6. Testing calendar load

| Test frequency | Controls |
| --- | --- |
| Quarterly | 22 |
| Annual | 13 |
| Monthly | 12 |
| Semi-annual | 5 |
| Per release | 2 |
| Per incident | 1 |
| Per build | 1 |
| Per project | 1 |

## 7. Control implementation status

| Status | Controls | Share |
| --- | --- | --- |
| implemented | 22 | 37% |
| partial | 27 | 45% |
| planned | 5 | 8% |
| not-implemented | 3 | 5% |
| not-applicable | 3 | 5% |

---

Mapping strength credit: full 1.0, partial 0.5, supporting 0.0. Implementation credit: implemented 1.0, partial 0.5, planned and not-implemented 0.0. An obligation is **met** only at combined credit 1.0. The reasoning behind these weights is in `docs/mapping-methodology.md` §4.
