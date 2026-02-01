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

        # 1️ Create Candidate
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

        print(f"Candidate created with ID: {candidate_id}")

        # 2️ Try to associate with Job (NON-BLOCKING)
        association_status = "ASSOCIATED"
        try:
            associate_payload = {
                "data": [{
                    # "Candidate_Id": candidate_id,
                    
                    "ids": [body["job_id"]] 

                   
                }]
            
             
            }
            print(associate_payload)

            zoho_request(
             "POST",
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
        params = event.get("queryStringParameters") or {}
        job_id = params.get("job_id")

        if not job_id:
            return response(400, json.dumps({"error": "job_id is required"}))

        # 1 Fetch ALL applications (Zoho limitation)
        data = zoho_request(
            "GET",
            "/recruit/v2/Applications"
        )



        applications = []

        for a in data.get("data", []):
            # Filter by job id manually
            if a.get("$Job_Opening_Id") != job_id:
                continue

            #  Extract candidate name safely
            candidate_name = (
                a.get("Full_Name")
                or f"{a.get('First_Name', '')} {a.get('Last_Name', '')}".strip()
            )

            applications.append({
                "id": a.get("id"),
                "candidate_id": a.get("$Candidate_Id"),
                "candidate_name": candidate_name,
                "status": a.get("Application_Status", "APPLIED"),
                "job_title": a.get("Job_Opening_Name")
            })

        return response(200, json.dumps(applications))

    except Exception as e:
        print("ERROR:", str(e))
        return response(500, json.dumps({"error": str(e)}))
