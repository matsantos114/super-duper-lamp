# Running Backend Learning Tracker

## Project Purpose

This project is a hands-on backend engineering curriculum built around a running activity platform.

The primary goal is not simply to finish an application. The goal is to understand how a production backend is designed, implemented, tested, debugged, and explained.

By the end of the project, you should be able to:

- Build a backend API from scratch.
- Design relational data models.
- Validate and persist user input.
- Separate routing, business logic, and database concerns.
- Write meaningful unit and integration tests.
- Handle duplicate requests and failure cases safely.
- Build asynchronous processing workflows.
- Explain technical tradeoffs clearly.
- Design a scalable version of the system.
- Discuss the project confidently in software engineering interviews.

---

# Current Learning Position — Reviewed Through September 6, 2026

**Resume at Lesson 3E: design the conversion from validated `RunCreate` input to a persisted `Run` and a database-backed response.**

The purpose remains learning backend engineering through work you can explain and repeat independently. The existing milestone catalog is a reference, not a requirement to complete one large feature every session. This review updates the curriculum; it does not implement the remaining application for you.

Companion learning map: [`Backend-Vocabulary.md`](Backend-Vocabulary.md). It follows the request lifecycle, gives core concepts more attention than supporting terms, connects definitions to real project code, and uses progressively harder recall questions.

## Progress Verified Against the Repository

Review baseline: commit `30598d2`; working tree was clean before this tracker update.

| Area | Evidence observed | What is still unverified or unfinished |
|---|---|---|
| Setup and Git | Project dependencies and lock file exist; setup is committed (`a48e305`). | Independent setup from a fresh checkout has not been demonstrated in this review. |
| HTTP and validation | Health endpoint, typed POST request, field constraints, and 201/422 behavior exist. | POST currently returns the request data; its 201 response does not prove a resource was saved. Earlier self-reported understanding is retained, not newly assessed. |
| Tests | Three tests pass: health, valid POST, zero-distance rejection. | Other constraints, database writes, migrations, and failure recovery are not covered. |
| Configuration | `app/config.py` declares a required database URL and local environment-file loading. | Configuration code is present; database availability was not checked. Secret values were not read. |
| Sessions | `app/database.py` defines the engine, session factory, and a generator that closes the session. | Routes do not use this dependency yet. Request cleanup, transaction ownership, and failure behavior need exercises. |
| Data model | `app/models.py` declares a primary key, unique external ID, four check constraints, nullable fields, and timestamps. | These are Python declarations. No migration files are present; the actual database schema was not inspected. |
| Migrations | Alembic is declared as a dependency. | Initialization, migration review, application, and verification remain pending. |

Verification on September 5: `.venv/bin/python -m pytest -q -p no:cacheprovider` → **3 passed**, with one TestClient/httpx deprecation warning. Treat the warning as a later dependency-maintenance exercise; it did not fail these tests. The test run does not establish PostgreSQL connectivity or persistence.

## Course Adjustments

1. **Learn in small, observable steps.** Each session has one concept, one learner-owned change or experiment, and one concrete completion check.
2. **Test throughout the course.** Bring validation tests into Milestone 2 and database integration tests into Milestone 3. Milestone 12 becomes consolidation and test-design practice.
3. **Use SQL before relying on ORM automation.** Read a small `CREATE TABLE`, write basic `INSERT`/`SELECT`, and explain `NULL`, keys, and constraints using this project's model.
4. **Teach the first migration alongside persistence.** Follow 3A → 3B → the initial-migration portion of Milestone 4 → 3D. Return to Milestone 4 later for schema evolution; do not wait until after building persistence to establish migration history.
5. **Introduce commit, rollback, and duplicate failures with the first write.** Milestones 9–11 later deepen those concepts with concurrency, multi-step transactions, and consistent errors.
6. **Add abstractions when there is a reason.** Milestone 6 is a refactoring exercise after working behavior exists. A repository layer is a design option to evaluate, not a compulsory wrapper around every query.
7. **Bring practical habits forward.** Practice environment setup and traceback reading now; add a minimal test CI workflow once database tests are reproducible. Revisit Docker, CI/CD, logging, and security in their full milestones.
8. **Separate essential skills from specialization.** SQL, HTTP, validation, persistence, testing, ownership checks, debugging, and basic deployment are the core. Queues, imports, caching, specific cloud products, and million-user design come after that core. Progress depends on evidence, not on installing every listed technology.

## Interactive Lesson Format

Suggested session length: 25–45 minutes, adjusted to understanding.

1. **Recall:** explain one prior concept without consulting the implementation.
2. **Predict:** state what a small experiment will do and why.
3. **Build or inspect:** make one focused change yourself, or gather evidence without changing code.
4. **Verify:** compare the prediction with actual output; include a failure case when applicable.
5. **Review:** discuss correctness, one relevant tradeoff, and the smallest useful improvement.
6. **Teach back:** explain the behavior in your own words and solve one variation.
7. **Record:** save evidence, remaining uncertainty, and the exact next task.

Use a hint ladder: question → location/concept → pseudocode → minimal example when needed. Review the learner's attempt before expanding the solution. Avoid introducing several unfamiliar concepts in one response.

Track these separately for each lesson:

- **Implemented:** an artifact or experiment exists.
- **Verified:** relevant behavior was observed; record the test or output.
- **Explained:** the learner explains mechanism and a failure case without reading a solution.
- **Retained:** the learner solves a related problem in a later session.

Code review cannot establish understanding on the learner's behalf. Leave explanation and retention evidence pending until demonstrated. Check a milestone complete only when its required behavior is verified and explained; revisit retention next session.

## Immediate Learning Path

These are separate lessons, not a single implementation assignment.

| Lesson | Focus and learner task | Evidence required before advancing |
|---|---|---|
| **3A — Explained** | Trace `RunCreate`, `Run`, `Base.metadata`, engine, and session to their roles. Inspect the model and predict whether POST writes anything. | Learner explained that POST currently returns the request without passing it to persistence; the model declares the intended table; a missing table causes a database error when SQL is sent. Retention check remains. |
| **3B — Explained** | Establish a dedicated local learning database; verify the intended database and run read-only connectivity/schema queries. Learn connection URL components without exposing credentials. | Connectivity to `localhost:5432/running_app` was verified. `inspect(engine).get_table_names()` returned `[]`. Learner recognized that a separate schema-changing action is required and raised migration versus seeding for clarification. Retention check remains. |
| **3C — Complete** | Initialize Alembic; load model metadata; generate and review the initial migration; apply it to the learning database. | Revision `3f7d9083d2ce` was generated, reviewed, recovered after a syntax-error exercise, and applied. `alembic current` reports head; inspection returns `alembic_version` and `runs`. Learner explained first-revision, upgrade, and downgrade responsibilities. Retention check remains. |
| **3D — Complete** | Insert and retrieve one run using a session before connecting the HTTP route. Predict `add`, `flush`, `commit`, and `rollback`. | Learner created, added, flushed, committed, retrieved, and rolled back runs. Explained commit as the lasting save, flush as sending work within an open transaction, and rollback as canceling uncommitted work. Retention check remains. |
| **3E — Current / test client fixture verified** | Connect POST to a request-scoped session and introduce a response schema that includes server-assigned fields. | The isolated `db_session` and `db_client` fixtures work together, and all 4 tests pass. Next: make `POST /runs` request a session through `Depends(get_db)`, then persist and return a `RunRead`. |
| 3F | Trigger a duplicate-ID failure; define the initial API conflict policy and session cleanup. | Duplicate attempt leaves one row; a subsequent valid request succeeds; the error response does not expose internals. |

Before 3E, learn test database separation, dependency overrides, and fixture cleanup. Do not let integration tests use an ordinary development database by accident. Preserve the existing validation tests and adapt repeated activity IDs to isolated test data. A single-request duplicate test is not proof of concurrency safety; that comes in Milestone 9.

Then continue with retrieval/404 and stable pagination (Milestone 5), schema evolution (remaining Milestone 4), and service extraction only as complexity warrants (Milestone 6). Follow with domain calculations and timezones (7–8), reliability depth (9–11), testing consolidation (12), and runner identity/ownership (13). Establish basic authentication/authorization before any public deployment or real user data; then advance through operations and optional integrations.

