---
title: ._arrive_in_buque()
id: services_container_monitor_containermonitor_arrive_in_buque
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L122
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# ._arrive_in_buque()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L122`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_log|._log()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_add_container|.add_container()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_generator_loop|._generator_loop()]] --calls--> _[EXTRACTED 1.00]_
