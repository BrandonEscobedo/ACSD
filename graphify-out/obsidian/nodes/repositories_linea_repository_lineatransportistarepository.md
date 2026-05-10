---
title: LineaTransportistaRepository
id: repositories_linea_repository_lineatransportistarepository
community: 7
source_file: backend/app/infrastructure/repositories/linea_repository.py
source_location: L8
file_type: code
tags:
  - graphify/node
  - community/7
  - type/code
---

# LineaTransportistaRepository

- Source: `backend/app/infrastructure/repositories/linea_repository.py` `L8`
- Type: `code`
- Community: [[_COMMUNITY_7|Community 7]]

## Outgoing

- --uses--> [[domain_linea_transportista_lineatransportista|LineaTransportista]] _[INFERRED 0.50]_
- --method--> [[repositories_linea_repository_lineatransportistarepository_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[repositories_linea_repository_lineatransportistarepository_get_all|.get_all()]] _[EXTRACTED 1.00]_

## Incoming

- [[api_dependencies_linea_repository|_linea_repository()]] --calls--> _[INFERRED 0.80]_
- [[backend_app_infrastructure_repositories_linea_repository_py|linea_repository.py]] --contains--> _[EXTRACTED 1.00]_
