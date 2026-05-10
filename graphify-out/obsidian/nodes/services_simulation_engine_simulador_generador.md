---
title: ._generador()
id: services_simulation_engine_simulador_generador
community: 0
source_file: backend/app/infrastructure/services/simulation_engine.py
source_location: L84
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# ._generador()

- Source: `backend/app/infrastructure/services/simulation_engine.py` `L84`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --calls--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.80]_
- --calls--> [[services_simulation_engine_simulador_proceso_contenedor|._proceso_contenedor()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_simulation_engine_simulacionengine_ejecutar|.ejecutar()]] --calls--> _[EXTRACTED 1.00]_
- [[services_simulation_engine_simulador|_Simulador]] --method--> _[EXTRACTED 1.00]_
