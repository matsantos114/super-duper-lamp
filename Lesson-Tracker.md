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
- [ ] I committed the setup to Git.

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

- [ ] `POST /runs` accepts valid data.
- [ ] Invalid requests are rejected.
- [ ] Response data follows a defined schema.
- [ ] The endpoint returns an appropriate status code.
- [ ] I understand FastAPI's automatic validation.
- [ ] I tested the endpoint manually.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Validation rules I added

- 

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

## Completion Checklist

- [ ] PostgreSQL runs locally.
- [ ] Application connects to PostgreSQL.
- [ ] Run records are persisted.
- [ ] Database sessions are managed correctly.
- [ ] Application handles database failures.
- [ ] Data survives application restarts.

## Lesson Notes

### What I learned

- 

### What confused me

- 

### Database decisions

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

- [ ] Alembic is configured.
- [ ] Initial tables are created through a migration.
- [ ] I created and applied a second migration.
- [ ] I understand upgrade and downgrade commands.
- [ ] I can explain a safe production migration.

## Lesson Notes

### What I learned

- 

### What confused me

- 

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

- [ ] Create a valid run.
- [ ] Reject invalid distance.
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

# Cursor Learning Rules

Use Cursor as a mentor, reviewer, and debugger—not as an automatic project generator.

## Good Uses

Ask Cursor to:

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

Do not ask Cursor to:

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