## Review Questions to Revisit at the Right Time

- **Validation coverage:** only zero distance has a rejection test. Add one boundary case at a time, including duration, optional values, field lengths, and invalid timestamps; learn parametrization when repetition becomes useful.
- **Time policy:** `RunCreate.started_at` currently uses plain `datetime`, while the ORM column declares timezone support. Decide whether offset-free input is accepted, and prove the chosen policy with tests before persisting timestamps. Database column configuration is not a substitute for an input policy.
- **Identity scope:** external IDs are currently globally unique. Keep the initial exercise simple, but document that runner/provider-scoped uniqueness must be revisited when multiple users or import providers exist.
- **Validation versus integrity:** explain why the database repeats positive-distance rules, and inspect which request rules are not database constraints (for example, nonempty external IDs).
- **Timestamp ownership:** investigate how the existing `updated_at` setting behaves for ORM updates versus direct SQL updates; do not assume all writers update it automatically.
- **Session ownership:** name who commits and rolls back when the route begins writing. Session cleanup alone is not evidence that successful writes are committed.

## Lesson 3A — First Exercise

**Goal:** explain what currently exists and what must happen before a row can survive a restart.

Read `app/main.py`, `app/models.py`, and `app/database.py`. Without changing application code, answer:

1. Does today's `POST /runs` write to PostgreSQL? Identify the line that supports your answer.
2. What is the difference between declaring `class Run(Base)` and creating the `runs` table in PostgreSQL?
3. What separate jobs do a migration and a session perform?

If needed, inspect `Run.__table__` and `Base.metadata.tables` in a Python shell after importing `Run` from `app.models`. This inspects Python metadata; it does not demonstrate that a database table exists. Compare your prediction with what you see.

**Stop point:** discuss your answers before writing migrations or persistence code. The next implementation exercise is 3B once the distinction is clear.

Targeted references: [SQLAlchemy: database metadata](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html) and [Alembic: generating and reviewing migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html). Use the relevant sections after making a prediction. Model declarations describe schema; database DDL creates it. Autogenerated migrations are candidates that require human review.

## Simple Terms Learned So Far

- **PostgreSQL:** the database program running on the computer.
- **Database (`running_app`):** the named container inside PostgreSQL that this project connects to.
- **Table (`runs`):** the structure inside that database that will hold run records.
- **Model (`Run`):** the Python description of what the table should look like. It does not create or update the real table by itself.
- **Migration:** saved instructions that change the real database structure.
- **Engine:** SQLAlchemy's configured entry point for obtaining database connections.
- **Connection:** an active conversation with the selected database.
- **Session:** SQLAlchemy's workspace for reading, adding, changing, committing, or rolling back records.
- **Query:** a request sent to the database.
- **`execute()`:** sends a query to the database.
- **`scalar_one()`:** returns the single value expected from a one-value result.
- **Current request flow:** `POST /runs` validates the input and returns it, but does not save it.

## Session Record — September 5, 2026

- Work completed: repository and lesson review; baseline tests; curriculum resequencing; next exercise prepared.
- Learner progress newly verified: no new explanation or retention assessment yet.
- Application changes: none in this review.
- Database state: not inspected or modified.
- Current lesson status: 3A assigned; learner response pending.
- Next action: answer the three 3A questions; review any misconception before moving to 3B.

## Session Record — September 6, 2026

