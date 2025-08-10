# Reasoning Trainer with LLM

This project provides a simple yet extensible backend for a Socratic reasoning trainer. Users can start a session, engage in a back‑and‑forth conversation over WebSockets, and receive both probing questions and numerical "Reasoning Quality Index" (RQI) scores from a large language model (LLM). The service is built on top of FastAPI and is designed to run anywhere Python is available.

## Features

- Session management via REST endpoints (`/session/start`, `/session/{id}/end`)
- Live interactions over WebSocket where each user message is followed by a model‑generated question and a numeric RQI score
- LLM abstraction so you can swap out OpenAI for another provider by extending `reasoning_app.llm.LLMService`
- Minimal HTML client served from `/` for manual testing
- Progress summary endpoint to monitor active sessions

## Configuration

Configuration values are read from environment variables at runtime via `reasoning_app.config.Settings`. Key variables include:

| Variable         | Description                                              | Default |
|------------------|----------------------------------------------------------|---------|
| `LLM_PROVIDER`   | Name of the LLM provider implementation                 | `openai` |
| `OPENAI_API_KEY` | API key for OpenAI; required when using the OpenAI LLM   | _none_ |
| `OPENAI_MODEL`   | Name of the OpenAI model to use                          | `gpt-5` |
| `TEMPERATURE`    | Sampling temperature for responses                       | `0.2` |

For production deployments you should set `OPENAI_API_KEY` to your own secret value. See `config.py` for details.

## Running the server

Assuming you have Python 3.10 or later installed, install the required packages and start the server like so:

```sh
pip install fastapi uvicorn openai
export OPENAI_API_KEY=sk-...your-key...
uvicorn reasoning_app.app:app --reload
```

Once running, visit `http://localhost:8000/` in your browser to try out the demo client. You can also interact with the API via curl or Postman.

## Extending to other providers

If you wish to support a different LLM provider, create a subclass of `reasoning_app.llm.LLMService` and implement the `generate` method. Then set the environment variable `LLM_PROVIDER` to the name of your implementation.
