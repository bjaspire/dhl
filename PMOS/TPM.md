Executive Definition
Technical Product Manager (TPM) — Single Owner of Engineering Execution Correctness, Architecture Integrity, and Technical Release Quality
A Technical Product Manager is not a project coordinator and not a pure architect detached from delivery. They are the engineering execution governor: the owner of technical correctness, system design integrity, SDLC enforcement, and production-quality outcomes.
In O Labs, TPMs translate frozen scope into buildable engineering truth, ensure engineering teams ship correctly, and protect the platform from quality collapse, architectural entropy, and hidden technical risk.

Role Ownership Model in O Labs
 

Role

Owns

CTO

Product vision and long-term technology vision

Platform strategy and architectural principles

R&D direction and innovation agenda

Technical governance, standards, and risk ownership

Final authority on technical and product trade-offs

Technical Product Manager (TPM)

System & software architecture (application, data, infra design)

SDLC ownership and engineering execution standards

Code quality, technical quality, and delivery correctness

Technical documentation and system design artifacts

Technical R&D and feasibility validation

Tech debt & tech credit identification, prioritisation, and translation into development strategy

Translation of approved scope, requirements, and priorities into development roadmap and engineering stories

Translation of market insights provided by PM/CTO into technical execution strategy

Project Manager (PM)

Scope clarity, scope freeze, and change control

Timelines, milestones, and delivery commitments (3–6–12 months). This needs to be outlined and documented in Monday.com after discussion with Product manager and / or CTO wherever needed

Delivery health, risk tracking, and escalation

Stakeholder visibility and communication

Release readiness and go-live orchestration

Go-to-market execution (enablement, onboarding, rollout)

Market study, market R&D, and competitive analysis (business & delivery focused)

Acting as the operational bridge between CTO, Technical PM, and external/internal stakeholders

Non-negotiable separation

PM owns “what/when/visibility/commitment.”

TPM owns “how/correctness/engineering plan/quality gates.”

CTO owns “why/strategy/tradeoffs.”

TPM Operating Mandates
Canonical Rules (must be true always)
No Frozen Scope = No Engineering Commitment.
Engineering can investigate, but cannot commit to build without a Frozen scope state from PM.

No Jira Truth = No Work Exists.
If engineering work is not represented in Jira with acceptance criteria and DoD, it is not recognized.

No Definition of Done = No “Done”.
“Done” requires code + tests + review + documentation updates + observability + release-readiness evidence.

No Silent Architecture.
Any architectural decision that affects future work must be recorded as an ADR (Architecture Decision Record).

No Quality Debt Without a Receipt.
Any compromise must be logged as Tech Debt with rationale + risk + payback plan.

TPM Core Responsibilities 
1) Technical Feasibility & Discovery (Pre-Commitment)
Purpose
Prevent impossible promises and reduce late surprises by validating technical feasibility before commitment.

Responsibilities
Provide feasibility decision to PM/CTO: 

Yes 

Yes-with-constraints 

No 

Needs-discovery-spike.

Identify:

Architecture constraints

Integration dependencies

Data availability issues

Performance risks

Security/compliance constraints

Produce Spike plan when uncertainty exists.

Required Outputs
Feasibility Note (in Monday intake item or linked Confluence Doc)

Baseline Work Estimation (days) (immutable unless scope changes)

Key Risks + Dependencies (explicit)

Out of Scope
Negotiating delivery dates with client (PM owns)

Changing due dates (CTO owns)

Benchmarks
≥ 95% of approved items have feasibility decision within 5 business days of request

0 “approved commitments” later declared infeasible due to missed basic discovery

2) Architecture Ownership (Application, Data, Infrastructure)
Purpose
Ensure the solution fits platform principles, scales, remains maintainable, and is secure.

Responsibilities
Produce system design for new modules/features:

Data flow

Service boundaries

APIs/contracts

Eventing/queues where applicable

Failure modes

Decide architectural approach (within CTO principles)

Maintain Architecture Decision Records (ADRs)

Required Outputs
System Design Doc (Confluence)

ADRs for key decisions (Confluence)

API Contract Specs OpenAPI 3.x (Swagger UI for docs) as the standard contract format for all REST APIs.

Data Model / Schema notes

This is where you describe:

What are the main entities? (e.g., User, Order, Subscription, Campaign, etc.)

What fields/attributes they have (e.g., user_id, email, status, created_at)

How they relate to each other (e.g., one user has many orders, each order has one payment)

ERD = Entity‑Relationship Diagram – a visual diagram that shows:

Boxes = entities/tables

Lines = relationships (one‑to‑many, many‑to‑many, etc.)

“Or equivalent” means you don’t have to draw a formal ERD; you can:

Add a simple diagram

Use a structured table

Or write clear textual notes that explain the data structure and relationships

Out of Scope
Final business prioritization (CTO/PM)