- Work completed: discussed the roles of the request schema, ORM model, migration, engine, connection, query, and session.
- Learner explanation: correctly identified that `POST /runs` only returns validated data and does not reach persistence logic. Correctly understood that changing the model requires a migration before an existing database table changes.
- Clarification needed: an engine/connection connects to the selected database, not directly to its tables; `execute()` sends SQL and `current_database()` reports the already-selected database.
- Verification evidence: a read-only connection query returned `running_app` at `localhost:5432`.
- Database state: connectivity is verified. `inspect(engine).get_table_names()` returned `[]`; `running_app` currently has no regular tables, including no `runs` table.
- Current lesson status: Lessons 3A and 3B explained; Lesson 3C is current. Retention checks remain pending.
- Learner teach-back: correctly recognized that defining a model does not create the table and that a separate operation is required. Clarified that migrations change schema, while seeding inserts starter/sample rows after the schema exists.
- Next action: initialize the Alembic file structure, inspect what was generated, and make no schema or application changes yet.
- Learning material updated: `Backend-Vocabulary.md` now organizes concepts around the `POST /runs` lifecycle. Major concepts include why they exist, where they fit, actual project code, important distinctions, failure implications, and three levels of recall practice. Terms are marked Core, Supporting, or Recognition so current priorities remain clear.
- Alembic initialization evidence: `.venv/bin/alembic init alembic` completed successfully and created the migration environment. The follow-up `rg` listing failed because `rg` is not installed on the learner's machine; `find` confirmed the expected files. This tooling error did not affect Alembic initialization.
- Current Alembic state: `alembic.ini` retains Alembic's harmless placeholder URL, while `env.py` overrides it at runtime with `settings.database_url`. `target_metadata` is still `None`. No revision has been generated or applied.
- Alembic connection evidence: `.venv/bin/alembic current` reported `PostgresqlImpl` and transactional DDL, confirming that Alembic reached PostgreSQL using the configured runtime URL. It printed no revision because none has been applied.
- Configuration still pending: the saved `alembic/env.py` continues to define `target_metadata = None`. Connectivity can succeed without model metadata, but autogeneration cannot compare the `Run` model until this becomes `Base.metadata`.
- Configuration completion: after a line-by-line walkthrough, `target_metadata` was saved as `Base.metadata`. A second `.venv/bin/alembic current` connected successfully. The earlier “configuration still pending” entry records the intermediate state and is now resolved.
- Migration generation evidence: `.venv/bin/alembic revision --autogenerate -m "create runs table"` detected the added `runs` table and created revision `f7558c5349f3`. The migration has been inspected but not applied. Existing tests still pass: 3 passed with the previously observed TestClient/httpx deprecation warning.
- Migration review evidence: learner correctly distinguished `upgrade()` from `downgrade()`. Clarified that `down_revision = None` means there is no earlier migration; it does not depend on the number of tables involved.
- Debugging evidence: `alembic upgrade head` and the following `alembic current` failed because terminal output had been pasted into the generated revision file. Python reported `SyntaxError` at line 1, where the shell prompt appeared. The failure happened while Alembic loaded the revision, so `upgrade()` did not execute and the database schema was not changed.
- Recovery plan: because this revision was generated, reviewed, and never applied, remove only the corrupted revision file and regenerate it from unchanged model metadata. Inspect the regenerated file before retrying the upgrade.
- Recovery evidence: the broken revision was preserved in `/tmp`, the versions directory was confirmed empty, and Alembic regenerated revision `3f7d9083d2ce`. The replacement contains only the expected Python migration, passes Python compilation, and `alembic history --verbose` recognizes it as `head` with parent `<base>`.
- Migration application evidence: `alembic upgrade head` ran upgrade `<base> → 3f7d9083d2ce`. `alembic current` reports `3f7d9083d2ce (head)`. SQLAlchemy inspection now returns `['alembic_version', 'runs']`, confirming the version-tracking and application tables exist in PostgreSQL.
- Lesson 3C completion: learner requested the checkpoint be marked complete after generation, review, debugging, application, revision verification, and table inspection. A later lesson will revisit schema/model consistency as a retention exercise.
- Lesson 3D first observation: learner initially predicted the internal `id` would equal the external activity ID and that `created_at` would already contain the time. Runtime inspection clarified the distinction: `external_activity_id` and `started_at` were supplied by Python, while `id` and server-default `created_at` remained `None` before insertion.
- Lesson 3D pending-state evidence: after `db.add(run)`, SQLAlchemy reported `(transient=False, pending=True, persistent=False)`. The database-assigned `id` and `created_at` remained `None`, demonstrating that adding tracks intended work without itself proving an insert or commit.
- Lesson 3D flush evidence: after flushing, SQLAlchemy reported `(transient=False, pending=False, persistent=True)`. PostgreSQL returned internal ID `1` and a server-created timestamp. This proves the insert was processed inside the current transaction; durability remains unverified until commit.
- Lesson 3D pre-commit visibility evidence: a second session queried the flushed run by primary key and returned `None`, then was closed. The insert remained isolated inside the original session's uncommitted transaction.
- Lesson 3D teach-back: learner explained that creating another `SessionLocal()` produced a separate session and that the first session's model data was not yet stored as committed table data. Refined distinction: flush had inserted the row inside the first transaction and assigned ID `1`, but the row was neither visible to the second transaction nor durable until commit.
- Lesson 3D commit evidence: after committing and closing the original session, a fresh session queried `external_activity_id == "lesson-3d-001"`; `saved_run is not None` returned `True`. This proves the row survived beyond the original session and transaction.
- Lesson 3D stored-value evidence: the fresh session retrieved internal ID `1`, external ID `lesson-3d-001`, distance `5000`, duration `1800`, the supplied start time, and PostgreSQL's creation time. The fresh session was then closed.
- Lesson 3D rollback evidence: after a second run was flushed and then rolled back, a fresh session queried its external activity ID. `missing_run is None` returned `True`, proving the uncommitted insert was canceled.
- Lesson 3D remaining concept: learner described flush as pushing data to the table and rollback as canceling it, but initially described commit as preparation for flush. Clarification required: commit automatically flushes pending work when necessary and then makes the transaction permanent; rollback is the alternative that cancels uncommitted work after an error or deliberate decision.
- Lesson 3D completion: learner compared commit to saving a document and explained that the rolled-back run did not persist. Final refinement: after flush, the insert was inside the open database transaction rather than still in the session's pending tray; `rollback()` canceled it, while `close()` only cleaned up the session afterward.
- Lesson 3E data-ownership decision: the client supplies external activity ID, measurements, start time, and optional notes. PostgreSQL generates the internal primary key and initial timestamps. Nuance retained for later: the current `updated_at` declaration uses an ORM-side `onupdate`, so PostgreSQL does not independently update it for every possible non-ORM writer.
- Lesson 3E response-schema evidence: learner added `RunRead(RunCreate)` with `ConfigDict(from_attributes=True)` and required generated fields `id`, `created_at`, and `updated_at`. The existing three tests still pass; conversion from a retrieved ORM object remains to be demonstrated.
- Lesson 3E ORM-to-response evidence: `RunRead.model_validate(saved_run).model_dump()` returned every client field plus ID and timestamps from the retrieved ORM object. Clarified that Python `datetime` values are converted to JSON strings later by FastAPI's response serialization.
- Lesson 3E test-isolation discussion: learner identified that test writes would skew development data. Clarification: database integration tests intentionally exercise session, insert, flush/commit, and query behavior; reliability comes from directing those writes to a separate resettable test database rather than skipping real persistence.
- Test-database setup attempt: creating `running_app_test` while authenticated as `running_app` failed twice with `permission denied to create database`. This proves authentication succeeded but the application role lacks the `CREATEDB` role attribute. Next: identify the local administrative PostgreSQL role and use it only to create a test database owned by `running_app`.
- PostgreSQL role inspection: `\du` showed local role `mathewsantos` has Superuser and Create DB attributes, while `running_app` has neither. Clarified that role attributes displayed by `psql` are descriptive output, not zsh commands. Use the administrator role for database setup while keeping routine application access limited to `running_app`.
- Test database creation evidence: administrator role `mathewsantos` created `running_app_test` with `running_app` as owner. `\l running_app_test` returned one matching UTF-8 database row with the expected owner. Application-role connectivity and schema migration remain pending.
- Test database connectivity evidence: an authenticated `psql` command using role `running_app` connected to `running_app_test`; `SELECT current_database()` returned `running_app_test`. The isolated database is reachable but does not yet have the migrated schema.
- Test configuration evidence: `.env.test` exists and `git check-ignore -v .env.test` identifies the `.gitignore` rule. `git status --short` does not list the secret-bearing file. Only its presence and ignore status were inspected; its credential value was not printed.
- Test schema migration evidence: a temporary subshell exported `.env.test` only for the Alembic process. `alembic upgrade head` ran `<base> → 3f7d9083d2ce`, creating the initial schema in `running_app_test` without changing the shell's normal development configuration.
- Test schema verification evidence: under the temporary `.env.test` environment, `alembic current` returned `3f7d9083d2ce (head)` and SQLAlchemy inspection returned `['alembic_version', 'runs']`. Migration history and real table state agree in the isolated database.
- Dependency-injection teach-back: learner explained that supplying the session through `get_db()` lets tests manipulate `running_app_test` instead of `running_app`. Additional benefit: route code remains independent of session construction and cleanup details.
- Safe test-engine evidence: Pytest discovered `tests/conftest.py`; it loaded `.env.test`, parsed the database URL, passed the exact-name safety guard, and created a lazy test engine and session factory. The existing suite reports 3 passed with the known TestClient/httpx warning. Because no fixture uses the engine yet, this test run does not itself prove a SQLAlchemy test connection was opened.
- Test-session fixture evidence: `db_session` opens a connection, begins an outer transaction, yields a savepoint-aware session, then closes the session, rolls back the outer transaction, and closes the connection. `test_uses_isolated_database` executed `SELECT current_database()` and passed against `running_app_test`; total suite result is 4 passed with the known warning.
- Test-client fixture attempt: `db_client` now overrides `get_db()` with the isolated `db_session`, yields a `TestClient`, and clears the override afterward. The route-test refactor produced two failures because `tests/test_runs.py` defines each test name twice. Python replaces the earlier fixture-based definition with the later definition, where `client` is undefined. This is a test-code naming/reference error; it does not show a failure in the fixture or database.
- Test-client fixture verification: after retaining one definition per route test, adding `db_client` as each test parameter, and sending requests through that fixture, Pytest reported **4 passed** with the known TestClient/httpx deprecation warning. The fixture wiring is verified. The route still does not request `get_db()`, so the override is ready but has not yet participated in route execution or persistence.
- Lesson 3E ORM conversion evidence: `RunRead.model_validate(saved_run)` succeeded, and `model_dump()` contained all expected run fields, internal ID `1`, and database timestamps. This verifies the ORM-to-response-schema boundary; FastAPI JSON serialization remains to be verified through the route.
- Debugging note: an assistant response accidentally duplicated several identifiers (`freshfresh_db`, `RRun`, and `printprint`), causing a first `NameError` and cascading undefined-variable errors. The learner recovered by querying with corrected names. Reinforced the practice of fixing the first error before interpreting later ones.

### Reusable Session Record

- Date / lesson:
- Prediction:
- Learner's change or experiment:
- Verification evidence:
- Explanation in the learner's words:
- Hint level needed:
- Remaining uncertainty:
- Next-session recall question:
- Exact next action:

---

# How to Use This Tracker

For each lesson:

1. Study the concept.
2. Implement the related feature yourself.
3. Test the feature.
4. Explain the feature without looking at your code.
5. Record what you learned.
6. Record what confused you.
7. Record one improvement you would make.

Do not mark a lesson complete simply because the code works.

A lesson is complete when you can answer:

- What problem does this solve?
- Why did I implement it this way?
- What alternatives could I have used?
- What can fail?
- How would I test it?
- How would this change at larger scale?

---

# Project Scope

## Initial Product Goal

Build a backend that allows runners to:

- Create and manage a runner profile.
- Record running activities.
- Retrieve individual runs.
- List historical runs.
- Calculate weekly running statistics.
- Prevent duplicate activity imports.
- Process derived analytics.
- Test the system thoroughly.

## Initial Technology Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest
- Docker
- Git and GitHub

## Possible Future Technologies

- Redis
- Celery or another background-job system
- AWS
- React and TypeScript
- Strava API
- Apple Health integrations
- CI/CD pipelines
- Monitoring and logging tools

---

# Learning Journey Overview

## Phase 1: Foundations

- Python backend fundamentals
- Project structure
- HTTP and REST APIs
- FastAPI routes
- Request and response models
- Validation
- Error handling

## Phase 2: Data Persistence

- Relational databases
- PostgreSQL
- SQLAlchemy
- Database sessions
- Models and relationships
- Alembic migrations
- Repository patterns

## Phase 3: Business Logic

- Service layers
- Derived metrics
- Pace calculations
- Weekly summaries
- Timezones
- Domain rules

## Phase 4: Reliability

- Idempotency
- Unique constraints
- Transactions
- Race conditions
- Retries
- Failure handling

