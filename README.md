# Local WiFi AI Server

Local WiFi AI is a lightweight, self-hosted chat server powered by Ollama, designed for seamless access across devices on the same network.

Users can connect through a browser, authenticate via a minimal interface, and interact with locally hosted AI models in a clean chat environment.

---

## Overview

The system provides a private, LAN-based AI experience without relying on cloud services. Each device is assigned a persistent identifier, enabling session continuity and personalized chat access.

After authentication, users are redirected to a dedicated chat endpoint tied to their device.

---

## Architecture

The system is composed of the following services:

* **Gateway**
  Nginx-based entry point exposed on the local network, handling routing and external access.

* **Frontend**
  A React-based user interface providing a responsive and minimal chat experience.

* **Backend**
  A FastAPI service managing authentication, session handling, chat processing, model orchestration, and conversation history.

* **Ollama Runtime**
  Responsible for running and managing local AI models.

* **Database**
  SQLite-based storage for session data and chat history.

---

## Model Management

The system supports multiple AI models, with a default model preconfigured.

### Default Model

* `phi3`

### Available Models

| ID  | Model          |
| --- | -------------- |
| M01 | phi3           |
| M02 | deepseek-coder |
| M03 | mistral        |
| M04 | llama3         |
| M05 | llava          |

---

## Runtime Behavior

* Only one model can actively generate responses at any given time.
* If a request is made while another model is active, the system prevents switching and returns a structured response indicating the active model.
* Model switching is handled safely by unloading the current model before initializing another, ensuring efficient resource usage.

---

## Session & Identity

* Each device is assigned a persistent device ID.
* Sessions are tied to this ID, allowing users to resume conversations across visits.
* Chat access is scoped per device via a dedicated endpoint.

---

## Data Handling

* Chat history and session data are stored locally.
* The system operates entirely within the local network, ensuring privacy and full data control.

---

## Authentication

A default API key is configured for access control. This can be modified for enhanced security in production environments.

---

## Design Philosophy

* **Local-first**: No dependency on external APIs or cloud services
* **Lightweight**: Minimal resource overhead
* **Private**: All data remains within the local network
* **Extensible**: Modular architecture for future enhancements

--- 

## Future Scope

* Multi-user role management
* Advanced analytics dashboard
* AI-assisted automation features
* Enhanced model orchestration and scaling

---

Local WiFi AI is built as a foundation for private, scalable, and customizable AI systems within controlled network environments.

**SHOULD HAVE OLLAMA PRE-INSTALLED WITH llama3, llava, mistral, deepseekcoder and phi3 PULLED**
