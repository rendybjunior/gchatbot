from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

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
    event = await request.json()
    logger.info(f"Received event: {event}")

    user_message = event.get("chat", {}).get("messagePayload", {}).get("message", {}).get("text", "")

    # Extract user email
    user_email = event.get("chat", {}).get("user", {}).get("email", "unknown email")

    # Create the reply using the requested template
    reply_text = f"PEOPLEBOT message : {user_message} (email: {user_email})"

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
