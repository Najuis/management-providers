# management-providers

## 1. Entorno Virtual

python -m venv venv

venv\Scripts\activate

## 2. Instalación de Dependencias

pip install -r requirements.txt

## 3. Ejecución del Servidor

uvicorn main:app --host 127.0.1.1 --port 8000

## Por cada cambio o trabajo nuevo se crea una nueva rama con el nombre del cambio o trabajo a realizar

## Ejemplo de rama 

## para nuevo cambio
git checkout -b feature/nombre-de-la-funcionalidad 

## para cuando se organiza algo 

git checkout -b fix/nombre-del-arreglo o  git checkout -b refactor/nombre-del-arreglo

