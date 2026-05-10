# ACSD

## Knowledge graph (graphify-out)

Este proyecto tiene un grafo de conocimiento pre-generado en [graphify-out/](graphify-out/). Úsalo como **primera fuente de búsqueda** antes de hacer grep/glob exhaustivos por el código.

**Cuándo usarlo:**
- Cualquier pregunta sobre arquitectura, relaciones entre archivos, o "¿dónde está X?"
- Localizar abstracciones centrales (god nodes) o módulos relacionados
- Entender qué comunidades/dominios existen en el código

**Cómo usarlo:**
1. Invoca el skill `graphify` (Skill tool con `skill: "graphify"`) — provee herramientas BFS/DFS sobre el grafo.
2. Archivos clave a consultar directamente si hace falta:
   - [graphify-out/GRAPH_REPORT.md](graphify-out/GRAPH_REPORT.md) — resumen, god nodes, comunidades, conexiones sorprendentes
   - [graphify-out/graph.json](graphify-out/graph.json) — nodos y aristas completos
   - [graphify-out/manifest.json](graphify-out/manifest.json) — índice de archivos procesados
   - [graphify-out/graph.html](graphify-out/graph.html) — visualización interactiva

**God nodes actuales:** `ContainerMonitor`, `Contenedor`, `TipoCarga`, `_Simulador`, `SimulacionEngine`, `VisualService`, `WebSocketManager`, `AssignmentUseCase`.

Si el grafo parece desactualizado respecto al código actual, verifica contra los archivos reales y avisa al usuario para re-generarlo con `/graphify`.
