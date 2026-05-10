---
title: TipoCarga
id: domain_enums_tipocarga
community: 0
source_file: backend/app/domain/enums.py
source_location: L4
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# TipoCarga

- Source: `backend/app/domain/enums.py` `L4`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --inherits--> [[str]] _[EXTRACTED 1.00]_
- --inherits--> [[enum|Enum]] _[EXTRACTED 1.00]_

## Incoming

- [[routers_assignment_assign_line|assign_line()]] --calls--> _[INFERRED 0.80]_
- [[routers_reports_dispatch_report|dispatch_report()]] --calls--> _[INFERRED 0.80]_
- [[application_assignment_use_case_assignmentresult|AssignmentResult]] --uses--> _[INFERRED 0.50]_
- [[application_assignment_use_case_assignmentusecase|AssignmentUseCase]] --uses--> _[INFERRED 0.50]_
- [[domain_contenedor_contenedor|Contenedor]] --uses--> _[INFERRED 0.50]_
- [[backend_app_domain_enums_py|enums.py]] --contains--> _[EXTRACTED 1.00]_
- [[services_container_monitor_monitorconfig|MonitorConfig]] --uses--> _[INFERRED 0.50]_
- [[services_container_monitor_containermonitor|ContainerMonitor]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulacionengine|SimulacionEngine]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulador|_Simulador]] --uses--> _[INFERRED 0.50]_
