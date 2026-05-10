---
title: .move_to_piso()
id: services_container_monitor_containermonitor_move_to_piso
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L127
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# .move_to_piso()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L127`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_broadcast|._broadcast()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_log|._log()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_auto_advance|._auto_advance()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_advance_container|.advance_container()]] --calls--> _[EXTRACTED 1.00]_
