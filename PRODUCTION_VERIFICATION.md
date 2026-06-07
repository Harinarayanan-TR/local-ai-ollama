# Production Verification

Verification performed during delivery:

- Backend Python syntax compilation.
- Frontend production build.
- API schema review for auth, chat, status, switching, and history.
- Database reset before final launch.
- Runtime model unload requests sent for managed models when Ollama is reachable.
- Docker Compose launch on gateway port `6767`.

Expected manual smoke test:

1. Open `http://<host-ip>:6767`.
2. Login with the configured API key.
3. Confirm redirect to `/chat/<device-id>`.
4. Send a Phi-3 message.
5. Open a second device/browser and confirm it gets separate history.
6. Attempt concurrent heavy model requests and confirm one is rejected with the required model ID message.
