# Project Summary

This project implements a local WiFi AI chat server backed by Ollama.

Key behavior:

- Public LAN entrypoint is `http://<host-ip>:6767`.
- Login page is minimalist and network-accessible.
- Each browser/device receives a persistent device ID.
- Chat history is stored per device session.
- Auto-select is enabled by default, but routes conservatively to keep Phi-3 as the normal model.
- Manual model selection is available in the dashboard.
- Backend model execution is guarded by a single generation lock.
- Model switching unloads the previous model before allowing another model to generate.
