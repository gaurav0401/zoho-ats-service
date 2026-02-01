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

        candidate_payload = {
            "data": [{
                "First_Name": body["name"],
                "Email": body["email"],
                "Mobile": body["phone"]
            }]
        }

        candidate = zoho_request(
            "POST",
            "/recruit/v2/Candidates",
            payload=candidate_payload
        )

        candidate_id = candidate["data"][0]["details"]["id"]

        application_payload = {
            "data": [{
                "Candidate_Name": candidate_id,
                "Job_Opening_Name": body["job_id"]
            }]
        }

        zoho_request(
            "POST",
            "/recruit/v2/Applications",
            payload=application_payload
        )

        return response(201, json.dumps({"message": "Candidate created"}))

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
