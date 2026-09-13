#!/usr/bin/env python3
"""Single source of truth for the control library and the framework crosswalk.

Emits:
  library/control-library.csv      one row per control, with evidence, test procedure,
                                   owner role and automation feasibility
  crosswalk/crosswalk.csv          one row per (control, framework, framework control id)
  crosswalk/crosswalk-matrix.md    human-readable coverage matrix

All content is synthetic and illustrative. Framework identifiers are cited from the public
control catalogues named in README.md; mapping strength is an editorial judgement documented
in docs/mapping-methodology.md.

Run:  python3 library/build_library.py
Stdlib only, no third-party dependencies.
"""

from __future__ import annotations

import csv
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# --------------------------------------------------------------------------------------
# Frameworks. Order is the column order everywhere downstream.
# --------------------------------------------------------------------------------------
FRAMEWORKS = [
    ("N53", "NIST SP 800-53 Rev 5"),
    ("CSF", "NIST CSF 2.0"),
    ("SOC2", "SOC 2 (TSC 2017, rev. 2022)"),
    ("HIPAA", "HIPAA Security Rule (45 CFR 164 subpart C)"),
    ("FEDRAMP", "FedRAMP Moderate baseline"),
    ("CMMC", "CMMC 2.0 Level 2"),
    ("ISO", "ISO/IEC 27001:2022 Annex A"),
    ("IEC62443", "ISA/IEC 62443-3-3 / -2-1"),
    ("CIP", "NERC CIP"),
    ("SOX", "SOX ITGC (PCAOB AS 2201 framing)"),
    ("GDPR", "GDPR (Regulation (EU) 2016/679)"),
]
FW_KEYS = [k for k, _ in FRAMEWORKS]
FW_NAMES = dict(FRAMEWORKS)

# Mapping strength codes
#   F  full        the framework requirement is satisfied by this control alone
#   P  partial     this control satisfies part of the requirement; other controls complete it
#   S  supporting  the control contributes evidence but does not satisfy the requirement
STRENGTHS = {"F": "full", "P": "partial", "S": "supporting"}

# Automation feasibility, 1-5
AUTOMATION = {
    5: "Evidence generated and validated by machine with no human step",
    4: "Evidence extracted by scheduled job; human reviews exceptions only",
    3: "Evidence extractable on demand; human assembles and attests scope",
    2: "Largely manual; automation limited to reminders and workflow state",
    1: "Manual by nature (judgement, negotiation, or physical observation)",
}

# --------------------------------------------------------------------------------------
# Control library.
# Tuple: (id, family, title, statement, owner_role, evidence, test_procedure, freq,
#         automation, automation_rationale, mappings)
# --------------------------------------------------------------------------------------
C = []


def ctl(cid, family, title, statement, owner, evidence, test, freq, auto, auto_why, maps):
    C.append(dict(
        control_id=cid, family=family, title=title, control_statement=statement,
        owner_role=owner, evidence_requirement=evidence, test_procedure=test,
        test_frequency=freq, automation_feasibility=auto,
        automation_rationale=auto_why, mappings=maps,
    ))


# ---- GV Governance -------------------------------------------------------------------
ctl("GV-01", "Governance", "Information security policy suite",
    "A board-approved security policy suite exists, is reviewed at least annually, is version "
    "controlled, and each policy names an accountable owner and the standards that implement it.",
    "CISO",
    "Approved policy documents with version history; approval record naming the approving body and "
    "date; annual review record; policy-to-standard mapping table.",
    "Select the policy suite index. Confirm each policy has an approval record within 12 months, a "
    "named owner still employed in that role, and at least one implementing standard. Confirm the "
    "version in the document repository matches the version published to staff.",
    "Annual", 2,
    "Approval and review are human governance acts; only the review-due tracking automates.",
    {"N53": "PM-1|F; PL-1|F", "CSF": "GV.PO-01|F; GV.PO-02|F", "SOC2": "CC1.1|P; CC5.3|F",
     "HIPAA": "164.316(a)|F", "FEDRAMP": "PL-1|F (M)", "CMMC": "CA.L2-3.12.4|P",
     "ISO": "A.5.1|F", "IEC62443": "62443-2-1 4.2.2|F", "CIP": "CIP-003-8 R1|F",
     "SOX": "ITGC-GOV-01|P", "GDPR": "Art.24(2)|P"}),

ctl("GV-02", "Governance", "Security roles, responsibilities and decision authority",
    "Security roles, decision rights, escalation paths and risk-acceptance authority are defined, "
    "documented and communicated, with segregation between those who operate a control and those "
    "who verify it.",
    "CISO",
    "Charter or equivalent authority document; RACI; delegation-of-authority records; org chart "
    "extract showing the operate/verify split.",
    "Trace three enforcement decisions from the prior year to the authority that made them. Confirm "
    "the decider held the documented authority at the time and that the verifier was not the "
    "operator of the control.",
    "Annual", 1,
    "Authority is an organizational construct; no system holds it as machine-readable state.",
    {"N53": "PM-2|F; PS-7|S", "CSF": "GV.RR-01|F; GV.RR-02|F", "SOC2": "CC1.3|F; CC1.5|P",
     "HIPAA": "164.308(a)(2)|F", "FEDRAMP": "PM-2|F (M)", "CMMC": "-",
     "ISO": "A.5.2|F; A.5.3|P", "IEC62443": "62443-2-1 4.3.2|F", "CIP": "CIP-003-8 R3|F",
     "SOX": "ITGC-GOV-02|F", "GDPR": "Art.24|P; Art.37|S"}),

ctl("GV-03", "Governance", "Risk acceptance and exception governance",
    "Deviations from security standards are registered, time-bounded, compensated, approved at an "
    "authority tier proportional to residual exposure, and void on expiry.",
    "GRC Manager",
    "Exception register extract with tier, accepter, expiry and compensating controls; risk "
    "acceptance records; evidence of void/closure actions for expired items.",
    "Sample 15 open exceptions. Confirm each has a named accepter with documented authority for its "
    "tier, an expiry within policy maximum, a stated exit condition, and evidence that the "
    "compensating controls are operating. Confirm zero items past expiry without a void record.",
    "Quarterly", 3,
    "Register state, aging and expiry are automatable; tiering and compensating-control adequacy "
    "are judgements.",
    {"N53": "CA-5|F; PM-9|P; RA-3|S", "CSF": "GV.RM-05|F; GV.OV-03|P", "SOC2": "CC3.2|P; CC9.1|P",
     "HIPAA": "164.308(a)(1)(ii)(B)|P", "FEDRAMP": "CA-5|F (M)", "CMMC": "CA.L2-3.12.2|F",
     "ISO": "A.5.4|S; 6.1.3(d)|F", "IEC62443": "62443-2-1 4.2.3.7|F", "CIP": "CIP-003-8 R2|P",
     "SOX": "ITGC-GOV-03|P", "GDPR": "Art.32(1)|S"}),

ctl("GV-04", "Governance", "Compliance obligation register",
    "Applicable statutory, regulatory and contractual security obligations are identified, recorded "
    "with their source, assigned to an owner, and mapped to the controls that satisfy them.",
    "Compliance Manager",
    "Obligation register with citation, owner, applicable scope and mapped control IDs; evidence of "
    "review following any regulatory change.",
    "Confirm the register covers every regime in the declared scope profile. Select three "
    "obligations and confirm the mapped controls exist in the library and are implemented in the "
    "scope the obligation applies to.",
    "Semi-annual", 2,
    "Regulatory change monitoring can be fed by subscription services, but applicability is a legal "
    "judgement.",
    {"N53": "PM-1|P; PL-2|S", "CSF": "GV.OC-03|F", "SOC2": "CC2.3|P; CC3.1|P",
     "HIPAA": "164.316(a)|P", "FEDRAMP": "PL-2|S (M)", "CMMC": "-",
     "ISO": "A.5.31|F; A.5.32|P", "IEC62443": "62443-2-1 4.2.2.3|P", "CIP": "-",
     "SOX": "ITGC-GOV-04|P", "GDPR": "Art.30|P; Art.24|P"}),

# ---- RM Risk management --------------------------------------------------------------
ctl("RM-01", "Risk Management", "Enterprise security risk assessment",
    "A documented risk assessment methodology is applied at least annually and on material change, "
    "producing scored risks with named owners and treatment decisions.",
    "GRC Manager",
    "Methodology document; completed assessment with scoring inputs; risk register entries created "
    "or updated; evidence of assessment following a material change.",
    "Confirm the most recent assessment is within 12 months and covers all in-scope systems. Select "
    "five risks and trace the score to its documented inputs. Confirm a material change in the "
    "period triggered a reassessment.",
    "Annual", 2,
    "Scoring and scenario construction are analytic work; only register mechanics automate.",
    {"N53": "RA-3|F; PM-9|P", "CSF": "ID.RA-01|F; ID.RA-04|P; GV.RM-01|P", "SOC2": "CC3.1|F; CC3.2|F",
     "HIPAA": "164.308(a)(1)(ii)(A)|F", "FEDRAMP": "RA-3|F (M)", "CMMC": "RA.L2-3.11.1|F",
     "ISO": "6.1.2|F; A.5.7|S", "IEC62443": "62443-3-2 ZCR 2|F", "CIP": "CIP-002-5.1a R1|P",
     "SOX": "ITGC-RSK-01|P", "GDPR": "Art.32(1)|P; Art.35|S"}),

ctl("RM-02", "Risk Management", "Risk register and treatment tracking",
    "A single enterprise risk register records inherent and residual scoring, treatment decision, "
    "owner, target date and evidence, and is reviewed on a defined cadence by severity.",
    "GRC Manager",
    "Register extract with all mandatory fields populated; review meeting minutes; evidence of "
    "treatment progress for a sample of entries.",
    "Confirm no register entry lacks an owner or a review date within its cadence. Recompute "
    "residual scores for five entries from the recorded control state. Confirm accepted risks carry "
    "a valid acceptance record.",
    "Quarterly", 3,
    "Field completeness, aging and cadence compliance are machine-checkable; scoring is not.",
    {"N53": "PM-9|F; RA-7|F", "CSF": "GV.RM-03|F; ID.RA-05|P; ID.RA-06|F", "SOC2": "CC3.2|P; CC4.2|P",
     "HIPAA": "164.308(a)(1)(ii)(B)|F", "FEDRAMP": "RA-7|F (M)", "CMMC": "RA.L2-3.11.1|P",
     "ISO": "6.1.3|F; A.5.7|S", "IEC62443": "62443-2-1 4.2.3|F", "CIP": "-",
     "SOX": "ITGC-RSK-02|P", "GDPR": "Art.32(2)|S"}),

