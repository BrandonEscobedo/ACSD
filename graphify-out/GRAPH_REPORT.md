# Graph Report - .  (2026-05-10)

## Corpus Check
- Corpus is ~16,451 words - fits in a single context window. You may not need a graph.

## Summary
- 260 nodes · 374 edges · 29 communities (26 shown, 3 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.61)
- Token cost: 150,059 input · 26,477 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Simulation Use Case|Simulation Use Case]]
- [[_COMMUNITY_Frontend API Client|Frontend API Client]]
- [[_COMMUNITY_Container Monitor Service|Container Monitor Service]]
- [[_COMMUNITY_React UI Components|React UI Components]]
- [[_COMMUNITY_Backend Build & Deps|Backend Build & Deps]]
- [[_COMMUNITY_Container Icon Set|Container Icon Set]]
- [[_COMMUNITY_Reports & DI Services|Reports & DI Services]]
- [[_COMMUNITY_Assignment Use Case|Assignment Use Case]]
- [[_COMMUNITY_API Schema Models|API Schema Models]]
- [[_COMMUNITY_Monitor Control API|Monitor Control API]]
- [[_COMMUNITY_3D Scene Renderer|3D Scene Renderer]]
- [[_COMMUNITY_WebSocket Manager|WebSocket Manager]]
- [[_COMMUNITY_Event Feed UI|Event Feed UI]]
- [[_COMMUNITY_Brown Container Icon|Brown Container Icon]]
- [[_COMMUNITY_Animation Hook|Animation Hook]]
- [[_COMMUNITY_QUO Brand Logo|QUO Brand Logo]]
- [[_COMMUNITY_Teal Container Icon|Teal Container Icon]]
- [[_COMMUNITY_Red Container Icon|Red Container Icon]]

