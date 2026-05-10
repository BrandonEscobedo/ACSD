---
title: AssignmentResult
id: application_assignment_use_case_assignmentresult
community: 7
source_file: backend/app/application/assignment_use_case.py
source_location: L19
file_type: code
tags:
  - graphify/node
  - community/7
  - type/code
---

# AssignmentResult

- Source: `backend/app/application/assignment_use_case.py` `L19`
- Type: `code`
- Community: [[_COMMUNITY_7|Community 7]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_
- --uses--> [[domain_linea_transportista_lineatransportista|LineaTransportista]] _[INFERRED 0.50]_

## Incoming

- [[backend_app_application_assignment_use_case_py|assignment_use_case.py]] --contains--> _[EXTRACTED 1.00]_
- [[application_assignment_use_case_assignmentusecase_ejecutar|.ejecutar()]] --calls--> _[EXTRACTED 1.00]_
