# Decision Records

Eight decisions behind this crosswalk. Each is a trade-off between fidelity and the cost of
maintaining fidelity at fixed headcount — which is the only real constraint in multi-framework
compliance.

Format per record: **Decision · Context and constraint · Options considered · Choice and rationale ·
Trade-off accepted · What was deliberately not done · How the decision would be revisited.**

---

## ADR-001 — Map through a single internal control library, not framework to framework

**Decision.** Maintain one enterprise control library and map each control outward to every
in-scope framework, rather than maintaining pairwise crosswalks between frameworks.

**Context and constraint.** Eleven frameworks in scope. One compliance analyst plus a fraction of a
GRC manager maintain the mapping. Framework revisions arrive unpredictably; ISO 27001 restructured
its Annex A in 2022, CSF added a Govern function in 2.0, and NERC CIP standards version
independently of anything else.

**Options considered.**

| Option | Maintenance cost | Why rejected or chosen |
| --- | --- | --- |
| A. Pairwise framework crosswalks | 55 mappings for 11 frameworks, each drifting separately | Quadratic growth; and no mapping terminates in anything the enterprise actually operates |
| B. Single internal library, mapped outward (chosen) | 11 one-way mappings from a stable centre | Every mapping terminates in a control with an owner, evidence and a test |
| C. Adopt one framework as the master, map others to it | 10 mappings, but the master's structure constrains everything | Fails where frameworks differ in kind: a prescriptive standard cannot be expressed as a view of a risk-based one |
| D. Vendor-supplied mappings from a GRC platform | Near zero to maintain | Unowned quality. A mapping nobody in-house can defend collapses at the first auditor challenge, and the defence is the artifact's whole value |

**Choice and rationale.** The library is the stable object. Frameworks change around it, and a
revision costs one re-mapping pass rather than ten. More importantly, mapping outward from
implementation forces every claim to be anchored to something that produces evidence — which is
what an auditor tests, and what a framework-to-framework mapping never touches.

**Trade-off accepted.** The library does not contain every requirement in every framework, so a
requirement can be missed entirely if no control happens to map to it. This is a real and
acknowledged gap in the model; the mitigation is the maintenance rule that a new framework is
mapped from existing controls first, with new controls added only where a genuine capability gap is
found, and the exclusion reasons recorded in the scope profile.

**What was deliberately not done.** No attempt to reproduce framework catalogues in full. No
importing of a public crosswalk without re-deriving the mappings, because an inherited mapping
carries an unknown error rate.

**How it would be revisited.** If the enterprise ever operates under a single dominant framework —
a successful FedRAMP authorization driving most revenue, for instance — option C becomes viable,
with an explicit reconciliation policy for the prescriptive conflicts that would then dominate.

---

## ADR-002 — Three mapping strengths, with supporting mappings scored at zero

**Decision.** Every mapping carries a strength of full, partial or supporting. Supporting mappings
contribute zero credit toward satisfying an obligation.

**Context and constraint.** An unqualified crosswalk asserts that a control satisfies a
requirement. In practice, most control-to-requirement relationships are partial, and a meaningful
minority are merely supportive. A crosswalk that does not distinguish these produces coverage
numbers that fail on first test.

**Options considered.** (1) Binary mapped/not-mapped — simplest, and it systematically overstates
coverage; every partial relationship reads as full. (2) Three strengths with graded credit
(chosen). (3) A percentage per mapping — finer-grained and unmaintainable, because nobody can
defend the difference between 60% and 70% coverage of a requirement in an audit conversation.
(4) Strength plus a written justification per mapping — best quality, and roughly 880 short essays
to author and maintain, which exceeds the analyst capacity that exists.

**Choice and rationale.** Three levels is the most granularity that can be applied consistently by
one analyst and defended in a conversation. Scoring supporting mappings at zero is the load-bearing
decision: it means the report cannot manufacture coverage out of tangential relationships, which is
the specific way crosswalks mislead their owners. The behaviour is pinned by a unit test so it
cannot be quietly relaxed under reporting pressure.

**Trade-off accepted.** Coverage numbers are lower — and for the core profile, considerably lower —
than a naive crosswalk would produce against identical facts. Anyone comparing this output to a
vendor's compliance dashboard will conclude the program is behind. That conversation is worth
having once; the alternative is having it after an audit.

**What was deliberately not done.** No weighting by requirement importance. All obligations count
equally in the score, which is wrong in principle — but importance weighting would need to be
defended per requirement, and a defensible weighting scheme would be a larger artifact than the
crosswalk.

**How it would be revisited.** If the annual independent re-derivation (methodology §8) shows
analysts disagreeing on full-versus-partial at a material rate, the definitions need sharpening
before the scale is extended.

---

## ADR-003 — Score obligations by maximum contributing control, not by sum

**Decision.** An obligation's credit is the maximum credit from any single mapped control, not the
sum across contributing controls.

