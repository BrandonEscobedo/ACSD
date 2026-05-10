---
title: AssignmentResponse
id: schemas_assignment_assignmentresponse
community: 8
source_file: backend/app/api/schemas/assignment.py
source_location: L25
file_type: code
tags:
  - graphify/node
  - community/8
  - type/code
---

# AssignmentResponse

- Source: `backend/app/api/schemas/assignment.py` `L25`
- Type: `code`
- Community: [[_COMMUNITY_8|Community 8]]

## Outgoing

- --inherits--> [[basemodel|BaseModel]] _[EXTRACTED 1.00]_
- --uses--> [[schemas_simulation_contenedorschema|ContenedorSchema]] _[INFERRED 0.50]_

## Incoming

- [[routers_assignment_assign_line|assign_line()]] --calls--> _[INFERRED 0.80]_
- [[backend_app_api_schemas_assignment_py|assignment.py]] --contains--> _[EXTRACTED 1.00]_