## Phase 5: Testing

- Unit tests
- Integration tests
- Test databases
- Fixtures
- Mocking
- Edge cases

## Phase 6: Asynchronous Systems

- Background jobs
- Queues
- Workers
- Event-driven workflows
- Retry policies
- Dead-letter handling

## Phase 7: Production Readiness

- Authentication
- Authorization
- Logging
- Monitoring
- Security
- Docker
- Deployment
- CI/CD

## Phase 8: System Design and Interview Readiness

- Scaling the platform
- Activity ingestion
- Data modeling
- Caching
- Observability
- Technical storytelling
- Project deep dives

---

# Milestone 1: Project Setup and Backend Foundations

## Goal

Create a clean Python backend project and understand how a FastAPI application starts and handles requests.

## Features

- Create the project directory.
- Set up a virtual environment.
- Install FastAPI and the development server.
- Create the application entry point.
- Add a health-check endpoint.
- Run the server locally.
- Make a request to the endpoint.

## Concepts to Learn

### Python Virtual Environments

Understand:

- Why dependencies should be isolated.
- How a virtual environment differs from a global Python installation.
- How to activate and deactivate it.
- How dependencies are recorded.

Questions:

- What problem does a virtual environment solve?
- What happens when two projects require different library versions?
- What is the purpose of a lock file or requirements file?

### Application Entry Point

Understand:

- Where the application begins.
- How the FastAPI application object is created.
- How the development server finds the application.
- Why application startup should remain lightweight.

Questions:

- What does `app = FastAPI()` create?
- What happens when the server starts?
- What is the difference between the framework and the server?

### HTTP Basics

Understand:

- Requests and responses.
- HTTP methods.
- Status codes.
- Headers.
- JSON payloads.
- URLs and query parameters.

Questions:

- Why is a health endpoint usually a GET request?
- What does a `200 OK` response communicate?
- What is the difference between a path parameter and query parameter?

### Health-Check Endpoint

Example behavior:

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

Understand:

- Why production services expose health endpoints.
- The difference between liveness and readiness checks.
- Why a healthy process may still be unable to serve real traffic.

## Completion Checklist

- [x] Project runs locally.
- [x] Virtual environment is configured.
- [x] Dependencies are recorded.
- [x] `GET /health` returns a successful response.
- [x] I can explain how the request reaches the route handler.
- [x] I committed the setup to Git. (Verified in history: `a48e305`.)

## Lesson Notes

### What I learned

- Learned: Set up an isolated Python environment, create a FastAPI health endpoint, and test its status code and JSON response.

### What confused me

- Confused by: How assertions work, Python import paths, and how to interpret Pytest collection errors.

### What I would improve

- Improve: Add tests alongside every new endpoint and read tracebacks carefully before attempting fixes.

### Interview takeaway

Explain the complete lifecycle of a request to `GET /health`.

---

# Milestone 2: API Design and Request Validation

## Goal

Create the first endpoint for recording a running activity.

## Feature

```http
POST /runs
```

Example request:

```json
{
  "external_activity_id": "apple-watch-2026-07-13-001",
  "distance_meters": 8046,
  "duration_seconds": 2700,
  "elevation_gain_meters": 72,
  "average_heart_rate": 148,
  "started_at": "2026-07-13T06:15:00-07:00",
  "notes": "Easy morning run"
}
```

## Concepts to Learn

### REST API Design

Understand:

- Resources.
- Endpoints.
- HTTP verbs.
- Request bodies.
- Response bodies.
- Status codes.
- Naming conventions.

Questions:

- Why is the resource named `runs`?
- Why should creation use POST?
- What should the endpoint return after successful creation?
- When should an API return `201 Created`?

### Pydantic Models

Understand:

- Request schemas.
- Response schemas.
- Type validation.
- Optional fields.
- Default values.
- Field constraints.
- Serialization.

Questions:

- What happens when the user sends a string instead of a number?
- Why should request and database models remain separate?
- What is the difference between required and optional fields?

### Input Validation

Add rules such as:

- Distance must be greater than zero.
- Duration must be greater than zero.
- Elevation gain cannot be negative.
- Heart rate must fall within a reasonable range.
- Started time must be a valid timestamp.
- Notes should have a maximum length.

Understand:

- Why validation belongs at the system boundary.
- Why frontend validation is not sufficient.
- The difference between structural and business validation.

### Status Codes

Learn when to use:

- `200 OK`
- `201 Created`
- `400 Bad Request`
- `404 Not Found`
- `409 Conflict`
- `422 Unprocessable Entity`
- `500 Internal Server Error`

## Completion Checklist

- [x] `POST /runs` accepts valid data.
- [x] Invalid requests are rejected.
- [x] Response data follows a defined schema.
- [x] The endpoint returns an appropriate status code.
- [x] I understand FastAPI's automatic validation.
- [ ] I tested the endpoint manually.

## Lesson Notes

### What I learned

- Pydantic models define and validate the expected request structure.
- FastAPI converts valid JSON into typed Python objects before calling the route.
- Resource creation should return `201 Created`.
- Invalid request data produces a `422` validation response.
- Pytest assertions fail a test when actual behavior does not match the expected behavior.
- API tests follow Arrange, Act, Assert: prepare a payload, send the request, and verify the response.
- FastAPI validation errors identify the invalid request location and failed constraint.

### What confused me

- The difference between `400 Bad Request` and `422 Unprocessable Entity`.
- Why request schemas and database models should remain separate.
- How optional fields and default values affect validation.

### Validation rules I added

- Activity IDs must contain between 1 and 255 characters.
- Distance and duration must be greater than zero.
- Elevation cannot be negative.
- Heart rate must be between 30 and 250.
- Notes cannot exceed 1,000 characters.
- The starting timestamp must be a valid datetime.

### Interview takeaway

Explain why backend validation is required even when the frontend validates the same form.

---

# Milestone 3: Relational Databases and Persistence

## Goal

Persist running activities so that they survive application restarts.

## Features

- Connect to PostgreSQL.
- Create a `runs` table.
- Save new runs.
- Retrieve saved runs.
- Configure database sessions.

## Suggested Run Table

```text
runs
- id
- runner_id
- external_activity_id
- distance_meters
- duration_seconds
- elevation_gain_meters
- average_heart_rate
- started_at
- notes
- created_at
- updated_at
```

## Concepts to Learn

### Relational Databases

Understand:

- Tables.
- Rows.
- Columns.
- Primary keys.
- Foreign keys.
- Constraints.
- Indexes.
- Relationships.

Questions:

- Why does each run need a primary key?
- Why use a runner ID?
- Which fields should be nullable?
- Which fields should be indexed?

### PostgreSQL

Understand:

- Database server versus database.
- Schemas.
- Connections.
- SQL queries.
- Data types.
- Transactions.

Questions:

- Why use PostgreSQL instead of storing JSON files?
- What happens when many requests access the database?
- What does a connection pool do?

### SQLAlchemy

Understand:

- ORM models.
- Database engines.
- Sessions.
- Queries.
- Commits.
- Rollbacks.
- Object mapping.

Questions:

- What is an ORM?
- What is gained by using SQLAlchemy?
- What tradeoffs come with an ORM?
- What happens when `commit()` fails?

### Database Sessions

Understand:

- Session lifecycle.
- Request-scoped sessions.
- Commits.
- Rollbacks.
- Closing connections.

Questions:

- Why should sessions not remain open indefinitely?
- Why is rollback important?
- What happens when one request accidentally shares a session with another?

## Implementation Evidence — September 5, 2026

- [x] Configuration class is written in `app/config.py`.
- [x] Engine, session factory, and cleanup generator are written in `app/database.py`.
- [x] ORM model, constraints, and timestamp declarations are written in `app/models.py`.
- [ ] I can explain and demonstrate these components working together.

These code-level checks do not complete persistence. Use lessons 3A–3F near the top of this tracker; the runtime checklist below remains pending.

## Completion Checklist

- [x] PostgreSQL runs locally.
- [x] Application connects to PostgreSQL.
- [x] A run record was persisted and retrieved manually through SQLAlchemy sessions. API persistence remains in Lesson 3E.
- [ ] Database sessions are managed correctly.
- [ ] Application handles database failures.
- [ ] Data survives application restarts.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Database decisions

