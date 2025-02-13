# main.py
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡La API está funcionando correctamente!"}

@app.get("/banco")
def banco():
    session = requests.Session()

    # === 📌 Solicitud 1 ===
    payload_1 = {
        "TipoProducto": "1",
        "IdProducto": "9902603919",
        "TipoDocumento": "1",
        "NumeroDocumento": "80050177",
        "UniqueCode": None
    }
    response_1 = session.post(
        "https://solicitud.bancofinandina.com:8443/PS/api/Products/GetRaiseMoneyInfo",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        json=payload_1,
        verify=False
    )

    data_1 = response_1.json()
    unique_code = data_1.get("Data", {}).get("UniqueCode")

    if not unique_code:
        return {"error": "No se obtuvo UniqueCode"}

    # === 📌 Solicitud 2 ===
    payload_2 = {
        "tipoParametria": "Bancos",
        "UniqueCode": unique_code
    }
    response_2 = session.post(
        "https://solicitud.bancofinandina.com:8443/PS/api/Params/LoadParametros",
        json=payload_2,
        verify=False
    )

    # === 📌 Solicitud 3 ===
    payload_3 = {
        "Monto": "10000",
        "TipoPersona": "0",
        "IdBanco": 1507,
        "UniqueCode": unique_code
    }
    response_3 = session.post(
        "https://solicitud.bancofinandina.com:8443/PS/api/Products/ConfirmRaiseMoney",
        json=payload_3,
        verify=False
    )

    return {
        "solicitud_1": data_1,
        "solicitud_2": response_2.json(),
        "solicitud_3": response_3.json()
    }
