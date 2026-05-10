---
title: EventoSimulacion
id: domain_evento_eventosimulacion
community: 0
source_file: backend/app/domain/evento.py
source_location: L5
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# EventoSimulacion

- Source: `backend/app/domain/evento.py` `L5`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Incoming

- [[application_simulation_use_case_simulationresult|SimulationResult]] --uses--> _[INFERRED 0.50]_
- [[application_simulation_use_case_simulationusecase|SimulationUseCase]] --uses--> _[INFERRED 0.50]_
- [[backend_app_domain_evento_py|evento.py]] --contains--> _[EXTRACTED 1.00]_
- [[services_simulation_engine_simulacionengine|SimulacionEngine]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulador|_Simulador]] --uses--> _[INFERRED 0.50]_
- [[services_simulation_engine_simulador_registrar|._registrar()]] --calls--> _[INFERRED 0.80]_
