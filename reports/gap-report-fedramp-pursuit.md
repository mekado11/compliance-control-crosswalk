# Compliance gap report — SaaS platform FedRAMP Moderate pursuit

Generated 2026-09-13 03:20 by `scripts/gap_report.py` from `implementation-status.csv`. All data is synthetic and illustrative.

**Scope note.** Enterprise status data is reused here deliberately. Control inheritance from the underlying cloud service provider is NOT modelled; inherited controls would materially change this picture and are the first thing a real authorization effort would separate out.

## 1. Summary

60 controls in the library. 6 frameworks declared in scope. 381 distinct framework obligations are mapped from those controls.

- **Met** (a fully mapped, implemented control exists): 114 (30%)
- **Partial** (implemented but only partially mapped, or mapped but only partially implemented): 214 (56%)
- **Gap** (no implemented control contributes): 53 (14%)

Partial is the row that matters. A program reporting 'compliant' on a partially mapped obligation is making a claim the crosswalk does not support, and it is the claim an auditor tests first.

## 2. Coverage by framework

| Framework | Obligations mapped | Met | Partial | Gap | Met rate |
| --- | --- | --- | --- | --- | --- |
| N53 | 118 | 30 | 70 | 18 | 25% met |
| CSF | 66 | 17 | 43 | 6 | 26% met |
| SOC2 | 37 | 14 | 20 | 3 | 38% met |
| FEDRAMP | 54 | 21 | 24 | 9 | 39% met |
| CMMC | 46 | 14 | 26 | 6 | 30% met |
| ISO | 60 | 18 | 31 | 11 | 30% met |

## 3. Open gaps, by control

An obligation is attributed to the control that provides the most credit toward it. A control shown as `implemented` still appears here when its mapping to an obligation is partial or supporting: the control operates, but it does not close that obligation by itself. Those rows are where a second control has to be named, not where remediation is owed.

