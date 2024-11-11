import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request

load_dotenv(find_dotenv())

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

app = App(token=SLACK_BOT_TOKEN)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


def get_bot_user_id():
    try:
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")


def my_function(text):
    response = text.upper()
    return response


@app.event("app_mention")
def handle_mentions(body, say):
    text = body["event"]["text"]

    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    response = my_function(text)
    say(response)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run()