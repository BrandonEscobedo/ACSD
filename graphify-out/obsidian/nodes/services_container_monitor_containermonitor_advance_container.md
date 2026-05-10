---
title: .advance_container()
id: services_container_monitor_containermonitor_advance_container
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L192
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# .advance_container()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L192`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_move_to_piso|.move_to_piso()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_move_to_patio|.move_to_patio()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
