# Backend Learning Map

This guide is a map of the backend concepts encountered while building the running application.

The goal is not to memorize definitions. For each concept, you should eventually be able to answer:

1. What is it?
2. Why does it exist?
3. Where does it appear in this project?
4. What does it interact with?
5. What could go wrong if it were missing or used incorrectly?

A concept is understood when you can follow it through the application and reason about its behavior.

## Priority Key

> [!IMPORTANT]
> **Core:** Explain this without notes at the current stage.

> [!NOTE]
> **Supporting:** Understand its general job and recognize it in the code. Deeper knowledge can come later.

> [!TIP]
> **Recognition:** Know why it appeared. Do not spend time memorizing its API yet.

## The Mental Model

Most concepts in this project fit somewhere in this flow:

```text
Client
  ↓
HTTP request
  ↓
FastAPI route
  ↓
Pydantic validation
  ↓
Application logic
  ↓
SQLAlchemy session
  ↓
Transaction
  ↓
PostgreSQL
  ↓
HTTP response
```

The application does not use every step yet.

### Current `POST /runs` flow

```text
Client
  ↓
POST /runs
  ↓
FastAPI
  ↓
RunCreate validation
  ↓
create_run()
  ↓
return validated data
```

### Flow after persistence is implemented

```text
Client
  ↓
POST /runs
  ↓
FastAPI route
  ↓
RunCreate validation
  ↓
Run ORM object
  ↓
SQLAlchemy session
  ↓
Transaction
  ↓
PostgreSQL
  ↓
runs table
  ↓
Commit
  ↓
HTTP response
```

When you encounter a new term, first ask: **Where does it fit in this flow?**

---

# 1. Python and Project Foundation

These concepts make the application reproducible and allow its files to work together.

## Dependency — Supporting

**Simple meaning:** Code written by somebody else that this project uses.

**Why it exists:** It lets the project use established tools instead of rebuilding a web framework, database driver, and test runner.

**In this project:** `pyproject.toml` records FastAPI, Pydantic, SQLAlchemy, Psycopg, Alembic, Uvicorn, and Pytest.

**Without it:** The imported package would be unavailable and the application could not start or perform that package's job.

### Check yourself

1. What is a dependency?
2. Where are this project's dependencies recorded?
3. Why should a new developer not install them from memory?

## Virtual Environment — Supporting

**Simple meaning:** A private area containing the Python packages installed for one project.

**Why it exists:** Two projects may require different versions of the same dependency.

**In this project:** `.venv` contains this project's installed packages.

**Important distinction:** A virtual environment isolates installed packages. It does not isolate the PostgreSQL database.

## Lock File — Supporting

**Simple meaning:** A record of the exact dependency versions selected for the project.

**Why it exists:** It helps different machines install the same versions and reduces “works on my machine” differences.

**In this project:** `uv.lock` records the resolved dependency versions.

## Import — Supporting

**Simple meaning:** Make a name from another module available in the current Python file.

**Where it fits:** Imports assemble the pieces used throughout the application flow.

**In this project:**

```python
from app.schemas import RunCreate
```

```text
app.schemas       → module containing the name
RunCreate         → imported name
app.main          → module that uses it
```

**Important distinction:** Importing an ORM model registers Python metadata. It does not create its PostgreSQL table.

## Type Annotation — Supporting

**Simple meaning:** A label describing the kind of value expected as input or output.

**Why it exists:** It communicates intent and gives frameworks and development tools useful information.

**In this project:**

```python
def create_run(run: RunCreate) -> RunCreate:
    return run
```

```text
run: RunCreate   → expected input type
-> RunCreate     → declared return type
```

---

# 2. An HTTP Request Arrives

This is the boundary between a client and the backend.

## HTTP Request — Core

**Simple meaning:** A message asking a server to perform an action.

**Why it exists:** A client and server need an agreed format for communicating across a network.

**Where it fits:**

`Client → HTTP request → FastAPI`

**In this project:** A request to `POST /runs` contains JSON describing a run.

**Without it:** The client has no standard way to tell the backend what it wants.

### Check yourself

1. What is an HTTP request?
2. What method, path, and body does the run-creation request use?
3. What should happen when the body contains a distance of zero?

## API — Core

**Simple meaning:** The agreement describing how software can ask another piece of software to perform work.

**Why it exists:** Clients need predictable paths, inputs, outputs, and error behavior.