| Control | Title | Status | Affected obligations | Frameworks | Exception / acceptance | Owner role |
| --- | --- | --- | --- | --- | --- | --- |
| CM-01 | Secure configuration baselines | partial | 11 | CMMC CSF FEDRAMP ISO N53 SOC2 | **none** | Platform Engineering Lead |
| SR-01 | Vendor security assessment and tiering | partial | 11 | CSF FEDRAMP ISO N53 SOC2 | RA-2026-005 | Third-Party Risk Analyst |
| AU-01 | Audit log generation standard | partial | 9 | CMMC CSF FEDRAMP ISO N53 | **none** | Security Engineer (Detection) |
| AU-03 | Security monitoring and detection content | not-implemented | 9 | CMMC CSF FEDRAMP ISO N53 | RA-2026-001 | Security Engineer (Detection) |
| DP-04 | Data retention and secure disposal | planned | 9 | CMMC CSF FEDRAMP ISO N53 SOC2 | **none** | Data Governance Lead |
| IR-02 | Incident detection, triage and escalation | partial | 8 | CMMC CSF FEDRAMP ISO N53 | **none** | Incident Response Manager |
| PR-01 | Records of processing and lawful basis | partial | 8 | CSF FEDRAMP ISO N53 SOC2 | **none** | Data Protection Officer |
| SI-01 | Endpoint protection and detection | partial | 8 | CMMC CSF FEDRAMP ISO N53 SOC2 | EX-2026-0077 | Security Engineer (Endpoint) |
| CP-02 | Disaster recovery objectives and testing | partial | 7 | CSF FEDRAMP ISO N53 | **none** | IT Operations Manager |
| PS-02 | Role-based security competence | partial | 7 | CMMC CSF FEDRAMP ISO N53 | **none** | GRC Manager |
| SA-03 | Product security postmarket obligations | partial | 7 | CSF FEDRAMP ISO N53 | **none** | Product Security Lead |
| AC-02 | Least privilege and role definition | partial | 6 | CMMC FEDRAMP ISO N53 SOC2 | **none** | Security Engineer (IAM) |
| AC-04 | Privileged access brokering and session recording | partial | 6 | CMMC FEDRAMP ISO N53 | EX-2026-0110 | Security Engineer (IAM) |
| AM-04 | Software bill of materials generation and maintenance | partial | 6 | CSF FEDRAMP ISO N53 | **none** | Product Security Lead |
| DP-02 | Encryption at rest | partial | 6 | CMMC CSF FEDRAMP N53 SOC2 | **none** | Platform Engineering Lead |
| IR-04 | Post-incident review and corrective action | partial | 6 | CSF ISO N53 SOC2 | **none** | Incident Response Manager |
| NW-02 | Egress control and data movement monitoring | not-implemented | 6 | CMMC FEDRAMP ISO N53 | RA-2026-004 | Network Engineer |
| SA-01 | Secure development lifecycle gates | partial | 6 | CSF FEDRAMP ISO N53 | **none** | Product Security Lead |
| VM-01 | Vulnerability scanning coverage | partial | 6 | CMMC CSF FEDRAMP ISO N53 | **none** | Security Engineer (Vulnerability) |
| AC-05 | Remote access control | implemented | 5 | CMMC CSF ISO N53 | **none** | Network Engineer |
| AM-01 | Hardware asset inventory | partial | 5 | CSF FEDRAMP ISO N53 | EX-2026-0091 | IT Operations Manager |
| AM-02 | Software inventory and authorized software | partial | 5 | CMMC CSF FEDRAMP ISO N53 | **none** | IT Operations Manager |
| DP-03 | Cryptographic key management | partial | 5 | CMMC FEDRAMP N53 | **none** | Security Engineer (Platform) |
| GV-04 | Compliance obligation register | partial | 5 | CSF FEDRAMP ISO N53 | EX-2026-0142 | Compliance Manager |
| IA-01 | Multi-factor authentication | partial | 5 | CMMC FEDRAMP ISO N53 | EX-2026-0033 | Security Engineer (IAM) |
| SI-03 | Software authenticity and integrity verification | planned | 5 | CSF FEDRAMP N53 | **none** | Platform Engineering Lead |
| AC-01 | Account lifecycle management | implemented | 4 | CMMC CSF N53 | **none** | Security Engineer (IAM) |
| AC-06 | Separation of duties | partial | 4 | CMMC FEDRAMP N53 SOC2 | **none** | GRC Manager |
| IR-03 | Regulatory and contractual breach notification | implemented | 4 | CSF ISO N53 SOC2 | **none** | General Counsel |
| NW-01 | Boundary protection | implemented | 4 | CSF ISO N53 | **none** | Network Engineer |
| PR-02 | Data subject rights fulfilment | implemented | 4 | N53 SOC2 | **none** | Data Protection Officer |
| PR-03 | Data protection impact assessment | partial | 4 | FEDRAMP N53 SOC2 | **none** | Data Protection Officer |
| RM-03 | System categorization and impact levels | partial | 4 | CSF FEDRAMP ISO N53 | **none** | Enterprise Architect |
| SA-04 | Environment separation and non-production data | not-implemented | 4 | FEDRAMP ISO N53 | EX-2026-0156 | Platform Engineering Lead |
| SI-02 | Patch management | partial | 4 | CMMC CSF FEDRAMP N53 | **none** | IT Operations Manager |
| SR-02 | Contractual security requirements and flow-down | implemented | 4 | CSF ISO N53 | **none** | General Counsel |
| VM-02 | Remediation within severity-based service levels | partial | 4 | CMMC CSF FEDRAMP N53 | **none** | Security Engineer (Vulnerability) |
| VM-03 | Penetration testing | implemented | 4 | CMMC ISO N53 SOC2 | **none** | Security Manager |
| AM-03 | Data inventory and classification | planned | 3 | CMMC FEDRAMP ISO | **none** | Data Governance Lead |
| AU-02 | Log retention, protection and integrity | implemented | 3 | CMMC N53 SOC2 | **none** | Security Engineer (Detection) |
| CM-02 | Change management and approval | implemented | 3 | CMMC N53 | **none** | IT Operations Manager |
| CP-01 | Backup and verified restore | implemented | 3 | CSF N53 SOC2 | **none** | IT Operations Manager |
| GV-02 | Security roles, responsibilities and decision authority | implemented | 3 | ISO N53 SOC2 | **none** | CISO |
| GV-03 | Risk acceptance and exception governance | implemented | 3 | CSF ISO SOC2 | **none** | GRC Manager |
| IA-03 | Non-human identity governance | planned | 3 | CMMC FEDRAMP N53 | **none** | Security Engineer (IAM) |
| IR-01 | Incident response plan and severity model | implemented | 3 | ISO N53 SOC2 | **none** | Incident Response Manager |
| PE-01 | Physical access control | implemented | 3 | CMMC ISO N53 | **none** | Facilities Manager |
| RM-01 | Enterprise security risk assessment | implemented | 3 | CSF ISO | **none** | GRC Manager |
| DP-01 | Encryption in transit | implemented | 2 | CMMC N53 | **none** | Network Engineer |
| GV-01 | Information security policy suite | implemented | 2 | CMMC SOC2 | **none** | CISO |
| PS-01 | Personnel screening and access authorization | implemented | 2 | CSF N53 | **none** | HR Business Partner |
| RM-02 | Risk register and treatment tracking | implemented | 2 | CSF SOC2 | **none** | GRC Manager |
| SR-03 | Supplier component provenance | planned | 2 | CSF FEDRAMP | **none** | Product Security Lead |
| AC-03 | Periodic access certification | implemented | 1 | CSF | **none** | GRC Analyst |
| IA-02 | Authenticator management | implemented | 1 | CSF | **none** | Security Engineer (IAM) |

