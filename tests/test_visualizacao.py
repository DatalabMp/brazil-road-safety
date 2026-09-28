import pandas as pd

from brazil_road_safety.visualizacao import ranking_causas, ranking_ufs, serie_mensal


def dados_exemplo():
    return pd.DataFrame(
        {
            "data_inversa": ["2025-02-01", "2025-01-01", "2025-01-02"],
            "uf": ["DF", "GO", "GO"],
            "causa_acidente": ["B", "A", "A"],
        }
    )


def test_serie_mensal_ordena_cronologicamente():
    resultado = serie_mensal(dados_exemplo())
    assert resultado.to_dict("records") == [
        {"mes": 1, "ocorrencias": 2},
        {"mes": 2, "ocorrencias": 1},
    ]


def test_rankings_refletem_contagens_observadas():
    dados = dados_exemplo()
    assert ranking_ufs(dados, 1).to_dict("records") == [{"uf": "GO", "ocorrencias": 2}]
    assert ranking_causas(dados, 1).to_dict("records") == [{"causa": "A", "ocorrencias": 2}]
