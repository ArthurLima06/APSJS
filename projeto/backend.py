from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ==== CONFIGURAÇÃO DO CORS ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite acesso de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== FUNÇÕES ORIGINAIS DE CÁLCULO ====
def emissao_combustivel(litros: float):
    return litros * 2.31  # kg CO2 / litro gasolina

def emissao_viagem_veiculo(km: float, tipo: str):
    fatores = {
        "carro": 0.15,
        "moto": 0.10,
        "avião": 0.25,
        "barco": 0.20
    }
    return km * fatores.get(tipo, 0)

def calcular_total(km, combustivel, tipo, passageiros=None, opcao="p"):
    if opcao == "pers":
        if tipo == "carro":
            mediaenergia = km * 0.67
        else:
            mediaenergia = km * 0.5
        return mediaenergia
    return emissao_combustivel(combustivel) + emissao_viagem_veiculo(km, tipo)

# ==== MODELO DE DADOS ====
class Viagem(BaseModel):
    km: float
    combustivel: float
    tipo: str
    passageiros: int | None = None
    opcao: str = "p"

# ==== ENDPOINT API ====
@app.post("/calcular")
def calcular(viagem: Viagem):
    total = calcular_total(
        viagem.km,
        viagem.combustivel,
        viagem.tipo,
        viagem.passageiros,
        viagem.opcao
    )
    return {"emissao_total": total}
