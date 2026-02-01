import json

def map_job(job):
    return {
        "id": job["id"],
        "title": job["Job_Opening_Name"],
        "location": job.get("City", ""),
        "status": job.get("Status", "OPEN"),
        "external_url": job.get("Job_Opening_URL", "")
    }

def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,PUT,OPTIONS",
        },
        "body": body
    }

