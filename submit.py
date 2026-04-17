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
import logging

logger = logging.getLogger("job-system")

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
        logger.error(f"[SUBMIT] Failed to prepare submission → {str(e)}")
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
        logger.info(f"[COURSERA RESPONSE] {data}")
    except Exception:
        logger.error("[COURSERA] Invalid JSON response")
        return {"success": False, "error": "Invalid response from server"}

    if "errorCode" in data or "error" in data:
        logger.error(f"[COURSERA ERROR] {data}")
        return {
            "success": False,
            "error": data.get("message") or data.get("error") or "Submission failed"
        }

    logger.info("[COURSERA] Submission success")
    return {
        "success": True,
        "data": data
    }