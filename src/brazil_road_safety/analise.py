"""Resumos descritivos para dados da PRF aprovados pelo gate de qualidade."""

from __future__ import annotations

import pandas as pd


def resumo_descritivo(dados: pd.DataFrame) -> dict[str, object]:
    """Calcula indicadores estritamente descritivos do conjunto validado."""
    datas = pd.to_datetime(dados["data_inversa"])
    return {
        "ocorrencias": len(dados),
        "mortos": int(pd.to_numeric(dados["mortos"]).sum()),
        "feridos": int(pd.to_numeric(dados["feridos"]).sum()),
        "feridos_graves": int(pd.to_numeric(dados["feridos_graves"]).sum()),
        "veiculos": int(pd.to_numeric(dados["veiculos"]).sum()),
        "ocorrencias_por_uf": dados["uf"].value_counts().to_dict(),
        "ocorrencias_por_mes": dados.groupby(datas.dt.month).size().to_dict(),
        "principais_causas": dados["causa_acidente"].value_counts().head(10).to_dict(),
        "principais_tipos": dados["tipo_acidente"].value_counts().head(10).to_dict(),
        "classificacao": dados["classificacao_acidente"].value_counts(dropna=False).to_dict(),
    }