Writing all production code personally (TPM can contribute, but not mandated)

Benchmarks
100% of features impacting architecture have ADRs

≤ 5% architecture rework due to missing/incorrect initial design assumptions

0 production releases with undocumented breaking changes

3) SDLC Governance & Engineering Execution Standards
Purpose of This Role Area
The Technical Product Manager (TPM) is the custodian of engineering correctness and execution integrity.

The TPM ensures that:

Engineering output is predictable, reviewable, testable, and releasable

Teams do not trade speed for long-term damage

Code, tests, and releases meet explicit quality gates

PMs and CTO can trust engineering commitments

The TPM does not write most code — but no code ships without standards defined by the TPM.

Responsibilities
Define and enforce:

Branch Strategy Governance (Source Control Discipline)

Objective: Ensure clean, predictable, low-risk integration of code across teams and environments.

Standard Strategy (Preferred): GitFlow (Mandatory default unless CTO approves exception)

Branch Structure

Branch

Purpose

main

Production-ready code only

develop

Integration branch for next release

feature/*

Feature or story-specific development

release/*

Pre-production stabilization

hotfix/*

Emergency production fixes

Rules (Non-Negotiable)

 

No direct commits to main or develop

All changes must go through Pull Requests (PRs)

Feature branches:

Must map to one Jira story

Must be short-lived (< 5–7 working days)

Release branches:

Only bug fixes, config changes, or release prep

Hotfix branches:

Must include post-release RCA ticket

 

TPM Accountability

Enforce branch rules via repo settings

Review violations monthly

Block releases if branch discipline is violated

Excellence Benchmark

0 direct commits to protected branches

< 10% long-running feature branches

 

Code review rules (mandatory reviewers, checklist)

Prevent defects, design erosion, and knowledge silos.

Mandatory Code Review Rules

Rule

Standard

Reviewers

Minimum 2 reviewers (1 senior)

Self-merge

❌ Not allowed

CI pass

Mandatory before merge

Checklist

Mandatory review checklist

PR size

Prefer < 400 LOC change

Code Review Checklist (Required)

Every PR must be reviewed for:

Correctness

Does the code do what the story says?

Edge cases handled?

Design & Architecture

Aligns with system architecture?

No unnecessary coupling?

Readability

Clear naming

Logical structure

Comments where intent isn’t obvious

Security

No secrets committed

Input validation present

Permissions respected

Performance

No obvious inefficiencies

Loops, queries, memory safe

Tests

Tests added/updated

Tests meaningful, not cosmetic

TPM Role

Define the checklist

Audit PR quality weekly

Coach reviewers who rubber-stamp

Excellence Benchmark

< 5% post-merge rollback rate

Declining production defects per release

 

Definition of Ready (DoR) for stories

Ensure engineering never starts work on ambiguous or incomplete stories.

A Story is “Ready for Dev” ONLY if:

✅ Business goal clearly stated
✅ Scope frozen
✅ Acceptance criteria defined
✅ Dependencies identified
✅ UX / API contracts attached (if applicable)
✅ Non-functional requirements stated
✅ Estimation completed
✅ PM approval recorded

TPM Enforcement

Stories without DoR → blocked

No sprint commitment without DoR

TPM has veto power on readiness

Example DoR Template (Jira)



Business Goal:
In Scope:
Out of Scope:
Acceptance Criteria:
Dependencies:
NFRs (Performance, Security, etc):
Test Scenarios:
Excellence Benchmark

< 5% sprint spillover due to unclear requirements

 

Definition of Done (DoD) for stories

Prevent “done-but-not-done” work.

A Story is “Done” ONLY if:

✅ Code merged to correct branch
✅ All PR reviews completed
✅ CI pipeline green
✅ Unit tests added/updated
✅ QA tests passed
✅ UAT acceptance (if applicable)
✅ Documentation updated
✅ No critical bugs open
✅ Monitoring / logging updated (if needed)

TPM Enforcement

No exceptions

“Almost done” ≠ Done

PM cannot demo unfinished work

Excellence Benchmark

0 production releases with missing DoD items

 

Test strategy and minimum coverage expectations

Catch defects early and reduce regression risk.

Mandatory Test Layers

Layer

Responsibility

Unit Tests

Developers

Integration Tests

Developers

Regression Tests

QA

UAT

Support / Business

Observability

DevOps / TPM

Coverage Expectations (Guideline)

Area

Minimum

Business logic

≥ 80%

Critical paths

100%

Bug fixes

Test mandatory

Coverage % is a signal, not a goal — quality matters more.

TPM Role

Define minimum thresholds

Block merges without tests

Track flaky tests

Excellence Benchmark

Decreasing escaped defects per release

 

Release gates (QA/UAT/observability/security)

Ensure production is stable, observable, and recoverable.

Mandatory Release Gates

Gate

Required

Code

PRs merged, tests passing

QA

Regression passed

UAT

Business verification

Security

No critical vulnerabilities

Observability

Logs/alerts in place

Rollback

Plan defined

TPM Authority

TPM can block release

No PM or Dev override without CTO approval

Excellence Benchmark

0 releases without rollback plan

MTTR decreasing over time

Required Outputs
Engineering Standards Doc (single source)

Jira workflow discipline:

“Ready for Dev” criteria

“Ready for QA” criteria

“Ready for Release” criteria

Out of Scope
Sprint cadence governance (PM/EM shared; TPM enforces DoR/DoD)

Stakeholder communications (PM)

Benchmarks
≥ 95% stories entering sprint meet DoR

≥ 90% stories exiting sprint meet DoD

0 “Done” stories reopened due to missing acceptance criteria/test gaps more than 2 times/sprint average

4) Engineering Breakdown: From Frozen Scope → Jira Execution Truth
Purpose
Convert frozen requirements into buildable work that engineers can execute without ambiguity.

Responsibilities
Break down frozen scope into:

Epics, Stories, Subtasks

Test notes

Non-functional requirements (NFR) → Prepare any needed non-functional requirement documents inside confluence. 

instrumentation/monitoring tasks

work items needed to make sure:

The system emits the right signals (metrics, logs, traces, events)

You have visibility into how the product behaves in production

Teams can detect issues early and measure success of the feature

Instrumentation = adding the code and configuration that records what is happening in the system.

Typical examples:

Product analytics events

Tracking user actions: signup_started, signup_completed, button_clicked, feature_used

Tracking funnels: search → view item → add to cart → checkout

Business/product metrics

daily_active_users, conversion_rate, retention, churn, revenue

Technical metrics

Latency, error rates, request counts, queue sizes, CPU/memory usage

Logging/tracing

Structured logs for important flows

Distributed traces across services (if you use tracing like OpenTelemetry/Jaeger/Datadog/etc.)

As a TPM, this usually means:

Defining what needs to be tracked and why

Specifying event names, properties, and when they fire

Aligning with analytics/data/engineering to ensure it’s implementable and useful

Monitoring = using those signals to observe health and performance over time.

Typical examples:

Dashboards (Grafana, Datadog, New Relic, etc.)

API latency and error rate

Feature adoption and usage

Infrastructure health

Alerts

Error rate above X%

Latency above Y ms

Drop in key business metric (e.g., conversions down 30% vs baseline)

SLOs/SLAs

Defining target reliability or performance (e.g., “99.9% of requests < 300ms”)

As a TPM, this usually means:

Ensuring key metrics are visible (dashboards exist and are correct)

Agreeing with engineering on alert conditions and what to do when they fire

Using monitoring data to validate the impact of the feature after release

migration tasks (if any)

Each story must include:

Description (precise)

Given/When/Then AC

negative cases

data assumptions

performance expectations

dependencies

rollout strategy (flags, migration, backward compat)

Required Outputs
Jira epic/story set with full engineering readiness

Linkages:

Monday item ↔ Jira epic

ADR ↔ epic

PRs ↔ stories

test runs ↔ stories

Out of Scope
ETA ownership (PM)

UAT sign-off ownership (PM), though TPM provides technical quality evidence

Benchmarks
≥ 90% stories require no clarification meetings after sprint starts

≤ 10% story scope churn after sprint commitment (excluding formal CRs)

5) Code Quality, Review Discipline, and Technical Correctness
Purpose
Quality is engineered, not inspected.

Responsibilities
Enforce code review rigor: making sure code reviews are thorough and consistent, not just rubber-stamped.

correctness

Ensure the code does what it is supposed to do:

Logic is right

Requirements are correctly implemented

No obvious bugs or broken flows

Edge cases

Check how the code behaves in non-happy paths:

Empty inputs, huge inputs, invalid data

Network failures, timeouts, race conditions

Unusual user actions or workflows

Security

Look for vulnerabilities:

Injection (SQL/NoSQL, XSS)

Authentication/authorization checks

Data exposure, secure storage of secrets

Proper use of encryption where needed

 

Performance

Ensure the code won’t cause performance issues:

Avoid unnecessary heavy operations (e.g. N+1 queries)

Reasonable time/space complexity

Efficient database and API usage

Maintainability

Make sure future engineers can work with this code:

Clear structure and naming

Good separation of concerns

Reasonable complexity (not overly clever)

Tests that are readable and reliable

Maintain codebase health: Beyond single PRs, this is about keeping the whole repository clean, consistent, and sustainable.

Linting

Enforce automated style and basic correctness checks:

Use linters (ESLint, Pylint, etc.)

Keep lint rules relevant and enforced in CI

Fix or eliminate ignored warnings over time

Static analysis

Use tools that analyze code without running it to find issues:

Type checking (TypeScript, MyPy, etc.)

Security scanners

Code smells, unreachable code, dead code

Dependency hygiene

Keep third-party libraries safe and manageable:

Regularly update dependencies

Remove unused libraries

Pay attention to security advisories and licenses

Avoid unnecessary dependency bloat

Consistent patterns

Ensure the codebase feels cohesive:

Common patterns for error handling, logging, configuration

Shared abstractions instead of duplicating logic

Follow agreed architectural conventions

Define “quality escape hatch” policy (rare, logged, CTO-visible)

Sometimes you need to ship something urgently even if it doesn’t meet all normal quality standards (e.g. a production incident fix, urgent regulatory change).

There is an “escape hatch” – a controlled way to bypass some quality checks in rare cases.

Its use must be:

Rare – not a normal path for delivery

Logged – documented clearly (who, why, what risk, follow-up actions)

CTO-visible – leadership is aware whenever this is used, creating strong accountability

In practice:

TPM along with CTO define criteria like:

When is it allowed? (e.g. severity-1 incident, regulatory deadline)

What can be skipped? (e.g. some tests, code review constraints)

What mandatory follow-up is required? (e.g. post-incident review, cleanup ticket)

CTO ensure every TPM understands this is an exception process, not a shortcut for normal work.

Required Outputs
Review checklists

CI quality gates

Quality debt log (when exceptions happen)

Out of Scope
Writing all tests personally (TPM ensures they exist and meet standards)

Benchmarks
0 critical security issues introduced via missed review gates

CI pass rate ≥ 90% on main branch

“Hotfix due to missed test” rate trending downward QoQ

6) Test Strategy, Automation, and Regression Control
Purpose
Reduce the UAT/regression bottleneck by shifting quality left and automating verification.

Responsibilities
Define layered testing approach:

unit

integration

contract tests

e2e (critical flows only)

performance smoke tests

Maintain regression suite and ensure it runs in CI/CD

Enforce minimum automated coverage for critical modules (risk-based)

Required Outputs
Test Plan per major epic

Regression Suite ownership map

Test reports attached/linked in Jira

Out of Scope
Manual QA execution ownership (QA team); TPM governs strategy and completeness

Benchmarks
≥ 80% of critical paths covered by automation

UAT cycle time reduced QoQ (target: 20–40% reduction over 2 quarters if currently heavy)

Post-release P1/P2 due to regression: 0–1 per quarter per product stream

7) Release Engineering & Environment Readiness (Technical Side)
Purpose
Ensure “release-ready” is technically true: build, deploy, observe, rollback.

Responsibilities
Define deployment architecture expectations with DevOps:

rollout strategy

rollback plan

migrations

feature flags

config management

Ensure observability:

logs

metrics

traces

dashboards/alerts for new features

Provide “technical release readiness” evidence to PM

Required Outputs
Deployment notes + rollback plan

Monitoring additions documented

Release checklist technical section completed

Out of Scope
Go-live scheduling and stakeholder notification (PM)

Benchmarks
0 releases without rollback plan for high-risk changes

Mean time to detect (MTTD) improves QoQ

Mean time to recover (MTTR) improves QoQ

8) Tech Debt & Tech Credit Governance
Purpose
Keep velocity sustainable and prevent platform collapse.

Responsibilities
Identify and classify:

tech debt (risk + interest)

tech credit (investments that increase future speed)

Translate into roadmap items with:

business risk narrative

cost of delay

mitigation options

Maintain a “debt ratio” view per service/module

Required Outputs
Tech Debt Register (Jira epics + tags)

Quarterly debt review pack for CTO

Out of Scope
PM-owned commitments; TPM provides technical risk and sequencing

Benchmarks
Tech debt items always include “risk + impact + payback plan” (100%)

No tech debt “unknowns” discovered during delivery > 1 sprint late without prior logging

9) Incident & Production Engineering Support (Technical Ownership)
Purpose
PM governs incident reporting; TPM ensures technical recovery and corrective engineering actions.

Responsibilities
Participate in incident response as technical lead (or ensure correct engineer leads)

Provide:

root cause analysis inputs

corrective actions breakdown

prevention architecture changes

Ensure PIR actions become Jira work and are completed

Required Outputs
PIR technical section

Corrective action epics/stories with owners and timelines

Out of Scope
PIR governance and submission SLA ownership (PM)

Benchmarks
100% PIR actions converted into Jira work within 3 business days

Repeat incidents with same root cause: 0

10) Engineering Team Enablement & Execution Leadership
Purpose
World-class TPMs scale engineering output, not by heroics, but by clarity and enablement.

Responsibilities
Mentor engineers in architecture, quality, patterns

Raise engineering maturity:

docs culture

review quality

testing discipline

Create reusable templates for stories, designs, ADRs, test plans

Required Outputs
Templates and reusable artifacts

Coaching evidence (tech talks, review notes, standards)

Benchmarks
≥ 2 reusable templates/dashboards/standards improvements per year

Reduced cycle time and rework QoQ attributable to clearer execution artifacts

Daily / Weekly Operating Rhythm (TPM)
Daily (non-negotiable)
Review Jira boards:

blockers

PR quality/merge health

test failures

Ensure stories in progress still match frozen scope (flag scope drift → PM)

Review CI/CD failures and enforce fixes

Weekly
Grooming session preparation:

ensure next sprint backlog meets DoR

Architecture review:

ADR updates

upcoming design risks

Quality review:

bug trends

escaped defects

regression stability

Monthly / Quarterly
Tech debt review & prioritization pack for CTO

Security/dependency audit cycle (with DevOps/Sec)

Platform maturity improvement plan

TPM Scope vs Out-of-Scope (Clarity Table)
Area

TPM Owns

TPM Does Not Own

Requirements

Translate frozen scope into buildable specs

Freeze scope (PM)

Timeline/ETA

Provide estimation and execution risk

ETA/due date commitments (PM/CTO)

Architecture

System/app/data design + ADRs

Product vision and platform principles (CTO)

Delivery

Technical correctness and engineering readiness

Stakeholder updates and GTM (PM)

Quality

DoR/DoD, testing strategy, review gates

Manual QA execution (QA), release approval (PM)

Incidents

RCA + corrective actions

Incident SLA reporting + comms governance (PM)

Tools & Technologies (World-Class TPM Stack)
Systems of Record
Jira: execution truth (epics, stories, workflows, evidence links)

Platform Central / Confluence: system design docs, ADRs, runbooks, PIR artifacts

GitHub: PR discipline, code owners, branching policy

CI/CD: Jenkins, GitHub Actions (quality gates, test automation)

Engineering Quality Tooling (recommended minimum)
Static analysis: SonarQube / CodeQL (depending stack)

Dependency scanning: Dependabot/Snyk

Observability: Datadog/New Relic/Prometheus + Grafana (choose one standard)

API specs: OpenAPI/Swagger

Feature flags: LaunchDarkly (or internal equivalent)

AI Tooling (mandatory usage)
Scope ambiguity detection (pre-grooming)

Test case generation (reviewed by humans)

PR review assistance (risk detection, edge cases)

Incident summarization + log correlation (assistive only)

Rule: AI output must be stored as artifact when it meaningfully changes decisions.

TPM Performance Benchmarks (CTO / Ops Evaluation)
Performance Dimensions & Weighting
Dimension

Weight

Architecture & Technical Integrity

25%

Engineering Predictability & Execution Readiness

20%

Quality, Testing & Regression Control

20%

SDLC Governance & Technical Discipline

15%

Production Excellence (Incidents, Reliability, Observability)

10%

Team Enablement & Org Maturity

10%

Total

100%

Quantifiable KPIs (Authoritative)
A) Architecture & Technical Integrity (25%)
Design coverage: % of impactful features with system design doc + ADRs = 100%

Architecture rework rate (avoidable redesign due to missing upfront design) ≤ 10% of major epics

Breaking changes without contract/version plan = 0

B) Engineering Predictability & Execution Readiness (20%)
Estimation accuracy (Estimation days vs actual dev effort) ≥ 75% within ±20%

Stories entering sprint meeting DoR ≥ 95%

Mid-sprint clarification churn (stories needing redefinition after start) ≤ 10%

C) Quality, Testing & Regression Control (20%)
Automated test coverage for critical flows ≥ 80%

Regression-caused P1/P2 incidents ≤ 1 per quarter per product stream

Reopened “Done” issues due to missing tests/AC ≤ 3 per sprint

D) SDLC Governance & Technical Discipline (15%)
PR review compliance (required reviewers/checklists) = 100%

CI pipeline stability (main branch pass rate) ≥ 90%

Quality gate bypass events = 0 (or ≤ 1/quarter with CTO-approved exception report)

E) Production Excellence (10%)
PIR corrective actions created within 3 business days = 100%

Repeat incidents same root cause = 0

Observability completeness for new features = 100% (dashboards/alerts defined)

F) Team Enablement & Org Maturity (10%)
Reusable engineering templates/standards delivered ≥ 2/year

Mentorship evidence (tech reviews, sessions, coaching) ≥ 1/month

Cycle-time improvement (lead time to merge/release) improves QoQ (tracked)

TPM Self-Evaluation Benchmark (Quarterly, Evidence-Based)
TPM must self-score with links/evidence:

Did every major decision have an ADR?

Did any feature ship without test evidence or observability updates?

Were any reworks caused by missing design, unclear AC, or weak DoR?

Did we bypass quality gates? If yes, is the exception documented and CTO-visible?

Are tech debt items documented with risk + payback plan?

Self-evaluation result bands

Green: all gates met; only controlled exceptions

Amber: recurring minor breaches; requires corrective plan

Red: quality gates bypassed, recurring incidents, missing ADRs → escalation

Competency Matrix (TPM Leveling Model)
Levels:
L1 Associate TPM → L2 TPM → L3 Senior TPM → L4 Principal TPM

Competency 1: Architecture & Design
L1: Understands existing architecture, contributes to design notes

L2: Authors system designs for features, produces ADRs

L3: Anticipates failure modes, optimizes boundaries, prevents rework

L4: Shapes cross-product architectural standards and platform direction (within CTO principles)

Evidence: design docs, ADRs, postmortems showing avoided failures

Competency 2: Execution Translation (Scope → Jira)
L1: Writes stories with supervision; uses templates

L2: Produces sprint-ready backlog with DoR compliance

L3: Produces dependency-aware plans across teams/streams

L4: Establishes org-wide story quality standards; reduces churn across portfolio

Evidence: DoR pass rate, reduced clarifications, stable backlog

Competency 3: SDLC & Quality Governance
L1: Follows SDLC rules, participates in reviews

L2: Enforces code review/testing discipline in a team

L3: Improves CI stability and regression strategy

L4: Establishes org-wide quality gates, measurably reduces escaped defects

Evidence: CI pass rate, escaped defect trends, gate compliance logs

Competency 4: Testing & Automation Strategy
L1: Understands test types, adds test notes

L2: Defines epic-level test strategy, enforces minimum automation

L3: Systematically reduces UAT/regression load

L4: Builds a culture of prevention; quality scales across teams

Evidence: automation coverage, UAT duration trends, regression incidents

Competency 5: Production Excellence
L1: Understands incident mechanics and runbooks

L2: Produces technical corrective actions after incidents

L3: Improves reliability via architecture and observability

L4: Drives platform reliability posture across products

Evidence: PIR actions closure rate, MTTR improvements, dashboards/alerts

Competency 6: Leadership & Enablement
L1: Helps teammates with clarity

L2: Mentors engineers in patterns/testing

L3: Drives engineering maturity and reusable assets

L4: Shapes engineering excellence programs across org

Evidence: templates, training cadence, adoption by multiple teams

Entry Benchmark & Transition Criteria for TPM Role
A) New TPM Hire (Entry Gate)
Mandatory

Proven experience owning architecture + execution standards

Evidence of:

system design writing

PR governance

testing strategy leadership

incident RCA participation

Tool literacy:

Jira workflows

CI/CD fundamentals

API contract practices

Disqualifiers

Only “feature coordination” without technical ownership

No evidence of enforcing quality gates

No experience with production systems reality

B) Internal Transition (Engineer/Lead → TPM)
Required evidence

Owned at least 1–2 production releases

Written at least 1 system design doc + ADR

Demonstrated code review leadership and testing discipline

Demonstrated ability to produce sprint-ready Jira stories

C) First 90 Days TPM KPIs
DoR compliance on owned backlog: ≥ 90%

ADR/design coverage for impactful work: 100%

Estimation accuracy: ≥ 70% within ±25%

Missing technical artifacts: 0

Quality gate bypasses: 0

TPM “No Confusion” Summary Rules
PM owns scope freeze and commitments; TPM owns buildability and correctness.

TPM cannot accept scope drift; must route to PM for CR.

No ADR for big decisions = decision not accepted.

No tests/observability for new features = not done.

 

Below is a Jira workflow blueprint that maps TPM responsibilities 1:1 to status transitions + DoR/DoD gates + required evidence fields, aligned to our O Labs PM constitution and our 3 parallel streams (2 product eng streams + 1 ML/CV stream).

One unified Jira workflow (works for all streams)

Stream-specific gates (ML/CV adds extra evidence states)

Exact DoR / DoD per status

Required Jira fields (evidence fields)

Automation/validators we can enforce in Jira

A) Jira Issue Types & When to Use What
Epic: business capability / end-user deliverable; maps to Monday Delivery Item (Frozen scope).
Story: user-facing or system functionality.
Task: enabling work (infra, refactor, tooling).
Bug: defect.
Spike: time-boxed discovery (allowed only pre-freeze or explicitly approved).
ML Experiment (optional custom issue type): experiments/training runs to keep ML work auditable.

Canonical rule: Once scope is Frozen in Monday, Spike scope must be explicit and time-boxed; otherwise it becomes hidden scope.

B) Status Workflow (Single Workflow for All 3 Streams)
Use this as the authoritative Jira workflow for Story/Task/Bug (Epics have slightly different statuses).

1) Story/Task/Bug Workflow States
Intake (Linked to Monday)

Discovery / Feasibility (TPM)

Ready for Scoping Freeze (PM Gate)

Backlog (Frozen Scope Confirmed)

Grooming (Engineering Ready)

Ready for Sprint (DoR Gate)

In Development

Code Review

Build/CI Verified

Ready for QA

In QA

QA Passed

Ready for UAT

In UAT (Support/Stakeholder Verification)

UAT Passed / Release Candidate

Ready for Release

Released to Production

Production Verified

Done

Blocked (overlay status, not terminal; can be implemented as a flag + reason field)

Cancelled (terminal)

Change Requested (routes back via PM CR governance)

Why this aligns to our PM constitution
Frozen Scope is upstream (PM). Jira reflects that with “Backlog (Frozen Scope Confirmed)”.

TPM owns engineering readiness: “Grooming → Ready for Sprint” is TPM-governed via DoR validators.

Release is not Done: we have explicit “Released → Prod Verified → Done” to match our Support/Verification rules.

C) Epic Workflow States (for Portfolio Visibility)
Epics should represent delivery outcomes and roll-up evidence.

Proposed (from Monday Intake)

Approved (CTO)

Scoped – Draft

Scoped – Frozen

Planned (Jira backlog ready)

In Execution

QA/UAT

Release Ready

Released

Adoption/Verification

Closed

On Hold / Parked

Cancelled

Epic Close rule: cannot move to Closed unless:

all child issues are Done/Cancelled

release pack link exists (Platform Central/Confluence)

production verification evidence exists

D) Definition of Ready (DoR) Gates — Enforced at “Ready for Sprint”
This is the single most important control point for TPM accountability.

DoR Checklist (Required for ALL streams)
A story/task/bug can move Grooming → Ready for Sprint only if:

1) Scope & Alignment
✅ Linked Monday Delivery item (URL field) AND scope state is Frozen (represented in Jira by field)

✅ “In Scope / Out of Scope” summary present (short form in Jira) OR link to scope doc

✅ No unapproved scope change (CR link required if changed)

2) Acceptance Criteria (Testable)
✅ Given/When/Then AC present

✅ Negative cases listed

✅ Data assumptions stated (inputs, edge data, nulls, corruption cases)

✅ Performance expectations stated (latency/throughput/accuracy etc.)

3) Engineering Plan
✅ Dependencies enumerated (other tickets / services / models / data)

✅ Rollout plan stated (flag, migration, backward compat)

✅ Observability plan stated (what logs/metrics, what dashboard/alert changed)

4) QA Readiness
✅ Test notes present (unit/integration/e2e expectations)

✅ Verification steps written for QA/UAT (human readable)

5) Ownership & Execution
✅ Owner assigned (dev)

✅ QA owner assigned (if applicable)

✅ Estimate present (from TPM/EM—our rule)

If any item missing → cannot enter sprint. This is how TPM prevents regression/UAT bottlenecks.

E) Definition of Done (DoD) Gates — Enforced at “QA Passed” and “Done”
we need two DoD levels:

DoD-1: “Dev Complete” (to move to Ready for QA)
✅ Code committed + PR linked

✅ Peer review completed (min 1 reviewer; 2 for high-risk)

✅ Unit tests added/updated

✅ Build green in CI

✅ No critical lints/static analysis failures

✅ Tech documentation updated if behavior changed

DoD-2: “Release Complete” (to move to Done)
To move Production Verified → Done, require:

✅ QA Passed evidence attached (test run link / checklist)

✅ UAT Passed evidence logged (Support/stakeholder comment)

✅ Release notes updated (link)

✅ Monitoring updated (dashboard/alert link if applicable)

✅ Production verification comment present (Support verification)

✅ No open Sev1/Sev2 bugs linked to this release

✅ If any compromise happened → Tech Debt ticket created + linked

F) Stream-Specific Additions (for 3 Parallel Streams)
Stream 1 & 2 (Product Engineering Streams)
Use the base workflow as-is.

Extra “Risk Class” field drives stricter gates:

Low / Medium / High
If High:

requires 2 reviewers

requires rollback plan mandatory

requires monitoring link mandatory

Stream 3 (ML/CV Stream) — Add Evidence States + Fields
ML work fails when we force it into pure software workflow without experiment audibility.

Recommended ML/CV sub-workflow (within same overall workflow)
Between Discovery/Feasibility and Ready for Sprint, add one extra state:

ML Design Ready (only for ML/CV labeled issues)

And between In Development and Ready for QA, add:

Model Training/Experiment
Model Evaluation
Model Packaging/Integration

we can implement these as:

separate statuses (preferred), OR

same statuses with mandatory ML fields (acceptable)

ML/CV DoR Additions (must be present)
To move to Ready for Sprint for ML/CV items:

✅ Dataset reference (versioned): dataset id + split definition

✅ Label schema reference (what annotations exist)

✅ Metric target(s): e.g., mAP@.5, IDF1, MOTA, latency fps, calibration

✅ Baseline benchmark recorded (current model performance)

✅ Evaluation protocol (how we measure, which dataset, leakage controls)

✅ Inference constraints (GPU/CPU target, runtime requirements)

✅ Failure modes list (occlusion, motion blur, crowding, lighting)

ML/CV DoD Additions (release-grade)
To move to Done:

✅ Model artifact version tag (registry ref)

✅ Training run log reference (experiment tracking)

✅ Evaluation report attached (metrics, confusion, ablations)

✅ Integration tests passing (pipeline or service)

✅ Drift/monitoring plan (at least metric logging in prod)

G) Required Jira Fields (Evidence Fields)
These are the fields that make the workflow enforceable and auditable.

Universal fields (All streams)
Monday Delivery Item Link (URL)

Scope State (single select): Draft / Frozen / Change Request

CR Link (URL or issue link) (required if Scope State = Change Request)

Acceptance Criteria (long text)

Negative Cases (long text)

Dependencies (issue links + text)

Data Assumptions (long text)

Performance Expectations (long text)

Rollout Plan (long text)

Observability Plan (long text)

QA Verification Steps (long text)

Risk Class (Low/Med/High)

Release Notes Link (URL)

Test Evidence Link (URL) (or attachment)

Prod Verification Evidence (comment template or field)

ML/CV extra fields
Dataset Version (text)

Label Schema Version (text/url)

Baseline Metric (number/text)

Target Metric (number/text)

Evaluation Protocol (long text)

Model Artifact Version (text)

Experiment Tracking Link (URL)

Inference Budget (fps/latency/hardware)

H) Transition Validators & Automations (Jira Enforceability)
Implement these using Jira Workflow Validators + Automation rules.

1) Validators (hard blockers)
Grooming → Ready for Sprint
Block transition unless:

Scope State = Frozen

AC, Negative Cases, Dependencies, QA Steps populated

Owner assigned

Estimate populated

Risk Class populated

For ML/CV: Dataset Version + Target Metric populated

In Development → Code Review
Block unless PR link is present (or dev branch attached via smart commits)

Code Review → Build/CI Verified
Block unless CI status is green (can be enforced by automation + label)

Ready for Release → Released
Block unless:

Release notes link exists

Rollback plan exists if Risk=High

UAT Passed status achieved

Production Verified → Done
Block unless:

Prod verification evidence exists

QA evidence exists

Any known compromise has linked Tech Debt ticket

2) Automations (soft/hard governance)
If Scope State changes to Change Request → auto move Jira issue to Change Requested

If Blocked flag set → comment template required: blocker reason + owner + ETA

If ticket sits in In QA > X days → auto alert TPM + PM

If Ready for Sprint and no sprint assigned within 7 days → alert TPM (backlog stagnation)

If Released but not Production Verified within 24–48h → alert PM + Support

I) RACI by Status (TPM responsibilities map 1:1)
Status

Responsible

Accountable

Evidence Owner

Intake / Discovery

TPM

TPM

Feasibility note, dependencies, estimation

Ready for Scoping Freeze

PM

PM

Scope doc + confirmation

Backlog (Frozen)

TPM

TPM

Story pack quality

Grooming

TPM

TPM

DoR completeness

Ready for Sprint

TPM

TPM

DoR validators satisfied

In Dev / Code Review / CI

Engineers (TPM governs)

TPM

PRs, tests, build

Ready for QA / In QA

QA (TPM governs completeness)

TPM

test evidence, defect linkage

Ready for UAT / In UAT

Support/Stakeholders

PM

verification notes

Ready for Release

PM + TPM

PM

release pack + tech readiness proof

Released / Prod Verified

PM + Support

PM

prod verification proof

Done

TPM (technical closure) + PM (delivery closure)

PM

closure notes, links, debt receipts

J) Minimal “Definition Templates” to Paste into Jira
Use these as mandatory sections inside each Story.

Story Template (All streams)
Problem / Context

In Scope

Out of Scope

Acceptance Criteria (Given/When/Then)

Negative Cases

Dependencies

Data Assumptions

Performance Expectations

Rollout Plan

Observability Plan

QA Verification Steps

Release Notes Requirements

ML/CV Addendum
Dataset Version + Split

Label Schema

Baseline Metrics

Target Metrics

Evaluation Protocol

Model Artifact Versioning

Inference Budget

Known Failure Modes

K) What This Solves (Directly tied to our bottlenecks)
Stops sprint-start ambiguity via DoR gating (TPM enforced)

Reduces UAT drag by requiring test evidence + QA-ready verification steps

Prevents silent scope changes by routing to “Change Requested” status

Makes ML work auditable with dataset/version/metric gates (no “mystery model” deliveries)

Prevents “Released = Done” confusion with explicit prod verification step