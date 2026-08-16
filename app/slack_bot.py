import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from app.agent import agent

load_dotenv()

slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"]
)

processed_events = set()


@slack_app.event("app_mention")
def handle_mention(body, event, say):
    event_id = body.get("event_id")

    if event_id in processed_events:
        return

    processed_events.add(event_id)

    text = event.get("text", "").strip()

    if not text:
        return

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    })

    answer = result["messages"][-1].content

    say(answer)


if __name__ == "__main__":
    SocketModeHandler(
        slack_app,
        os.environ["SLACK_APP_TOKEN"]
    ).start()