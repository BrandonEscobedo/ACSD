---
title: AssignmentUseCase
id: application_assignment_use_case_assignmentusecase
community: 7
source_file: backend/app/application/assignment_use_case.py
source_location: L24
file_type: code
tags:
  - graphify/node
  - community/7
  - type/code
---

# AssignmentUseCase

- Source: `backend/app/application/assignment_use_case.py` `L24`
- Type: `code`
- Community: [[_COMMUNITY_7|Community 7]]

## Outgoing

- --method--> [[application_assignment_use_case_assignmentusecase_ejecutar|.ejecutar()]] _[EXTRACTED 1.00]_
- --method--> [[application_assignment_use_case_assignmentusecase_calcular_eir|._calcular_eir()]] _[EXTRACTED 1.00]_
- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_
- --uses--> [[domain_linea_transportista_lineatransportista|LineaTransportista]] _[INFERRED 0.50]_

## Incoming

- [[api_dependencies_get_assignment_use_case|get_assignment_use_case()]] --calls--> _[INFERRED 0.80]_
- [[backend_app_application_assignment_use_case_py|assignment_use_case.py]] --contains--> _[EXTRACTED 1.00]_
