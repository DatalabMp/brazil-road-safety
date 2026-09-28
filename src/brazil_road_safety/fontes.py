"""Registro auditável das fontes públicas oficiais usadas pelo projeto."""

from __future__ import annotations

from dataclasses import dataclass

PAGINA_DADOS_ABERTOS_PRF = (
    "https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf"
)


@dataclass(frozen=True)
class FontePRF:
    """Identidade de uma extração oficial do BAT publicada pela PRF."""

    ano: int
    granularidade: str
    arquivo: str
    google_drive_file_id: str
    pagina_oficial: str = PAGINA_DADOS_ABERTOS_PRF

    @property
    def url_download(self) -> str:
        """Retorna a URL de download derivada do identificador publicado pela PRF."""
        return (
            "https://drive.usercontent.google.com/download"
            f"?id={self.google_drive_file_id}&export=download&confirm=t"
        )


FONTE_ACIDENTES_2025 = FontePRF(
    ano=2025,
    granularidade="ocorrencia",
    arquivo="datatran2025.zip",
    google_drive_file_id="1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR",
)