**Context and constraint.** Several controls can contribute to one requirement. Summing lets two
half-built controls report a satisfied obligation.

**Options considered.** (1) Sum with a cap at 1.0 — represents genuine complementary coverage, and
allows 0.5 + 0.5 from two partially implemented controls to report as met, which no auditor would
accept. (2) Maximum (chosen). (3) Sum only where mappings are explicitly declared complementary —
most accurate, requires an additional relationship type per obligation and roughly doubles the data
model.

**Choice and rationale. In an audit artifact, the direction of error matters more than its
magnitude.** Maximum under-reports; sum over-reports. Under-reporting produces unnecessary work;
over-reporting produces a finding and a credibility loss that attaches to every other number the
program publishes.

**Trade-off accepted.** Genuine complementary coverage — two partial controls that together fully
satisfy a requirement — is scored as partial and has to be resolved by a human reviewing the report.
The gap report's section 3 makes these visible by listing the contributing control for every partial
obligation, so the resolution is a reading exercise rather than a search.

**What was deliberately not done.** No manual override field to force an obligation to met. An
override field is used within a quarter of being introduced, and thereafter the score reflects the
overrides rather than the controls.

**How it would be revisited.** Add option 3's declared-complementary relationship if the count of
partial obligations resolved manually each cycle exceeds roughly 30 — below that, the data-model
cost is not repaid.

---

## ADR-004 — Standard library only, no third-party dependencies

**Decision.** `gap_report.py` and `build_library.py` use only the Python standard library. CSV and
JSON rather than YAML or a database.

**Context and constraint.** These scripts need to run inside change-controlled environments where
installing a package is itself a change request, and on an auditor's laptop during fieldwork
without a procurement conversation.

**Options considered.** (1) pandas plus PyYAML — more expressive, and it makes the script
un-runnable exactly where it is most useful. (2) Standard library with CSV and JSON (chosen).
(3) A small web application with a database — better for a large control set, and it turns a
150-line script into a system with an owner, a backup requirement and a patching obligation.

**Choice and rationale.** The artifact's value is that anyone can run it and read its output
without infrastructure. CSV is also diffable in Git, which means the control library's change
history is reviewable line by line in a pull request — that property is worth more than YAML's
readability for nested data, because the data here is flat.

**Trade-off accepted.** CSV handles the flat library well and the crosswalk awkwardly; the
mappings are authored as compact strings in `build_library.py` and expanded into rows, which is one
more transformation than a nested format would need. Multi-line control statements in CSV are also
harder to review in a plain diff than YAML would be.

**What was deliberately not done.** No database. No web interface. No API. Each would improve
usability and would make the repository a system to be maintained rather than a document to be read.

**How it would be revisited.** Above roughly 300 controls or 5,000 mappings, CSV authoring becomes
error-prone and a structured store with validation is worth the operational cost.

---

## ADR-005 — Treat prescriptive and risk-based frameworks differently, but keep the difference out of the score

**Decision.** Document the prescriptive-versus-risk-based distinction in the methodology and the
scope profile notes, and deliberately keep it out of the numeric scoring.

**Context and constraint.** A NERC CIP gap and an ISO 27001 gap are not the same kind of object:
one is a potential violation of a mandatory standard, the other may be a conforming risk decision.
Both appear as a gap in the report.

**Options considered.** (1) Ignore the distinction — the default, and it leads directly to the most
damaging error in multi-framework compliance, using an enterprise risk acceptance to close a
prescriptive gap. (2) Weight prescriptive gaps more heavily in the score — makes the number
directionally better and still blends two incommensurable things into one figure. (3) Document the
distinction and keep the score neutral, forcing a human to read the framework column (chosen).
(4) Produce two separate reports — cleanest conceptually, and it hides the overlap that is the whole
point of a crosswalk.

**Choice and rationale.** A single number that blends "we accepted this risk" with "we are in
violation" is worse than no number, because it is actionable in the wrong direction. The report's
job here is to route the gap to the right decision process, not to price it. `conflict-reconciliation.md`
§6 states the rule in a table: for prescriptive requirements, a documented risk acceptance is never
a valid response.

**Trade-off accepted.** Someone reading only section 1 of a report cannot tell how much of the gap
is regulatory exposure. That reader is going to be wrong about this artifact in several ways, and
the response is the scope profile note that appears immediately under the title, not a more clever
score.

**What was deliberately not done.** No compliance-risk-score composite. No traffic-light rollup per
framework.

**How it would be revisited.** If the industrial division's CIP scope grows to dominate the
enterprise's regulatory exposure, a separate prescriptive-obligation report with its own
mitigation-plan tracking becomes the right artifact — that is option 4, and it becomes correct at
the point where CIP obligations stop being a subset and start being the main event.

---

## ADR-006 — Rate automation feasibility per control, and publish the ratings