**In this project:** The current API includes `GET /health` and `POST /runs`.

## JSON — Supporting

**Simple meaning:** A text format for sending structured values such as objects, strings, numbers, booleans, lists, and null.

**Where it fits:**

`HTTP request body → JSON → Pydantic validation`

**In this project:** The client sends run fields as JSON; FastAPI also sends JSON responses.

## GET and POST — Core

**Simple meaning:** HTTP methods communicate the kind of action being requested.

**Why they exist:** The same URL can support different behaviors with clear expectations.

**In this project:**

- `GET /health` retrieves health information.
- `POST /runs` submits a run for creation.

**Important distinction:** `GET /runs` and `POST /runs` would be different endpoints even though they share `/runs`.

### Check yourself

1. Which method normally retrieves information?
2. Which method is used here to create a run?
3. Why would using GET to create a run be misleading and unsafe for retries or caching?

---

# 3. FastAPI Selects a Route

FastAPI decides which Python function should receive the request.

## FastAPI — Core

**Simple meaning:** The web framework connecting HTTP requests to Python code and Python results to HTTP responses.

**Why it exists:** It handles routing, request parsing, validation integration, and response conversion so the application can focus on its behavior.

**Where it fits:**

`HTTP request → FastAPI → route function`

**In this project:**

```python
app = FastAPI()
```

The `app` object stores the registered routes.

## Uvicorn — Supporting

**Simple meaning:** The server process that listens for network requests and passes them to the FastAPI application.

**Why it exists:** A FastAPI application describes behavior; a server must run it and communicate over the network.

**Important distinction:** FastAPI is the application framework. Uvicorn is the server running the application.

## Route and Route Decorator — Core

**Simple meaning:** A route joins an HTTP method and path to a Python function. The decorator registers that connection.

**Why it exists:** FastAPI must know which function handles each kind of request.

**Where it fits:**

`POST /runs → route matching → create_run()`

**In this project:**

```python
@app.post("/runs", status_code=status.HTTP_201_CREATED)
def create_run(run: RunCreate) -> RunCreate:
    return run
```

```text
@app.post(...)       → route decorator
POST                 → HTTP method
"/runs"              → URL path
run: RunCreate       → validated request-body input
create_run()         → route function
return run           → current response value
```

**Without the decorator:** FastAPI would not know that `POST /runs` should call `create_run()`.

### Check yourself

1. What is a route?
2. Which function handles `POST /runs`?
3. If the decorator changed to `@app.get("/runs")`, what client behavior would change?

---

# 4. Pydantic Validates the Data

Validation occurs before `create_run()` receives the request-body object.

## Request Schema — Core

**Simple meaning:** A description of the data an API accepts and the rules it must follow.

**Why it exists:** Data arriving from outside the backend cannot be trusted automatically.

**Where it fits:**

`JSON body → RunCreate schema → route function`

**In this project:**

```python
class RunCreate(BaseModel):
    external_activity_id: str = Field(min_length=1, max_length=255)
    distance_meters: int = Field(gt=0)
    duration_seconds: int = Field(gt=0)
    started_at: datetime
```

```text
BaseModel                → Pydantic model behavior
distance_meters: int     → expected type
Field(gt=0)              → value must be greater than zero
started_at: datetime     → text must be convertible to a datetime
```

**Important distinction:** A request schema protects the API boundary. An ORM model maps application objects to database rows.

## Validation — Core

**Simple meaning:** Check that incoming data has the required shape, types, and allowed values.

**Why it exists:** Invalid data should be rejected before application or database work depends on it.

**In this project:** Distance and duration must be positive, heart rate has a range, and notes have a maximum length.

**Without it:** Bad values could reach business logic or be stored, leading to incorrect calculations and harder failures.

### Check yourself

1. What is validation?
2. Which class validates a new run?
3. Why must the backend validate input even if a frontend form already does so?

## Required, Optional, and Constraint — Supporting

**Simple meaning:**

- A required field must be provided.
- An optional field may be omitted.
- A constraint limits which provided values are accepted.

**In this project:**

```python
distance_meters: int = Field(gt=0)             # required and constrained
notes: str | None = Field(default=None, max_length=1000)  # optional
```

## Pydantic — Supporting

**Simple meaning:** The library used here to turn incoming values into typed Python objects and apply schema rules.

