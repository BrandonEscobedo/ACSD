---
title: SimulationUseCase
id: application_simulation_use_case_simulationusecase
community: 0
source_file: backend/app/application/simulation_use_case.py
source_location: L16
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# SimulationUseCase

- Source: `backend/app/application/simulation_use_case.py` `L16`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --method--> [[application_simulation_use_case_simulationusecase_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[application_simulation_use_case_simulationusecase_ejecutar|.ejecutar()]] _[EXTRACTED 1.00]_
- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_evento_eventosimulacion|EventoSimulacion]] _[INFERRED 0.50]_
- --uses--> [[services_simulation_engine_simulacionengine|SimulacionEngine]] _[INFERRED 0.50]_

## Incoming

- [[backend_app_application_simulation_use_case_py|simulation_use_case.py]] --contains--> _[EXTRACTED 1.00]_
