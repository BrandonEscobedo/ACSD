---
title: .get_state()
id: services_container_monitor_containermonitor_get_state
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L49
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# .get_state()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L49`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[services_container_monitor_containermonitor_ser|._ser()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_broadcast|._broadcast()]] --calls--> _[EXTRACTED 1.00]_
