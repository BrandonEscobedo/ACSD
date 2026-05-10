---
title: PDFService
id: services_pdf_service_pdfservice
community: 6
source_file: backend/app/infrastructure/services/pdf_service.py
source_location: L14
file_type: code
tags:
  - graphify/node
  - community/6
  - type/code
---

# PDFService

- Source: `backend/app/infrastructure/services/pdf_service.py` `L14`
- Type: `code`
- Community: [[_COMMUNITY_6|Community 6]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --method--> [[services_pdf_service_pdfservice_generar_reporte_despacho|.generar_reporte_despacho()]] _[EXTRACTED 1.00]_

## Incoming

- [[api_dependencies_pdf_service|_pdf_service()]] --calls--> _[INFERRED 0.80]_
- [[application_report_use_case_reportusecase|ReportUseCase]] --uses--> _[INFERRED 0.50]_
- [[backend_app_infrastructure_services_pdf_service_py|pdf_service.py]] --contains--> _[EXTRACTED 1.00]_
