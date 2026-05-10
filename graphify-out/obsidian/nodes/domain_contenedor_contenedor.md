---
title: Contenedor
id: domain_contenedor_contenedor
community: 0
source_file: backend/app/domain/contenedor.py
source_location: L8
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# Contenedor

- Source: `backend/app/domain/contenedor.py` `L8`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --uses--> [[domain_base_entity|Entity]] _[INFERRED 0.50]_
- --inherits--> [[entity|Entity]] _[EXTRACTED 1.00]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_

## Incoming

- [[routers_assignment_assign_line|assign_line()]] --calls--> _[INFERRED 0.80]_
- [[routers_reports_dispatch_report|dispatch_report()]] --calls--> _[INFERRED 0.80]_
- [[application_assignment_use_case_assignmentresult|AssignmentResult]] --uses--> _[INFERRED 0.50]_
- [[application_assignment_use_case_assignmentusecase|AssignmentUseCase]] --uses--> _[INFERRED 0.50]_
- [[application_report_use_case_reportusecase|ReportUseCase]] --uses--> _[INFERRED 0.50]_
- [[application_simulation_use_case_simulationresult|SimulationResult]] --uses--> _[INFERRED 0.50]_
- [[application_simulation_use_case_simulationusecase|SimulationUseCase]] --uses--> _[INFERRED 0.50]_
- [[backend_app_domain_contenedor_py|contenedor.py]] --contains--> _[EXTRACTED 1.00]_
- [[services_container_monitor_monitorconfig|MonitorConfig]] --uses--> _[INFERRED 0.50]_
- [[services_container_monitor_containermonitor|ContainerMonitor]] --uses--> _[INFERRED 0.50]_
- [[services_pdf_service_pdfservice|PDFService]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulacionengine|SimulacionEngine]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulador|_Simulador]] --uses--> _[INFERRED 0.50]_
- [[services_container_monitor_containermonitor_make_container|._make_container()]] --calls--> _[INFERRED 0.80]_
- [[services_simulation_engine_simulador_generador|._generador()]] --calls--> _[INFERRED 0.80]_
