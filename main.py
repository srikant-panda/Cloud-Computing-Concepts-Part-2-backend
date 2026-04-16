# # from fastapi import FastAPI, HTTPException,Depends
# # from contextlib import asynccontextmanager
# # from fastapi.middleware.cors import CORSMiddleware
# # from starlette.status import HTTP_424_FAILED_DEPENDENCY
# # import submit
# # from pydantic import BaseModel, EmailStr                                                                        
# # from sqlalchemy import MetaData
# # from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
# # from sqlalchemy.orm import DeclarativeBase
# # from dotenv import load_dotenv
# # from os import getenv
# # from sqlalchemy import Integer,String,DateTime,func,select,text,MetaData
# # from sqlalchemy.orm import Mapped,mapped_column
# # from datetime import datetime
# # load_dotenv()

# # DATABASE_URL = str(getenv("DATABASE_URL"))
# # DEFAULT_SCHEMA_NAME = "cloude_computing"
# # metadata = MetaData(schema=DEFAULT_SCHEMA_NAME)

# # class Base(DeclarativeBase):
# #     metadata = metadata

# # engine = create_async_engine(DATABASE_URL,echo=False,future = True,connect_args = {"statement_cache_size":0})

# # AsyncSessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

# # async def getDb():
# #     try:
# #         async with AsyncSessionLocal() as session:
# #             yield session
# #     except Exception as e:
# #         print(str(e))
# #         raise

# # # '''______database models______'''
# # class RequestModel(Base):
# #     __tablename__ = 'requests'
# #     __table_args__ = {"schema":DEFAULT_SCHEMA_NAME}
# #     id : Mapped[int] = mapped_column(Integer,primary_key=True)
# #     email : Mapped[str] = mapped_column(String(100),nullable=False)
# #     click : Mapped[int] = mapped_column(Integer,nullable=False,autoincrement=True,default=1)
# #     created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default= func.now())
# #     updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
# # class Info(BaseModel):
# #     email: EmailStr
# #     token: str

# # class BaseInfo(BaseModel):
# #     msg: str
# #     error: str | None = None




# # # '''______lifespan_____'''
# # @asynccontextmanager
# # async def lifespan(app : FastAPI):
# #     print("Applocation started.")
# #     try:
# #         async with engine.begin() as conn:
# #             await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{DEFAULT_SCHEMA_NAME}"')) 
# #             await conn.run_sync(Base.metadata.create_all)
# #     except Exception as e:
# #         # logger.exception("Database Connection failed.")
# #         raise RuntimeError("Database Connection failed.") from e
# #     yield
    
# #     await engine.dispose()
# #     print("Application stopped.")


# # app = FastAPI(lifespan=lifespan)


# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # @app.post('/submit')
# # async def submit_application(data: Info,db:AsyncSession=Depends(getDb)):
# #     result = await submit.submit(email=data.email, token=data.token,)

# #     # 🔥 FIX: proper success check
# #     if not result.get("success"):
# #         raise HTTPException(
# #             status_code=HTTP_424_FAILED_DEPENDENCY,
# #             detail=result.get("error", "Submission failed")
# #         )
# #     db_result= await db.execute(select(RequestModel).where(RequestModel.email==data.email))
# #     result = db_result.scalar_one_or_none()
# #     if not result:
# #         db.add(RequestModel(email=data.email))
# #         await db.commit()
# #     else:
# #         result.click+=1
# #         await db.commit()
# #     return BaseInfo(
# #         msg="Application submitted successfully. Check your progress on Coursera."
# #     )



# import os
# import uuid
# import shutil
# import subprocess
# import asyncio

# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.status import HTTP_424_FAILED_DEPENDENCY

# from pydantic import BaseModel, EmailStr

# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, DateTime, func, select, text, MetaData

# from contextlib import asynccontextmanager
# from datetime import datetime
# from dotenv import load_dotenv
# from os import getenv

# import submit

# # ================= CONFIG =================

# load_dotenv()

# DATABASE_URL = str(getenv("DATABASE_URL"))
# DEFAULT_SCHEMA_NAME = "cloude_computing"

# metadata = MetaData(schema=DEFAULT_SCHEMA_NAME)


# # ================= DB =================

# class Base(DeclarativeBase):
#     metadata = metadata


