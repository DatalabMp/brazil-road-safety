from brazil_road_safety.fontes import FONTE_ACIDENTES_2025, PAGINA_DADOS_ABERTOS_PRF


def test_fonte_2025_preserva_identidade_publicada_pela_prf() -> None:
    fonte = FONTE_ACIDENTES_2025

    assert fonte.ano == 2025
    assert fonte.granularidade == "ocorrencia"
    assert fonte.arquivo == "datatran2025.zip"
    assert fonte.google_drive_file_id == "1-G3MdmHBt6CprDwcW99xxC4BZ2DU5ryR"
    assert fonte.pagina_oficial == PAGINA_DADOS_ABERTOS_PRF
    assert fonte.google_drive_file_id in fonte.url_download
    assert fonte.url_download.startswith("https://drive.usercontent.google.com/download?")
