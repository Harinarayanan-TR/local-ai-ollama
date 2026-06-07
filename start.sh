#!/usr/bin/env bash
set -euo pipefail

HOST_IP="$(hostname -I | awk '{print $1}')"

echo "Starting Local WiFi AI on http://${HOST_IP}:6767"
docker compose up --build -d
docker compose ps