## God Nodes (most connected - your core abstractions)
1. `ContainerMonitor` - 25 edges
2. `Contenedor` - 18 edges
3. `TipoCarga` - 12 edges
4. `_Simulador` - 11 edges
5. `SimulacionEngine` - 9 edges
6. `VisualService` - 9 edges
7. `Root Python Requirements` - 9 edges
8. `WebSocketManager` - 8 edges
9. `ContenedorSchema` - 7 edges
10. `AssignmentUseCase` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Backend Python Requirements` --semantically_similar_to--> `Root Python Requirements`  [INFERRED] [semantically similar]
  backend/requirements.txt → requirements.txt
- `PyInstaller Build Command` --references--> `streamlit`  [EXTRACTED]
  exe_comando.txt → requirements.txt
- `PyInstaller Build Command` --references--> `plotly`  [EXTRACTED]
  exe_comando.txt → requirements.txt
- `MySSD_FRONT Project` --conceptually_related_to--> `Frontend HTML Entry`  [INFERRED]
  README.md → frontend/index.html
- `Backend Python Requirements` --references--> `pandas`  [EXTRACTED]
  backend/requirements.txt → requirements.txt

## Hyperedges (group relationships)
- **Simulator Python Stack** — requirements_streamlit, requirements_simpy, requirements_plotly, requirements_reportlab [INFERRED 0.85]
- **FastAPI Backend Stack** — backend_requirements_fastapi, backend_requirements_uvicorn, backend_requirements_python_multipart [INFERRED 0.85]
- **PyInstaller Packaging Flow** — exe_comando_pyinstaller_build, exe_comando_simulador_contenedores_exe, exe_comando_lineas_transportistas_data, exe_comando_assets_folder [EXTRACTED 1.00]

## Communities (29 total, 3 thin omitted)

### Community 0 - "Simulation Use Case"
Cohesion: 0.14
Nodes (12): SimulationResult, SimulationUseCase, Contenedor, EstadoContenedor, TipoCarga, EventoSimulacion, Enum, assign_line() (+4 more)

### Community 1 - "Frontend API Client"
Cohesion: 0.13
Nodes (14): addContainer(), advanceContainer(), assignLine(), del(), downloadReport(), post(), put(), removeContainer() (+6 more)

### Community 3 - "React UI Components"
Cohesion: 0.1
Nodes (5): CARGA_ICON, ZONE_META, CARGA_COLOR, useWebSocket(), App()

### Community 4 - "Backend Build & Deps"
Cohesion: 0.11
Nodes (22): Backend Python Requirements, fastapi, python-multipart, uvicorn[standard], Assets Folder, lineas_transportistas.json Data, PyInstaller Build Command, SimuladorContenedores Executable (+14 more)

### Community 5 - "Container Icon Set"
Cohesion: 0.09
Nodes (21): Yellow Container Icon (container-amarillo.svg), Green Container Icon (container-verde.svg), Dark Olive Inner Fill #939D41, Vertical Ridge Color #828E38, Yellow/Olive Fill #AEAD4B, Container Color-coded Status Set, Shipping Container Icon (UI symbol), Strong Blue Color Palette (+13 more)

### Community 6 - "Reports & DI Services"
Cohesion: 0.12
Nodes (10): get_lineas(), get_monitor(), get_report_use_case(), get_ws_manager(), _linea_repository(), _pdf_service(), ReportUseCase, lifespan() (+2 more)

### Community 7 - "Assignment Use Case"
Cohesion: 0.14
Nodes (8): ABC, get_assignment_use_case(), AssignmentResult, AssignmentUseCase, Entity, LineaTransportista, Entity, LineaTransportistaRepository

### Community 8 - "API Schema Models"
Cohesion: 0.26
Nodes (11): BaseModel, run_simulation(), AssignmentRequest, AssignmentResponse, LineResultSchema, ReportRequest, MonitorConfigSchema, ContenedorSchema (+3 more)

### Community 10 - "3D Scene Renderer"
Cohesion: 0.36
Nodes (4): animar_simulacion(), crear_escena_html_completa(), crear_zona_buque_piso(), crear_zona_patio_3d()

### Community 12 - "Event Feed UI"
Cohesion: 0.33
Nodes (4): EventRow(), relTime(), ZONE_COLORS, ZONE_ICONS

### Community 13 - "Brown Container Icon"
Cohesion: 0.4
Nodes (5): UI Icon Asset (Cafe Container), Container Cafe Icon (SVG), Brown Container Body (#AE864B / #9D7241), Container Base Feet / Supports, Vertical Corrugation Ribs (#8E6338)

### Community 14 - "Animation Hook"
Cohesion: 0.83
Nodes (3): emptyPatio(), emptyZones(), useAnimation()

### Community 15 - "QUO Brand Logo"
Cohesion: 0.5
Nodes (4): QUO (registered trademark brand), QUO wordmark design elements, LogoQuo.png - QUO brand logo image, Project branding asset (third-party logo)

### Community 17 - "Teal Container Icon"
Cohesion: 0.67
Nodes (3): Container Azul Icon (SVG), Teal Container Icon Style, Container Visual Marker (UI Purpose)

### Community 18 - "Red Container Icon"
Cohesion: 0.67
Nodes (3): Red Container Icon (SVG), Corrugated Container Visual Pattern, Red Container Status Variant

## Knowledge Gaps
- **44 isolated node(s):** `CARGA_ICON`, `ZONE_META`, `ZONE_COLORS`, `ZONE_ICONS`, `MEDALS` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Contenedor` connect `Simulation Use Case` to `Container Monitor Service`, `Reports & DI Services`, `Assignment Use Case`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `ContainerMonitor` connect `Container Monitor Service` to `Simulation Use Case`, `WebSocket Manager`, `Reports & DI Services`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `assign_line()` connect `Simulation Use Case` to `API Schema Models`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ContainerMonitor` (e.g. with `Contenedor` and `TipoCarga`) actually correct?**
  _`ContainerMonitor` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Contenedor` (e.g. with `AssignmentResult` and `AssignmentUseCase`) actually correct?**
  _`Contenedor` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `TipoCarga` (e.g. with `AssignmentResult` and `AssignmentUseCase`) actually correct?**
  _`TipoCarga` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_Simulador` (e.g. with `Contenedor` and `TipoCarga`) actually correct?**
  _`_Simulador` has 4 INFERRED edges - model-reasoned connections that need verification._