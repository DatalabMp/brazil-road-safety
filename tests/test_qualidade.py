import pandas as pd

from brazil_road_safety.qualidade import COLUNAS_MINIMAS, avaliar_qualidade


def _dados_validos() -> pd.DataFrame:
    linha = {coluna: "valor" for coluna in COLUNAS_MINIMAS}
    linha.update(
        {
            "id": 1,
            "data_inversa": "2025-01-15",
            "mortos": 0,
            "feridos_leves": 1,
            "feridos_graves": 0,
            "ilesos": 1,
            "ignorados": 0,
            "feridos": 1,
            "veiculos": 2,
        }
    )
    return pd.DataFrame([linha])


def test_aprova_conjunto_minimo_valido() -> None:
    relatorio = avaliar_qualidade(_dados_validos(), 2025)
    assert relatorio.aprovado
    assert relatorio.linhas == 1
    assert relatorio.colunas_ausentes == []


def test_reprova_coluna_obrigatoria_ausente() -> None:
    dados = _dados_validos().drop(columns=["id"])
    relatorio = avaliar_qualidade(dados, 2025)
    assert not relatorio.aprovado
    assert relatorio.colunas_ausentes == ["id"]


def test_reprova_id_duplicado() -> None:
    dados = pd.concat([_dados_validos(), _dados_validos()], ignore_index=True)
    relatorio = avaliar_qualidade(dados, 2025)
    assert not relatorio.aprovado
    assert relatorio.duplicidades_id == 1


def test_reprova_data_invalida_ou_fora_do_ano() -> None:
    dados = pd.concat([_dados_validos(), _dados_validos()], ignore_index=True)
    dados.loc[0, "id"] = 1
    dados.loc[1, "id"] = 2
    dados.loc[0, "data_inversa"] = "data-invalida"
    dados.loc[1, "data_inversa"] = "2024-12-31"
    relatorio = avaliar_qualidade(dados, 2025)
    assert not relatorio.aprovado
    assert relatorio.datas_invalidas == 1
    assert relatorio.datas_fora_do_ano == 1


def test_reprova_contagem_negativa() -> None:
    dados = _dados_validos()
    dados.loc[0, "mortos"] = -1
    relatorio = avaliar_qualidade(dados, 2025)
    assert not relatorio.aprovado
    assert relatorio.valores_negativos["mortos"] == 1
