---
title: VisualService
id: services_visual_service_visualservice
community: 6
source_file: backend/app/infrastructure/services/visual_service.py
source_location: L9
file_type: code
tags:
  - graphify/node
  - community/6
  - type/code
---

# VisualService

- Source: `backend/app/infrastructure/services/visual_service.py` `L9`
- Type: `code`
- Community: [[_COMMUNITY_6|Community 6]]

## Outgoing

- --method--> [[services_visual_service_visualservice_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[services_visual_service_visualservice_load|._load()]] _[EXTRACTED 1.00]_
- --method--> [[services_visual_service_visualservice_get_random|.get_random()]] _[EXTRACTED 1.00]_

## Incoming

- [[api_dependencies_get_monitor|get_monitor()]] --calls--> _[INFERRED 0.80]_
- [[services_container_monitor_monitorconfig|MonitorConfig]] --uses--> _[INFERRED 0.50]_
- [[services_container_monitor_containermonitor|ContainerMonitor]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulacionengine|SimulacionEngine]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulador|_Simulador]] --uses--> _[INFERRED 0.50]_
- [[backend_app_infrastructure_services_visual_service_py|visual_service.py]] --contains--> _[EXTRACTED 1.00]_
