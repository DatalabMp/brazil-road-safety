import pandas as pd

from brazil_road_safety.analise import resumo_descritivo


def test_resumo_descritivo_agrega_sem_inferir_causalidade():
    dados = pd.DataFrame(
        {
            "data_inversa": ["2025-01-01", "2025-02-01"],
            "uf": ["GO", "DF"],
            "causa_acidente": ["Causa A", "Causa B"],
            "tipo_acidente": ["Tipo A", "Tipo B"],
            "classificacao_acidente": ["Com Vítimas Feridas", "Sem Vítimas"],
            "mortos": [0, 1],
            "feridos": [1, 0],
            "feridos_graves": [0, 0],
            "veiculos": [2, 1],
        }
    )

    resumo = resumo_descritivo(dados)

    assert resumo["ocorrencias"] == 2
    assert resumo["mortos"] == 1
    assert resumo["feridos"] == 1
    assert resumo["veiculos"] == 3
    assert resumo["ocorrencias_por_mes"] == {1: 1, 2: 1}
