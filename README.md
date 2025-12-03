# Google Chat App

This is a simple Google Chat App. It handles Google Chat message and replies to the user.
I put this on github public as [the documentation](https://developers.google.com/workspace/add-ons/chat/quickstart-http?hl=en) is confusing.

Built with [FastAPI](https://fastapi.tiangolo.com/).

## Prerequisites

- Python 3.9+
- Docker (optional, for containerization)
- A Google Cloud Project with the Google Chat API enabled.

## Setup

1.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application:**
    Google Chat needs to access your service, consider ngrok or Render (use $PORT for Render).
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

## Google Chat API Configuration

To connect this bot to Google Chat, you need to configure the Google Chat API in the Google Cloud Console.

1.  **Go to the Google Chat API page:**
    [Google Cloud Console - Google Chat API](https://console.cloud.google.com/apis/library/chat.googleapis.com)

2.  **Enable the API** if it is not already enabled.

3.  **Click on "Manage"** and then go to the **"Configuration"** tab.

4.  **App Configuration:**
    -   **App name**: Give your bot a name.
    -   **Avatar URL**: Provide a URL for your bot's avatar.
    -   **Description**: A short description.

5.  **Interactive features:**
    -   Enable **"Receive 1:1 messages"** and **"Join spaces and group conversations"**.

6.  **Connection settings:**
    -   Select **"HTTP endpoint"**.
    -   **App URL**: Enter the public URL where your bot is deployed (e.g., your ngrok URL `https://your-ngrok-id.ngrok-free.app/` or your production URL).

7.  **Visibility:**
    -   Select who can install your app (e.g., "Specific people and groups" for testing).

8.  **Save** your changes.