ctl("RM-03", "Risk Management", "System categorization and impact levels",
    "Each system is categorized by the confidentiality, integrity and availability impact of its "
    "data and function, and the categorization drives the control baseline applied to it.",
    "Enterprise Architect",
    "System inventory with categorization, data types and rationale; baseline assignment per "
    "category; approval by the system owner and the data owner.",
    "Select five systems across categories. Confirm the categorization matches the data actually "
    "processed (sampled from the data inventory) and that the applied baseline matches the "
    "category.",
    "Annual", 3,
    "Categorization can be inherited from the data inventory once that is reliable; the initial "
    "determination is judgement.",
    {"N53": "RA-2|F; CM-8|S", "CSF": "ID.AM-05|F", "SOC2": "CC3.2|S",
     "HIPAA": "164.308(a)(7)(ii)(E)|P", "FEDRAMP": "RA-2|F (M)", "CMMC": "-",
     "ISO": "A.5.12|P", "IEC62443": "62443-3-2 ZCR 3|F (SL-T assignment)",
     "CIP": "CIP-002-5.1a R1|F", "SOX": "ITGC-SCP-01|F", "GDPR": "Art.32(1)(b)|S"}),

# ---- AM Asset management -------------------------------------------------------------
ctl("AM-01", "Asset Management", "Hardware asset inventory",
    "An authoritative inventory of hardware assets is maintained with owner, location, criticality "
    "and network zone, reconciled against at least two independent discovery sources.",
    "IT Operations Manager",
    "Inventory export; reconciliation report showing discovery-source deltas and their disposition; "
    "unowned-asset aging report.",
    "Reconcile the inventory against endpoint-agent and network-discovery sources. Quantify assets "
    "present in one source and absent from the inventory. Confirm deltas older than 30 days have a "
    "disposition.",
    "Monthly", 4,
    "Discovery and reconciliation automate well; ownership assignment and disposition of orphans "
    "require a human.",
    {"N53": "CM-8|F; PM-5|P", "CSF": "ID.AM-01|F", "SOC2": "CC6.1|P",
     "HIPAA": "164.310(d)(1)|P", "FEDRAMP": "CM-8|F (M)", "CMMC": "CM.L2-3.4.1|P",
     "ISO": "A.5.9|F", "IEC62443": "62443-2-1 4.2.3.4|F", "CIP": "CIP-002-5.1a R1|P",
     "SOX": "ITGC-SCP-02|S", "GDPR": "-"}),

ctl("AM-02", "Asset Management", "Software inventory and authorized software",
    "Installed software is inventoried, compared against an authorized-software list, and "
    "unauthorized or end-of-support software is identified with a remediation or acceptance record.",
    "IT Operations Manager",
    "Software inventory export; authorized list with approval dates; end-of-support report with "
    "dispositions; acceptance records for any retained unsupported software.",
    "Sample 20 endpoints and 10 servers. Confirm installed software appears in the inventory within "
    "the collection interval. Confirm every end-of-support item has a dated remediation plan or a "
    "valid acceptance.",
    "Monthly", 4,
    "Collection and end-of-support comparison automate; the authorized list is a governance "
    "artifact.",
    {"N53": "CM-7(5)|F; CM-8|P; SI-2|S", "CSF": "ID.AM-02|F; PR.PS-02|P", "SOC2": "CC6.8|P",
     "HIPAA": "164.308(a)(5)(ii)(B)|P", "FEDRAMP": "CM-7(5)|F (M)", "CMMC": "CM.L2-3.4.8|F",
     "ISO": "A.8.19|F", "IEC62443": "62443-3-3 SR 7.7|P", "CIP": "CIP-010-4 R1.1|P",
     "SOX": "ITGC-CHG-05|S", "GDPR": "-"}),

ctl("AM-03", "Asset Management", "Data inventory and classification",
    "Data stores holding regulated or sensitive data are inventoried with data type, classification, "
    "lawful basis where applicable, retention period, owner and geographic location.",
    "Data Governance Lead",
    "Data inventory with the mandatory fields; discovery-scan results for regulated data types; "
    "sign-off by each data owner.",
    "Run discovery for the regulated data types against a sample of stores not listed in the "
    "inventory. Any positive result is a completeness finding. Confirm classification labels match "
    "the data found.",
    "Semi-annual", 3,
    "Discovery tooling finds candidate stores; classification and lawful-basis determination are "
    "human judgements with legal input.",
    {"N53": "CM-8|P; RA-2|P; PM-5(1)|F", "CSF": "ID.AM-07|F; ID.AM-08|P", "SOC2": "CC6.1|P; C1.1|F",
     "HIPAA": "164.308(a)(1)(ii)(A)|P; 164.310(d)(2)(iii)|S", "FEDRAMP": "PM-5(1)|P",
     "CMMC": "MP.L2-3.8.1|P", "ISO": "A.5.12|F; A.5.13|P", "IEC62443": "-", "CIP": "-",
     "SOX": "ITGC-SCP-03|P", "GDPR": "Art.30|F; Art.5(1)(e)|P"}),

ctl("AM-04", "Asset Management", "Software bill of materials generation and maintenance",
    "A machine-readable SBOM is generated for every product release and material internal "
    "application, in CycloneDX 1.7 or SPDX 3.0.1 format, retained per release and updated on "
    "component change.",
    "Product Security Lead",
    "SBOM artifacts per release with format and timestamp; pipeline configuration showing generation "
    "is a build step; retention index linking SBOM to release identifier.",
    "Select three releases. Confirm an SBOM exists, parses against its schema, and lists components "
    "matching the build manifest. Confirm the SBOM is retained and retrievable for the oldest "
    "supported release.",
    "Per release", 5,
    "Generation, schema validation and retention are entirely mechanical once wired into the build.",
    {"N53": "SA-15|P; SR-4|P; CM-8|S", "CSF": "ID.AM-08|P; GV.SC-04|P", "SOC2": "CC8.1|S",
     "HIPAA": "-", "FEDRAMP": "SR-4|P (M)", "CMMC": "-", "ISO": "A.8.30|S",
     "IEC62443": "62443-4-1 SM-9|F", "CIP": "CIP-013-2 R1.2.5|P", "SOX": "-", "GDPR": "-"}),

# ---- AC Access control ---------------------------------------------------------------
ctl("AC-01", "Access Control", "Account lifecycle management",
    "Accounts are created from an authorized request, modified on role change, and disabled within "
    "defined intervals of separation, with privileged accounts held to a shorter interval.",
    "Security Engineer (IAM)",
    "Joiner/mover/leaver tickets with approvals; HR termination feed reconciled against account "
    "state; deprovisioning latency report by account type.",
    "Reconcile all terminations in the period against account state. Compute the latency "
    "distribution. Any privileged account active beyond the defined interval after separation is an "
    "exception requiring an incident record.",
    "Monthly", 4,
    "Reconciliation is automatable once the HR feed is authoritative; approvals remain human.",
    {"N53": "AC-2|F; AC-2(3)|P; PS-4|P", "CSF": "PR.AA-01|F; PR.AA-05|P", "SOC2": "CC6.2|F; CC6.3|F",
     "HIPAA": "164.308(a)(3)(ii)(C)|F; 164.308(a)(4)(ii)(B)|P", "FEDRAMP": "AC-2|F (M)",
     "CMMC": "AC.L2-3.1.1|P", "ISO": "A.5.16|F; A.5.18|P", "IEC62443": "62443-3-3 SR 1.3|F",
     "CIP": "CIP-004-6 R5|F", "SOX": "ITGC-ACC-01|F", "GDPR": "Art.32(1)(b)|S"}),

ctl("AC-02", "Access Control", "Least privilege and role definition",
    "Access is granted through defined roles carrying the minimum privileges required, with standing "
    "privileged access eliminated in favour of time-bound elevation where technically feasible.",
    "Security Engineer (IAM)",
    "Role definitions with entitlement contents and approver; standing-privilege inventory with "
    "trend; elevation request records.",
    "Enumerate accounts holding tier-0 privileges. Confirm each is either a break-glass account "
    "under the break-glass control or has an approved standing-privilege exception. Sample five "
    "roles and confirm entitlements match the definition.",
    "Quarterly", 3,
    "Enumeration automates; role right-sizing is an analytic exercise with business input.",
    {"N53": "AC-6|F; AC-6(5)|P; AC-6(7)|P", "CSF": "PR.AA-05|F", "SOC2": "CC6.1|F; CC6.3|P",
     "HIPAA": "164.308(a)(4)(ii)(A)|P; 164.312(a)(1)|P", "FEDRAMP": "AC-6|F (M)",
     "CMMC": "AC.L2-3.1.5|F", "ISO": "A.8.2|F", "IEC62443": "62443-3-3 SR 2.1|F",
     "CIP": "CIP-004-6 R4.1|F", "SOX": "ITGC-ACC-02|F", "GDPR": "Art.32(1)(b)|S; Art.5(1)(f)|S"}),

ctl("AC-03", "Access Control", "Periodic access certification",
    "Access to in-scope systems is reviewed by an accountable business reviewer on a defined "
    "cadence, with revocations executed and verified within a defined interval of the decision.",
    "GRC Analyst",
    "Campaign records with reviewer identity, decisions and timestamps; revocation tickets with "
    "completion evidence; reviewer-level approve-all-rate report.",
    "Select two campaigns. Confirm every entitlement in scope received a decision, that revocations "
    "were executed within the interval, and that reviewers with an approve-all rate above the "
    "threshold were re-reviewed. Confirm no reviewer certified their own access.",
    "Quarterly", 4,
    "Campaign mechanics and revocation verification automate; review quality is the residual human "
    "problem and is itself measurable.",
    {"N53": "AC-2(j)|F; AC-6(7)|F", "CSF": "PR.AA-05|P; GV.OV-02|S", "SOC2": "CC6.2|F; CC6.3|F",
     "HIPAA": "164.308(a)(4)(ii)(C)|F; 164.308(a)(3)(ii)(B)|P", "FEDRAMP": "AC-2(j)|F (M)",
     "CMMC": "AC.L2-3.1.1|P", "ISO": "A.5.18|F", "IEC62443": "62443-2-1 4.3.3.5|P",
     "CIP": "CIP-004-6 R4.3|F", "SOX": "ITGC-ACC-03|F", "GDPR": "Art.32(1)(d)|P"}),

