# # import httpx
# # import os
# # import asyncio
# # import uuid
# # import shutil
# # import subprocess

# # # ================= CONFIG =================

# # SUBMIT_URL = "https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1"

# # akey = 'Lm64BvbLEeWEJw5JS44kjw'
# # partIds = ['PH3Q7', 'PIXym', 'mUKdC', 'peNB6']


# # # ================= CORE =================

# # async def submit(email: str, token: str):
# #     print("==\n== [sandbox] Submitting Solutions \n==")

# #     if not email:
# #         return {"success": False, "error": "Missing email"}

# #     job_dir = f"/tmp/{uuid.uuid4()}"
# #     os.makedirs(job_dir, exist_ok=True)

# #     try:
# #         # run grader
# #         await asyncio.to_thread(run_script, job_dir)

# #         # read logs
# #         submissions = [read_source(job_dir, i) for i in range(4)]

# #         # send to Coursera
# #         result = await send_submission(email, token, submissions)

# #         return result

# #     except Exception as e:
# #         return {"success": False, "error": str(e)}

# #     finally:
# #         shutil.rmtree(job_dir, ignore_errors=True)


# # # ================= HELPERS =================

# # def run_script(job_dir):
# #     subprocess.run(
# #         ['sh', 'run.sh', job_dir, os.getcwd()],
# #         check=True
# #     )


# # def read_source(job_dir, partIdx):
# #     path = f"{job_dir}/dbg.{partIdx}.log"

# #     if not os.path.exists(path):
# #         raise Exception(f"Missing output file: {path}")

# #     with open(path) as f:
# #         return f.read()


# # async def send_submission(email, token, submissions):
# #     payload = {
# #         "assignmentKey": akey,
# #         "submitterEmail": email,
# #         "secret": token,
# #         "parts": {
# #             partIds[i]: {"output": submissions[i]} for i in range(4)
# #         }
# #     }

# #     headers = {
# #         "Content-Type": "application/json",
# #         "Accept": "application/json",
# #         "User-Agent": "Mozilla/5.0"
# #     }

# #     async with httpx.AsyncClient(timeout=30) as client:
# #         response = await client.post(
# #             SUBMIT_URL,
# #             json=payload,
# #             headers=headers
# #         )

# #     # 🔥 CRITICAL: parse response
# #     try:
# #         data = response.json()
# #     except Exception:
# #         return {"success": False, "error": "Invalid response from server"}

# #     # 🔴 Coursera error handling
# #     if "errorCode" in data or "error" in data:
# #         return {
# #             "success": False,
# #             "error": data.get("message") or data.get("error") or "Submission failed"
# #         }

# #     return {
# #         "success": True,
# #         "data": data
# #     }



# import httpx
# import os

# SUBMIT_URL = "https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1"

# akey = 'Lm64BvbLEeWEJw5JS44kjw'
# partIds = ['PH3Q7', 'PIXym', 'mUKdC', 'peNB6']


# def read_source(job_dir, partIdx):
#     path = f"{job_dir}/dbg.{partIdx}.log"

#     if not os.path.exists(path):
#         raise Exception(f"Missing output file: {path}")

#     with open(path) as f:
#         return f.read()


# async def process_submission(job_dir, email, token):
#     try:
#         submissions = [read_source(job_dir, i) for i in range(4)]
#         return await send_submission(email, token, submissions)
#     except Exception as e:
#         return {"success": False, "error": str(e)}


# async def send_submission(email, token, submissions):
#     payload = {
#         "assignmentKey": akey,
#         "submitterEmail": email,
#         "secret": token,
#         "parts": {
#             partIds[i]: {"output": submissions[i]} for i in range(4)
#         }
#     }

#     headers = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "User-Agent": "Mozilla/5.0"
#     }

#     async with httpx.AsyncClient(timeout=30) as client:
#         response = await client.post(
#             SUBMIT_URL,
#             json=payload,
#             headers=headers
#         )

#     try:
#         data = response.json()
#     except Exception:
#         return {"success": False, "error": "Invalid response from server"}

#     if "errorCode" in data or "error" in data:
#         return {
#             "success": False,
#             "error": data.get("message") or data.get("error") or "Submission failed"
#         }

#     return {
#         "success": True,
#         "data": data
#     }

import httpx
import os

SUBMIT_URL = "https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1"

akey = 'Lm64BvbLEeWEJw5JS44kjw'
partIds = ['PH3Q7', 'PIXym', 'mUKdC', 'peNB6']


def read_source(job_dir, partIdx):
    path = f"{job_dir}/dbg.{partIdx}.log"

    if not os.path.exists(path):
        raise Exception(f"Missing output file: {path}")

    with open(path) as f:
        return f.read()


async def process_submission(job_dir, email, token):
    try:
        submissions = [read_source(job_dir, i) for i in range(4)]
        return await send_submission(email, token, submissions)
    except Exception as e:
        return {"success": False, "error": str(e)}


async def send_submission(email, token, submissions):
    payload = {
        "assignmentKey": akey,
        "submitterEmail": email,
        "secret": token,
        "parts": {
            partIds[i]: {"output": submissions[i]} for i in range(4)
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            SUBMIT_URL,
            json=payload,
            headers=headers
        )

    try:
        data = response.json()
    except Exception:
        return {"success": False, "error": "Invalid response from server"}

    if "errorCode" in data or "error" in data:
        return {
            "success": False,
            "error": data.get("message") or data.get("error") or "Submission failed"
        }

    return {
        "success": True,
        "data": data
    }