---
title: LineaTransportista
id: domain_linea_transportista_lineatransportista
community: 7
source_file: backend/app/domain/linea_transportista.py
source_location: L6
file_type: code
tags:
  - graphify/node
  - community/7
  - type/code
---

# LineaTransportista

- Source: `backend/app/domain/linea_transportista.py` `L6`
- Type: `code`
- Community: [[_COMMUNITY_7|Community 7]]

## Outgoing

- --uses--> [[domain_base_entity|Entity]] _[INFERRED 0.50]_
- --inherits--> [[entity|Entity]] _[EXTRACTED 1.00]_

## Incoming

- [[application_assignment_use_case_assignmentresult|AssignmentResult]] --uses--> _[INFERRED 0.50]_
- [[application_assignment_use_case_assignmentusecase|AssignmentUseCase]] --uses--> _[INFERRED 0.50]_
- [[backend_app_domain_linea_transportista_py|linea_transportista.py]] --contains--> _[EXTRACTED 1.00]_
- [[repositories_linea_repository_lineatransportistarepository|LineaTransportistaRepository]] --uses--> _[INFERRED 0.50]_
- [[repositories_linea_repository_lineatransportistarepository_get_all|.get_all()]] --calls--> _[INFERRED 0.80]_