- Observed in code: integer primary key, globally unique external activity ID, nullable optional measurements/notes, named check constraints, and timezone-capable timestamp columns. Rationale and runtime verification remain to be recorded by the learner.
- 

### Interview takeaway

Walk through what happens from receiving `POST /runs` to committing the new record in PostgreSQL.

---

# Milestone 4: Database Migrations

## Goal

Manage database schema changes safely using Alembic.

## Features

- Initialize Alembic.
- Create the initial migration.
- Apply the migration.
- Add a new column through a later migration.
- Roll back a migration locally.

## Concepts to Learn

### Schema Migrations

Understand:

- Why database schemas change over time.
- Why manually editing production databases is risky.
- Upgrade and downgrade operations.
- Migration history.
- Backward compatibility.

Questions:

- Why should migrations be committed to Git?
- What happens if application code deploys before its required migration?
- When can a migration lock a table?
- Why are destructive migrations risky?

### Safe Migration Strategy

Learn patterns such as:

1. Add a nullable column.
2. Deploy code that writes both formats.
3. Backfill existing records.
4. Read from the new field.
5. Make the field required later.
6. Remove old behavior only after migration is complete.

## Completion Checklist

- [x] Alembic is configured.
- [x] Initial tables are created through a migration.
- [ ] I created and applied a second migration.
- [x] I understand the basic jobs of upgrade and downgrade commands.
- [ ] I can explain a safe production migration.

## Lesson Notes

### What I learned

- A SQLAlchemy model describes the intended table; it does not change PostgreSQL by itself.
- Alembic compares model metadata with the real database and generates a migration proposal.
- `upgrade()` moves the schema forward, while `downgrade()` describes how to reverse that change.
- Applying the migration created both `runs` and Alembic's `alembic_version` tracking table.

### What confused me

- The difference between the database URL and target metadata, and where each belongs in `alembic/env.py`. Resolved through a line-by-line walkthrough.

### Migration risks

- 

### Interview takeaway

Explain how you would add a required field to a table that already contains millions of rows.

---

# Milestone 5: Retrieving Runs and Pagination

## Goal

Allow users to retrieve historical running activities efficiently.

## Features

```http
GET /runs
GET /runs/{run_id}
```

Possible query parameters:

```http
GET /runs?limit=20&offset=0
GET /runs?start_date=2026-07-01&end_date=2026-07-31
GET /runs?sort=started_at&order=desc
```

## Concepts to Learn

### Resource Retrieval

Understand:

- List endpoints.
- Detail endpoints.
- Filtering.
- Sorting.
- Pagination.
- Empty responses.
- Missing resources.

### Offset Pagination

Understand:

- Limit and offset.
- Ordering.
- Performance tradeoffs.
- Missing or duplicate rows during changing datasets.

### Cursor Pagination

Understand:

- Stable ordering.
- Cursor values.
- Advantages for large datasets.
- Complexity compared with offset pagination.

Questions:

- When is offset pagination sufficient?
- Why must paginated results use deterministic ordering?
- What happens when new runs are inserted between page requests?

### Database Indexes

Consider indexes on:

- `runner_id`
- `started_at`
- `external_activity_id`
- Combined fields commonly used in filters

Questions:

- What makes a query slow?
- How does an index improve reads?
- What costs do indexes add to writes?

## Completion Checklist

- [ ] Individual runs can be retrieved.
- [ ] Missing runs return `404`.
- [ ] Run history supports pagination.
- [ ] Results have stable ordering.
- [ ] Date filtering works.
- [ ] I understand where indexes may be useful.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Pagination choice

- 

### Interview takeaway

Compare offset and cursor pagination for a user's activity feed.

---

# Milestone 6: Service Layer and Clean Architecture

## Goal

Separate HTTP concerns from business logic and database access.

## Target Architecture

```text
Route or Controller
        ↓
Service Layer
        ↓
Repository Layer
        ↓
Database
```

## Responsibilities

### Route Layer

Responsible for:

- HTTP request parsing.
- Authentication context.
- Calling service methods.
- Mapping results to HTTP responses.

Should not contain:

- Complex calculations.
- Repeated database logic.
- Large blocks of business rules.

### Service Layer

Responsible for:

- Business rules.
- Orchestrating operations.
- Calculations.
- Domain validation.
- Transaction boundaries.

### Repository Layer

Responsible for:

- Database queries.
- Persistence.
- Retrieval.
- Hiding ORM details when useful.

## Concepts to Learn

- Separation of concerns.
- Dependency injection.
- Coupling.
- Cohesion.
- Testability.
- Abstraction tradeoffs.

Questions:

- Why is putting all logic in route handlers a problem?
- When is a repository layer useful?
- When can too many abstractions make the system harder to understand?
- Which layer should calculate running pace?

## Completion Checklist

- [ ] Routes remain small.
- [ ] Business calculations live in services.
- [ ] Database access is organized consistently.
- [ ] Components can be tested independently.
- [ ] I can explain the reason for each layer.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Architecture tradeoffs

- 

### Interview takeaway

Explain how you decide whether logic belongs in a route, service, or repository.

---

# Milestone 7: Running Metrics and Domain Logic

## Goal

Implement meaningful calculations that belong to the running domain.

## Metrics

- Distance in miles.
- Average pace.
- Weekly mileage.
- Total duration.
- Longest run.
- Average heart rate.
- Elevation gain.
- Number of runs.

## Pace Calculation

Store:

- Distance in meters.
- Duration in seconds.

Derive:

```text
distance_miles = distance_meters / 1609.344
pace_seconds_per_mile = duration_seconds / distance_miles
```

## Concepts to Learn

### Source-of-Truth Data

Understand why raw measurements should usually be stored in consistent units.

Questions:

- Why store meters rather than formatted miles?
- Why store seconds rather than `"8:15"`?
- Should calculated pace be stored or derived?
- When is denormalization useful?

### Floating-Point Precision

Understand:

- Floating-point representation.
- Rounding.
- Display values versus stored values.
- Decimal types for domains requiring exactness.

Questions:

- How much precision does a running application require?
- Why would a payment system use decimals rather than floating point?
- Where should rounding occur?

### Domain Rules

Examples:

- A run cannot have zero distance.
- A run cannot have negative duration.
- Pace should not be trusted if GPS data is invalid.
- Treadmill and outdoor activities may have different data sources.

## Completion Checklist

- [ ] Pace calculation is correct.
- [ ] Unit conversion is consistent.
- [ ] Domain calculations are tested.
- [ ] Display rounding is separate from stored data.
- [ ] Edge cases are defined.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Domain decisions

- 

### Interview takeaway

Explain why raw data and derived metrics should be modeled separately.

---

# Milestone 8: Weekly Analytics and Timezones

## Goal

Calculate weekly running summaries correctly.

## Feature

```http
GET /stats/weekly
```

Example response:

```json
{
  "week_start": "2026-07-13",
  "week_end": "2026-07-19",
  "total_runs": 4,
  "total_distance_miles": 21.4,
  "total_duration_seconds": 10820,
  "average_pace_seconds_per_mile": 505,
  "longest_run_miles": 8.2
}
```

## Concepts to Learn

### Aggregate Queries

Understand:

- Count.
- Sum.
- Average.
- Minimum and maximum.
- Grouping.
- Filtering by time range.

### Weighted Average Pace

Correct weekly pace:

```text
total_duration / total_distance
```

Potentially misleading approach:

```text
average of each individual run's pace
```

Questions:

- Why are these calculations different?
- Which result better reflects weekly pace?
- When is a weighted average needed?

### Timezones

Understand:

- UTC.
- Local time.
- Timezone-aware datetimes.
- Daylight saving time.
- Week boundaries.
- User preferences.

Questions:

- Which timezone determines the user's week?
- How should timestamps be stored?
- What happens to a run at 11:30 p.m. while the user travels?
- Should weeks begin Sunday or Monday?

## Completion Checklist

- [ ] Weekly totals are accurate.
- [ ] Empty weeks return sensible results.
- [ ] Week boundaries are clearly defined.
- [ ] Timezone-aware timestamps are used.
- [ ] Aggregate calculations have tests.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Timezone policy

- 

### Interview takeaway

Explain how timezone choices can create incorrect analytics.

---

