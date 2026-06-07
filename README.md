# Local WiFi AI Server

Local WiFi AI is a small Ollama-backed chat server for devices on the same network.

Open:

```text
http://<host-ip>:6767
```

The app shows a minimalist login screen, assigns each browser/device a persistent device ID, and redirects successful users to `/chat/<device-id>`.

## Architecture

- `gateway`: nginx, public LAN entrypoint on port `6767`.
- `frontend`: React chat UI.
- `backend`: FastAPI API for auth, sessions, chat, model status, model switching, and history.
- `ollama`: local model runtime.
- `sqlite`: local database at `backend/app/database/data/chat.db`.

## Model Policy

Default model: `phi3`.

Model IDs:

| ID | Model |
| --- | --- |
| M01 | phi3 |
| M02 | deepseek-coder |
| M03 | mistral |
| M04 | llama3 |
| M05 | llava |

The backend enforces one active generation at a time. If a user requests a different model while the runtime is busy, the API returns:

```text
UNABLE TO LOAD MODEL. PLEASE CONTINUE THE CONVERSATION WITH MODEL ID: X
```

Before switching models, the previous model is unloaded through Ollama `keep_alive: 0`.

## Run

```bash
chmod +x start.sh
./start.sh
```

Then open `http://<host-ip>:6767` from any device on the same WiFi network.

Default API key:

```text
thoovara@hari
```

## Reset Runtime State

To clear local session/history data:

```bash
rm -f backend/app/database/data/chat.db
```

To ask Ollama to unload all managed models:

```bash
for model in phi3 deepseek-coder mistral llama3 llava; do
  curl -s http://localhost:11434/api/generate -d "{\"model\":\"$model\",\"stream\":false,\"keep_alive\":0}" >/dev/null
done
```