ctl("AC-04", "Access Control", "Privileged access brokering and session recording",
    "Privileged sessions to in-scope systems are brokered through a managed path with credential "
    "injection, session recording and automatic credential rotation.",
    "Security Engineer (IAM)",
    "Broker configuration export; session recording index with retention; rotation logs; list of "
    "privileged targets not yet brokered with acceptance records.",
    "Attempt a direct privileged connection bypassing the broker from a representative network "
    "position; the attempt should fail or generate an alert. Confirm recordings exist for a sample "
    "of sessions and that credentials rotated after use.",
    "Quarterly", 4,
    "Configuration state, rotation and recording completeness are machine-verifiable; the bypass "
    "test is a human exercise.",
    {"N53": "AC-2(7)|F; AC-6(9)|F; AU-14|P", "CSF": "PR.AA-05|P; PR.PS-01|S", "SOC2": "CC6.1|P; CC6.6|P",
     "HIPAA": "164.312(a)(2)(i)|P; 164.312(b)|P", "FEDRAMP": "AC-6(9)|F (M)",
     "CMMC": "AC.L2-3.1.7|F", "ISO": "A.8.2|P; A.8.18|F", "IEC62443": "62443-3-3 SR 1.5|F; SR 2.5|P",
     "CIP": "CIP-005-6 R2.1|P; CIP-007-6 R5.1|P", "SOX": "ITGC-ACC-04|F", "GDPR": "Art.32(1)(b)|S"}),

ctl("AC-05", "Access Control", "Remote access control",
    "Remote access to internal and industrial networks requires multi-factor authentication, "
    "terminates at a controlled boundary, and is logged with session attribution.",
    "Network Engineer",
    "Remote access configuration; authentication policy showing factor requirement; session logs "
    "with user attribution; list of remote-access paths reconciled against the network diagram.",
    "Enumerate all inbound remote access paths from external scanning and firewall configuration. "
    "Confirm each terminates at a controlled boundary and enforces multi-factor authentication. Any "
    "undocumented path is a finding.",
    "Quarterly", 4,
    "Path enumeration and policy state automate; reconciliation against intent needs an engineer.",
    {"N53": "AC-17|F; AC-17(2)|P; IA-2(1)|P", "CSF": "PR.AA-03|P; PR.IR-01|P", "SOC2": "CC6.6|F; CC6.7|P",
     "HIPAA": "164.312(e)(1)|P; 164.308(a)(4)|S", "FEDRAMP": "AC-17|F (M)",
     "CMMC": "AC.L2-3.1.12|F; AC.L2-3.1.13|P", "ISO": "A.6.7|P; A.8.20|P",
     "IEC62443": "62443-3-3 SR 1.13|F; SR 2.6|P", "CIP": "CIP-005-6 R2|F", "SOX": "ITGC-ACC-05|P",
     "GDPR": "Art.32(1)(b)|S"}),

ctl("AC-06", "Access Control", "Separation of duties",
    "Incompatible duties are identified and enforced so that no single individual can author, "
    "approve and deploy a change, or grant and use privileged access, without detection.",
    "GRC Manager",
    "Conflict matrix defining incompatible duty pairs; entitlement analysis showing conflicts; "
    "mitigating-control records where a conflict is unavoidable.",
    "Run the conflict matrix against current entitlements. Confirm every detected conflict has a "
    "documented mitigating control with evidence it operates. Test one deployment path to confirm "
    "the author cannot self-approve.",
    "Quarterly", 3,
    "Detection automates once the conflict matrix exists; defining the matrix is business analysis.",
    {"N53": "AC-5|F; CM-5|P", "CSF": "PR.AA-05|P; GV.RR-02|S", "SOC2": "CC5.2|P; CC6.3|P; CC8.1|P",
     "HIPAA": "164.308(a)(3)(ii)(A)|P", "FEDRAMP": "AC-5|F (M)", "CMMC": "AC.L2-3.1.4|F",
     "ISO": "A.5.3|F", "IEC62443": "62443-3-3 SR 2.1 RE 1|P", "CIP": "-",
     "SOX": "ITGC-ACC-06|F", "GDPR": "-"}),

# ---- IA Identification and authentication --------------------------------------------
ctl("IA-01", "Identity", "Multi-factor authentication",
    "Interactive human authentication to in-scope systems requires a second factor, with "
    "phishing-resistant factors required for privileged and externally reachable access, and every "
    "exemption registered with an expiry.",
    "Security Engineer (IAM)",
    "Authentication policy export; enforcement report by population with denominator definition; "
    "exemption register with expiry dates.",
    "Confirm the enforcement denominator includes legacy-protocol and shared-station paths. Attempt "
    "authentication from an unenrolled context and confirm the challenge. Confirm every exemption "
    "has an unexpired registration.",
    "Monthly", 5,
    "Policy state and coverage are fully machine-readable; only the denominator definition requires "
    "human agreement, and it is the part most often wrong.",
    {"N53": "IA-2(1)|F; IA-2(2)|F; IA-2(6)|P", "CSF": "PR.AA-03|F", "SOC2": "CC6.1|F; CC6.6|P",
     "HIPAA": "164.312(d)|F; 164.308(a)(5)(ii)(D)|P", "FEDRAMP": "IA-2(1)|F (M)",
     "CMMC": "IA.L2-3.5.3|F", "ISO": "A.8.5|F", "IEC62443": "62443-3-3 SR 1.1 RE 1|F",
     "CIP": "CIP-005-6 R2.3|F", "SOX": "ITGC-ACC-07|P", "GDPR": "Art.32(1)(b)|S"}),

ctl("IA-02", "Identity", "Authenticator management",
    "Credential issuance, strength, storage, rotation and revocation follow a defined standard, and "
    "shared or non-attributable credentials are prohibited for privileged use.",
    "Security Engineer (IAM)",
    "Credential policy configuration; vault inventory with rotation timestamps; report of accounts "
    "with non-expiring or shared credentials and their dispositions.",
    "Query for accounts with non-expiring credentials, credentials older than the rotation interval, "
    "and accounts flagged as shared. Confirm each has a disposition. Confirm no shared credential "
    "holds privileged entitlements.",
    "Monthly", 5,
    "Directory and vault state expose all of this directly.",
    {"N53": "IA-5|F; IA-5(1)|F", "CSF": "PR.AA-01|P; PR.AA-02|P", "SOC2": "CC6.1|P",
     "HIPAA": "164.308(a)(5)(ii)(D)|F", "FEDRAMP": "IA-5|F (M)", "CMMC": "IA.L2-3.5.7|F",
     "ISO": "A.5.17|F", "IEC62443": "62443-3-3 SR 1.5|F; SR 1.7|P", "CIP": "CIP-007-6 R5.5|F",
     "SOX": "ITGC-ACC-08|P", "GDPR": "Art.32(1)(b)|S"}),

ctl("IA-03", "Identity", "Non-human identity governance",
    "Every service account, workload identity and API credential has a named human owner, a "
    "documented purpose, a scoped entitlement set, and a rotation or attestation record.",
    "Security Engineer (IAM)",
    "Non-human identity inventory with owner, purpose, entitlements and last rotation; ownerless "
    "identity aging report; decommissioning records.",
    "Confirm the inventory reconciles with directory and cloud IAM enumeration. Sample ten "
    "identities and confirm the owner acknowledges ownership and the entitlements match the stated "
    "purpose. Any ownerless identity older than the threshold is a finding.",
    "Quarterly", 4,
    "Enumeration and rotation state automate; ownership attribution is the hard, human part and is "
    "where these programs stall.",
    {"N53": "AC-2|P; IA-9|F; IA-5(1)|P", "CSF": "PR.AA-01|P; ID.AM-01|S", "SOC2": "CC6.2|P; CC6.3|P",
     "HIPAA": "164.308(a)(4)(ii)(B)|S", "FEDRAMP": "IA-9|P (M)", "CMMC": "IA.L2-3.5.1|P",
     "ISO": "A.5.16|P; A.8.2|P", "IEC62443": "62443-3-3 SR 1.2|F", "CIP": "CIP-007-6 R5.2|P",
     "SOX": "ITGC-ACC-09|P", "GDPR": "-"}),

# ---- CM Configuration management -----------------------------------------------------
ctl("CM-01", "Configuration", "Secure configuration baselines",
    "Hardening baselines derived from a recognized benchmark are defined per platform, approved, "
    "applied at build, and measured for conformance in production.",
    "Platform Engineering Lead",
    "Baseline definitions with benchmark provenance and approved deviations; build images "
    "referencing the baseline; conformance scan results by platform.",
    "Scan a sample of production hosts per platform against the baseline. Compute conformance. "
    "Confirm each deviation is either an approved baseline exception or a finding with a "
    "remediation record.",
    "Monthly", 5,
    "Conformance scanning is fully automatable; deviation approval is governance.",
    {"N53": "CM-2|F; CM-6|F; CM-6(1)|P; AU-8|S", "CSF": "PR.PS-01|F; DE.CM-09|P", "SOC2": "CC6.8|P; CC7.1|F",
     "HIPAA": "164.308(a)(5)(ii)(B)|S", "FEDRAMP": "CM-6|F (M)", "CMMC": "CM.L2-3.4.1|F; CM.L2-3.4.2|F",
     "ISO": "A.8.9|F", "IEC62443": "62443-3-3 SR 7.6|F", "CIP": "CIP-010-4 R1.1|F; CIP-010-4 R2|P",
     "SOX": "ITGC-CHG-06|P; ITGC-CHG-02|P", "GDPR": "Art.32(1)(b)|S"}),

ctl("CM-02", "Configuration", "Change management and approval",
    "Changes to production systems follow a documented process with risk assessment, testing, "
    "authorization by someone other than the implementer, and a rollback plan.",
    "IT Operations Manager",
    "Change records with approval identity and timestamp, test evidence, and rollback plan; "
    "emergency-change records with post-hoc approval; unauthorized-change detection report.",
    "Sample 25 production changes including 5 emergency changes. Confirm approval preceded "
    "implementation (or followed within the emergency window), that the approver differs from the "
    "implementer, and that test evidence exists. Reconcile deployed changes against change records "
    "to detect unrecorded changes.",
    "Quarterly", 4,
    "Ticket-to-deployment reconciliation automates; the approval judgement does not.",
    {"N53": "CM-3|F; CM-4|P; CM-5|P", "CSF": "PR.PS-01|P; ID.AM-08|S", "SOC2": "CC8.1|F",
     "HIPAA": "164.308(a)(8)|P", "FEDRAMP": "CM-3|F (M)", "CMMC": "CM.L2-3.4.3|F; CM.L2-3.4.5|P",
     "ISO": "A.8.32|F", "IEC62443": "62443-2-1 4.3.4.3|F", "CIP": "CIP-010-4 R1.2|F",
     "SOX": "ITGC-CHG-01|F", "GDPR": "-"}),

