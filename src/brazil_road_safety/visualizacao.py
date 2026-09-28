"""Preparação de séries auditáveis para visualizações do projeto."""

from __future__ import annotations

import pandas as pd


def serie_mensal(dados: pd.DataFrame) -> pd.DataFrame:
    """Retorna ocorrências mensais em ordem cronológica."""
    datas = pd.to_datetime(dados["data_inversa"])
    serie = dados.assign(mes=datas.dt.month).groupby("mes").size()
    return serie.rename("ocorrencias").reset_index()


def ranking_ufs(dados: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    """Retorna UFs com maior número absoluto de ocorrências no conjunto."""
    ranking = dados["uf"].value_counts().head(limite)
    return ranking.rename_axis("uf").rename("ocorrencias").reset_index()


def ranking_causas(dados: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    """Retorna causas mais registradas, sem interpretação causal adicional."""
    ranking = dados["causa_acidente"].value_counts().head(limite)
    return ranking.rename_axis("causa").rename("ocorrencias").reset_index()
