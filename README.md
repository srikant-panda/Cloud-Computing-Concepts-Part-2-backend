# Cloud Computing Concepts Part 2

Coursera specialization:
https://www.coursera.org/specializations/cloud-computing

This repository currently contains two related parts:

1. MP2 C++ distributed key-value store implementation and grader flow.
2. A FastAPI service that runs the grader and submits results to Coursera asynchronously.

## Key-Value Store (MP2)

The MP2 implementation provides:

1. CRUD operations (create, read, update, delete).
2. Consistent hashing based node/key placement.
3. Replication factor 3.
4. Quorum-style operations (majority behavior for reads/writes).
5. Stabilization behavior after failures.

Architecture image:

![kvstore](kvstore.png)

## Project Structure

Core files:

1. `MP2Node.cpp` / `MP2Node.h`: MP2 key-value store protocol logic.
2. `MP1Node.cpp` / `MP1Node.h`: membership protocol logic.
3. `Makefile`: C++ build for `Application`.
4. `KVStoreGrader.sh`: local MP2 grader script.
5. `testcases/`: CRUD and failure simulation configs.

Submission API files:

1. `main.py`: FastAPI app and async job orchestration.
2. `run.sh`: prepares Coursera grader package, builds, runs tests, writes `dbg.*.log`.
3. `submit.py`: sends logs to Coursera programming assignment endpoint.

## Run MP2 Locally (C++)

Build:

```bash
make clean
make
```

Run a specific testcase:

```bash
./Application ./testcases/create.conf
./Application ./testcases/delete.conf
./Application ./testcases/read.conf
./Application ./testcases/update.conf
```

Run full local grader:

```bash
chmod +x KVStoreGrader.sh
./KVStoreGrader.sh
```

## FastAPI Submission Service

`main.py` exposes APIs to run grading and submit to Coursera.

Current endpoints:

1. `POST /submit` (rate limited to `3/minutes` per IP)
2. `GET /status/{job_id}`
3. `POST /cancel/{job_id}`
4. `GET /health`

Job states:

1. `running`
2. `grading`
3. `submitting`
4. terminal states: `done`, `failed`, `killed`

### Request/Response Examples

Submit:

```http
POST /submit
Content-Type: application/json

{
  "email": "you@example.com",
  "token": "coursera-secret-token"
}
```

```json
{
  "job_id": "2f3f3d4f-...",
  "status": "running",
  "msg": "Submission started"
}
```

Status:

```http
GET /status/{job_id}
```

```json
{
  "status": "grading",
  "result": null
}
```

Cancel:

```http
POST /cancel/{job_id}
```

```json
{
  "msg": "Job cancelled"
}
```

Health:

```http
GET /health
```

```json
{
  "status": "running",
  "msg": "ok"
}
```

## Run FastAPI Service Locally

Prerequisites:

1. Python 3.12+
2. `g++`, `make`
3. `wget`, `unzip`
4. PostgreSQL connection string in `DATABASE_URL`

Setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install slowapi
```

Run:

```bash
export DATABASE_URL="postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME"
uvicorn main:app --reload
```

Service URL (default):

```text
http://127.0.0.1:8000
```

## Notes

1. The service creates job folders under `/tmp/<job_id>` and removes them after completion/cancel.
2. `run.sh` downloads the official Coursera MP2 grader package at runtime.
3. `submit.py` expects four generated logs: `dbg.0.log` to `dbg.3.log`.