ctl("VM-01", "Vulnerability Management", "Vulnerability scanning coverage",
    "Authenticated vulnerability scanning covers the in-scope estate on a defined cadence, with "
    "coverage measured against the reconciled asset inventory rather than the scanner's own target "
    "list.",
    "Security Engineer (Vulnerability)",
    "Scan schedules and completion records; coverage report using the inventory as denominator; "
    "authentication success rate by platform; list of unscannable assets with compensating controls.",
    "Compare scanned assets against the reconciled inventory. Confirm coverage meets target and that "
    "unscanned assets have a documented reason. Verify authenticated scanning actually authenticated "
    "by sampling scan detail.",
    "Monthly", 5,
    "Fully automatable once the inventory denominator exists; without it the coverage number is "
    "meaningless regardless of automation.",
    {"N53": "RA-5|F; RA-5(5)|P", "CSF": "ID.RA-01|F; DE.CM-08|P", "SOC2": "CC7.1|F",
     "HIPAA": "164.308(a)(1)(ii)(A)|P; 164.308(a)(8)|F", "FEDRAMP": "RA-5|F (M)",
     "CMMC": "RA.L2-3.11.2|F", "ISO": "A.8.8|F", "IEC62443": "62443-2-1 4.3.4.4|P",
     "CIP": "CIP-010-4 R3.1|F", "SOX": "ITGC-OPS-03|S", "GDPR": "Art.32(1)(d)|P"}),

ctl("VM-02", "Vulnerability Management", "Remediation within severity-based service levels",
    "Identified vulnerabilities are remediated within intervals set by severity and exposure, with "
    "overdue items escalated and any deferral recorded as a time-bound exception.",
    "Security Engineer (Vulnerability)",
    "Remediation records with detection and closure timestamps; aging report by severity; escalation "
    "records for overdue items; exceptions for accepted vulnerabilities.",
    "Compute time-to-remediate distributions by severity against the SLA. Confirm overdue items were "
    "escalated per policy. Confirm accepted items have valid, unexpired acceptance records with "
    "compensating controls.",
    "Monthly", 4,
    "Measurement automates; the remediation work and the SLA negotiation do not.",
    {"N53": "RA-5(c)|F; SI-2|P", "CSF": "ID.RA-06|F; RS.MI-03|P", "SOC2": "CC7.1|P; CC7.4|P",
     "HIPAA": "164.308(a)(1)(ii)(B)|P", "FEDRAMP": "RA-5(c)|F (M, with FedRAMP timelines)",
     "CMMC": "RA.L2-3.11.3|F", "ISO": "A.8.8|P", "IEC62443": "62443-2-1 4.3.4.4|P",
     "CIP": "CIP-007-6 R2.3|P", "SOX": "-", "GDPR": "Art.32(1)(d)|P"}),

ctl("VM-03", "Vulnerability Management", "Penetration testing",
    "Independent technical testing is performed at defined intervals against internet-facing "
    "systems, internal networks and products, with findings tracked to closure.",
    "Security Manager",
    "Scope document and rules of engagement; test report with methodology; finding tracker with "
    "closure evidence; retest results for high-severity findings.",
    "Confirm scope covers the systems the framework requires. Trace each high finding to closure "
    "evidence or an acceptance record. Confirm retesting occurred for remediated high findings.",
    "Annual", 1,
    "Testing is expert human work; only the finding tracking automates.",
    {"N53": "CA-8|F; RA-5(11)|P", "CSF": "ID.IM-02|F", "SOC2": "CC4.1|P",
     "HIPAA": "164.308(a)(8)|P", "FEDRAMP": "CA-8|F (M)", "CMMC": "CA.L2-3.12.1|P",
     "ISO": "A.8.8|P; A.5.35|S", "IEC62443": "62443-4-1 SVV-3|F", "CIP": "CIP-010-4 R3.2|P",
     "SOX": "-", "GDPR": "Art.32(1)(d)|F"}),

# ---- SI System and information integrity ---------------------------------------------
ctl("SI-01", "System Integrity", "Endpoint protection and detection",
    "Endpoints and servers run a managed protection agent in prevention mode, with coverage measured "
    "against the reconciled inventory and agent health monitored.",
    "Security Engineer (Endpoint)",
    "Agent coverage report reconciled to inventory; policy export showing prevention mode; agent "
    "health and last-check-in report; list of unprotected assets with compensating controls.",
    "Reconcile agent console inventory against the asset inventory in both directions. Confirm "
    "prevention mode is enforced, not merely available. Execute a benign detection test on a sample "
    "host and confirm the event reaches the console.",
    "Monthly", 5,
    "Coverage, policy state and health are console-readable; the reconciliation denominator is the "
    "only judgement.",
    {"N53": "SI-3|F; SI-4(2)|P", "CSF": "DE.CM-01|P; PR.PS-05|F", "SOC2": "CC6.8|F; CC7.1|P",
     "HIPAA": "164.308(a)(5)(ii)(B)|F", "FEDRAMP": "SI-3|F (M)", "CMMC": "SI.L2-3.14.2|F; SI.L2-3.14.4|P",
     "ISO": "A.8.7|F", "IEC62443": "62443-3-3 SR 3.2|F", "CIP": "CIP-007-6 R3|F",
     "SOX": "-", "GDPR": "Art.32(1)(b)|S"}),

ctl("SI-02", "System Integrity", "Patch management",
    "Security patches are evaluated, tested and deployed within intervals set by severity and "
    "system class, with unpatchable systems compensated and registered.",
    "IT Operations Manager",
    "Patch deployment reports by system class with timestamps; evaluation records for systems on a "
    "mandated evaluation cycle; compensating-control records for unpatchable systems.",
    "Sample systems per class and confirm current patch level against the applicable interval. For "
    "regulated cycles, confirm an evaluation record exists within the mandated period even where no "
    "patch was applied.",
    "Monthly", 4,
    "State and deployment automate; validated and industrial systems require change windows and "
    "human coordination.",
    {"N53": "SI-2|F; CM-3|S", "CSF": "ID.RA-01|P; PR.PS-02|F", "SOC2": "CC7.1|P",
     "HIPAA": "164.308(a)(5)(ii)(B)|P", "FEDRAMP": "SI-2|F (M)", "CMMC": "SI.L2-3.14.1|F",
     "ISO": "A.8.8|P", "IEC62443": "62443-2-3|F", "CIP": "CIP-007-6 R2|F (35-day evaluation cycle)",
     "SOX": "ITGC-CHG-03|P", "GDPR": "Art.32(1)(b)|S"}),

ctl("SI-03", "System Integrity", "Software authenticity and integrity verification",
    "Software and firmware installed on production and product systems is verified for authenticity "
    "and integrity before installation, using vendor signatures or hash verification.",
    "Platform Engineering Lead",
    "Verification records or pipeline configuration showing signature checks; artifact repository "
    "policy; exception records where verification is not technically possible.",
    "Select five recent installations including one firmware update. Confirm verification occurred "
    "and was recorded. Attempt to install an unsigned artifact in a test context and confirm it is "
    "rejected.",
    "Quarterly", 4,
    "Pipeline enforcement is automatable; vendor-supplied industrial firmware often is not, which is "
    "where the exceptions concentrate.",
    {"N53": "SI-7|F; CM-14|F; SR-11|P", "CSF": "PR.DS-06|F; GV.SC-06|P", "SOC2": "CC8.1|P",
     "HIPAA": "164.312(c)(1)|P", "FEDRAMP": "SI-7|F (M)", "CMMC": "SI.L2-3.14.1|P",
     "ISO": "A.8.19|P; A.8.30|S", "IEC62443": "62443-3-3 SR 3.4|F; 62443-4-1 SM-6|P",
     "CIP": "CIP-010-4 R1.6|F", "SOX": "ITGC-CHG-04|P", "GDPR": "-"}),

# ---- AU Audit and logging ------------------------------------------------------------
ctl("AU-01", "Logging", "Audit log generation standard",
    "In-scope systems generate audit records for authentication, privilege use, configuration change "
    "and data access, containing the fields required to attribute an action to an identity.",
    "Security Engineer (Detection)",
    "Logging standard defining required events and fields; per-platform configuration evidence; "
    "log-source inventory with onboarding status against the standard.",
    "Select five platforms. Confirm the required event classes are produced with the required "
    "fields. Perform a test action of each class and confirm a corresponding record appears.",
    "Quarterly", 4,
    "Configuration verification automates; defining what must be logged is engineering judgement.",
    {"N53": "AU-2|F; AU-3|F; AU-12|P", "CSF": "PR.PS-04|F; DE.AE-03|P", "SOC2": "CC7.2|P",
     "HIPAA": "164.312(b)|F; 164.308(a)(1)(ii)(D)|P", "FEDRAMP": "AU-2|F (M)",
     "CMMC": "AU.L2-3.3.1|F; AU.L2-3.3.2|F", "ISO": "A.8.15|F", "IEC62443": "62443-3-3 SR 2.8|F",
     "CIP": "CIP-007-6 R4.1|F", "SOX": "ITGC-OPS-01|P", "GDPR": "Art.32(1)(b)|S; Art.30|S"}),

ctl("AU-02", "Logging", "Log retention, protection and integrity",
    "Audit records are retained for the period required by the most demanding applicable obligation, "
    "protected from modification by the subjects they record, and access to them is itself logged.",
    "Security Engineer (Detection)",
    "Retention configuration per log store; access control on the log platform; integrity mechanism "
    "description; retention-period mapping to each obligation.",
    "Retrieve a record from the earliest retained date and confirm completeness. Confirm "
    "administrators of source systems cannot alter or delete records in the log store. Confirm "
    "log-platform access is logged.",
    "Annual", 4,
    "Retention and access state are readable; obligation mapping requires legal and compliance "
    "input.",
    {"N53": "AU-9|F; AU-11|F; AU-6(7)|P", "CSF": "PR.PS-04|P; PR.DS-01|S", "SOC2": "CC7.2|P; CC6.1|S",
     "HIPAA": "164.312(b)|P; 164.316(b)(2)(i)|F", "FEDRAMP": "AU-11|F (M)",
     "CMMC": "AU.L2-3.3.8|F; AU.L2-3.3.9|P", "ISO": "A.8.15|P", "IEC62443": "62443-3-3 SR 2.9|F; SR 2.11|P",
     "CIP": "CIP-007-6 R4.3|F", "SOX": "ITGC-OPS-02|F", "GDPR": "Art.5(1)(e)|P"}),

ctl("AU-03", "Logging", "Security monitoring and detection content",
    "Security-relevant events are monitored against version-controlled detection content mapped to "
    "adversary techniques, with alert disposition recorded and content effectiveness reviewed.",
    "Security Engineer (Detection)",
    "Detection content repository with commit history; technique coverage mapping; alert disposition "
    "records; tuning change log with rationale.",
    "Select five detections and confirm each has a documented technique mapping, a test result, and "
    "a defined response action. Review disposition records for a sample period and confirm "
    "closed-as-false-positive items produced a tuning action or a documented decision not to tune.",
    "Monthly", 3,
    "Content deployment and alert mechanics automate; authorship, tuning judgement and coverage "
    "assessment do not.",
    {"N53": "SI-4|F; AU-6|F; IR-4(1)|P", "CSF": "DE.CM-01|F; DE.AE-02|F; DE.AE-07|P", "SOC2": "CC7.2|F",
     "HIPAA": "164.308(a)(1)(ii)(D)|F", "FEDRAMP": "SI-4|F (M)", "CMMC": "SI.L2-3.14.6|F; AU.L2-3.3.5|P",
     "ISO": "A.8.16|F", "IEC62443": "62443-3-3 SR 6.2|F", "CIP": "CIP-007-6 R4.2|F",
     "SOX": "-", "GDPR": "Art.32(1)(d)|S"}),

