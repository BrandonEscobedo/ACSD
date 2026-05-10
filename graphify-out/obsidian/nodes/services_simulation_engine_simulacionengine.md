---
title: SimulacionEngine
id: services_simulation_engine_simulacionengine
community: 0
source_file: backend/app/infrastructure/services/simulation_engine.py
source_location: L16
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# SimulacionEngine

- Source: `backend/app/infrastructure/services/simulation_engine.py` `L16`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_
- --uses--> [[domain_evento_eventosimulacion|EventoSimulacion]] _[INFERRED 0.50]_
- --method--> [[services_simulation_engine_simulacionengine_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[services_simulation_engine_simulacionengine_ejecutar|.ejecutar()]] _[EXTRACTED 1.00]_
- --uses--> [[services_visual_service_visualservice|VisualService]] _[INFERRED 0.50]_

## Incoming

- [[application_simulation_use_case_simulationresult|SimulationResult]] --uses--> _[INFERRED 0.50]_
- [[application_simulation_use_case_simulationusecase|SimulationUseCase]] --uses--> _[INFERRED 0.50]_
- [[backend_app_infrastructure_services_simulation_engine_py|simulation_engine.py]] --contains--> _[EXTRACTED 1.00]_
