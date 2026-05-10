---
title: ReportUseCase
id: application_report_use_case_reportusecase
community: 6
source_file: backend/app/application/report_use_case.py
source_location: L7
file_type: code
tags:
  - graphify/node
  - community/6
  - type/code
---

# ReportUseCase

- Source: `backend/app/application/report_use_case.py` `L7`
- Type: `code`
- Community: [[_COMMUNITY_6|Community 6]]

## Outgoing

- --method--> [[application_report_use_case_reportusecase_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[application_report_use_case_reportusecase_generar_despacho|.generar_despacho()]] _[EXTRACTED 1.00]_
- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[services_pdf_service_pdfservice|PDFService]] _[INFERRED 0.50]_

## Incoming

- [[api_dependencies_get_report_use_case|get_report_use_case()]] --calls--> _[INFERRED 0.80]_
- [[backend_app_application_report_use_case_py|report_use_case.py]] --contains--> _[EXTRACTED 1.00]_
