from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import os
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

APP_ENDPOINT_URL = os.getenv("APP_ENDPOINT_URL")
WORKSPACE_DOMAIN_ID = os.getenv("WORKSPACE_DOMAIN_ID") 
EMAIL_DOMAIN_ID = os.getenv("EMAIL_DOMAIN_ID")
CHAT_ISSUER = os.getenv("CHAT_ISSUER")

@app.get("/")
async def handle_chat_event(request: Request):
    return {"status": "ok"}


def validate_chat_request(event_data: dict, handle_name: str) -> bool:
    """
    Performs two checks:
    1. Validates the systemIdToken to ensure the request is from Google Chat.
    2. Validates the domainId to ensure the user is from your company's Workspace.
    """
    
    # --- 1. Request Integrity (JWT) Validation ---
    try:
        token = event_data['authorizationEventObject']['systemIdToken']
    except KeyError:
        logger.error("Error: Missing systemIdToken.")
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Use the google-auth library to verify the token.
        # This automatically fetches Google's public keys, checks the signature,
        # checks the expiration (exp), checks the audience (aud), and checks the issuer (iss).
        id_info = id_token.verify_token(
            token, 
            google_requests.Request(),
            audience=f"{APP_ENDPOINT_URL}/{handle_name}"
        )

        # Explicitly verify the issuer (iss)
        if id_info.get('iss') != CHAT_ISSUER:
            logger.error(f"Error: Invalid issuer. Expected '{CHAT_ISSUER}', got '{id_info.get('iss')}'")
            raise HTTPException(status_code=401, detail="Unauthorized")

    except Exception as e:
        # This block catches all JWT validation failures (e.g., bad signature, expired, wrong audience)
        logger.error(f"Request Integrity Check: FAILED. JWT verification failed: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")
        
    # --- 2. Company Domain Validation ---
    user_domain_id = event_data.get('chat', {}).get('user', {}).get('domainId')
    if user_domain_id != WORKSPACE_DOMAIN_ID:
        logger.error(f"Unauthorized user domainId: {user_domain_id}")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_email = event_data.get("chat", {}).get("user", {}).get("email", "unknown email")
    user_email_domain = user_email.split("@")[1]
    if user_email_domain != EMAIL_DOMAIN_ID:
        logger.error(f"Unauthorized user email domain: {user_email_domain}")
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
async def health_check(request: Request):
    return {"status": "ok"}


@app.post("/databot")
async def handle_databot_event(request: Request):
    event = await request.json()
    validate_chat_request(event, "databot")

    user_message = event.get("chat", {}).get("messagePayload", {}).get("message", {}).get("text", "")
    user_email = event.get("chat", {}).get("user", {}).get("email", "unknown email")

    reply_text = f"DATABOT message : {user_message} (email: {user_email})"

    response = build_response(reply_text)
    logger.debug(f"Sending response: {response}")
    return response


@app.post("/peoplebot")
async def handle_peoplebot_event(request: Request):
    event = await request.json()
    validate_chat_request(event, "peoplebot")

    reply_text = f"Boleh."

    response = build_response(reply_text)
    logger.debug(f"Sending response: {response}")
    return response


def build_response(text):
    response ={
        "hostAppDataAction": {
            "chatDataAction": {
            "createMessageAction": {
                "message": {
                "text": text
                }
            }
            }
        }
    }
    return JSONResponse(content=response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
