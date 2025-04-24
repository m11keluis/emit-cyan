from pathlib import Path
import re
from datetime import datetime
from scripts.modules.process_emit_granule import process_emit_granule
from scripts.modules.process_cyan_granule import process_cyan_granule

def extract_date_from_emit_filename(fname):
    match = re.search(r"_(\d{8})T\d{6}_", fname)
    return match.group(1) if match else None

def batch_compare_emit_cyan(
    emit_folder, cyan_folder,
    bounds=None,
    start_date=None, end_date=None
):
    emit_folder = Path(emit_folder)
    cyan_folder = Path(cyan_folder)

    emit_files = sorted(emit_folder.glob("EMIT_L2A_RFL_*.nc"))
    print(f"🔍 Found {len(emit_files)} EMIT files total")

    for emit_path in emit_files:
        date_str = extract_date_from_emit_filename(emit_path.name)
        if not date_str:
            print(f"⚠️ Skipping {emit_path.name} (date not found)")
            continue

        date_obj = datetime.strptime(date_str, "%Y%m%d").date()
        if start_date and date_obj < start_date:
            continue
        if end_date and date_obj > end_date:
            continue

        # Match CyAN by date
        cyan_matches = list(cyan_folder.glob(f"*{date_str}*.nc"))
        if not cyan_matches:
            print(f"🟡 No CyAN file found for {date_str}")
            continue

        cyan_path = cyan_matches[0]
        print(f"🔗 Matched: {emit_path.name} ↔ {cyan_path.name}")

        try:
            emit_ds = process_emit_granule(emit_path, bounds=bounds)
            cyan_da = process_cyan_granule(cyan_path, bounds=bounds)

            # Example: access a preview pixel stat
            print(f"  EMIT shape: {emit_ds['reflectance'].shape}")
            print(f"  CyAN CI shape: {cyan_da.shape}")

        except Exception as e:
            print(f"❌ Error processing {emit_path.name}: {e}")
