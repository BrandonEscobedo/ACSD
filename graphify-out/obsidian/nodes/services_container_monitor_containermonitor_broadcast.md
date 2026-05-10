---
title: ._broadcast()
id: services_container_monitor_containermonitor_broadcast
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L83
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# ._broadcast()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L83`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_get_state|.get_state()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_move_to_piso|.move_to_piso()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_move_to_patio|.move_to_patio()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_remove_from_patio|.remove_from_patio()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_add_container|.add_container()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_start_auto|.start_auto()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_stop_auto|.stop_auto()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_generator_loop|._generator_loop()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_reset|.reset()]] --calls--> _[EXTRACTED 1.00]_
