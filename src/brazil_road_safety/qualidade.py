"""Validações reproduzíveis para acidentes da PRF agrupados por ocorrência."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import pandas as pd

COLUNAS_MINIMAS = {
    "id",
    "data_inversa",
    "uf",
    "br",
    "km",
    "municipio",
    "causa_acidente",
    "tipo_acidente",
    "classificacao_acidente",
    "mortos",
    "feridos_leves",
    "feridos_graves",
    "ilesos",
    "ignorados",
    "feridos",
    "veiculos",
}

COLUNAS_CONTAGEM = {
    "mortos",
    "feridos_leves",
    "feridos_graves",
    "ilesos",
    "ignorados",
    "feridos",
    "veiculos",
}


@dataclass(frozen=True)
class RelatorioQualidade:
    """Resumo auditável do gate de qualidade."""

    aprovado: bool
    linhas: int
    colunas_ausentes: list[str]
    duplicidades_id: int
    datas_invalidas: int
    datas_fora_do_ano: int
    ausencias: dict[str, int]
    valores_nao_numericos: dict[str, int]
    valores_negativos: dict[str, int]
    valores_fracionarios: dict[str, int]

    def como_dict(self) -> dict[str, Any]:
        return asdict(self)


def avaliar_qualidade(dados: pd.DataFrame, ano_esperado: int) -> RelatorioQualidade:
    """Avalia requisitos mínimos antes de liberar dados para análise estatística."""
    colunas_ausentes = sorted(COLUNAS_MINIMAS - set(dados.columns))
    ausencias = {coluna: int(dados[coluna].isna().sum()) for coluna in dados.columns}

    duplicidades_id = 0
    if "id" in dados:
        duplicidades_id = int(dados["id"].duplicated().sum())

    datas_invalidas = 0
    datas_fora_do_ano = 0
    if "data_inversa" in dados:
        datas = pd.to_datetime(dados["data_inversa"], errors="coerce")
        datas_invalidas = int(datas.isna().sum())
        datas_fora_do_ano = int((datas.dropna().dt.year != ano_esperado).sum())

    valores_nao_numericos: dict[str, int] = {}
    valores_negativos: dict[str, int] = {}
    valores_fracionarios: dict[str, int] = {}
    for coluna in sorted(COLUNAS_CONTAGEM & set(dados.columns)):
        numerico = pd.to_numeric(dados[coluna], errors="coerce")
        valores_nao_numericos[coluna] = int((dados[coluna].notna() & numerico.isna()).sum())
        valores_negativos[coluna] = int((numerico < 0).sum())
        valores_fracionarios[coluna] = int((numerico.notna() & (numerico % 1 != 0)).sum())

    ids_ausentes = ausencias.get("id", 0)
    aprovado = bool(
        len(dados) > 0
        and not colunas_ausentes
        and ids_ausentes == 0
        and duplicidades_id == 0
        and datas_invalidas == 0
        and datas_fora_do_ano == 0
        and not any(valores_nao_numericos.values())
        and not any(valores_negativos.values())
        and not any(valores_fracionarios.values())
    )

    return RelatorioQualidade(
        aprovado=aprovado,
        linhas=len(dados),
        colunas_ausentes=colunas_ausentes,
        duplicidades_id=duplicidades_id,
        datas_invalidas=datas_invalidas,
        datas_fora_do_ano=datas_fora_do_ano,
        ausencias=ausencias,
        valores_nao_numericos=valores_nao_numericos,
        valores_negativos=valores_negativos,
        valores_fracionarios=valores_fracionarios,
    )
