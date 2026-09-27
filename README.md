# Sample 1 — Your first OpenAI Agents API session

This is Lab 1 of a planned 50-lab course. You will create one agent, give it one task, and inspect the events returned by the Agents API. This lab uses the **Agents API** through the `openai` Python package (`client.beta.agents`), not the separate Agents SDK (`openai-agents`).

## Learning goals

- Identify the agent's model and instructions.
- Start a session with a user task.
- Recognize a completed turn in the event stream.

## Prerequisites

- Python 3.10 or newer.
- An OpenAI Platform application API key with `api.agents.read`, `api.agents.write`, and `api.responses.write` permissions. API usage may incur charges.

## Run the lab

From this folder, create an environment and install the dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY = "your-application-api-key"
python main.py
```

On macOS or Linux, activate with `source .venv/bin/activate` and set the key with `export OPENAI_API_KEY="your-application-api-key"`.

Keep your key out of source files and course screenshots. The SDK reads it from the environment.

## What the code does

1. `OpenAI()` creates the client.
2. `agent` supplies the model and the instructions that guide its behavior.
3. `environment={"type": "none"}` gives this text-only agent no sandbox. Later labs can add a hosted sandbox, tools, and files.
4. `input` is the learner's question. `stream=True` returns progress events. The script turns these into a short timeline and prints the answer as readable text.

The answer text varies between runs. A successful run shows **Session created**, **Agent is working**, **Agent answer**, and **Turn completed successfully**. The answer arrives in small `output_text.delta` pieces. The script prints those pieces without the surrounding JSON.

To see the original event stream, run:

```powershell
python main.py --raw-events
```

In raw mode, find `agent.session.turn.completed`. An `agent.session.idle` event alone does not establish success. The script exits with an error if a turn fails, is cancelled, or the stream ends without a completed turn.

## Student exercise

Change `QUESTION` to ask about Python lists. Run the script again. Then change `INSTRUCTIONS` to request a two-sentence answer and compare the outputs. Finally, run with `--raw-events` and locate the events that produced the readable timeline. Each run starts a new session; this lab does not continue a previous one.

## Troubleshooting

- `ModuleNotFoundError: openai`: activate the virtual environment and install `requirements.txt`.
- `Set OPENAI_API_KEY`: set the variable in the same terminal used to run the script.
- Authentication or permission error: check that you used an application API key with the permissions above.
- Model access error: confirm that your project can use the model shown in `main.py`.

## Official OpenAI documentation

- [Agents API quickstart](https://developers.openai.com/api/docs/guides/agents-api/quickstart)
- [Agents API overview](https://developers.openai.com/api/docs/guides/agents-api/overview)