**Decision.** Every control carries a 1–5 automation feasibility rating with a written rationale,
and the gap report summarizes the distribution.

**Context and constraint.** Compliance automation business cases are routinely built on the
assumption that most evidence can be machine-generated. In this library, 14 of 60 controls rate 2
or below: their evidence will be assembled by a human every cycle at any level of tooling spend.

**Options considered.** (1) No rating — leaves the automation conversation to vendor claims.
(2) Binary automatable/not — loses the distinction between "extractable on demand with human scope
attestation" and "fully machine-generated", which is exactly the distinction that determines
whether an automation project pays back. (3) Five-point scale with rationale (chosen). (4) Estimated
hours saved per control — most decision-useful, and it requires baseline time data the program does
not have and would have to fabricate.

**Choice and rationale.** Publishing the rating alongside reuse count gives a defensible investment
order: high reuse plus high feasibility first, high reuse plus low feasibility staffed rather than
tooled. It also arms the compliance manager for the conversation where a platform is proposed as a
substitute for headcount — with 14 controls at rating 2 or below, it is not, and the rating makes
that a data point rather than an opinion.

**Trade-off accepted.** The ratings are judgements and will be wrong in specific cases, particularly
where a platform the enterprise does not own would change the answer. They are stated as ratings
with rationale rather than as measurements, and the rationale is the part to argue with.

**What was deliberately not done.** No tool-specific ratings. The moment a rating says "automatable
with product X", the library becomes a procurement document and dates within a year.

**How it would be revisited.** Re-rate annually and after any platform change that materially alters
evidence collection.

---

## ADR-007 — Ship synthetic implementation status with the library

**Decision.** Include `examples/implementation-status.csv` covering all 60 controls with a realistic
mixed state — 22 implemented, 29 partial, 5 planned, 4 not implemented — rather than shipping an
empty template.

**Context and constraint.** A gap report against an empty or all-implemented status file
demonstrates nothing. The interesting behaviour of the tool is entirely in how it handles partial
implementation, partial mappings and registered exceptions.

**Options considered.** (1) Empty template — honest about being a template, and the tooling cannot
be evaluated without the reader authoring 60 rows first. (2) All-implemented — produces a clean
report that exercises none of the logic. (3) Realistic mixed synthetic state (chosen), carrying the
same acceptance and exception identifiers used in the sibling `security-program-blueprint`.

**Choice and rationale.** The synthetic state makes the two most valuable report behaviours visible
immediately: controls that are implemented but only partially mapped (so the obligation is still
open), and controls that are unimplemented with no registered exception — which the report calls out
by name as a governance failure rather than a control failure. Neither is visible against a clean
status file.

**Trade-off accepted.** Every generated report carries numbers that could be mistaken for a real
assessment. Mitigated by a synthetic-data statement in the README, in each report header, and in
each scope profile — three places, because one is routinely missed when a file is shared on its own.

**What was deliberately not done.** No attempt to make the synthetic state flattering. The core
profile shows 29% of obligations met, which is what an honest mid-transformation program looks like
and what a portfolio artifact should show.

**How it would be revisited.** Not applicable; this is a property of the demonstration rather than a
design decision that would change with circumstances.

---

## ADR-008 — Fail the build on data-integrity defects, not on gap count

**Decision.** The test suite fails on structural defects — a control with no evidence requirement, a
crosswalk row referencing an unknown control, a status file that does not cover the library. Gap
count is exposed through an opt-in `--fail-on-gap` flag and is never a test failure.

**Context and constraint.** These scripts are the sort of thing that ends up in a pipeline. What
belongs in a pipeline gate is a different question from what belongs in a compliance report.

**Options considered.** (1) Fail on any gap — turns the crosswalk into a blocker for unrelated work
and creates immediate pressure to close gaps by editing the status file. (2) Fail on integrity
defects only, with gaps as an opt-in flag (chosen). (3) Warn on everything, fail on nothing — a
suite that cannot fail is not run.

**Choice and rationale.** Structural defects make the report silently wrong, which is the failure
mode worth blocking on. A gap is a true and expected state of the world; blocking on it teaches
people to edit the data rather than fix the control, and a compliance dataset that people have
learned to edit under pressure is worth less than no dataset. The `--fail-on-gap` flag exists for
the narrow legitimate case: a release pipeline for a system whose scope profile genuinely requires
zero gaps.

**Trade-off accepted.** Nothing automatically stops the gap count from drifting upward. Trend
reporting against the generated output is the intended compensating control, and it is a human
process.

**What was deliberately not done.** No threshold configuration, no gap budget. Both are mechanisms
for making a rising number acceptable, which is the outcome they are usually adopted to produce.

**How it would be revisited.** If the crosswalk is adopted as a release gate for a regulated
product, the gate belongs in the product's own pipeline with its own scope profile, not in this
repository's test suite.
