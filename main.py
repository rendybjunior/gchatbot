from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/")
async def handle_chat_event(request: Request):
    """
    Handle incoming Google Chat events.
    """
    event = await request.json()
    logger.info(f"Received event: {event}")

    user_message = event.get("chat", {}).get("messagePayload", {}).get("message", {}).get("text", "")
    
    # Extract user email
    user_email = event.get("chat", {}).get("user", {}).get("email", "unknown email")
    
    # Create the reply using the requested template
    reply_text = f"your message : {user_message} (email: {user_email})"
    
    response = build_response(reply_text)
    logger.info(f"Sending response: {response}")
    return response

# Replace this with your endpoint URL (must match what you set in Chat App config)
EXPECTED_AUDIENCE = os.getenv("EXPECTED_AUDIENCE")

def validate_request(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = auth_header.split(" ")[1]

    try:
        # Verify the ID Token
        payload = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            audience=EXPECTED_AUDIENCE
        )
    except Exception as e:
        print("Token verification error:", e)
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Ensure that the token was issued by Google Chat
    if payload.get("email") != "chat@system.gserviceaccount.com":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
async def health_check(request: Request):
    return {"status": "ok"}


@app.post("/databot")
async def handle_databot_event(request: Request):
    event = await request.json()
    logger.info(f"Received event: {event}")

    user_message = event.get("chat", {}).get("messagePayload", {}).get("message", {}).get("text", "")

    # Extract user email
    user_email = event.get("chat", {}).get("user", {}).get("email", "unknown email")

    # Create the reply using the requested template
    reply_text = f"DATABOT message : {user_message} (email: {user_email})"

    response = build_response(reply_text)
    logger.info(f"Sending response: {response}")
    return response


@app.post("/peoplebot")
async def handle_peoplebot_event(request: Request):
    validate_request(request)

    event = await request.json()
    logger.info(f"Received event: {event}")

    user_message = event.get("chat", {}).get("messagePayload", {}).get("message", {}).get("text", "")

    # Extract user email
    user_email = event.get("chat", {}).get("user", {}).get("email", "unknown email")

    # Create the reply using the requested template
    reply_text = f"Boleh."

    response = build_response(reply_text)
    logger.info(f"Sending response: {response}")
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
