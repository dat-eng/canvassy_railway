import os
import shutil
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parent.parent
SEED_DATA_FILE = APP_ROOT / "data_final.csv"


def get_data_file() -> Path:
    """Return the writable voter-data file for the current environment.

    Railway exposes RAILWAY_VOLUME_MOUNT_PATH when a persistent volume is
    attached. Locally, Canvassy continues to use the repository's
    data_final.csv file.
    """
    volume_path = os.getenv("RAILWAY_VOLUME_MOUNT_PATH")

    if volume_path:
        return Path(volume_path) / "data_final.csv"

    return SEED_DATA_FILE


def initialize_data_file() -> Path:
    """Seed the persistent data file on first startup, then reuse it."""
    data_file = get_data_file()

    if data_file == SEED_DATA_FILE:
        return data_file

    data_file.parent.mkdir(parents=True, exist_ok=True)

    if not data_file.exists():
        shutil.copy2(SEED_DATA_FILE, data_file)

    return data_file