# Milestone 9: Idempotency and Duplicate Protection

## Goal

Prevent the same external activity from being stored multiple times.

## Scenario

A watch, mobile app, or integration retries the same upload because it did not receive a response.

Without protection:

```text
One real run → multiple database records
```

## Design

Use a unique combination such as:

```text
runner_id + external_activity_id
```

## Concepts to Learn

### Idempotency

An operation is idempotent when repeating it does not produce additional unintended effects.

Questions:

- Is GET naturally idempotent?
- Is POST naturally idempotent?
- How can POST be made safe for retries?
- Should duplicate creation return the original resource or a conflict?

### Database Constraints

Understand:

- Unique constraints.
- Composite constraints.
- Why application checks alone are insufficient.
- Concurrency and race conditions.

### Race Condition Example

Two requests arrive simultaneously:

1. Request A checks for an existing run.
2. Request B checks for an existing run.
3. Neither finds one.
4. Both attempt insertion.

A database unique constraint protects against this.

## Completion Checklist

- [ ] Duplicate imports do not create additional records.
- [ ] Database uniqueness is enforced.
- [ ] Concurrent duplicate behavior is considered.
- [ ] API response behavior is documented.
- [ ] Duplicate scenarios are tested.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Duplicate-response policy

- 

### Interview takeaway

Explain why a database constraint is still necessary when the application checks for duplicates first.

---

# Milestone 10: Transactions and Consistency

## Goal

Ensure related database changes succeed or fail together.

## Example Scenario

Creating a run may involve:

- Saving the raw activity.
- Updating weekly totals.
- Recording an import event.

These operations may need atomic behavior.

## Concepts to Learn

### Database Transactions

Understand:

- Begin.
- Commit.
- Rollback.
- Atomicity.
- Consistency.
- Isolation.
- Durability.

### ACID

Be able to explain:

- Atomicity
- Consistency
- Isolation
- Durability

### Isolation and Concurrency

Understand at a high level:

- Dirty reads.
- Non-repeatable reads.
- Phantom reads.
- Lost updates.
- Row locks.

Questions:

- What happens when the database fails halfway through an operation?
- Which updates must happen atomically?
- When should work occur outside the transaction?
- Why should external network calls generally not remain inside long database transactions?

## Completion Checklist

- [ ] Multi-step database operations use appropriate transactions.
- [ ] Failures cause rollback.
- [ ] Transaction boundaries are deliberate.
- [ ] I understand basic isolation concerns.
- [ ] Tests cover partial-failure behavior.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Transaction boundaries

- 

### Interview takeaway

Explain how you would prevent partially saved data during a multi-step operation.

---

# Milestone 11: Error Handling

## Goal

Return consistent, useful errors without exposing internal details.

## Error Categories

- Validation errors.
- Missing resources.
- Duplicate resources.
- Unauthorized access.
- Database failures.
- External service failures.
- Unexpected application errors.

## Concepts to Learn

### Domain Errors

Examples:

- `RunNotFound`
- `DuplicateRun`
- `InvalidRunData`
- `UnauthorizedRunnerAccess`

### Error Mapping

Example:

```text
Domain error
    ↓
HTTP exception handler
    ↓
Consistent JSON response
```

Example response:

```json
{
  "error": {
    "code": "duplicate_run",
    "message": "This activity has already been imported."
  }
}
```

### Security

Do not expose:

- Stack traces.
- Database credentials.
- SQL queries containing sensitive values.
- Internal infrastructure details.

## Completion Checklist

- [ ] Errors follow a consistent format.
- [ ] Expected domain failures have clear status codes.
- [ ] Unexpected failures are logged.
- [ ] Internal details are not exposed.
- [ ] Error paths have tests.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Error response standard

- 

### Interview takeaway

Explain the difference between an expected domain error and an unexpected server error.

---

# Milestone 12: Testing Strategy

## Goal

Build confidence that the backend behaves correctly and remains maintainable.

## Testing Layers

### Unit Tests

Test isolated logic such as:

- Pace calculations.
- Date boundaries.
- Validation rules.
- Personal-record comparison.
- Service-layer decisions.

### Integration Tests

Test interactions involving:

- API routes.
- Database.
- Serialization.
- Migrations.
- Dependency wiring.

### End-to-End Tests

Test a realistic workflow:

1. Create a runner.
2. Record a run.
3. Retrieve the run.
4. View weekly statistics.

## Concepts to Learn

### Pytest

Understand:

- Test discovery.
- Assertions.
- Fixtures.
- Parametrized tests.
- Setup and teardown.
- Exception testing.

### Test Fixtures

Create reusable fixtures for:

- Test application.
- Test database.
- Database session.
- Runner.
- Sample run data.
- Authenticated client later.

### Test Isolation

Understand:

- Why tests should not depend on execution order.
- Why each test requires predictable state.
- Rollback strategies.
- Separate test databases.

### Mocking

Mock only where appropriate:

- External APIs.
- Time.
- Queue publishers.
- Email or notification systems.

Avoid mocking the behavior you actually need to verify.

## Required Test Cases

- [ ] Create and persist a valid run. (Current request/response test passes; persistence is not covered.)
- [x] Reject zero distance. (Existing test passes; other invalid-distance boundaries remain to be tested.)
- [ ] Reject invalid duration.
- [ ] Reject invalid heart rate.
- [ ] Retrieve an existing run.
- [ ] Return `404` for a missing run.
- [ ] Prevent duplicate imports.
- [ ] Calculate weekly totals.
- [ ] Handle empty weeks.
- [ ] Apply pagination correctly.
- [ ] Handle timezone boundaries.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Testing philosophy

- 

### Interview takeaway

Explain the difference between a unit test and an integration test using this project.

---

# Milestone 13: Authentication and Authorization

## Goal

Ensure runners can access only their own data.

## Features

- Register a runner.
- Log in.
- Authenticate API requests.
- Associate runs with the authenticated runner.
- Prevent access to another runner's activities.

## Concepts to Learn

### Authentication

Answers:

> Who are you?

### Authorization

Answers:

> What are you allowed to do?

### Password Security

Understand:

- Password hashing.
- Salts.
- Why passwords must never be stored directly.
- Secure reset workflows.

### Tokens and Sessions

Compare:

- Cookie-based sessions.
- JWT access tokens.
- Refresh tokens.
- Token expiration.
- Revocation tradeoffs.

### Object-Level Authorization

Every request for a run must confirm:

```text
run.runner_id == authenticated_runner.id
```

## Completion Checklist

- [ ] Users can authenticate.
- [ ] Passwords are securely hashed.
- [ ] Runs belong to a runner.
- [ ] Users cannot retrieve another user's data.
- [ ] Authorization failures have tests.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Authentication choice

- 

### Interview takeaway

Explain why checking that a user is logged in is not enough to protect individual resources.

---

# Milestone 14: Background Jobs and Asynchronous Processing

## Goal

Move slow or nonessential processing outside the main request.

## Example Workflow

```text
Client uploads run
        ↓
API validates and stores raw run
        ↓
API publishes analytics job
        ↓
API returns response
        ↓
Worker calculates derived metrics
```

## Possible Background Tasks

- Personal-record detection.
- Training-load calculation.
- Route processing.
- Weekly summary updates.
- Notifications.
- Import synchronization.

## Concepts to Learn

### Synchronous vs. Asynchronous Work

Synchronous:

- Caller waits for completion.
- Simpler result handling.
- Longer response time.

Asynchronous:

- Caller receives a response earlier.
- Work is completed separately.
- Requires job status and failure handling.

### Queues

Understand:

- Producer.
- Queue.
- Consumer or worker.
- Acknowledgment.
- Visibility timeout.
- Retries.
- Dead-letter queue.

### At-Least-Once Delivery

Many queue systems may deliver the same job more than once.

Therefore:

- Jobs should be idempotent.
- Results should tolerate duplicates.
- Database constraints may still be necessary.

## Completion Checklist

- [ ] Run creation publishes a background job.
- [ ] Worker processes the job.
- [ ] Repeated delivery is safe.
- [ ] Failures are retried.
- [ ] Permanently failing jobs are visible.
- [ ] Job processing is tested.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Retry policy

- 

### Interview takeaway

Explain why background workers must assume a message can be delivered more than once.

---

