# Deployment Guide

1. Install Docker and Docker Compose.
2. Install or pull the desired Ollama models in the `ollama` service volume.
3. Start the stack:

```bash
./start.sh
```

4. Find the host IP:

```bash
hostname -I
```

5. Open `http://<host-ip>:6767` from phones, tablets, or laptops on the same WiFi.

The gateway is the only public service. Backend, frontend, and Ollama communicate on the internal Docker network.

If Docker Compose is unavailable but Podman is installed, build the backend and frontend images, then run them with host networking and use `nginx.host.conf` for the gateway.
