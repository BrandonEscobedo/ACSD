---
title: WebSocketManager
id: services_websocket_manager_websocketmanager
community: 11
source_file: backend/app/infrastructure/services/websocket_manager.py
source_location: L7
file_type: code
tags:
  - graphify/node
  - community/11
  - type/code
---

# WebSocketManager

- Source: `backend/app/infrastructure/services/websocket_manager.py` `L7`
- Type: `code`
- Community: [[_COMMUNITY_11|Community 11]]

## Outgoing

- --method--> [[services_websocket_manager_websocketmanager_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[services_websocket_manager_websocketmanager_connect|.connect()]] _[EXTRACTED 1.00]_
- --method--> [[services_websocket_manager_websocketmanager_disconnect|.disconnect()]] _[EXTRACTED 1.00]_
- --method--> [[services_websocket_manager_websocketmanager_broadcast|.broadcast()]] _[EXTRACTED 1.00]_

## Incoming

- [[api_dependencies_get_ws_manager|get_ws_manager()]] --calls--> _[INFERRED 0.80]_
- [[services_container_monitor_monitorconfig|MonitorConfig]] --uses--> _[INFERRED 0.50]_
- [[services_container_monitor_containermonitor|ContainerMonitor]] --uses--> _[INFERRED 0.50]_
- [[backend_app_infrastructure_services_websocket_manager_py|websocket_manager.py]] --contains--> _[EXTRACTED 1.00]_
