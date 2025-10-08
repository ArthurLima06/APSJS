from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ======= CONFIGURAÇÃO DO CORS =======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======= MODELO DE DADOS =======
class Viagem(BaseModel):
    km: float
    tipo: str  # 'todos' ou veículo específico
    passageiros: int | None = None


# ======= FUNÇÕES DE CÁLCULO =======
def calcular_media_geral(km):
    # média de todos os veículos
    fatores = {"carro": 0.15, "moto": 0.10, "avião": 0.25, "barco": 0.20}
    total = sum(km * v for v in fatores.values())
    media = total / len(fatores)
    return media


def calcular_por_veiculo(km, tipo, passageiros=None):
    fatores = {"carro": 0.15, "moto": 0.10, "avião": 0.25, "barco": 0.20}
    fator = fatores.get(tipo, 0)
    emissao_total = km * fator

    if tipo == "avião" and passageiros and passageiros > 0:
        emissao_total /= passageiros  # divide entre os passageiros

    return emissao_total


# ======= ENDPOINT API =======
@app.post("/calcular")
def calcular(viagem: Viagem):
    if viagem.tipo == "todos":
        total = calcular_media_geral(viagem.km)
        return {"tipo": "média geral", "emissao_total": total}

    else:
        total = calcular_por_veiculo(viagem.km, viagem.tipo, viagem.passageiros)
        return {"tipo": viagem.tipo, "emissao_total": total}
