---
title: get_monitor()
id: api_dependencies_get_monitor
community: 6
source_file: backend/app/api/dependencies.py
source_location: L41
file_type: code
tags:
  - graphify/node
  - community/6
  - type/code
---

# get_monitor()

- Source: `backend/app/api/dependencies.py` `L41`
- Type: `code`
- Community: [[_COMMUNITY_6|Community 6]]

## Outgoing

- --calls--> [[api_dependencies_get_ws_manager|get_ws_manager()]] _[EXTRACTED 1.00]_
- --calls--> [[services_visual_service_visualservice|VisualService]] _[INFERRED 0.80]_
- --calls--> [[services_container_monitor_containermonitor|ContainerMonitor]] _[INFERRED 0.80]_

## Incoming

- [[backend_main_lifespan|lifespan()]] --calls--> _[INFERRED 0.80]_
- [[backend_app_api_dependencies_py|dependencies.py]] --contains--> _[EXTRACTED 1.00]_