ctl("IR-01", "Incident Response", "Incident response plan and severity model",
    "A documented incident response plan defines severity levels, declaration authority, roles, "
    "communication paths and regulatory triggers, and is exercised at least annually.",
    "Incident Response Manager",
    "Current plan with version and approval; severity definitions with declaration authority; "
    "exercise report with participants, scenario and identified gaps; gap remediation tracker.",
    "Confirm the plan is within its review period and reflects the current organization. Confirm the "
    "annual exercise occurred, included executive participants, and that gaps identified have owners "
    "and dates.",
    "Annual", 1,
    "Plans and exercises are human artifacts; only version and review tracking automate.",
    {"N53": "IR-1|F; IR-8|F; IR-3|P", "CSF": "RS.MA-01|F; ID.IM-02|P", "SOC2": "CC7.3|P; CC7.4|F",
     "HIPAA": "164.308(a)(6)(i)|F", "FEDRAMP": "IR-8|F (M)", "CMMC": "IR.L2-3.6.1|F; IR.L2-3.6.3|F",
     "ISO": "A.5.24|F; A.5.26|P", "IEC62443": "62443-2-1 4.3.4.5|F", "CIP": "CIP-008-6 R1|F",
     "SOX": "-", "GDPR": "Art.33|S"}),

ctl("IR-02", "Incident Response", "Incident detection, triage and escalation",
    "Security events are triaged against defined criteria, escalated within severity-based "
    "intervals, and recorded with a timeline sufficient to reconstruct the response.",
    "Incident Response Manager",
    "Incident records with detection, triage, escalation and containment timestamps; escalation "
    "criteria document; on-call roster covering the stated coverage window.",
    "Select five incidents including one at high severity. Confirm escalation occurred within the "
    "interval, that the timeline is reconstructable from records, and that the declared severity "
    "matches the criteria.",
    "Quarterly", 3,
    "Timestamps and workflow automate; triage judgement is the control.",
    {"N53": "IR-4|F; IR-5|P; IR-6|P", "CSF": "RS.MA-02|F; RS.MA-03|F; DE.AE-06|P", "SOC2": "CC7.3|F; CC7.4|P",
     "HIPAA": "164.308(a)(6)(ii)|F", "FEDRAMP": "IR-4|F (M)", "CMMC": "IR.L2-3.6.1|P; IR.L2-3.6.2|F",
     "ISO": "A.5.25|F; A.5.26|F", "IEC62443": "62443-3-3 SR 6.1|P", "CIP": "CIP-008-6 R1.2|F",
     "SOX": "-", "GDPR": "Art.33(1)|P"}),

ctl("IR-03", "Incident Response", "Regulatory and contractual breach notification",
    "Incidents meeting regulatory or contractual thresholds are assessed for notification obligations "
    "and reported within the applicable clock, with the assessment recorded whether or not "
    "notification was required.",
    "General Counsel",
    "Notification assessment records including the no-notification determinations with reasoning; "
    "submitted notifications with timestamps; obligation matrix showing clocks per regime and "
    "contract.",
    "For every incident in the period at or above the assessment threshold, confirm a documented "
    "notification determination exists. For any notification made, confirm it was within the clock. "
    "Confirm the obligation matrix covers all regimes in the scope profile.",
    "Per incident", 2,
    "Clock tracking can be automated once the determination is made; the determination is legal "
    "judgement and cannot be.",
    {"N53": "IR-6|F; IR-6(1)|P", "CSF": "RS.CO-04|F; RS.CO-03|P", "SOC2": "CC2.3|P; CC7.4|P",
     "HIPAA": "164.404|F; 164.408|F; 164.410|P", "FEDRAMP": "IR-6|F (M, US-CERT timelines)",
     "CMMC": "IR.L2-3.6.2|P", "ISO": "A.5.24|P; A.5.5|P", "IEC62443": "-",
     "CIP": "CIP-008-6 R4|F", "SOX": "-", "GDPR": "Art.33|F; Art.34|F"}),

ctl("IR-04", "Incident Response", "Post-incident review and corrective action",
    "Incidents at or above a defined severity receive a documented review identifying contributing "
    "factors and corrective actions with owners and dates, tracked to closure.",
    "Incident Response Manager",
    "Post-incident review documents; corrective action tracker with closure evidence; evidence that "
    "recurring contributing factors are escalated.",
    "Select three qualifying incidents. Confirm a review occurred within the defined interval, that "
    "corrective actions have owners and dates, and that overdue actions were escalated. Check "
    "whether the same contributing factor appears across multiple reviews.",
    "Quarterly", 2,
    "Action tracking automates; the analysis is the deliverable and it is entirely human.",
    {"N53": "IR-4(m)|F; CA-7|S", "CSF": "RC.RP-06|P; ID.IM-04|F", "SOC2": "CC4.2|P; CC7.5|F",
     "HIPAA": "164.308(a)(6)(ii)|P; 164.308(a)(8)|P", "FEDRAMP": "IR-4|P (M)",
     "CMMC": "IR.L2-3.6.1|P", "ISO": "A.5.27|F", "IEC62443": "62443-2-1 4.3.4.5.11|F",
     "CIP": "CIP-008-6 R3|F", "SOX": "-", "GDPR": "Art.32(1)(d)|S"}),

# ---- CP Contingency --------------------------------------------------------------------
ctl("CP-01", "Resilience", "Backup and verified restore",
    "Backups of in-scope systems and data are taken on a defined schedule, stored with at least one "
    "immutable or offline copy, and validated by actual restore tests rather than job-success "
    "status.",
    "IT Operations Manager",
    "Backup job reports; immutability or offline-copy configuration; restore test records naming the "
    "system, data set, date, duration and outcome.",
    "Select two Tier-1 systems and require a restore to an isolated environment. Measure actual "
    "restore duration against the stated recovery objective. A job-success report alone does not "
    "satisfy this test.",
    "Quarterly", 3,
    "Job state automates; restore validation requires an environment and a person, and is the part "
    "most often skipped.",
    {"N53": "CP-9|F; CP-10|P; CP-9(1)|F", "CSF": "PR.DS-11|F; RC.RP-03|P", "SOC2": "A1.2|F; A1.3|P",
     "HIPAA": "164.308(a)(7)(ii)(A)|F; 164.310(d)(2)(iv)|P", "FEDRAMP": "CP-9|F (M)",
     "CMMC": "MP.L2-3.8.9|F", "ISO": "A.8.13|F", "IEC62443": "62443-3-3 SR 7.3|F; SR 7.4|P",
     "CIP": "CIP-009-6 R1.5|F", "SOX": "ITGC-OPS-05|F", "GDPR": "Art.32(1)(c)|F"}),

ctl("CP-02", "Resilience", "Disaster recovery objectives and testing",
    "Recovery time and recovery point objectives are defined per system tier from a business impact "
    "analysis, and recovery capability is tested against those objectives.",
    "IT Operations Manager",
    "Business impact analysis with tier assignments; documented RTO/RPO per tier; recovery test "
    "reports showing achieved versus target; gap remediation plans.",
    "Confirm every Tier-1 system has a documented RTO/RPO traceable to the impact analysis. Review "
    "the most recent test and compare achieved recovery to target. Confirm gaps have funded plans.",
    "Annual", 2,
    "Test execution and measurement are largely manual exercises involving business stakeholders.",
    {"N53": "CP-2|F; CP-4|F; CP-10|P", "CSF": "RC.RP-01|F; ID.BE-05|P", "SOC2": "A1.2|P; A1.3|F",
     "HIPAA": "164.308(a)(7)(ii)(B)|F; 164.308(a)(7)(ii)(C)|P", "FEDRAMP": "CP-4|F (M)",
     "CMMC": "-", "ISO": "A.5.29|F; A.5.30|P", "IEC62443": "62443-2-1 4.3.2.5|F",
     "CIP": "CIP-009-6 R2|F", "SOX": "ITGC-OPS-06|P", "GDPR": "Art.32(1)(c)|P"}),

# ---- DP Data protection ----------------------------------------------------------------
ctl("DP-01", "Data Protection", "Encryption in transit",
    "Data in transit across untrusted networks, and regulated data across internal networks, is "
    "protected with current cryptographic protocols and validated certificate handling.",
    "Network Engineer",
    "Protocol and cipher configuration per service; external scan results showing negotiated "
    "protocols; certificate inventory with expiry monitoring; exception records for legacy paths.",
    "Scan in-scope endpoints and confirm deprecated protocol versions and weak ciphers are refused. "
    "Confirm certificates are valid, in-date and issued by an approved authority. Confirm legacy "
    "exceptions are registered.",
    "Quarterly", 5,
    "Scanning and certificate inventory are fully automatable.",
    {"N53": "SC-8|F; SC-8(1)|F; SC-13|P", "CSF": "PR.DS-02|F", "SOC2": "CC6.7|F",
     "HIPAA": "164.312(e)(1)|F; 164.312(e)(2)(ii)|F", "FEDRAMP": "SC-8(1)|F (M, FIPS-validated)",
     "CMMC": "SC.L2-3.13.8|F; SC.L2-3.13.11|P", "ISO": "A.8.24|F", "IEC62443": "62443-3-3 SR 4.1|F",
     "CIP": "CIP-005-6 R2.2|P", "SOX": "-", "GDPR": "Art.32(1)(a)|F"}),

ctl("DP-02", "Data Protection", "Encryption at rest",
    "Regulated and sensitive data at rest is encrypted with approved algorithms, with key access "
    "separated from data access.",
    "Platform Engineering Lead",
    "Encryption configuration per data store; algorithm and key-length evidence; key access policy "
    "showing separation from data-plane roles; inventory of unencrypted stores with acceptance.",
    "Enumerate data stores from the data inventory and confirm encryption state for each. Confirm "
    "that a data-plane administrator cannot retrieve keys. Any unencrypted regulated store is a "
    "finding.",
    "Quarterly", 5,
    "Cloud and database platforms expose encryption state directly; the only gap is knowing which "
    "stores exist, which is AM-03's problem.",
    {"N53": "SC-28|F; SC-28(1)|F; SC-13|P", "CSF": "PR.DS-01|F", "SOC2": "CC6.1|P; C1.1|P",
     "HIPAA": "164.312(a)(2)(iv)|F", "FEDRAMP": "SC-28|F (M)", "CMMC": "SC.L2-3.13.16|F",
     "ISO": "A.8.24|P", "IEC62443": "62443-3-3 SR 4.1|P", "CIP": "CIP-011-2 R1.2|P",
     "SOX": "-", "GDPR": "Art.32(1)(a)|F"}),