**Why it exists:** It provides consistent parsing and useful validation errors without writing every check manually.

---

# 5. Application Logic Runs

This is where the backend decides what the request should actually do.

## Route Function — Core

**Simple meaning:** The Python function FastAPI calls after matching and validating a request.

**Why it exists:** It is the entry point from HTTP behavior into application behavior.

**Where it fits:**

`Validated RunCreate → create_run() → application/database work`

**Current project behavior:**

```python
def create_run(run: RunCreate) -> RunCreate:
    return run
```

The function returns the validated request. It does not construct a `Run`, open a session, or save a row.

**Important distinction:** Returning data proves that the response works. It does not prove persistence.

### Check yourself

1. What does `create_run()` currently do?
2. Where is the incoming value validated?
3. Which missing steps are needed before the endpoint truly creates a stored run?

## Persistence — Core

**Simple meaning:** Save data so it remains available after the request and application process finish.

**Why it exists:** Useful application data must survive restarts and be available to later requests.

**Where it fits:**

`Application logic → session → transaction → PostgreSQL row`

**In this project:** Persistence is the current milestone and has not yet been connected to `POST /runs`.

---

# 6. SQLAlchemy Connects to PostgreSQL

Before data can be saved, the application needs a path to the intended database.

## Configuration and Environment Variable — Supporting

**Simple meaning:** Configuration supplies values that can differ between environments. An environment variable supplies such a value outside normal source code.

**Why it exists:** Development, testing, and production can use different databases without rewriting application logic.

**In this project:**

```python
class Settings(BaseSettings):
    database_url: str
    model_config = SettingsConfigDict(env_file=".env")
```

The local `.env` provides `DATABASE_URL`. Credentials inside it are secrets and should remain outside Git.

## Database URL — Supporting

**Simple meaning:** A compact description of how and where to connect.

**In this project:**

```text
postgresql+psycopg://<credentials>@localhost:5432/running_app
```

```text
postgresql   → database type
psycopg      → Python driver
localhost    → host computer
5432         → PostgreSQL port
running_app  → selected database
```

## Driver — Supporting

**Simple meaning:** The library performing low-level communication between Python and a particular database.

**In this project:** SQLAlchemy uses Psycopg to communicate with PostgreSQL.

**Concept chain:**

`Application → SQLAlchemy → Psycopg → PostgreSQL`

## Engine — Supporting

**Simple meaning:** SQLAlchemy's configured entry point for obtaining database connections.

**Why it exists:** It centralizes connection settings and manages reusable connections.

**In this project:**

```python
engine = create_engine(settings.database_url)
```

**Important distinction:** An engine is a connection manager. It is not the database and is not itself a table.

## Connection — Supporting

**Simple meaning:** An active conversation with the selected database.

**Why it exists:** SQL statements need an open communication channel to PostgreSQL.

**In this project:**

```python
with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database()"))
    print(result.scalar_one())
```

The experiment returned `running_app`. It proved the server, credentials, database, driver, and SQLAlchemy connection worked together. It did not prove that the `runs` table exists.

## Connection Pool — Recognition

**Simple meaning:** A managed set of reusable database connections.

**Why it exists:** Reusing connections is usually cheaper than opening a new network connection for every query.

At this stage, recognize that the engine manages this. Detailed pool configuration can wait until there is a measured need.

## `execute()` and `scalar_one()` — Recognition

**Simple meaning:** `execute()` sends a statement. `scalar_one()` extracts the single expected value from a one-value result.

These methods helped with the connection experiment. Understanding the connection result matters more right now than memorizing these exact method names.

---

# 7. A Session Manages Database Work

The code for creating sessions exists, but no route uses it yet.

## Session — Core

**Simple meaning:** SQLAlchemy's workspace for reading, adding, changing, and deleting ORM objects as a unit of work.

**Why it exists:** It coordinates object changes and database transactions rather than forcing application code to manage every SQL statement and object state manually.

**Where it fits:**

`Route/application logic → Session → Transaction → PostgreSQL`

**In this project:**

```python
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()
```

`SessionLocal` is a factory: calling it creates a session connected through the engine.

**Important distinction:** A session is not PostgreSQL and is not identical to a connection. It uses database connections while managing ORM work.

**Without it:** The application would manage more connection, transaction, SQL, and object state itself.

### Check yourself

1. What does a session manage?
2. Where is a session created in this project?
3. Why does `db.add(run)` not mean the run is permanently saved?

