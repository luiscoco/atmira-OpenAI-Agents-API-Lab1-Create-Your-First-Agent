"""Lab 1: run one Agents API task and explain its event stream."""

import argparse
import os

from openai import OpenAI

MODEL = "gpt-6-sol"
INSTRUCTIONS = "You are a patient Python tutor. Answer clearly and briefly."
QUESTION = "What is a Python function? Give one short example."


def show_events(events, raw_events: bool) -> None:
    """Display one streamed turn, keeping the low-level events available."""
    completed = False
    answer_started = False

    for event in events:
        if raw_events:
            print(event.to_json(indent=None), flush=True)
        else:
            if event.type == "agent.session.created":
                print(f"[1] Session created: {event.session.id}")
            elif event.type == "agent.session.turn.in_progress":
                print("[2] Agent is working...")
            elif event.type == "agent.session.turn.output_text.delta":
                if not answer_started:
                    print("[3] Agent answer:\n")
                    answer_started = True
                print(event.delta, end="", flush=True)
            elif event.type == "agent.session.turn.completed":
                if answer_started:
                    print("\n")
                print("Turn completed successfully.")

        if event.type == "agent.session.turn.completed":
            completed = True
        elif event.type in {
            "agent.session.turn.failed",
            "agent.session.turn.cancelled",
            "agent.session.failed",
        }:
            raise SystemExit(f"Agent run ended with: {event.type}")

    if not completed:
        raise SystemExit("The stream ended without a completed turn. Check the session status.")

    if not raw_events:
        print("\nWhat happened: a session started, the answer arrived in pieces, and the turn completed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 1: your first Agents API session")
    parser.add_argument(
        "--raw-events",
        action="store_true",
        help="Print every JSON event instead of the learner-friendly view",
    )
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY before running this lab.")

    if not args.raw_events:
        print("LAB 1 | YOUR FIRST AGENTS API SESSION")
        print(f"Model: {MODEL}")
        print(f"Question: {QUESTION}\n")

    with OpenAI() as client:
        with client.beta.agents.sessions.create(
            agent={
                "model": MODEL,
                "instructions": INSTRUCTIONS,
            },
            environment={"type": "none"},
            input=QUESTION,
            stream=True,
        ) as events:
            show_events(events, args.raw_events)


if __name__ == "__main__":
    main()
