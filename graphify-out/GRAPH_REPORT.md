# Graph Report - ACSD  (2026-05-11)

## Corpus Check
- 60 files · ~24,060 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 313 nodes · 446 edges · 34 communities (30 shown, 4 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 66 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3b6d849d`
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
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]

## God Nodes (most connected - your core abstractions)
1. `ContainerMonitor` - 26 edges
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

## Communities (34 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.1
Nodes (15): ABC, get_assignment_use_case(), AssignmentResult, AssignmentUseCase, Entity, Contenedor, EstadoContenedor, TipoCarga (+7 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (14): addContainer(), advanceContainer(), assignLine(), del(), downloadReport(), post(), put(), removeContainer() (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (10): EventRow(), relTime(), ZONE_COLORS, ZONE_ICONS, CARGO_COLORS, FALLBACK, CARGO_COLORS, ZONE_COLORS (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (10): get_lineas(), get_monitor(), get_report_use_case(), get_ws_manager(), _linea_repository(), _pdf_service(), ReportUseCase, lifespan() (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (3): ContainerMonitor, Stagger departures so containers don't all move at once when pre-filled., Stagger departures so containers don't all move at once when pre-filled.

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (6): SimulationResult, SimulationUseCase, EventoSimulacion, SimulacionEngine, _Simulador, VisualService

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (22): Backend Python Requirements, fastapi, python-multipart, uvicorn[standard], Assets Folder, lineas_transportistas.json Data, PyInstaller Build Command, SimuladorContenedores Executable (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (21): Yellow Container Icon (container-amarillo.svg), Green Container Icon (container-verde.svg), Dark Olive Inner Fill #939D41, Vertical Ridge Color #828E38, Yellow/Olive Fill #AEAD4B, Container Color-coded Status Set, Shipping Container Icon (UI symbol), Strong Blue Color Palette (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.26
Nodes (11): BaseModel, run_simulation(), AssignmentRequest, AssignmentResponse, LineResultSchema, ReportRequest, MonitorConfigSchema, ContenedorSchema (+3 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (3): CARGA_ICON, ZONE_META, CARGA_COLOR

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (3): COLORS, CraneCanvas(), makeShipContainers()

### Community 13 - "Community 13"
Cohesion: 0.5
Nodes (7): edge_confidence(), main(), Build an Obsidian vault from graphify-out/graph.json.  The vault lives INSIDE gr, slug(), wikilink(), write_note(), str

### Community 14 - "Community 14"
Cohesion: 0.36
Nodes (4): animar_simulacion(), crear_escena_html_completa(), crear_zona_buque_piso(), crear_zona_patio_3d()

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (4): crear ambiente con Python 3.10.8, ejecutar comando python .\main.py desde src para iniciar el proyecto, instalar librerias de requirements.txt (pip install -r .\requirements.txt), MySSD_FRONT

### Community 16 - "Community 16"
Cohesion: 0.4
Nodes (5): UI Icon Asset (Cafe Container), Container Cafe Icon (SVG), Brown Container Body (#AE864B / #9D7241), Container Base Feet / Supports, Vertical Corrugation Ribs (#8E6338)

### Community 17 - "Community 17"
Cohesion: 0.83
Nodes (3): emptyPatio(), emptyZones(), useAnimation()

### Community 18 - "Community 18"
Cohesion: 0.5
Nodes (4): QUO (registered trademark brand), QUO wordmark design elements, LogoQuo.png - QUO brand logo image, Project branding asset (third-party logo)

### Community 21 - "Community 21"
Cohesion: 0.67
Nodes (3): Container Azul Icon (SVG), Teal Container Icon Style, Container Visual Marker (UI Purpose)

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (3): Red Container Icon (SVG), Corrugated Container Visual Pattern, Red Container Status Variant

## Knowledge Gaps
- **59 isolated node(s):** `Stagger departures so containers don't all move at once when pre-filled.`, `COLORS`, `CARGA_ICON`, `ZONE_META`, `ZONE_COLORS` (+54 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Contenedor` connect `Community 0` to `Community 3`, `Community 4`, `Community 5`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `ContainerMonitor` connect `Community 4` to `Community 0`, `Community 3`, `Community 5`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `TipoCarga` connect `Community 0` to `Community 5`, `Community 4`, `Community 13`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `ContainerMonitor` (e.g. with `Contenedor` and `TipoCarga`) actually correct?**
  _`ContainerMonitor` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Contenedor` (e.g. with `AssignmentResult` and `AssignmentUseCase`) actually correct?**
  _`Contenedor` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `TipoCarga` (e.g. with `AssignmentResult` and `AssignmentUseCase`) actually correct?**
  _`TipoCarga` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `_Simulador` (e.g. with `Contenedor` and `TipoCarga`) actually correct?**
  _`_Simulador` has 4 INFERRED edges - model-reasoned connections that need verification._