## `get_db()` and `yield` — Supporting

**Simple meaning:** `get_db()` prepares one session, provides it for work, and closes it afterward. `yield` pauses the function while the caller uses the session, then allows cleanup to continue.

**Why it exists:** Each request needs controlled access to a session and reliable cleanup.

**In this project:**

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```text
db = SessionLocal()  → create session
yield db             → provide it to the caller
finally              → run cleanup even after an error
db.close()           → release session resources
```

**Important distinction:** Closing a session is cleanup. It does not automatically prove that intended data was committed.

## Add — Supporting

**Simple meaning:** Tell the session to track a new ORM object for insertion.

**Where it fits:**

`Run object → session.add() → pending insert`

**Important distinction:** `add()` tracks intended work. It does not make a row permanent.

## Flush — Supporting

**Simple meaning:** Send pending changes as SQL while keeping them inside the current transaction.

**Why it exists:** The application may need the database to process changes before the whole transaction is committed.

**Important distinction:** Flush sends SQL. Commit makes the transaction permanent.

If the `runs` table is missing, the database error usually appears when SQLAlchemy flushes, either explicitly or as part of committing.

## Transaction — Core

**Simple meaning:** A boundary around database work that succeeds together or is canceled together.

**Why it exists:** It prevents partial changes from leaving stored data in an inconsistent state.

**Where it fits:**

`Session work → Transaction → Commit or Rollback`

### Check yourself

1. What promise does a transaction provide?
2. Which transaction contains a future run insert?
3. If a later operation fails, why might both database changes need to be canceled?

## Commit — Core

**Simple meaning:** Successfully finish a transaction and make its changes permanent.

**Why it exists:** The database needs a clear point at which completed work becomes lasting data.

**Where it fits:**

`Pending changes → flush → commit → lasting rows`

**Without it:** Another fresh session should not be expected to see the uncommitted run as lasting data.

## Rollback — Core

**Simple meaning:** Cancel the current transaction's uncommitted changes after a failure or deliberate decision.

**Why it exists:** Failed work should not leave partial changes, and the session must be returned to a usable transaction state.

### Check yourself

1. What does rollback cancel?
2. Where would a future run insert be committed?
3. PostgreSQL rejects an insert and the code never rolls back. What problem might the session have on its next operation?

---

# 8. PostgreSQL Persists Rows

The Python model and the real database schema must agree before ORM persistence can work.

## PostgreSQL, Database, Table, Row, and Column — Core

**Simple meaning:**

- PostgreSQL is the database program.
- `running_app` is a database managed by PostgreSQL.
- `runs` is the intended table inside that database.
- A row represents one saved run.
- A column represents one kind of value stored for each row.

**Why they exist:** They organize lasting data into structures that can enforce rules and be queried efficiently.

**Where they fit:**

`PostgreSQL → running_app database → runs table → run row → column values`

**In this project:** The successful connection query verified `running_app`. The next experiment must inspect whether `runs` actually exists.

### Check yourself

1. What is the difference between PostgreSQL, `running_app`, and `runs`?
2. Which intended column stores distance?
3. If `Run` exists in Python but `runs` is absent from PostgreSQL, what happens when the insert SQL is sent?

## ORM Model — Core

**Simple meaning:** A Python class describing a database table and the objects mapped to its rows.

**Why it exists:** Application code can work with typed Python objects while SQLAlchemy handles much of the mapping to SQL records.

**Where it fits:**

`Validated RunCreate → Run ORM object → Session → runs row`

**In this project:**

```python
class Run(Base):
    __tablename__ = "runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_activity_id: Mapped[str] = mapped_column(String(255), unique=True)
    distance_meters: Mapped[int] = mapped_column()
```

```text
class Run(Base)        → mapped Python class
__tablename__          → intended database table name
Mapped[int]            → Python/ORM type information
mapped_column(...)     → database column description
primary_key=True       → unique row identity
unique=True            → duplicate value protection
```

**Important distinction:** The model describes the intended table. It does not create or alter an existing table by itself.

## Primary Key — Core

**Simple meaning:** A column or group of columns that uniquely identifies each row.

**Why it exists:** Updates, relationships, and lookups need a stable way to identify one exact record.

**In this project:** `Run.id` is the intended primary key.

## Unique and Check Constraints — Supporting

**Simple meaning:** Database rules that reject invalid stored data.

