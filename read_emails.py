import json
import os

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        refreshed = False
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                refreshed = True
            except RefreshError:
                # Token expired (happens after 7 days for Google apps in "Testing" mode).
                print("Token expired. Please log in again in the browser.")
        if not refreshed:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def parse_json_list(text):
    """Extract a JSON list from the AI response (handles ```json fences or extra text)."""
    text = (text or "").replace("```json", "").replace("```", "").strip()
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("AI did not return a JSON list: " + text[:200])
    data = json.loads(text[start:end + 1])
    return [d for d in data if isinstance(d, dict)]


def main():
    service = get_service()
    results = service.users().messages().list(userId="me", maxResults=10).execute()
    for m in results.get("messages", []):
        msg = service.users().messages().get(
            userId="me", id=m["id"], format="metadata",
            metadataHeaders=["From", "Subject"]
        ).execute()
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        print(headers.get("From"), "|", headers.get("Subject"))


if __name__ == "__main__":
    main()