ctl("DP-03", "Data Protection", "Cryptographic key management",
    "Cryptographic keys are generated, stored, rotated, revoked and destroyed under a documented "
    "policy, with access restricted and all key operations logged.",
    "Security Engineer (Platform)",
    "Key management policy; key inventory with type, purpose, owner, creation and rotation dates; "
    "key-store access logs; rotation and destruction records.",
    "Sample five keys across purposes. Confirm rotation occurred within the policy interval, that "
    "access is restricted to authorized roles, and that key operations appear in the log. Confirm "
    "destroyed keys are recorded as destroyed.",
    "Semi-annual", 4,
    "Managed key services expose lifecycle state; policy definition and exception handling are human.",
    {"N53": "SC-12|F; SC-12(1)|P; SC-17|P", "CSF": "PR.DS-01|P; PR.AA-01|S", "SOC2": "CC6.1|P",
     "HIPAA": "164.312(a)(2)(iv)|P", "FEDRAMP": "SC-12|F (M)", "CMMC": "SC.L2-3.13.10|F",
     "ISO": "A.8.24|F", "IEC62443": "62443-3-3 SR 4.3|F", "CIP": "-",
     "SOX": "-", "GDPR": "Art.32(1)(a)|P"}),

ctl("DP-04", "Data Protection", "Data retention and secure disposal",
    "Data is retained no longer than its defined retention period and is disposed of using methods "
    "that prevent reconstruction, with disposal recorded for regulated data and media.",
    "Data Governance Lead",
    "Retention schedule by data type with legal basis; deletion job records or certificates of "
    "destruction; media sanitization records; legal-hold register showing suspended deletions.",
    "Select three data types and confirm data older than the retention period is absent, or covered "
    "by a documented legal hold. Confirm media disposal in the period produced sanitization records.",
    "Semi-annual", 3,
    "Automated deletion is achievable in modern stores and rarely implemented in legacy ones; "
    "physical media disposal is manual by nature.",
    {"N53": "MP-6|F; SI-12|P; AU-11|S", "CSF": "PR.DS-03|F; ID.AM-08|P", "SOC2": "C1.2|F; P4.3|P",
     "HIPAA": "164.310(d)(2)(i)|F; 164.310(d)(2)(ii)|F", "FEDRAMP": "MP-6|F (M)",
     "CMMC": "MP.L2-3.8.3|F", "ISO": "A.8.10|F; A.7.14|P", "IEC62443": "62443-3-3 SR 4.2|F",
     "CIP": "CIP-011-2 R2|F", "SOX": "-", "GDPR": "Art.5(1)(e)|F; Art.17|P"}),

# ---- PS Personnel ----------------------------------------------------------------------
ctl("PS-01", "Personnel", "Personnel screening and access authorization",
    "Personnel are screened commensurate with the sensitivity of the access they will hold, before "
    "access is granted, and re-screened where the regime requires it.",
    "HR Business Partner",
    "Screening completion records linked to access grant dates; role-to-screening-level matrix; "
    "re-screening records where required; contractor screening attestations.",
    "Sample ten access grants to sensitive systems and confirm screening completed before the grant "
    "date at the required level. Confirm contractor screening attestations exist and are current.",
    "Annual", 2,
    "Completion state can be tracked in HR systems; the screening itself and its adjudication are "
    "human processes with legal constraints that vary by jurisdiction.",
    {"N53": "PS-3|F; PS-2|P", "CSF": "GV.RR-04|P; PR.AA-01|S", "SOC2": "CC1.4|F",
     "HIPAA": "164.308(a)(3)(ii)(B)|F", "FEDRAMP": "PS-3|F (M)", "CMMC": "PS.L2-3.9.1|F",
     "ISO": "A.6.1|F", "IEC62443": "62443-2-1 4.3.3.2|F", "CIP": "CIP-004-6 R3|F",
     "SOX": "-", "GDPR": "Art.32(4)|P"}),

ctl("PS-02", "Personnel", "Role-based security competence",
    "Personnel in roles with security responsibilities receive role-specific training appropriate to "
    "those responsibilities, with completion tracked and competence assessed for specialized roles.",
    "GRC Manager",
    "Role-to-curriculum mapping; completion records by role; assessment results for specialized "
    "roles such as secure development and industrial control engineering.",
    "Confirm every role in the mapping has an assigned curriculum and that completion meets the "
    "threshold. For specialized roles, confirm competence was assessed rather than only attended.",
    "Annual", 4,
    "Completion tracking automates; competence assessment requires role-specific evaluation.",
    {"N53": "AT-3|F; AT-2|P", "CSF": "PR.AT-02|F; PR.AT-01|P", "SOC2": "CC1.4|P",
     "HIPAA": "164.308(a)(5)(i)|P", "FEDRAMP": "AT-3|F (M)", "CMMC": "AT.L2-3.2.2|F",
     "ISO": "A.6.3|F", "IEC62443": "62443-2-1 4.3.2.4|F; 62443-4-1 SM-4|P", "CIP": "CIP-004-6 R2|F",
     "SOX": "-", "GDPR": "Art.39(1)(b)|S"}),

# ---- PE Physical -----------------------------------------------------------------------
ctl("PE-01", "Physical", "Physical access control",
    "Physical access to facilities, data centres, control rooms and network cabinets is restricted, "
    "logged, reviewed, and revoked on separation or role change.",
    "Facilities Manager",
    "Badge system access lists by zone; access logs; periodic review records; revocation records "
    "reconciled against HR separations; visitor logs for restricted zones.",
    "Reconcile badge access for restricted zones against current authorization. Confirm separations "
    "in the period resulted in badge deactivation within the interval. Observe whether tailgating "
    "controls operate at one restricted entrance.",
    "Quarterly", 3,
    "Badge state and reconciliation automate; physical observation of control effectiveness does "
    "not.",
    {"N53": "PE-2|F; PE-3|F; PE-6|P", "CSF": "PR.AA-06|F", "SOC2": "CC6.4|F",
     "HIPAA": "164.310(a)(1)|F; 164.310(a)(2)(ii)|P", "FEDRAMP": "PE-3|F (M)",
     "CMMC": "PE.L2-3.10.1|F; PE.L2-3.10.3|P", "ISO": "A.7.2|F; A.7.3|P",
     "IEC62443": "62443-2-1 4.3.3.3|F", "CIP": "CIP-006-6 R1|F", "SOX": "ITGC-OPS-07|P",
     "GDPR": "Art.32(1)(b)|S"}),

ctl("PE-02", "Physical", "Media handling and removable media control",
    "Removable media use is restricted by policy and technical control, media containing regulated "
    "data is tracked, and media entering industrial environments is scanned before connection.",
    "Security Engineer (Endpoint)",
    "Endpoint policy showing removable media restrictions; exception register; industrial media "
    "scanning station records; media tracking log for regulated data.",
    "Attempt to write to removable media from a standard endpoint and from an industrial workstation "
    "and confirm the policy result. Confirm scanning station records exist for the period. Confirm "
    "exceptions are registered with expiry.",
    "Quarterly", 4,
    "Endpoint policy state automates; the industrial scanning step is a procedural control depending "
    "on operator behaviour.",
    {"N53": "MP-2|F; MP-5|P; MP-7|F", "CSF": "PR.DS-01|S; PR.PS-01|S", "SOC2": "CC6.7|P",
     "HIPAA": "164.310(d)(1)|F", "FEDRAMP": "MP-7|F (M)", "CMMC": "MP.L2-3.8.7|F; MP.L2-3.8.8|P",
     "ISO": "A.7.10|F", "IEC62443": "62443-3-3 SR 2.3|F", "CIP": "CIP-003-8 Att.1 §5|F",
     "SOX": "-", "GDPR": "Art.32(1)(b)|S"}),

# ---- SA Secure development -------------------------------------------------------------
ctl("SA-01", "Secure Development", "Secure development lifecycle gates",
    "Product and application development follows a defined lifecycle with security requirements, "
    "threat modelling, security testing and a release gate that records the disposition of open "
    "findings.",
    "Product Security Lead",
    "Lifecycle procedure; threat models per product with review dates; gate records per release "
    "showing open findings and their disposition; evidence of gate enforcement in the pipeline.",
    "Select two releases. Confirm a threat model exists and was reviewed within the period, that the "
    "gate record lists open findings with dispositions, and that any override carries a named "
    "approver.",
    "Per release", 3,
    "Gate enforcement automates; threat modelling is expert work and is the input the gate depends "
    "on.",
    {"N53": "SA-3|F; SA-8|P; SA-11|P", "CSF": "PR.PS-06|F; GV.SC-05|S", "SOC2": "CC8.1|P",
     "HIPAA": "-", "FEDRAMP": "SA-3|F (M)", "CMMC": "-", "ISO": "A.8.25|F; A.8.27|P",
     "IEC62443": "62443-4-1 SR-2|F; SD-1|F; SVV-1|P", "CIP": "-", "SOX": "ITGC-CHG-07|S",
     "GDPR": "Art.25|P"}),

ctl("SA-02", "Secure Development", "Application and dependency security testing",
    "Application code and third-party dependencies are tested for known vulnerability classes at "
    "defined pipeline stages, with severity-based thresholds that block release.",
    "Product Security Lead",
    "Pipeline configuration showing test stages and thresholds; scan results per build; "
    "suppression register with justification and expiry; dependency inventory with known-vulnerability "
    "status.",
    "Confirm the pipeline enforces the threshold by inspecting a build that exceeded it. Review the "
    "suppression register for expired or unjustified entries. Confirm dependency scanning covers "
    "transitive dependencies.",
    "Per build", 5,
    "Entirely automatable; the human work is threshold setting and suppression review, which is "
    "where the control actually fails.",
    {"N53": "SA-11|F; RA-5|P; SI-2|S", "CSF": "PR.PS-06|P; ID.RA-01|S", "SOC2": "CC7.1|P; CC8.1|P",
     "HIPAA": "-", "FEDRAMP": "SA-11|F (M)", "CMMC": "-", "ISO": "A.8.28|F; A.8.29|F",
     "IEC62443": "62443-4-1 SVV-1|F; SVV-2|F", "CIP": "-", "SOX": "-", "GDPR": "Art.32(1)(d)|S"}),

