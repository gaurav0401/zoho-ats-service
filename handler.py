import json
from zoho_client import zoho_request
from utils import map_job, response


def get_jobs(event, context):
    try:
        data = zoho_request("GET", "/recruit/v2/JobOpenings")
        jobs = [map_job(j) for j in data.get("data", [])]
        return response(200, json.dumps(jobs))
    except Exception as e:
        return response(500, json.dumps({"error": str(e)}))
    
def create_candidate(event, context):
    try:
        body = json.loads(event["body"])

        # Split name
        full_name = body["name"].strip()
        parts = full_name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else "NA"

        # 1️⃣ Create Candidate
        candidate_payload = {
            "data": [{
                "First_Name": first_name,
                "Last_Name": last_name,
                "Email": body["email"],
                "Mobile": body["phone"]
            }]
        }

        candidate_res = zoho_request(
            "POST",
            "/recruit/v2/Candidates",
            payload=candidate_payload
        )

        data = candidate_res.get("data", [])
        if not data or "details" not in data[0] or "id" not in data[0]["details"]:
            raise Exception(f"Candidate creation failed: {candidate_res}")

        candidate_id = data[0]["details"]["id"]

        # 2️⃣ Try to associate with Job (NON-BLOCKING)
        association_status = "ASSOCIATED"
        try:
            associate_payload = {
                "data": [{
                    "Candidate_Id": candidate_id,
                    "Job_Opening_Id": body["job_id"]
                }]
            }

            zoho_request(
                "PUT",
                "/recruit/v2/Candidates/actions/associate",
                payload=associate_payload
            )

        except Exception as assoc_error:
            # Log but DO NOT fail entire request
            association_status = "CANDIDATE_CREATED_BUT_NOT_ASSOCIATED"

        return response(
            201,
            json.dumps({
                "message": "Candidate created",
                "candidate_id": candidate_id,
                "application_status": association_status
            })
        )

    except Exception as e:
        return response(500, json.dumps({"error": str(e)}))


def get_applications(event, context):
    try:
        job_id = event["queryStringParameters"]["job_id"]

        data = zoho_request(
            "GET",
            "/recruit/v2/Applications",
            params={"criteria": f"(Job_Opening_Name:equals:{job_id})"}
        )

        apps = []
        for a in data.get("data", []):
            apps.append({
                "id": a["id"],
                "candidate_name": a["Candidate_Name"]["name"],
                "email": a.get("Email", ""),
                "status": a.get("Application_Status", "APPLIED")
            })

        return response(200, json.dumps(apps))

    except Exception as e:
        return response(500, json.dumps({"error": str(e)}))
