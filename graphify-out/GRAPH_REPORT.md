# Graph Report - ACSD  (2026-05-10)

## Corpus Check
- 55 files · ~18,031 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 277 nodes · 399 edges · 33 communities (28 shown, 5 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 66 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8e2c88a7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]

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

## Communities (33 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (19): addContainer(), advanceContainer(), assignLine(), del(), downloadReport(), post(), put(), removeContainer() (+11 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (22): Backend Python Requirements, fastapi, python-multipart, uvicorn[standard], Assets Folder, lineas_transportistas.json Data, PyInstaller Build Command, SimuladorContenedores Executable (+14 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (21): Yellow Container Icon (container-amarillo.svg), Green Container Icon (container-verde.svg), Dark Olive Inner Fill #939D41, Vertical Ridge Color #828E38, Yellow/Olive Fill #AEAD4B, Container Color-coded Status Set, Shipping Container Icon (UI symbol), Strong Blue Color Palette (+13 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (10): get_lineas(), get_monitor(), get_report_use_case(), get_ws_manager(), _linea_repository(), _pdf_service(), ReportUseCase, lifespan() (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.14
Nodes (8): ABC, get_assignment_use_case(), AssignmentResult, AssignmentUseCase, Entity, LineaTransportista, Entity, LineaTransportistaRepository

### Community 6 - "Community 6"
Cohesion: 0.21
Nodes (6): SimulationResult, SimulationUseCase, Contenedor, EventoSimulacion, SimulacionEngine, _Simulador

### Community 7 - "Community 7"
Cohesion: 0.21
Nodes (12): BaseModel, assign_line(), run_simulation(), AssignmentRequest, AssignmentResponse, LineResultSchema, ReportRequest, MonitorConfigSchema (+4 more)

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (11): EstadoContenedor, TipoCarga, Enum, dispatch_report(), edge_confidence(), main(), Build an Obsidian vault from graphify-out/graph.json.  The vault lives INSIDE gr, slug() (+3 more)

### Community 10 - "Community 10"
Cohesion: 0.36
Nodes (4): animar_simulacion(), crear_escena_html_completa(), crear_zona_buque_piso(), crear_zona_patio_3d()

### Community 12 - "Community 12"
Cohesion: 0.33
Nodes (4): EventRow(), relTime(), ZONE_COLORS, ZONE_ICONS

### Community 13 - "Community 13"
Cohesion: 0.4
Nodes (4): crear ambiente con Python 3.10.8, ejecutar comando python .\main.py desde src para iniciar el proyecto, instalar librerias de requirements.txt (pip install -r .\requirements.txt), MySSD_FRONT

### Community 14 - "Community 14"
Cohesion: 0.4
Nodes (5): UI Icon Asset (Cafe Container), Container Cafe Icon (SVG), Brown Container Body (#AE864B / #9D7241), Container Base Feet / Supports, Vertical Corrugation Ribs (#8E6338)

### Community 16 - "Community 16"
Cohesion: 0.83
Nodes (3): emptyPatio(), emptyZones(), useAnimation()

### Community 17 - "Community 17"
Cohesion: 0.5
Nodes (4): QUO (registered trademark brand), QUO wordmark design elements, LogoQuo.png - QUO brand logo image, Project branding asset (third-party logo)

### Community 20 - "Community 20"
Cohesion: 0.67
Nodes (3): Container Azul Icon (SVG), Teal Container Icon Style, Container Visual Marker (UI Purpose)

### Community 21 - "Community 21"
Cohesion: 0.67
Nodes (3): Red Container Icon (SVG), Corrugated Container Visual Pattern, Red Container Status Variant

## Knowledge Gaps
- **50 isolated node(s):** `CARGA_ICON`, `ZONE_META`, `ZONE_COLORS`, `ZONE_ICONS`, `MEDALS` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Contenedor` connect `Community 6` to `Community 1`, `Community 4`, `Community 5`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `ContainerMonitor` connect `Community 1` to `Community 8`, `Community 11`, `Community 4`, `Community 6`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `TipoCarga` connect `Community 8` to `Community 1`, `Community 5`, `Community 6`, `Community 7`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ContainerMonitor` (e.g. with `Contenedor` and `TipoCarga`) actually correct?**
  _`ContainerMonitor` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Contenedor` (e.g. with `AssignmentResult` and `AssignmentUseCase`) actually correct?**
  _`Contenedor` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `TipoCarga` (e.g. with `AssignmentResult` and `AssignmentUseCase`) actually correct?**
  _`TipoCarga` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_Simulador` (e.g. with `Contenedor` and `TipoCarga`) actually correct?**
  _`_Simulador` has 4 INFERRED edges - model-reasoned connections that need verification._