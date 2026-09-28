"""Ingestão reproduzível de acidentes da PRF agrupados por ocorrência."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import BadZipFile, ZipFile

import pandas as pd


@dataclass(frozen=True)
class ResultadoIngestao:
    """Metadados necessários para auditar uma ingestão."""

    dados: pd.DataFrame
    sha256: str
    arquivo_origem: str
    encoding: str


def baixar_bytes(url: str, timeout: int = 60) -> bytes:
    """Baixa uma fonte pública sem autenticação e retorna seus bytes."""
    requisicao = Request(url, headers={"User-Agent": "DatalabMp-brazil-road-safety/0.1"})
    with urlopen(requisicao, timeout=timeout) as resposta:
        return resposta.read()


def _csv_do_zip(conteudo: bytes) -> tuple[bytes, str]:
    try:
        with ZipFile(BytesIO(conteudo)) as arquivo_zip:
            csvs = sorted(nome for nome in arquivo_zip.namelist() if nome.lower().endswith(".csv"))
            if len(csvs) != 1:
                raise ValueError("O ZIP da fonte deve conter exatamente um arquivo CSV.")
            nome = csvs[0]
            return arquivo_zip.read(nome), nome
    except BadZipFile as erro:
        raise ValueError("O conteúdo informado não é um ZIP válido.") from erro


def _ler_csv_bytes(csv_bytes: bytes) -> tuple[pd.DataFrame, str]:
    """Lê o CSV preservando a codificação efetivamente aceita."""
    ultimo_erro: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "latin1"):
        try:
            dados = pd.read_csv(
                BytesIO(csv_bytes), sep=";", encoding=encoding, low_memory=False
            )
            return dados, encoding
        except UnicodeDecodeError as erro:
            ultimo_erro = erro
    raise ValueError("Não foi possível decodificar o CSV da PRF.") from ultimo_erro


def ler_csv_prf(conteudo: bytes, nome_origem: str = "fonte.csv") -> ResultadoIngestao:
    """Lê CSV/ZIP da PRF preservando hash e codificação do artefato recebido."""
    hash_fonte = sha256(conteudo).hexdigest()
    nome_csv = nome_origem
    csv_bytes = conteudo
    if nome_origem.lower().endswith(".zip") or conteudo.startswith(b"PK"):
        csv_bytes, nome_csv = _csv_do_zip(conteudo)

    dados, encoding = _ler_csv_bytes(csv_bytes)
    dados.columns = [str(coluna).strip() for coluna in dados.columns]
    return ResultadoIngestao(
        dados=dados,
        sha256=hash_fonte,
        arquivo_origem=nome_csv,
        encoding=encoding,
    )


def ingerir_url(url: str) -> ResultadoIngestao:
    """Baixa e interpreta uma URL pública da PRF."""
    conteudo = baixar_bytes(url)
    nome = Path(url.split("?", 1)[0]).name or "fonte.zip"
    return ler_csv_prf(conteudo, nome)
