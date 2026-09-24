# Real-time Decision Matrix

## Candidates
Polling, SSE, WebSockets, MQTT, queues/streams.

## Rules
- Low-frequency one-way updates: polling may be sufficient.
- Server-to-browser event stream: evaluate SSE.
- Bidirectional low-latency interaction: evaluate WebSockets.
- Device/IoT telemetry: evaluate MQTT.
- Durable multi-consumer event processing: evaluate a queue/stream platform.

Choose the simplest mechanism satisfying freshness, delivery, ordering, reconnection, scale, and infrastructure requirements.
