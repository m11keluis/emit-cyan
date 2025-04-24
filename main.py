from scripts.modules.batch_compare import batch_compare_emit_cyan
from datetime import date

if __name__ == "__main__":
    batch_compare_emit_cyan(
        emit_folder="data/emit",
        cyan_folder="data/cyan",
        bounds=(-122.1, 42.23, -121.78, 42.58),
        start_date=date(2024, 7, 24),
        end_date=date(2024, 7, 26)
    )