# Milestone 15: External Activity Imports and Webhooks

## Goal

Design ingestion from a service such as Strava.

## Possible Flow

```text
Strava sends webhook
        ↓
Webhook endpoint verifies request
        ↓
Event is recorded
        ↓
Background job fetches activity
        ↓
Activity is normalized
        ↓
Run is created or updated
```

## Concepts to Learn

### Webhooks

Understand:

- Event notifications.
- Signature verification.
- Duplicate delivery.
- Out-of-order delivery.
- Retry behavior.
- Fast acknowledgment.

### Import Normalization

External providers may use different:

- Field names.
- Units.
- Activity types.
- Time formats.
- IDs.
- Error formats.

Create a normalized internal model rather than coupling the system directly to one provider.

### Provider Reliability

Plan for:

- Rate limits.
- Timeouts.
- Temporary outages.
- Invalid tokens.
- Partial data.
- Deleted activities.

## Completion Checklist

- [ ] Webhook endpoint validates requests.
- [ ] Events are recorded safely.
- [ ] Processing happens asynchronously.
- [ ] Duplicate events are tolerated.
- [ ] Provider data is normalized.
- [ ] Import failures are observable.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Provider abstraction

- 

### Interview takeaway

Explain how you would handle duplicate and out-of-order webhook events.

---

# Milestone 16: Logging and Observability

## Goal

Make production behavior understandable when something goes wrong.

## Observability Areas

### Logs

Include:

- Request ID.
- Runner ID when appropriate.
- Operation name.
- Error category.
- Duration.
- Relevant identifiers.

Avoid:

- Passwords.
- Tokens.
- Sensitive health information unless essential and protected.
- Full request payloads by default.

### Metrics

Track:

- Request count.
- Error rate.
- Latency.
- Runs created.
- Duplicate imports.
- Failed jobs.
- Queue depth.
- Database connection usage.

### Tracing

Understand how tracing follows a request across:

```text
API → database → queue → worker → external service
```

### Alerts

Examples:

- Elevated API error rate.
- Worker failures.
- Queue backlog.
- Database connection exhaustion.
- External provider failures.

## Completion Checklist

- [ ] Logs are structured.
- [ ] Requests use correlation IDs.
- [ ] Important operations emit metrics.
- [ ] Failures can be traced.
- [ ] Sensitive values are not logged.
- [ ] Basic alert conditions are defined.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Useful metrics

- 

### Interview takeaway

Describe how you would investigate a sudden increase in failed run imports.

---

# Milestone 17: Performance and Caching

## Goal

Understand where performance problems originate and how to address them.

## Concepts to Learn

### Query Performance

Review:

- N+1 queries.
- Missing indexes.
- Large result sets.
- Expensive aggregates.
- Unnecessary columns.
- Database query plans.

### Caching

Potential cache targets:

- Weekly summaries.
- Runner profile.
- Common leaderboard queries.
- Static configuration.

Understand:

- Cache keys.
- Expiration.
- Invalidation.
- Cache misses.
- Stale data.
- Cache-aside pattern.

### Precomputed Analytics

Compare:

1. Calculate weekly stats on every request.
2. Cache calculated results.
3. Maintain a summary table.
4. Update summaries asynchronously.

Questions:

- When does dynamic calculation stop scaling?
- How fresh must statistics be?
- What happens when a run is edited or deleted?
- How is cached data invalidated?

## Completion Checklist

- [ ] Slow-query risks are identified.
- [ ] Appropriate indexes are added.
- [ ] One analytics response can be cached.
- [ ] Cache invalidation is defined.
- [ ] Performance is measured before optimization.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Optimization decisions

- 

### Interview takeaway

Explain how you would speed up weekly analytics for a platform with millions of runs.

---

# Milestone 18: Security Fundamentals

## Goal

Protect users, credentials, and application infrastructure.

## Topics

- Input validation.
- Authentication.
- Authorization.
- Password hashing.
- Secret management.
- SQL injection.
- Rate limiting.
- CORS.
- HTTPS.
- Dependency vulnerabilities.
- Secure logging.
- Data minimization.

## Concepts to Learn

### SQL Injection

Understand why parameterized ORM queries are safer than constructing SQL strings manually.

### Secrets

Never commit:

- Database passwords.
- API tokens.
- Signing keys.
- Cloud credentials.

Use environment variables or a secret manager.

### Rate Limiting

Protect:

- Login endpoints.
- Webhook endpoints.
- Expensive analytics endpoints.
- Public APIs.

### Data Privacy

Running data can reveal:

- Location.
- Routines.
- Health-related metrics.
- Travel.
- Home and work patterns.

Consider privacy even if the learning project uses sample data.

## Completion Checklist

- [ ] Secrets are not committed.
- [ ] Environment configuration is documented.
- [ ] Authorization is enforced.
- [ ] Sensitive values are not logged.
- [ ] Rate-limiting strategy is understood.
- [ ] Security risks are documented.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Security risks

- 

### Interview takeaway

Identify the most sensitive data in a running platform and explain how you would protect it.

---

# Milestone 19: Docker and Local Development

## Goal

Make the application reproducible across development environments.

## Features

- Dockerfile for the API.
- Docker Compose configuration.
- PostgreSQL container.
- Environment configuration.
- Startup instructions.

## Concepts to Learn

### Containers

Understand:

- Images.
- Containers.
- Layers.
- Ports.
- Volumes.
- Networks.
- Environment variables.

### Docker Compose

Use Compose to run:

```text
API
PostgreSQL
Redis
Worker
```

### Persistence

Understand:

- Container filesystem.
- Database volumes.
- What happens when containers are deleted.
- Why source code may be mounted during development.

## Completion Checklist

- [ ] API runs in Docker.
- [ ] Database runs in Docker.
- [ ] Containers communicate correctly.
- [ ] Database data persists.
- [ ] Setup instructions work from a clean environment.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Container decisions

- 

### Interview takeaway

Explain the difference between a Docker image and a running container.

---

# Milestone 20: CI/CD

## Goal

Automatically validate code changes and prepare the application for safe deployment.

## Pipeline Stages

```text
Pull request
    ↓
Install dependencies
    ↓
Lint and type check
    ↓
Run tests
    ↓
Build image
    ↓
Apply deployment process
```

## Concepts to Learn

### Continuous Integration

Automatically validates every code change.

Potential checks:

- Formatting.
- Linting.
- Type checking.
- Unit tests.
- Integration tests.
- Migration validation.
- Docker build.

### Continuous Delivery and Deployment

Understand:

- Artifact creation.
- Environment promotion.
- Deployment approvals.
- Rollback.
- Feature flags.
- Database migration ordering.

## Completion Checklist

- [ ] Pull requests run automated checks.
- [ ] Failing tests block merging.
- [ ] Docker image builds in CI.
- [ ] Deployment steps are documented.
- [ ] Rollback strategy is understood.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Pipeline decisions

- 

### Interview takeaway

Explain what should happen between opening a pull request and deploying code to production.

---

# Milestone 21: Deployment and Cloud Architecture

## Goal

Understand how the application would operate in a cloud environment.

## Example AWS Architecture

```text
Client
  ↓
Load Balancer
  ↓
Containerized FastAPI service
  ↓
PostgreSQL database
  ↓
Queue
  ↓
Background workers
```

Additional services:

- Object storage for route data.
- Redis for caching.
- Secret management.
- Centralized logs.
- Metrics and alerts.
- CDN for a future frontend.

## AWS Concepts to Learn

- ECS or another container runtime.
- RDS.
- S3.
- SQS.
- CloudWatch.
- IAM.
- Secrets Manager.
- Load balancers.
- Auto scaling.
- VPC basics.

## Questions

- Where does the API run?
- Where is PostgreSQL hosted?
- How are secrets supplied?
- How do workers receive jobs?
- How is traffic distributed?
- How does the system scale?
- How are deployments rolled back?

## Completion Checklist

- [ ] Production architecture is diagrammed.
- [ ] Each cloud component has a clear responsibility.
- [ ] Network boundaries are understood at a high level.
- [ ] Secrets and permissions are considered.
- [ ] Scaling and rollback strategies are documented.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Cloud architecture

- 

### Interview takeaway

Design a deployment architecture for the API, database, queue, and workers.

---

# Milestone 22: System Design at Scale

