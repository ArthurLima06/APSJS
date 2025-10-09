# projeto/backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS (para permitir chamadas do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada
class Viagem(BaseModel):
    km: float
    combustivel: float   # litros consumidos na viagem (informado pelo usuário)
    tipo: str            # 'todos', 'carro', 'moto', 'avião', 'barco'
    passageiros: Optional[int] = None

# fatores de emissão por km (kg CO2 por km) — mantidos
VEICULOS_FATORES = {
    "carro": 0.15,
    "moto": 0.10,
    "avião": 0.25,
    "barco": 0.20
}

# baseline: litros POR KM usados para calcular a média esperada
# (valores de demonstração — você pode ajustá-los para sua apresentação)
BASELINE_LITROS_POR_KM = {
    "carro": 0.08,   # 0.08 L/km -> ~12.5 km/L
    "moto": 0.04,    # 0.04 L/km -> ~25 km/L
    "avião": 0.03,   # 0.03 L/km por passageiro (valor por passageiro)
    "barco": 0.20    # barco costuma gastar mais por km
}

# emissão do combustível (kg CO2 por litro)
def emissao_combustivel(litros: float) -> float:
    return litros * 2.31

# calcula emissão para um veículo específico (usa o combustível informado pelo usuário)
def calcular_por_veiculo(km: float, combustivel: float, tipo: str, passageiros: Optional[int] = None) -> float:
    fator = VEICULOS_FATORES.get(tipo, 0)
    emissao_viagem = km * fator
    emissao_comb = emissao_combustivel(combustivel)
    total = emissao_viagem + emissao_comb
    # se avião e houver número de passageiros válido, retornar emissão por passageiro
    if tipo == "avião" and passageiros and passageiros > 0:
        return total / passageiros
    return total

# calcula média esperada para um tipo (usa baseline, NÃO o combustível do usuário)
def media_esperada_por_tipo(km: float, tipo: str) -> float:
    fator = VEICULOS_FATORES.get(tipo, 0)
    baseline_lpk = BASELINE_LITROS_POR_KM.get(tipo, 0)
    baseline_litros = km * baseline_lpk
    # para avião: baseline_litros já pensado por passageiro (emissão por passageiro)
    return (km * fator) + emissao_combustivel(baseline_litros)

# classifica comparando valor com a média: dentro de ±10% => "na média"
def classificar(valor: float, media: float) -> str:
    if media == 0:
        return "na média"
    limite_baixo = media * 0.9
    limite_alto = media * 1.1
    if valor < limite_baixo:
        return "abaixo"
    if valor > limite_alto:
        return "acima"
    return "na média"

@app.post("/calcular")
def calcular(viagem: Viagem):
    km = viagem.km
    combustivel = viagem.combustivel
    tipo = viagem.tipo.lower()
    passageiros = viagem.passageiros

    # caso "todos": calcule média esperada por veículo (com baseline) e comparação para cada um
    if tipo == "todos":
        detalhes = []
        medias = {}
        for t in VEICULOS_FATORES.keys():
            medias[t] = media_esperada_por_tipo(km, t)

        for t in VEICULOS_FATORES.keys():
            emissao_usuario = calcular_por_veiculo(km, combustivel, t, passageiros if t == "avião" else None)
            classific = classificar(emissao_usuario, medias[t])
            detalhes.append({
                "tipo": t,
                "emissao_usuario": round(emissao_usuario, 4),
                "media_esperada": round(medias[t], 4),
                "classificacao": classific
            })

        media_geral = sum(medias.values()) / len(medias)
        return {
            "tipo": "todos",
            "media_geral": round(media_geral, 4),
            "detalhes": detalhes
        }

    # único veículo
    if tipo not in VEICULOS_FATORES:
        return {"error": "tipo de veículo inválido"}

    emissao_usuario = calcular_por_veiculo(km, combustivel, tipo, passageiros if tipo == "avião" else None)
    media_esperada = media_esperada_por_tipo(km, tipo)
    classific = classificar(emissao_usuario, media_esperada)
    return {
        "tipo": tipo,
        "emissao_usuario": round(emissao_usuario, 4),
        "media_esperada": round(media_esperada, 4),
        "classificacao": classific
    }