# class RequestModel(Base):
#     __tablename__ = 'requests'
#     __table_args__ = {"schema": DEFAULT_SCHEMA_NAME}

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     email: Mapped[str] = mapped_column(String(100), nullable=False)
#     click: Mapped[int] = mapped_column(Integer, default=1)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# engine = create_async_engine(
#     DATABASE_URL,
#     echo=False,
#     future=True,
#     connect_args={"statement_cache_size": 0}
# )

# AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# async def getDb():
#     async with AsyncSessionLocal() as session:
#         yield session


# # ================= JOB SYSTEM =================

# jobs = {}


# async def handle_job(job_id):
#     job = jobs[job_id]
#     process = job["process"]

#     # wait for script
#     await asyncio.to_thread(process.wait)

#     if process.returncode != 0:
#         job["status"] = "failed"
#         return

#     result = await submit.process_submission(
#         job["job_dir"],
#         job["email"],
#         job["token"]
#     )

#     job["status"] = "done" if result.get("success") else "failed"
#     job["result"] = result

#     shutil.rmtree(job["job_dir"], ignore_errors=True)


# # ================= API =================

# class Info(BaseModel):
#     email: EmailStr
#     token: str


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{DEFAULT_SCHEMA_NAME}"'))
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await engine.dispose()


# app = FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ================= ROUTES =================

# @app.post('/submit')
# async def submit_application(data: Info):
#     job_id = str(uuid.uuid4())
#     job_dir = f"/tmp/{job_id}"

#     os.makedirs(job_dir, exist_ok=True)

#     process = subprocess.Popen(
#         ['sh', 'run.sh', job_dir, os.getcwd()],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE
#     )

#     jobs[job_id] = {
#         "process": process,
#         "status": "running",
#         "job_dir": job_dir,
#         "email": data.email,
#         "token": data.token
#     }

#     asyncio.create_task(handle_job(job_id))

#     return {"job_id": job_id}


# @app.get("/status/{job_id}")
# def get_status(job_id: str):
#     job = jobs.get(job_id)

#     if not job:
#         raise HTTPException(404, "Job not found")

#     return {
#         "status": job["status"],
#         "result": job.get("result")
#     }


# @app.post("/cancel/{job_id}")
# def cancel_job(job_id: str):
#     job = jobs.get(job_id)

#     if not job:
#         raise HTTPException(404, "Job not found")

#     process = job["process"]

#     if process.poll() is None:
#         process.kill()
#         job["status"] = "killed"

#     shutil.rmtree(job["job_dir"], ignore_errors=True)

#     return {"msg": "Job cancelled"}


# import os
# import uuid
# import shutil
# import subprocess
# import asyncio

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, EmailStr

# import submit

# # ================= JOB SYSTEM =================

# jobs = {}


# async def handle_job(job_id):
#     job = jobs[job_id]
#     process = job["process"]

#     # 🔥 Step 1: grading
#     job["status"] = "grading"

#     await asyncio.to_thread(process.wait)

#     if process.returncode != 0:
#         job["status"] = "failed"
#         return

#     # 🔥 Step 2: submitting
#     job["status"] = "submitting"

#     result = await submit.process_submission(
#         job["job_dir"],
#         job["email"],
#         job["token"]
#     )

#     # 🔥 Step 3: final state
#     job["status"] = "done" if result.get("success") else "failed"
#     job["result"] = result

#     shutil.rmtree(job["job_dir"], ignore_errors=True)


# # ================= API =================

# class Info(BaseModel):
#     email: EmailStr
#     token: str


# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # ================= ROUTES =================

# @app.post("/submit")
# async def submit_application(data: Info):
#     job_id = str(uuid.uuid4())
#     job_dir = f"/tmp/{job_id}"

#     os.makedirs(job_dir, exist_ok=True)

#     process = subprocess.Popen(
#         ['sh', 'run.sh', job_dir, os.getcwd()],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE
#     )

#     jobs[job_id] = {
#         "process": process,
#         "status": "running",  # running → grading → submitting → done/failed
#         "job_dir": job_dir,
#         "email": data.email,
#         "token": data.token
#     }

#     asyncio.create_task(handle_job(job_id))

#     return {
#         "job_id": job_id,
#         "status": "running",
#         "msg": "Submission started"
#     }


