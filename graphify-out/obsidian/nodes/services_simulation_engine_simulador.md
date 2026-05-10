---
title: _Simulador
id: services_simulation_engine_simulador
community: 0
source_file: backend/app/infrastructure/services/simulation_engine.py
source_location: L29
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# _Simulador

- Source: `backend/app/infrastructure/services/simulation_engine.py` `L29`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_
- --uses--> [[domain_evento_eventosimulacion|EventoSimulacion]] _[INFERRED 0.50]_
- --method--> [[services_simulation_engine_simulador_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[services_simulation_engine_simulador_registrar|._registrar()]] _[EXTRACTED 1.00]_
- --method--> [[services_simulation_engine_simulador_proceso_contenedor|._proceso_contenedor()]] _[EXTRACTED 1.00]_
- --method--> [[services_simulation_engine_simulador_generador|._generador()]] _[EXTRACTED 1.00]_
- --method--> [[services_simulation_engine_simulador_colocar_en_patio|._colocar_en_patio()]] _[EXTRACTED 1.00]_
- --uses--> [[services_visual_service_visualservice|VisualService]] _[INFERRED 0.50]_

## Incoming

- [[backend_app_infrastructure_services_simulation_engine_py|simulation_engine.py]] --contains--> _[EXTRACTED 1.00]_
- [[services_simulation_engine_simulacionengine_ejecutar|.ejecutar()]] --calls--> _[EXTRACTED 1.00]_
