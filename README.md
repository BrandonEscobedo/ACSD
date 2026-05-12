# ACSD

## Requisitos
- Python 3.10.8
- Node.js 18 o superior

## Backend
1. Abrir una terminal en la carpeta `backend`.
2. Crear y activar el entorno virtual si no existe.
```powershell
python -m venv env
```
3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Iniciar el servidor:

```powershell
uvicorn main:app --reload
```

## Frontend
1. Abrir otra terminal en la carpeta `frontend`.
2. Instalar dependencias:

```powershell
npm install
```

3. Iniciar la aplicación:

```powershell
npm run dev
```

## Notas
- El backend expone la API con FastAPI desde `backend/main.py`.
- El frontend corre con Vite en el puerto 5173.