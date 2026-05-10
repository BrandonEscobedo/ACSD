---
title: ._make_container()
id: services_container_monitor_containermonitor_make_container
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L96
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# ._make_container()

- Source: `backend/app/infrastructure/services/container_monitor.py` `L96`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --calls--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.80]_

## Incoming

- [[services_container_monitor_containermonitor|ContainerMonitor]] --method--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_add_container|.add_container()]] --calls--> _[EXTRACTED 1.00]_
- [[services_container_monitor_containermonitor_generator_loop|._generator_loop()]] --calls--> _[EXTRACTED 1.00]_
