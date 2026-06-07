# API Reference

Base URL through the LAN gateway:

```text
http://<host-ip>:6767/api
```

## POST /auth/login

Request:

```json
{
  "api_key": "thoovara@hari",
  "device_id": "browser-generated-device-id"
}
```

Response:

```json
{
  "success": true,
  "session_id": "uuid",
  "device_id": "browser-generated-device-id",
  "message": "Welcome! Session ... created"
}
```

## POST /chat/send

Request:

```json
{
  "session_id": "uuid",
  "message": "Hello",
  "model": "phi3",
  "auto_mode": true
}
```

Response:

```json
{
  "response": "AI response text",
  "model_used": "phi3",
  "session_id": "uuid",
  "tokens_used": 42,
  "blocked": false
}
```

## GET /chat/status

Returns current model, model IDs, available models, and whether a generation is active.

## POST /chat/switch-model

Switches the active model when the runtime is idle.

## GET /chat/history/{session_id}

Returns chat history for the authenticated device session.
