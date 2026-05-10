---
title: ._generator_loop()
id: services_container_monitor_containermonitor_generator_loop
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L217
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# ._generator_loop()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L217`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_broadcast|._broadcast()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_make_container|._make_container()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_arrive_in_buque|._arrive_in_buque()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_auto_advance|._auto_advance()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_start_auto|.start_auto()]] --calls--> _[EXTRACTED 1.00]_