**5 control(s) are unimplemented with no registered exception or acceptance: DP-04, SI-03, AM-03, IA-03, SR-03.** An unimplemented control without a record is not a risk decision, it is an undocumented deviation, and it is the finding an auditor writes up as a governance failure rather than a control failure.

## 4. Highest-leverage remediations

Ranked by the number of in-scope framework obligations closed by bringing one control to fully implemented. This is the ordering a resource-constrained program should work in, adjusted for the risk reduction each control delivers — which this script deliberately does not model, because obligation count and risk reduction are different quantities and collapsing them hides the trade-off.

| Control | Title | Current status | Obligations closed | Frameworks touched | Which | Automation rating |
| --- | --- | --- | --- | --- | --- | --- |
| IR-02 | Incident detection, triage and escalation | partial | 13 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 3 |
| NW-02 | Egress control and data movement monitoring | not-implemented | 12 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 4 |
| AM-03 | Data inventory and classification | planned | 11 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 3 |
| AU-03 | Security monitoring and detection content | not-implemented | 11 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 3 |
| CM-01 | Secure configuration baselines | partial | 11 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 5 |
| SR-01 | Vendor security assessment and tiering | partial | 11 | 5 | CSF FEDRAMP ISO N53 SOC2 | 2 |
| AC-04 | Privileged access brokering and session recording | partial | 10 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 4 |
| AU-01 | Audit log generation standard | partial | 10 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 4 |
| CP-02 | Disaster recovery objectives and testing | partial | 10 | 5 | CSF FEDRAMP ISO N53 SOC2 | 2 |
| DP-04 | Data retention and secure disposal | planned | 10 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 3 |
| IA-03 | Non-human identity governance | planned | 10 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 4 |
| SI-01 | Endpoint protection and detection | partial | 10 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 5 |
| AC-02 | Least privilege and role definition | partial | 9 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 3 |
| AC-06 | Separation of duties | partial | 9 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 3 |
| DP-02 | Encryption at rest | partial | 9 | 6 | CMMC CSF FEDRAMP ISO N53 SOC2 | 5 |

## 5. Evidence burden and reuse

56 evidence-producing controls are in scope. They carry 538 obligation references across 6 frameworks — a reuse ratio of **9.6 obligations satisfied per evidence artifact**. Collecting the same artifact once per framework instead would multiply the collection cost by roughly that factor. See `docs/evidence-reuse-model.md`.

| Control | Title | Frameworks | Obligation refs | Test frequency | Automation |
| --- | --- | --- | --- | --- | --- |
| IR-02 | Incident detection, triage and escalation | 6 | 13 | Quarterly | 3 |
| NW-02 | Egress control and data movement monitoring | 6 | 13 | Quarterly | 4 |
| AC-05 | Remote access control | 6 | 12 | Quarterly | 4 |
| CM-01 | Secure configuration baselines | 6 | 12 | Monthly | 5 |
| IR-01 | Incident response plan and severity model | 6 | 12 | Annual | 1 |
| GV-03 | Risk acceptance and exception governance | 6 | 11 | Quarterly | 3 |
| RM-01 | Enterprise security risk assessment | 6 | 11 | Annual | 2 |
| RM-02 | Risk register and treatment tracking | 6 | 11 | Quarterly | 3 |
| AM-03 | Data inventory and classification | 6 | 11 | Semi-annual | 3 |
| AC-01 | Account lifecycle management | 6 | 11 | Monthly | 4 |
| AC-04 | Privileged access brokering and session recording | 6 | 11 | Quarterly | 4 |
| IA-03 | Non-human identity governance | 6 | 11 | Quarterly | 4 |

Automation feasibility distribution across in-scope controls (5 = evidence generated by machine, 1 = manual by nature):

| Rating | Controls | Share |
| --- | --- | --- |
| 5 | 10 | 18% |
| 4 | 18 | 32% |
| 3 | 14 | 25% |
| 2 | 11 | 20% |
| 1 | 3 | 5% |

14 in-scope controls rate 2 or below, meaning their evidence will be assembled by a human every cycle regardless of tooling investment. Any automation business case that promises to eliminate the compliance calendar has mis-scoped these.

## 6. Testing calendar load

| Test frequency | Controls |
| --- | --- |
| Quarterly | 21 |
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
| partial | 26 | 43% |
| planned | 5 | 8% |
| not-implemented | 3 | 5% |
| not-applicable | 4 | 7% |

---

Mapping strength credit: full 1.0, partial 0.5, supporting 0.0. Implementation credit: implemented 1.0, partial 0.5, planned and not-implemented 0.0. An obligation is **met** only at combined credit 1.0. The reasoning behind these weights is in `docs/mapping-methodology.md` §4.
