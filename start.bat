@echo off
echo Starting Local WiFi AI on http://HOST-IP:6767
docker compose up --build -d
docker compose ps
