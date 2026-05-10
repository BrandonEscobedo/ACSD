---
title: MonitorConfig
id: services_container_monitor_monitorconfig
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L19
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# MonitorConfig

- Source: `backend/app/infrastructure/services/container_monitor.py` `L19`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_
- --uses--> [[services_visual_service_visualservice|VisualService]] _[INFERRED 0.50]_
- --uses--> [[services_websocket_manager_websocketmanager|WebSocketManager]] _[INFERRED 0.50]_

## Incoming

- [[backend_app_infrastructure_services_container_monitor_py|container_monitor.py]] --contains--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_init|.__init__()]] --calls--> _[EXTRACTED 1.00]_