- A unique constraint prevents duplicate protected values.
- A check constraint requires a condition to be true.

**In this project:** `external_activity_id` is declared unique, and distance must be greater than zero.

**Why they exist:** Data may reach PostgreSQL through paths other than this FastAPI request schema. The database protects itself at the final storage boundary.

## Nullable — Supporting

**Simple meaning:** A nullable column may store SQL `NULL`, meaning no value is present.

**In this project:** Elevation, heart rate, and notes may be null.

## Metadata — Supporting

**Simple meaning:** SQLAlchemy's in-memory collection of Python table, column, and constraint descriptions.

**Why it exists:** SQLAlchemy and migration tools need a combined view of the intended schema.

**Important distinction:** Seeing `runs` in `Base.metadata.tables` proves that Python knows the model. It does not prove the table exists in PostgreSQL.

## Migration — Core

**Simple meaning:** A saved, ordered instruction for changing the real database structure.

**Why it exists:** Every environment needs a repeatable, reviewable way to make the same schema changes over time.

**Where it fits:**

`ORM model → metadata → Alembic migration → PostgreSQL schema`

**In this project:** The first migration will create `runs`. A later migration could change `notes` from `VARCHAR(1000)` to `VARCHAR(2000)`.

**Important distinction:**

```text
Edit model       → change the intended structure in Python
Create migration → describe the database change
Apply migration  → change the real PostgreSQL structure
```

**Without migrations:** Developers and deployed environments could have different schemas, with no reliable history of how each one changed.

### Check yourself

1. What does a migration change?
2. Has this project created an Alembic migration yet?
3. If you edit `String(1000)` to `String(2000)` but never apply a migration, what size does the existing PostgreSQL column keep?

## Alembic — Supporting

**Simple meaning:** The tool used here to create, order, apply, and reverse SQLAlchemy-related database migrations.

**Why it exists:** Model changes and database schema changes need managed history.

**In this project:** Alembic is installed, but its migration environment and files have not been created yet.

---

# 9. FastAPI Sends a Response

The response tells the client what happened and may include returned data.

## HTTP Response — Core

**Simple meaning:** The message the backend sends after handling a request.

**Why it exists:** The client needs the result, status, and any returned data or error details.

**Where it fits:**

`Route result → FastAPI serialization → HTTP response → client`

**In this project:** `GET /health` returns `{"status": "ok"}`. `POST /runs` currently returns the validated input.

## Serialization — Supporting

**Simple meaning:** Convert an application value into a format that can be sent or stored.

**In this project:** FastAPI converts the returned Pydantic object into JSON.

## Status Code — Core

**Simple meaning:** A number summarizing the HTTP result.

**Why it exists:** Clients need a standard, quick way to distinguish success, invalid input, missing data, conflicts, and server failures.

**In this project:**

| Code | Simple meaning | Current use |
|---:|---|---|
| 200 | Request succeeded | Health check |
| 201 | A resource was created | Configured for `POST /runs`; persistence still needs to make this fully true |
| 422 | Submitted data failed validation | Zero-distance request |

### Check yourself

1. What does 201 mean?
2. Which invalid request currently produces 422 in a test?
3. Why does returning 201 and echoing input fail to prove that a run was created?

---

# 10. Tests Check the Flow

A passing test proves only the behavior its assertions actually observe.

## Automated Test — Core

**Simple meaning:** Code that performs an action and checks whether the actual result matches the expected result.

**Why it exists:** It gives repeatable evidence that known behavior works and helps detect later regressions.

**Where it fits:** Tests can enter at the HTTP boundary and inspect the response, database state, or an isolated unit of logic.

**In this project:** Three tests currently pass: health, valid POST response, and zero-distance rejection.

## Test Client — Supporting

**Simple meaning:** A helper that sends requests directly to the application during tests.

**In this project:**

```python
client = TestClient(app)
response = client.post("/runs", json=payload)
```

## Assertion — Core

**Simple meaning:** A statement that must be true for the test to pass.

**In this project:**

```python
assert response.status_code == 201
assert response_body["distance_meters"] == payload["distance_meters"]
```

**Important distinction:** These assertions verify the response. They do not query PostgreSQL, so they do not verify persistence.

## Arrange, Act, Assert — Supporting

**Simple meaning:** A common test structure.

