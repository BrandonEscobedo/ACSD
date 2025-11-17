from services.linea_transportista_service import LineaTransportistaServicio
from dataclasses import asdict

def main():
    servicio = LineaTransportistaServicio('data/lineas_transportistas.json')
    lineas = servicio.listar_lineas()
    for linea in lineas:
        print(asdict(linea))

if __name__ == "__main__":
    main()