from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ===== FUNÇÕES ORIGINAIS DE CÁLCULO =====
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
    # energia média/personalizada
    if opcao == "pers":
        if tipo == "carro":
            mediaenergia = km * 0.67
        elif tipo == "moto":
            mediaenergia = km * 0.33
        elif tipo == "avião":
            mediaenergia = km * 0.33 * (passageiros or 1)
        elif tipo == "barco":
            mediaenergia = km * 4.8
    else:  # padrão
        mediaenergia = (km * combustivel) * 9.5

    emissao_c = emissao_combustivel(combustivel)
    emissao_v = emissao_viagem_veiculo(km, tipo)
    emissao_e = mediaenergia * 0.233

    total = emissao_c + emissao_v + emissao_e
    return total

def calcular_creditos(total_emissao):
    preco_credito = 50.0
    toneladas = total_emissao / 1000
    custo = toneladas * preco_credito
    return {"toneladas": toneladas, "custo": custo}

# ===== MODELOS DE REQUISIÇÃO =====
class EmissaoRequest(BaseModel):
    km: float
    combustivel: float
    tipo: str
    opcao: str = "p"
    passageiros: int | None = None

# ===== ROTAS =====
@app.post("/calcular")
def calcular_emissao(dados: EmissaoRequest):
    total = calcular_total(
        dados.km, dados.combustivel, dados.tipo,
        passageiros=dados.passageiros,
        opcao=dados.opcao
    )
    creditos = calcular_creditos(total)
    return {
        "total_emissao": round(total, 2),
        "creditos": creditos
    }
