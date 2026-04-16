# Cloud-Computing-Concepts-Part-2
Coursera course : https://www.coursera.org/specializations/cloud-computing
# What is the project?
*	Building a **Fault-Tolerant Key-Value Store**.

*	The main functionalities of the Key-Value Store :
	*	**CRUD operations :** A key-value store supporting CRUD operations (Create, Read, Update, Delete).
	*	**Load-balancing :** via a consistent hashing ring to hash both servers and keys.
	*	**Fault-tolerance up to two failures :** by replicating each key three times to three successive nodes in the ring, 	    starting from the first node at or to the clockwise of the hashed key.
	*	**Quorum consistency level** for both reads and writes (at least two replicas).
	*	**Stabilization :** after failure (recreate three replicas after failure).
      
# Principle of **Fault-Tolerant Key-Value Store** : 
![image](https://github.com/kevin85421/Cloud-Computing-Concepts-Part-2/blob/master/kvstore.png)

# How do I run the Grader on my computer ?
*	There is a grader script KVStoreGrader.sh. The tests include:
      * **Basic CRUD** tests that test if three replicas respond
      * **Single failure** followed immediately by operations which should succeed (as quorum can still be
reached with 1 failure)
      * **Multiple failures** followed immediately by operations which should fail as quorum cannot be
reached
      * Failures followed by a time for the system to re-stabilize, followed by operations that should
succeed because the key has been re-replicated again at three nodes.
```
	$ chmod +x KVStoreGrader.sh
	$ ./KVStoreGrader.sh
```
# Result
*	Points achieved: 90 out of 90 [100%]

# Cloud Computing Concepts - Part 2

This repository contains:

1. The original MP2 distributed key-value store code and grader scripts.
2. A FastAPI backend that runs asynchronous Coursera submission jobs.
3. A React frontend (Vite + Tailwind + Framer Motion) that submits and tracks job progress.

## Project Structure

1. Backend API: [main.py](main.py)
2. Submission logic: [submit.py](submit.py)
3. Grading runner script: [run.sh](run.sh)
4. Frontend app: [frontend](frontend)
5. Backend container config: [Dockerfile](Dockerfile)

## Backend Overview

The backend uses an async job workflow.

1. `POST /submit`
2. `GET /status/{job_id}`
3. `POST /cancel/{job_id}`

Job status progression:

1. `running`
2. `grading`
3. `submitting`
4. terminal states: `done`, `failed`, or `killed`

On submit, the backend:

1. Creates a job ID and temporary folder under `/tmp`.
2. Runs [run.sh](run.sh) in a subprocess.
3. Submits generated logs to Coursera through [submit.py](submit.py).
4. Exposes status through `/status/{job_id}`.

## API Contract

### POST /submit

Request body:

```json
{
	"email": "you@example.com",
	"token": "your-token"
}
```

Response:

```json
{
	"job_id": "...",
	"status": "running",
	"msg": "Submission started"
}
```

### GET /status/{job_id}

Response:

```json
{
	"status": "running|grading|submitting|done|failed|killed",
	"result": {}
}
```

### POST /cancel/{job_id}

Response:

```json
{
	"msg": "Job cancelled"
}
```

## Backend Local Setup

### Prerequisites

1. Python 3.12+
2. C++ toolchain (`g++`, `make`)
3. `wget`, `unzip`
4. A valid `DATABASE_URL` environment variable

### Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]" sqlalchemy python-dotenv asyncpg httpx email-validator
export DATABASE_URL="postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME"
uvicorn main:app --reload
```

API base URL (default): `http://127.0.0.1:8000`

## Frontend Setup

The frontend is in [frontend](frontend).

```bash
cd frontend
npm install
```

Create [frontend/.env](frontend/.env) with:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Run frontend:

```bash
npm run dev
```

Build frontend:

```bash
npm run build
```

## Docker (Backend)

Build:

```bash
docker build -t cloud-backend .
```

Run:

```bash
docker run --rm -p 8000:8000 \
	-e DATABASE_URL="postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME" \
	cloud-backend
```

If you see Docker exit code `125`, check for:

1. Port conflict on `8000`
2. Invalid Docker command formatting
3. Existing container using the same published port

## MP2 Grader Notes

The original MP2 files and grader scripts are preserved in this repo.

1. [KVStoreGrader.sh](KVStoreGrader.sh)
2. MP2 source files (`MP2Node.*`, `Application.*`, etc.)

These are used by [run.sh](run.sh) during submission workflows.
	