# @app.get("/status/{job_id}")
# def get_status(job_id: str):
#     job = jobs.get(job_id)

#     if not job:
#         raise HTTPException(404, "Job not found")

#     return {
#         "status": job["status"],
#         "result": job.get("result")
#     }


# @app.post("/cancel/{job_id}")
# def cancel_job(job_id: str):
#     job = jobs.get(job_id)

#     if not job:
#         raise HTTPException(404, "Job not found")

#     process = job["process"]

#     if process.poll() is None:
#         process.kill()
#         job["status"] = "killed"

#     shutil.rmtree(job["job_dir"], ignore_errors=True)

#     return {"msg": "Job cancelled"}


import os
import uuid
import shutil
import subprocess
import asyncio

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func, select, text, MetaData

from contextlib import asynccontextmanager
from datetime import datetime
from dotenv import load_dotenv
from os import getenv

import submit

# ================= CONFIG =================

load_dotenv()

DATABASE_URL = str(getenv("DATABASE_URL"))
DEFAULT_SCHEMA_NAME = "cloude_computing"

metadata = MetaData(schema=DEFAULT_SCHEMA_NAME)

# ================= DATABASE =================

class Base(DeclarativeBase):
    metadata = metadata


class RequestModel(Base):
    __tablename__ = 'requests'
    __table_args__ = {"schema": DEFAULT_SCHEMA_NAME}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    click: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"statement_cache_size": 0}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def getDb():
    async with AsyncSessionLocal() as session:
        yield session


# ================= JOB SYSTEM =================

jobs = {}


async def handle_job(job_id: str):
    job = jobs[job_id]
    process = job["process"]

    try:
        # 🔥 Step 1: grading
        job["status"] = "grading"

        await asyncio.to_thread(process.wait)

        if process.returncode != 0:
            job["status"] = "failed"
            return

        # 🔥 Step 2: submitting
        job["status"] = "submitting"

        result = await submit.process_submission(
            job["job_dir"],
            job["email"],
            job["token"]
        )

        # 🔥 Step 3: final state
        job["status"] = "done" if result.get("success") else "failed"
        job["result"] = result

    except Exception as e:
        job["status"] = "failed"
        job["result"] = {"error": str(e)}

    finally:
        shutil.rmtree(job["job_dir"], ignore_errors=True)


# ================= API MODELS =================

class Info(BaseModel):
    email: EmailStr
    token: str


# ================= LIFESPAN =================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Application started")

    async with engine.begin() as conn:
        await conn.execute(
            text(f'CREATE SCHEMA IF NOT EXISTS "{DEFAULT_SCHEMA_NAME}"')
        )
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()
    print("🛑 Application stopped")


# ================= APP =================

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= ROUTES =================

@app.post("/submit")
async def submit_application(data: Info, db: AsyncSession = Depends(getDb)):
    print(data.email)
    job_id = str(uuid.uuid4())
    job_dir = f"/tmp/{job_id}"

    os.makedirs(job_dir, exist_ok=True)

    # 🔥 DB TRACKING (user clicks)
    db_result = await db.execute(
        select(RequestModel).where(RequestModel.email == data.email)
    )
    user = db_result.scalar_one_or_none()

    if not user:
        db.add(RequestModel(email=data.email))
    else:
        user.click += 1

    await db.commit()

    # 🔥 START BACKGROUND PROCESS
    process = subprocess.Popen(
        ['sh', 'run.sh', job_dir, os.getcwd()],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    jobs[job_id] = {
        "process": process,
        "status": "running",  # running → grading → submitting → done/failed
        "job_dir": job_dir,
        "email": data.email,
        "token": data.token
    }

    asyncio.create_task(handle_job(job_id))

    return {
        "job_id": job_id,
        "status": "running",
        "msg": "Submission started"
    }


@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = jobs.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "status": job["status"],
        "result": job.get("result")
    }


@app.post("/cancel/{job_id}")
def cancel_job(job_id: str):
    job = jobs.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    process = job["process"]

    if process.poll() is None:
        process.kill()
        job["status"] = "killed"

    shutil.rmtree(job["job_dir"], ignore_errors=True)

    return {"msg": "Job cancelled"}

@app.get("/health")
async def health():
    return {
        "status":"running",
        "msg" : "ok"
    }
@app.get('/')
async def root():
    return RedirectResponse('/health')