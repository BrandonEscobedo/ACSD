---
title: ._proceso_contenedor()
id: services_simulation_engine_simulador_proceso_contenedor
community: 0
source_file: backend/app/infrastructure/services/simulation_engine.py
source_location: L50
file_type: code
tags:
  - graphify/node
  - community/0
  - type/code
---

# ._proceso_contenedor()

- Source: `backend/app/infrastructure/services/simulation_engine.py` `L50`
- Type: `code`
- Community: [[_COMMUNITY_0|Community 0]]

## Outgoing

- --calls--> [[services_simulation_engine_simulador_registrar|._registrar()]] _[EXTRACTED 1.00]_
- --calls--> [[services_simulation_engine_simulador_colocar_en_patio|._colocar_en_patio()]] _[EXTRACTED 1.00]_

## Incoming

- [[services_simulation_engine_simulador|_Simulador]] --method--> _[EXTRACTED 1.00]_
- [[services_simulation_engine_simulador_generador|._generador()]] --calls--> _[EXTRACTED 1.00]_
