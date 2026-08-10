from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


def test_scheduled_analysis_exists():

    script = (
        BASE_DIR
        / "scheduled_analysis.py"
    )

    assert script.exists()


def test_batch_file_exists():

    batch_file = (
        BASE_DIR
        / "run_monitor.bat"
    )

    assert batch_file.exists()


def test_data_directory_exists():

    data_dir = (
        BASE_DIR
        / "data"
    )

    assert data_dir.exists()

