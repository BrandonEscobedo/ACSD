---
title: ._auto_advance()
id: services_container_monitor_containermonitor_auto_advance
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L170
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# ._auto_advance()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L170`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_move_to_piso|.move_to_piso()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_move_to_patio|.move_to_patio()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_add_container|.add_container()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_generator_loop|._generator_loop()]] --calls--> _[EXTRACTED 1.00]_
