---
title: ContainerMonitor
id: services_container_monitor_containermonitor
community: 2
source_file: backend/app/infrastructure/services/container_monitor.py
source_location: L27
file_type: code
tags:
  - graphify/node
  - community/2
  - type/code
---

# ContainerMonitor

- Source: `backend/app/infrastructure/services/container_monitor.py` `L27`
- Type: `code`
- Community: [[_COMMUNITY_2|Community 2]]

## Outgoing

- --uses--> [[domain_contenedor_contenedor|Contenedor]] _[INFERRED 0.50]_
- --uses--> [[domain_enums_tipocarga|TipoCarga]] _[INFERRED 0.50]_
- --method--> [[services_container_monitor_containermonitor_init|.__init__()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_set_ws_manager|.set_ws_manager()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_get_state|.get_state()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_ser|._ser()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_broadcast|._broadcast()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_log|._log()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_make_container|._make_container()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_place_in_patio|._place_in_patio()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_arrive_in_buque|._arrive_in_buque()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_move_to_piso|.move_to_piso()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_move_to_patio|.move_to_patio()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_remove_from_patio|.remove_from_patio()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_auto_advance|._auto_advance()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_add_container|.add_container()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_advance_container|.advance_container()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_start_auto|.start_auto()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_stop_auto|.stop_auto()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_generator_loop|._generator_loop()]] _[EXTRACTED 1.00]_
- --method--> [[services_container_monitor_containermonitor_reset|.reset()]] _[EXTRACTED 1.00]_
- --uses--> [[services_visual_service_visualservice|VisualService]] _[INFERRED 0.50]_
- --uses--> [[services_websocket_manager_websocketmanager|WebSocketManager]] _[INFERRED 0.50]_

## Incoming

- [[api_dependencies_get_monitor|get_monitor()]] --calls--> _[INFERRED 0.80]_
- [[backend_app_infrastructure_services_container_monitor_py|container_monitor.py]] --contains--> _[EXTRACTED 1.00]_
