# Presentation purposes

University Edition separates **who presents**, **what the audience needs** and **how slides look**. The same person can teach in the morning, request a decision in the afternoon and present student research later. Do not infer purpose from a job title alone.

## Routing matrix

| Purpose ID | Intended outcome | Typical users / occasions | Default visual mode | Narrative spine |
|---|---|---|---|---|
| `general` | Understand a topic and know the next step | Any university member; unclear or broad brief | Institutional | Purpose → context → supported points → conclusion / next step |
| `teaching` | Learn and apply a concept | Lecturers, tutors, student-led learning | Lecture | Objectives → explanation → worked example → practice → recap |
| `research` | Assess a supported scientific claim | Researchers, postgraduate students, thesis defenses | Research | Question → related work → method → results → limitations → conclusion |
| `leadership` | Make a decision or review performance | Leadership, administrative teams, department/program reviews | Institutional | Decision needed → evidence → options → recommendation → action / review |
| `partnership` | Explore or advance cooperation | International relations, industry engagement, visiting delegations | Institutional | Verified context → mutual need → proposed scope → responsibilities → discussion / next steps |
| `admissions` | Make an informed applicant choice | Admissions, outreach, school visits, recruitment | Institutional | Audience need → verified programs → experience/support → requirements → next action |
| `training` | Perform a practical task safely | IT, HR, professional services, staff onboarding | Lecture | Task → prerequisites → reviewed procedure → demonstration → practice → help |
| `student-project` | Demonstrate a contribution and learning | Course projects, competitions, capstone showcases | Research | Problem → own contribution → approach → prototype/evidence → limits → next test |
| `event` | Orient participants and support an event | Organizers, clubs, orientation, ceremonies, conferences | Institutional | Welcome → purpose → confirmed programme → participation / logistics → closing |

These are supported use cases, not a verified organizational chart, university policy or fixed requirement to include every possible section. Choose only the sections that serve the actual brief. A three-minute welcome and a 40-minute proposal need different lengths.

## Purpose and mode are separate

Mode selects the shared visual treatment. Purpose selects the outline and starter wording. A `research` visual override on an admissions deck must not fabricate experimental methods. A `lecture` appearance on a leadership brief must not insert objectives or a quiz.

The builder provides explicit routing through `--purpose`; it does **not** interpret natural-language intent by itself. The agent reads the brief, selects the purpose and passes the corresponding ID. The machine-readable starter text lives in `purpose-profiles.json`.

If neither purpose nor mode is supplied, the CLI uses `general` + `institutional`. Explicit old-style `--mode lecture` infers `teaching`; `--mode research` infers `research`; `--mode institutional` infers `general`. An explicit purpose always controls content, even when the selected visual mode differs.

## A compact working brief

Record these fields from the user or source material rather than asking for them repeatedly:

```text
Purpose: the action, decision, understanding or learning sought
Audience: who is attending and what they already know
Language: English / Uzbek / Russian, matching the brief
Duration or approximate slide count: stated or transparently assumed
Sources: supplied materials and any authorized current primary sources
Sharing context: internal / external / mixed / not specified
Content status: sourced fact / proposal / student work / synthetic example
Presentation mode: selected from purpose or explicitly requested
Output: HTML, plus PDF when requested
```

If a source is absent, do not create impressive-looking university metrics as filler. Use a structural draft, explicitly mark missing evidence in the working notes, and report the limitation. Do not call the draft a verified final presentation. Unspecified sharing context is not permission to publish.

## Narrative recipes and evidence requirements

### General
Open with the main question or purpose. Provide just enough context, organize the supported points and end with a takeaway or action. Avoid accidental lecture wording. This is the neutral fallback, not a recommendation to use one generic layout for every slide.

### Teaching
Use measurable learning outcomes, explanations, worked examples, brief checks and a recap. Preserve required syllabus coverage. Follow `teaching-guidelines.md` for source mapping, accessibility and an audience-safe answer copy.

### Research
Use the real question, method, sample/protocol, results, uncertainty, limitations and references. Distinguish published findings, preliminary results and a future proposal. A research proposal should not contain imaginary completed results.

### Leadership and administration
Put the decision or review question early. Indicators need a period, definition, unit, denominator and source when applicable. Separate actuals from targets and forecasts. Compare relevant options, resource implications and risks; name owners/dates only when supplied or clearly proposed. A departmental status update may need exceptions and action items rather than a formal approval request.

### Partnerships
Use verified institutional introductions. Frame potential work as a proposal until its status is established. Explain mutual benefit, scope, responsibilities, dependencies and a next discussion. Distinguish contact, discussion, draft memorandum, signed agreement and active delivery; one does not establish another. Do not add partner marks, named attendees or commitments merely because a partner was mentioned.

### Admissions and outreach
Use current, approved program names and claims. Verify availability, degree-awarding arrangements, entry conditions, fees, scholarships, dates, accreditation and contact/application routes before including them. Preserve conditional wording. Do not promise admission, employment, visas, scholarships or rankings. If no current material is available, prepare a review draft without those claims.

### Staff training
Use a reviewed procedure or supplied system material. Cover prerequisites, safe examples, steps, common mistakes, practice and an authorized help route. Screenshots must not expose passwords, access tokens or personal records. Training content is not automatically an approved policy document. A process update needing a management decision may be `leadership`, not `training`.

### Student projects
Identify the author/team as supplied; show the actual contribution, approach, evidence and limitations. Cite borrowed material and comply with disclosed course/competition requirements. Include a readable “Student project” or equivalent label when institutional endorsement could be inferred. A thesis defense normally uses `research`; the presenter's student status does not force a less rigorous narrative.

### Events and student organizations
Use only confirmed details for public-facing schedules. Mark drafts and proposed slots explicitly. Do not invent speakers, sponsors, venue allocations or registration links. A research talk at an event is still `research`; `event` is for the welcome, logistics, programme or closing.

## Examples of routing

“I'm a professor hosting a visiting delegation” → `partnership`, not Teaching.

“I'm a student defending an experimental study” → `research`, not automatically Student Project.

“Present the finance team's process for submitting expense requests” → `training` when teaching the procedure; `leadership` when requesting a process change.

“Make a short university update from this note” → infer the outcome if clear; otherwise use `general` and disclose the assumption.

“Prepare a public open-day deck” → `admissions`; load `institutional-content.md` and verify changeable claims.