```text
Arrange → prepare the payload and expected result
Act     → send the request
Assert  → check the response or stored state
```

## Happy Path and Failure Path — Supporting

**Simple meaning:**

- A happy-path test checks expected valid usage.
- A failure-path test checks an invalid input or expected problem.

**In this project:** The valid POST test is a happy path. The zero-distance test is a failure path.

## Integration Test — Core

**Simple meaning:** A test showing that multiple real parts work together.

**Why it exists:** Individual pieces can work separately while their connection is broken.

**Future project example:**

`HTTP request → FastAPI → session → PostgreSQL → verify stored row`

The current POST test stops at the HTTP response, so database persistence is still unverified.

### Check yourself

1. What does an assertion do?
2. Which current tests exercise a failure path?
3. What extra observation would turn the future POST persistence test into useful database integration evidence?

---

# Concept Chains

Use these chains to understand relationships between terms.

## Handling the current request

```text
HTTP request
→ FastAPI
→ route decorator
→ RunCreate validation
→ create_run()
→ serialization
→ HTTP response
```

## Creating and saving a run

```text
JSON
→ RunCreate
→ Run ORM object
→ Session
→ INSERT
→ Transaction
→ Commit
→ PostgreSQL row
```

## Connecting to PostgreSQL

```text
DATABASE_URL
→ SQLAlchemy Engine
→ Psycopg driver
→ PostgreSQL
→ running_app database
```

## Changing database structure

```text
Run model
→ SQLAlchemy metadata
→ Alembic migration
→ PostgreSQL schema
```

## Testing validation

```text
Test payload
→ TestClient request
→ RunCreate validation
→ HTTP response
→ assertion
```

## Testing persistence later

```text
Test payload
→ POST /runs
→ Session
→ Commit
→ fresh database query
→ stored row assertion
```

---

# Similar Terms That Are Easy to Mix Up

| Terms | Simplest distinction |
|---|---|
| FastAPI / Uvicorn | FastAPI defines application behavior; Uvicorn runs it and listens for requests. |
| Request schema / ORM model | A request schema validates API data; an ORM model maps objects to database rows. |
| PostgreSQL / database / table | PostgreSQL is the program; `running_app` is a database; `runs` is a table. |
| Model / migration | A model describes intended structure in Python; a migration changes the real database. |
| Engine / connection | An engine manages connection configuration; a connection is an active conversation. |
| Connection / session | A connection sends database commands; a session coordinates ORM objects and database work. |
| Add / flush / commit | Add tracks an object; flush sends SQL; commit makes the transaction permanent. |
| Validation / constraint | Validation protects the API boundary; a database constraint protects stored data. |
| Response / persistence | A response sends data to the client; persistence saves data for later. |
| Passing test / complete feature | A test proves only what it observes. Response assertions do not prove a stored row exists. |

---

# Progressive Recall Practice

Use these levels instead of trying to memorize the whole guide at once.

## Level 1 — Definition

Explain each in one simple sentence:

- Request
- Route
- Schema
- ORM model
- Session
- Transaction
- Commit
- Migration

## Level 2 — Locate It in This Project

Find and explain:

1. Where the FastAPI application is created.
2. Where `POST /runs` is connected to `create_run()`.
3. Where the run request rules are defined.
4. Where the intended `runs` table is described.
5. Where the engine and session factory are created.
6. Which current test checks a validation failure.

## Level 3 — Reason About Behavior

1. The route returns a `RunCreate`, but no database call occurs. What survives an application restart?
2. `Run` exists in Python, but the `runs` table is absent. When should an insert fail?
3. A new `Run` is added and flushed, but the transaction is rolled back. What should a fresh session see?
4. The model changes from `String(1000)` to `String(2000)`, but no migration is applied. What changes in PostgreSQL?
5. A test checks only the 201 response and returned JSON. What important behavior remains unproven?

---

# Personal Concept Record

Use this when a core concept remains unclear.

## Concept

- Name:
- My one-sentence explanation:
- Why it exists:
- Where it fits in the request flow:
- Where it appears in this project:
- What it interacts with:
- What could go wrong without it:
- What I previously confused it with:
- Confidence from 1 to 5:
- Question to revisit:

---

# Current Focus

The current lesson is to inspect the real `running_app` database and determine whether the `runs` table exists.

Before running the inspection, predict the result. Afterward, explain what the result proves about PostgreSQL and what it does not prove about the Python application.