ctl("SA-03", "Secure Development", "Product security postmarket obligations",
    "Products placed on regulated markets maintain a vulnerability disclosure path, postmarket "
    "monitoring of component vulnerabilities, and a documented process for assessing and "
    "communicating security updates over the supported lifetime.",
    "Product Security Lead",
    "Published disclosure policy and intake records; postmarket monitoring records linking SBOM "
    "components to vulnerability sources; update assessment decisions with clinical or operational "
    "risk input; customer communications.",
    "Confirm the disclosure path is reachable and intake is triaged within the stated interval. "
    "Select one component vulnerability affecting a supported product and trace the assessment "
    "decision and customer communication.",
    "Quarterly", 3,
    "SBOM-to-advisory matching automates; the safety and clinical risk assessment for each update "
    "cannot be, and it is the rate-limiting step.",
    {"N53": "SA-15(6)|P; SI-5|F; SR-8|P", "CSF": "ID.RA-02|F; RS.CO-02|P", "SOC2": "CC2.3|S",
     "HIPAA": "-", "FEDRAMP": "SI-5|P (M)", "CMMC": "-", "ISO": "A.5.6|P; A.8.8|S",
     "IEC62443": "62443-4-1 DM-1|F; DM-4|F; SUM-1|F", "CIP": "-", "SOX": "-", "GDPR": "-"}),

ctl("SA-04", "Secure Development", "Environment separation and non-production data",
    "Development, test and production environments are separated, and production regulated data is "
    "not used in non-production without approved de-identification.",
    "Platform Engineering Lead",
    "Environment architecture showing separation controls; data-provisioning procedure for "
    "non-production; de-identification method documentation; scan results for regulated data in "
    "non-production stores.",
    "Run regulated-data discovery against non-production environments. Any positive result without "
    "an approved de-identification record is a finding and a potential notifiable event. Confirm "
    "developers cannot reach production data stores directly.",
    "Quarterly", 4,
    "Discovery scanning and access-path testing automate; de-identification adequacy is a judgement "
    "requiring privacy input.",
    {"N53": "CM-4(1)|F; SC-7|P; SA-15|S", "CSF": "PR.IR-01|P; PR.DS-01|S", "SOC2": "CC6.1|P; CC8.1|P",
     "HIPAA": "164.514(a)|P; 164.308(a)(4)|S", "FEDRAMP": "CM-4(1)|F (M)", "CMMC": "-",
     "ISO": "A.8.31|F; A.8.33|F", "IEC62443": "62443-4-1 SI-1|P", "CIP": "-",
     "SOX": "ITGC-CHG-08|F", "GDPR": "Art.5(1)(b)|P; Art.32(1)(a)|P"}),

# ---- SR Supply chain -------------------------------------------------------------------
ctl("SR-01", "Supply Chain", "Vendor security assessment and tiering",
    "Third parties are tiered by the access and data they hold, assessed before onboarding at a "
    "depth matching their tier, and reassessed on a tier-based cadence.",
    "Third-Party Risk Analyst",
    "Vendor register with tier, access type, data types and assessment dates; completed assessments "
    "with findings and dispositions; reassessment schedule and compliance against it.",
    "Confirm tiering criteria are applied consistently by sampling ten vendors and re-deriving their "
    "tier. Confirm Tier-1 vendors were assessed before access was granted and reassessed on cadence. "
    "Confirm findings have dispositions.",
    "Annual", 2,
    "Register and cadence tracking automate; assessment itself is analyst work and does not scale "
    "with automation.",
    {"N53": "SR-6|F; SA-9|P; SR-3|P", "CSF": "GV.SC-06|F; GV.SC-07|F; ID.RA-10|P", "SOC2": "CC9.2|F",
     "HIPAA": "164.308(b)(1)|P; 164.314(a)|P", "FEDRAMP": "SA-9|F (M)", "CMMC": "-",
     "ISO": "A.5.19|F; A.5.21|P; A.5.22|F", "IEC62443": "62443-2-4|P", "CIP": "CIP-013-2 R1.1|F",
     "SOX": "ITGC-VEN-01|P", "GDPR": "Art.28(1)|F"}),

ctl("SR-02", "Supply Chain", "Contractual security requirements and flow-down",
    "Contracts with third parties handling enterprise or regulated data include security "
    "requirements, breach notification obligations, audit rights, and flow-down to subprocessors.",
    "General Counsel",
    "Executed agreements with the security schedule; processor agreements and business associate "
    "agreements where applicable; subprocessor registers; evidence of notification-clause review.",
    "Sample five contracts across tiers. Confirm the security schedule is attached and current, that "
    "breach notification intervals meet the enterprise's own regulatory clocks, and that a "
    "subprocessor list exists where required.",
    "Annual", 2,
    "Contract metadata can be tracked; drafting and negotiation are legal work.",
    {"N53": "SR-5|F; SA-4|P; SA-9(1)|P", "CSF": "GV.SC-05|F; GV.SC-09|P", "SOC2": "CC9.2|P",
     "HIPAA": "164.308(b)(3)|F; 164.314(a)(2)|F", "FEDRAMP": "SA-4|F (M)", "CMMC": "-",
     "ISO": "A.5.20|F; A.5.23|P", "IEC62443": "62443-2-4 SP.01|P", "CIP": "CIP-013-2 R1.2|F",
     "SOX": "ITGC-VEN-02|P", "GDPR": "Art.28(3)|F; Art.28(2)|P; Art.44|S"}),

ctl("SR-03", "Supply Chain", "Supplier component provenance",
    "Software and hardware components entering products or production systems are sourced from "
    "identified suppliers, with provenance recorded and component-level vulnerability monitoring in "
    "place.",
    "Product Security Lead",
    "Supplier list per component; ingested supplier SBOMs; provenance records in the artifact "
    "repository; monitoring configuration linking components to vulnerability feeds.",
    "Select three components in a shipped product. Confirm the supplier is identified, that an SBOM "
    "or equivalent component list was ingested, and that the component is under vulnerability "
    "monitoring.",
    "Semi-annual", 4,
    "Ingest and monitoring automate where suppliers provide machine-readable SBOMs; supplier "
    "non-participation is the binding constraint, not tooling.",
    {"N53": "SR-4|F; SR-3|P; SR-11|P", "CSF": "GV.SC-08|P; ID.AM-08|P", "SOC2": "CC9.2|S",
     "HIPAA": "-", "FEDRAMP": "SR-3|P (M)", "CMMC": "-", "ISO": "A.5.21|F",
     "IEC62443": "62443-4-1 SM-9|F; SM-10|P", "CIP": "CIP-013-2 R1.2.5|F", "SOX": "-",
     "GDPR": "-"}),

# ---- PR Privacy ------------------------------------------------------------------------
ctl("PR-01", "Privacy", "Records of processing and lawful basis",
    "Processing activities involving personal data are recorded with purpose, categories of data and "
    "subjects, recipients, transfers, retention and lawful basis, and kept current.",
    "Data Protection Officer",
    "Records of processing with all required elements; review records; transfer mechanism "
    "documentation; linkage from each record to the systems in the asset inventory.",
    "Select three processing activities and confirm the record matches actual system behaviour, "
    "including recipients and transfers. Confirm the record was reviewed within the period and that "
    "a lawful basis is stated for each purpose.",
    "Annual", 2,
    "Records can be partially derived from the data inventory, but purpose and lawful basis are "
    "legal determinations.",
    {"N53": "PM-5(1)|P; PT-2|F; PT-3|F", "CSF": "GV.OC-03|P; ID.AM-07|P", "SOC2": "P1.1|F; P2.1|P",
     "HIPAA": "164.502(b)|S", "FEDRAMP": "PT-3|P (M)", "CMMC": "-", "ISO": "A.5.34|F",
     "IEC62443": "-", "CIP": "-", "SOX": "-", "GDPR": "Art.30|F; Art.6|F; Art.13|P"}),

ctl("PR-02", "Privacy", "Data subject rights fulfilment",
    "Requests from individuals to access, correct, delete, restrict or port their personal data are "
    "received, verified, actioned and answered within the statutory period, with the outcome "
    "recorded.",
    "Data Protection Officer",
    "Request register with receipt, verification, action and response dates; response templates; "
    "evidence of fulfilment in source systems; records of refusals with the exemption relied upon.",
    "Sample five requests including one refusal. Confirm identity verification occurred, the "
    "statutory clock was met, and the action was actually executed in the source systems rather than "
    "only recorded. Confirm refusals cite a valid exemption.",
    "Quarterly", 3,
    "Workflow and clock tracking automate; locating and actioning data across systems is manual "
    "wherever the data inventory is incomplete.",
    {"N53": "PT-6|P; PM-22|P", "CSF": "GV.OC-03|S", "SOC2": "P5.1|F; P5.2|P; P6.1|S",
     "HIPAA": "164.524|F; 164.526|F", "FEDRAMP": "-", "CMMC": "-", "ISO": "A.5.34|P",
     "IEC62443": "-", "CIP": "-", "SOX": "-",
     "GDPR": "Art.12|F; Art.15|F; Art.16|F; Art.17|F; Art.20|P"}),

ctl("PR-03", "Privacy", "Data protection impact assessment",
    "Processing likely to result in high risk to individuals is assessed before it begins, with "
    "mitigations identified, residual risk recorded, and consultation escalated where required.",
    "Data Protection Officer",
    "Screening records showing which activities required an assessment and which did not; completed "
    "assessments with mitigations and residual risk; sign-off; consultation records where "
    "applicable.",
    "Identify new or materially changed processing in the period. Confirm screening occurred for "
    "each and that assessments exist where the threshold was met. Confirm identified mitigations "
    "were implemented rather than only proposed.",
    "Per project", 2,
    "Screening can be embedded in intake workflow; the assessment is legal and analytic work.",
    {"N53": "RA-8|F; PT-4|S", "CSF": "ID.RA-01|S; GV.RM-01|S", "SOC2": "P3.1|P",
     "HIPAA": "164.308(a)(1)(ii)(A)|S", "FEDRAMP": "RA-8|F (M)", "CMMC": "-",
     "ISO": "A.5.34|P", "IEC62443": "-", "CIP": "-", "SOX": "-", "GDPR": "Art.35|F; Art.36|P"}),

# ---- OT Operational technology ---------------------------------------------------------
ctl("OT-01", "Operational Technology", "Zone and conduit segmentation",
    "Industrial networks are divided into zones with defined security levels, and traffic between "
    "zones traverses conduits with explicitly enumerated, owned and reviewed allow rules.",
    "OT Security Engineer",
    "Zone and conduit model with assigned target security levels; firewall rule base with owner and "
    "justification per rule; rule review records; flow analysis showing actual traffic against "
    "permitted flows.",
    "Compare the rule base against the zone model. Any any/any rule or rule without an owner is a "
    "finding. Sample permitted flows and confirm they are still required by the operating process.",
    "Semi-annual", 3,
    "Rule analysis automates; the zone model and the judgement that a flow is still required are "
    "engineering work with plant operations.",
    {"N53": "SC-7|F; SC-7(5)|P; AC-4|P", "CSF": "PR.IR-01|F; ID.AM-03|P", "SOC2": "CC6.6|P",
     "HIPAA": "164.312(e)(1)|S", "FEDRAMP": "SC-7|F (M)", "CMMC": "SC.L2-3.13.1|F; SC.L2-3.13.5|P",
     "ISO": "A.8.20|F; A.8.22|F", "IEC62443": "62443-3-2 ZCR 4|F; 62443-3-3 SR 5.1|F; SR 5.2|F",
     "CIP": "CIP-005-6 R1|F", "SOX": "-", "GDPR": "-"}),

