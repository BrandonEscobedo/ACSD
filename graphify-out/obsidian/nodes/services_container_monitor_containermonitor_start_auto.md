---
title: .start_auto()
id: services_container_monitor_containermonitor_start_auto
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L199
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# .start_auto()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L199`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_broadcast|._broadcast()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_log|._log()]] _[EXTRACTED 1.00]_
- --calls--> [[services_container_monitor_containermonitor_generator_loop|._generator_loop()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
