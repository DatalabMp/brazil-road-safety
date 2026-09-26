from pathlib import Path


def test_managed_manifest_exists() -> None:
    assert Path('.datalab/manifest.json').is_file()
