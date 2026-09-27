from io import BytesIO
from zipfile import ZipFile

import pytest
from brazil_road_safety.ingestao import ler_csv_prf

CSV = b"id;data_inversa;uf\n1;2025-01-01;DF\n2;2025-01-02;GO\n"


def test_le_csv_com_separador_oficial() -> None:
    resultado = ler_csv_prf(CSV, "datatran2025.csv")
    assert resultado.arquivo_origem == "datatran2025.csv"
    assert resultado.dados.shape == (2, 3)
    assert resultado.dados["uf"].tolist() == ["DF", "GO"]
    assert len(resultado.sha256) == 64


def test_le_zip_com_um_csv() -> None:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as arquivo:
        arquivo.writestr("datatran2025.csv", CSV)

    resultado = ler_csv_prf(buffer.getvalue(), "datatran2025.zip")
    assert resultado.arquivo_origem == "datatran2025.csv"
    assert len(resultado.dados) == 2


def test_rejeita_zip_sem_csv_unico() -> None:
    buffer = BytesIO()
    with ZipFile(buffer, "w") as arquivo:
        arquivo.writestr("a.csv", CSV)
        arquivo.writestr("b.csv", CSV)

    with pytest.raises(ValueError, match="exatamente um arquivo CSV"):
        ler_csv_prf(buffer.getvalue(), "fonte.zip")