ctl("OT-02", "Operational Technology", "Industrial remote and vendor access",
    "Remote access to industrial systems, including vendor access, is brokered through a controlled "
    "path, enabled only for the duration of an approved activity, and recorded.",
    "OT Security Engineer",
    "Access request and approval records with time windows; jump host configuration; session "
    "recordings; vendor access register with contractual basis.",
    "Confirm no persistent vendor access path exists by enumerating inbound paths to the industrial "
    "zone. For three vendor activities, confirm an approval preceded access, the window matched, and "
    "a recording exists.",
    "Quarterly", 4,
    "Path enumeration and session state automate; the approval and the operational coordination do "
    "not.",
    {"N53": "AC-17|P; MA-4|F; AC-2(11)|P", "CSF": "PR.AA-05|P; GV.SC-07|S", "SOC2": "CC6.6|P; CC9.2|S",
     "HIPAA": "-", "FEDRAMP": "MA-4|F (M)", "CMMC": "MA.L2-3.7.5|F", "ISO": "A.8.21|P; A.5.22|S",
     "IEC62443": "62443-3-3 SR 1.13|F; SR 2.6|F", "CIP": "CIP-005-6 R2.4|F; R2.5|F",
     "SOX": "-", "GDPR": "-"}),

ctl("OT-03", "Operational Technology", "Unsupported industrial system compensations",
    "Industrial systems that cannot be patched or cannot run standard protective agents are "
    "inventoried, isolated to an enumerated flow set, monitored, and covered by a time-bound, "
    "compensated acceptance.",
    "OT Security Engineer",
    "Inventory of unsupported systems with OS version and constraint reason; firewall policy "
    "restricting each system; monitoring configuration; current acceptance records with compensating "
    "controls and expiry.",
    "Confirm the inventory reconciles with the OT asset inventory. For each system, confirm the "
    "restricted flow set is enforced and that an unexpired acceptance exists. Confirm systems under "
    "a prescriptive regulatory patch regime are handled under that regime and not under enterprise "
    "acceptance.",
    "Quarterly", 3,
    "Inventory and policy state automate; the acceptance lifecycle and the regulatory carve-out are "
    "governance work.",
    {"N53": "SI-2|P; CA-5|P; SC-7(5)|P", "CSF": "ID.AM-01|P; GV.RM-05|P; PR.IR-01|P", "SOC2": "CC7.1|P",
     "HIPAA": "-", "FEDRAMP": "CA-5|P (M)", "CMMC": "-", "ISO": "A.8.8|P; A.5.4|S",
     "IEC62443": "62443-2-3|F; 62443-3-3 SR 7.6|P", "CIP": "CIP-007-6 R2.3|F (mitigation plan)",
     "SOX": "-", "GDPR": "-"}),

# ---- NW Network ------------------------------------------------------------------------
ctl("NW-01", "Network", "Boundary protection",
    "Enterprise network boundaries are defined, traffic crossing them is controlled by default-deny "
    "policy, and the externally reachable surface is enumerated and reconciled against intent.",
    "Network Engineer",
    "Boundary device configuration with default-deny evidence; external attack surface enumeration; "
    "reconciliation of discovered services against an approved exposure register.",
    "Run external enumeration against the published address space. Compare discovered services to "
    "the approved exposure register. Any unregistered externally reachable service is a finding "
    "regardless of its vulnerability status.",
    "Monthly", 5,
    "External enumeration and configuration comparison are fully automatable and cheap; the approved "
    "exposure register is the human-maintained half.",
    {"N53": "SC-7|F; SC-7(4)|P; CM-7|P", "CSF": "PR.IR-01|F; DE.CM-01|P", "SOC2": "CC6.6|F",
     "HIPAA": "164.312(e)(1)|P", "FEDRAMP": "SC-7|F (M)", "CMMC": "SC.L2-3.13.1|F; SC.L2-3.13.6|F",
     "ISO": "A.8.20|F; A.8.22|P", "IEC62443": "62443-3-3 SR 5.1|P", "CIP": "CIP-005-6 R1.3|F",
     "SOX": "-", "GDPR": "Art.32(1)(b)|S"}),

ctl("NW-02", "Network", "Egress control and data movement monitoring",
    "Outbound traffic from environments holding regulated data is restricted to approved "
    "destinations and protocols, and bulk or anomalous data movement is detected.",
    "Network Engineer",
    "Egress policy configuration; approved destination register; detection rules for anomalous "
    "volume or destination; alert disposition records.",
    "Attempt an outbound connection to an unapproved destination from a regulated environment and "
    "confirm the result. Review detections for bulk movement in the period and confirm each was "
    "dispositioned.",
    "Quarterly", 4,
    "Policy enforcement and volumetric detection automate; defining 'approved destination' for a "
    "real business is the slow part.",
    {"N53": "SC-7(5)|F; AC-4|F; SI-4(4)|P", "CSF": "PR.DS-02|P; DE.CM-01|P; DE.AE-02|S", "SOC2": "CC6.7|P; CC7.2|P",
     "HIPAA": "164.312(e)(1)|P", "FEDRAMP": "SC-7(5)|F (M)", "CMMC": "SC.L2-3.13.1|P; AC.L2-3.1.3|F",
     "ISO": "A.8.12|F; A.8.20|P", "IEC62443": "62443-3-3 SR 5.2|P", "CIP": "CIP-005-6 R1.3|P",
     "SOX": "-", "GDPR": "Art.32(1)(b)|P; Art.44|S"}),


# --------------------------------------------------------------------------------------
# Emit
# --------------------------------------------------------------------------------------
LIB_FIELDS = [
    "control_id", "family", "title", "control_statement", "owner_role",
    "evidence_requirement", "test_procedure", "test_frequency",
    "automation_feasibility", "automation_label", "automation_rationale",
    "mapped_frameworks", "mapping_count",
]


def parse_maps(raw):
    """'AC-2|F; PS-4|P' -> [('AC-2','F'), ('PS-4','P')]; '-' -> []"""
    out = []
    if not raw or raw.strip() == "-":
        return out
    for part in raw.split(";"):
        part = part.strip()
        if not part or part == "-":
            continue
        if "|" in part:
            fid, strength = part.rsplit("|", 1)
            strength = strength.strip()
            # strengths may carry a parenthetical note: 'F (M)'
            code = strength.split()[0] if strength else "P"
            note = strength[len(code):].strip() if len(strength) > len(code) else ""
        else:
            fid, code, note = part, "P", ""
        if code not in STRENGTHS:
            code, note = "P", strength
        out.append((fid.strip(), code, note.strip("() ")))
    return out


def main():
    os.makedirs(os.path.join(ROOT, "crosswalk"), exist_ok=True)

    lib_path = os.path.join(HERE, "control-library.csv")
    xw_path = os.path.join(ROOT, "crosswalk", "crosswalk.csv")
    matrix_path = os.path.join(ROOT, "crosswalk", "crosswalk-matrix.md")

    xw_rows = []
    with open(lib_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=LIB_FIELDS)
        w.writeheader()
        for c in C:
            mapped = []
            count = 0
            for fk in FW_KEYS:
                entries = parse_maps(c["mappings"].get(fk, "-"))
                if entries:
                    mapped.append(fk)
                for fid, code, note in entries:
                    count += 1
                    xw_rows.append({
                        "control_id": c["control_id"],
                        "control_title": c["title"],
                        "framework_key": fk,
                        "framework_name": FW_NAMES[fk],
                        "framework_control_id": fid,
                        "mapping_strength": STRENGTHS[code],
                        "mapping_note": note,
                    })
            row = {k: c[k] for k in LIB_FIELDS if k in c}
            row["automation_label"] = AUTOMATION[c["automation_feasibility"]]
            row["mapped_frameworks"] = " ".join(mapped)
            row["mapping_count"] = count
            w.writerow(row)

    with open(xw_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "control_id", "control_title", "framework_key", "framework_name",
            "framework_control_id", "mapping_strength", "mapping_note"])
        w.writeheader()
        w.writerows(xw_rows)

    # coverage matrix
    by_ctl = defaultdict(lambda: defaultdict(list))
    for r in xw_rows:
        by_ctl[r["control_id"]][r["framework_key"]].append(
            (r["framework_control_id"], r["mapping_strength"][0].upper()))

    lines = ["# Crosswalk coverage matrix", "",
             "Generated by `library/build_library.py`. Do not edit by hand.", "",
             "Cell notation: framework control identifiers, each suffixed with mapping strength ",
             "(**F** full, **P** partial, **S** supporting). An empty cell means the control has no ",
             "mapping in that framework, which is itself a documented finding rather than an omission ",
             "— see `docs/mapping-methodology.md` §5.", "",
             "| Control | " + " | ".join(FW_KEYS) + " |",
             "| --- | " + " | ".join("---" for _ in FW_KEYS) + " |"]
    for c in C:
        cells = []
        for fk in FW_KEYS:
            ent = by_ctl[c["control_id"]].get(fk, [])
            cells.append("<br>".join(f"{i} {s}" for i, s in ent) if ent else "—")
        lines.append(f"| **{c['control_id']}** {c['title']} | " + " | ".join(cells) + " |")
    lines += ["", "## Framework key", "",
              "| Key | Framework and version |", "| --- | --- |"]
    for k, n in FRAMEWORKS:
        lines.append(f"| {k} | {n} |")
    with open(matrix_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    fam = Counter(c["family"] for c in C)
    auto = Counter(c["automation_feasibility"] for c in C)
    fwc = Counter(r["framework_key"] for r in xw_rows)
    strc = Counter(r["mapping_strength"] for r in xw_rows)
    print(f"controls={len(C)} families={len(fam)} mappings={len(xw_rows)}")
    print("by family:", dict(sorted(fam.items())))
    print("automation feasibility distribution:", dict(sorted(auto.items())))
    print("mappings per framework:", {k: fwc[k] for k in FW_KEYS})
    print("mapping strength:", dict(strc))
    print("avg frameworks per control: %.1f" %
          (sum(len(by_ctl[c["control_id"]]) for c in C) / len(C)))
    print("wrote:", lib_path, xw_path, matrix_path, sep="\n  ")


if __name__ == "__main__":
    main()