## Prompt

Design a running platform that supports one million users importing activities from watches and external providers.

## Functional Requirements

- Record runs.
- Retrieve run history.
- Calculate weekly statistics.
- Import activities.
- Prevent duplicates.
- Detect personal records.
- Support background processing.

## Nonfunctional Requirements

- Reliable ingestion.
- Low-latency reads.
- Eventual consistency for analytics.
- Secure user data.
- Horizontal scalability.
- Observability.
- Fault tolerance.

## Areas to Cover

### API Layer

- Authentication.
- Rate limiting.
- Request validation.
- Pagination.
- Versioning.

### Data Storage

- Relational database.
- Indexes.
- Read replicas.
- Partitioning possibilities.
- Archival strategy.

### Activity Ingestion

- Provider webhooks.
- Import queues.
- Idempotent workers.
- Retry policies.
- Dead-letter queues.

### Analytics

- Dynamic queries.
- Cache.
- Precomputed summaries.
- Event-driven updates.

### Reliability

- Duplicate events.
- Lost messages.
- Worker failures.
- Provider outages.
- Database failures.

### Observability

- Request tracing.
- Import success rate.
- Queue depth.
- Processing latency.
- Error-rate alerts.

## Completion Checklist

- [ ] Requirements are clarified before designing.
- [ ] APIs are defined.
- [ ] Data model is explained.
- [ ] Major components are diagrammed.
- [ ] Failure modes are discussed.
- [ ] Tradeoffs are explicit.
- [ ] Scaling is based on actual bottlenecks.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Major tradeoffs

- 

### Interview takeaway

Deliver a 30-minute system-design explanation without relying heavily on notes.

---

# Engineering Habits Tracker

## Before Writing Code

- [ ] I understand the user problem.
- [ ] I can describe the expected behavior.
- [ ] I have identified edge cases.
- [ ] I know what should be tested.
- [ ] I understand which layer should own the logic.

## While Writing Code

- [ ] I am writing the implementation myself.
- [ ] I understand every imported dependency.
- [ ] I am keeping functions focused.
- [ ] I am naming variables clearly.
- [ ] I am handling expected failure cases.
- [ ] I am avoiding premature abstraction.

## After Writing Code

- [ ] I tested the happy path.
- [ ] I tested at least one failure path.
- [ ] I read the error messages carefully.
- [ ] I reviewed the diff.
- [ ] I removed unnecessary code.
- [ ] I committed the change with a meaningful message.

---

# AI-Assisted Learning Guidelines

Use an assistant as a mentor, reviewer, and debugger. These are learning preferences documented for this project; the learner’s current request determines the scope of a session.

## Good Uses

Ask the assistant to:

- Explain a concept.
- Review code you wrote.
- Ask you guiding questions.
- Identify edge cases.
- Explain an error message.
- Compare design alternatives.
- Suggest tests.
- Review a Git diff.
- Challenge your architecture.

## Avoid

Avoid asking the assistant to:

- Generate the entire application.
- Replace complete files without explanation.
- Make large architectural changes you do not understand.
- Add dependencies without explaining why.
- Solve every bug before you investigate it.
- Produce code you cannot explain.

## Session Prompt

```text
Act as my backend engineering mentor.

Do not build the project for me. Give me one small task at a time. Before showing code, explain the concept and ask me how I think it should work.

Review code that I write for:
- correctness
- architecture
- edge cases
- testing
- maintainability

When I encounter an error:
1. Ask me what I expected.
2. Ask me what actually happened.
3. Help me inspect the logs and traceback.
4. Give me hints before giving me the solution.

At the end of each task, ask me to explain what I built in my own words.
```

---

# Debugging Framework

When something fails, record:

## Expected Behavior

- 

## Actual Behavior

- 

## Error Message

```text

```

## Relevant Logs

```text

```

## My Initial Hypothesis

- 

## Investigation Steps

1. 
2. 
3. 

## Root Cause

- 

## Fix

- 

## Prevention

- 

## What I Learned

- 

---

# Architecture Decision Record Template

Use this whenever you make a meaningful technical choice.

## Decision

- 

## Context

- 

## Options Considered

1. 
2. 
3. 

## Chosen Option

- 

## Why

- 

## Tradeoffs

- 

## Future Reconsideration Trigger

- 

---

# Weekly Reflection Template

## Week

- Dates:
- Main milestone:

## What I Built

- 

## Concepts I Learned

- 

## Bugs I Solved

- 

## Decisions I Made

- 

## What Remains Unclear

- 

## Most Important Lesson

- 

## One Thing I Can Explain Better Now

- 

## Next Week's Priority

- 

## Confidence Ratings

Rate each area from 1 to 5.

| Area | Rating | Notes |
|---|---:|---|
| Python |  |  |
| FastAPI |  |  |
| HTTP and REST |  |  |
| Validation |  |  |
| PostgreSQL |  |  |
| SQLAlchemy |  |  |
| Migrations |  |  |
| Testing |  |  |
| Architecture |  |  |
| Reliability |  |  |
| Async processing |  |  |
| System design |  |  |
| Interview explanation |  |  |

---

# Daily Study Log

## Date

- 

## Time Spent

- 

## Goal

- 

## What I Completed

- 

## What I Learned

- 

## What Confused Me

- 

## Errors or Bugs

- 

## Questions to Revisit

- 

## Next Action

- 

---

# Interview Story Builder

## Project Summary

Prepare a concise answer to:

> Tell me about the running backend you built.

### Problem

- 

### Users

- 

### Core Features

- 

### Technology Choices

- 

### My Ownership

- 

### Hardest Technical Problem

- 

### Reliability Challenge

- 

### Testing Strategy

- 

### Tradeoff

- 

### Result

- 

### What I Would Build Next

- 

---

# Project Deep-Dive Questions

You should eventually answer each question clearly.

## Product

- What problem does the platform solve?
- Who is the primary user?
- What is included in the MVP?
- What did you deliberately leave out?
- How did you prioritize features?

## Backend

- How does a request flow through the system?
- How is data validated?
- How is business logic organized?
- How are database sessions managed?
- How are failures handled?
- How are duplicate uploads prevented?

## Database

- Why did you choose PostgreSQL?
- How are runners and runs related?
- Which constraints protect data integrity?
- Which indexes are needed?
- How are migrations managed?

## Reliability

- What happens when the client retries?
- What happens when two duplicate requests arrive simultaneously?
- What happens when a worker crashes?
- How are failed jobs recovered?
- What operations require transactions?

## Testing

- Which logic is unit tested?
- Which behavior requires integration tests?
- How is the test database isolated?
- What edge cases were most important?

## Scale

- What becomes a bottleneck first?
- How would weekly analytics scale?
- When would you add caching?
- How would you process millions of imports?
- How would you partition or archive old data?

## Security

- How are passwords protected?
- How is authorization enforced?
- What data is sensitive?
- How are secrets managed?
- What should never appear in logs?

## Operations

- What metrics would you monitor?
- How would you debug an import outage?
- How would you deploy safely?
- How would you roll back?
- How would you handle a dangerous migration?

---

# Final Project Success Criteria

The project is successful when you can independently:

- [ ] Set up a backend project.
- [ ] Design REST endpoints.
- [ ] Validate API requests.
- [ ] Model relational data.
- [ ] Use migrations.
- [ ] Persist and retrieve records.
- [ ] Implement domain calculations.
- [ ] Handle timezones.
- [ ] Prevent duplicate writes.
- [ ] Use database transactions.
- [ ] Structure services cleanly.
- [ ] Write unit and integration tests.
- [ ] Add authentication and authorization.
- [ ] Implement background jobs.
- [ ] Handle webhook events.
- [ ] Add meaningful logs and metrics.
- [ ] Containerize the application.
- [ ] Configure CI checks.
- [ ] Explain a cloud deployment.
- [ ] Design the platform at scale.
- [ ] Present the project confidently in an interview.

---

# Final Reflection

## What I believed about backend engineering before this project

- 

## What I understand now

- 

## The most difficult concept

- 

## The most valuable engineering habit I developed

- 

## The feature I am most proud of

- 

## A mistake that improved my understanding

- 

## How this project changed the way I think about full-stack development

- 

## How I would rebuild the project differently

- 

## My next backend project

-
