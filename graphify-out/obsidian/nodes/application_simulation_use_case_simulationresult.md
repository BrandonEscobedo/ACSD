---
title: SimulationResult
id: application_simulation_use_case_simulationresult
community: 0
source_file: backend/app/application/simulation_use_case.py
source_location: L10
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# SimulationResult

- Source: `backend/app/application/simulation_use_case.py` `L10`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_evento_eventosimulacion|EventoSimulacion]] _[INFERRED 0.50]_
- --uses--> [[services_simulation_engine_simulacionengine|SimulacionEngine]] _[INFERRED 0.50]_

## Incoming

- [[backend_app_application_simulation_use_case_py|simulation_use_case.py]] --contains--> _[EXTRACTED 1.00]_
- [[application_simulation_use_case_simulationusecase_ejecutar|.ejecutar()]] --calls--> _[EXTRACTED 1.00]_
