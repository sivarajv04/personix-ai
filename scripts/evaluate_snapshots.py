import os
import subprocess

# ---------------- CONFIG ----------------
SNAPSHOT_DIR = "model"
OUTPUT_DIR = "samples"
SEEDS = "0-63"          # number of images = 64
PYTHON = "python"       # or "python3"
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

snapshots = sorted([
    f for f in os.listdir(SNAPSHOT_DIR)
    if f.endswith(".pkl")
])

if not snapshots:
    raise RuntimeError("❌ No .pkl files found in snapshots directory")

print(f"🔍 Found {len(snapshots)} snapshots")

for snap in snapshots:
    snap_name = os.path.splitext(snap)[0]
    outdir = os.path.join(OUTPUT_DIR, snap_name)
    os.makedirs(outdir, exist_ok=True)

    print(f"\n🚀 Generating samples for {snap}")

    cmd = [
        PYTHON, "generate.py",
        f"--network={os.path.join(SNAPSHOT_DIR, snap)}",
        f"--seeds={SEEDS}",
        f"--outdir={outdir}"
    ]

    subprocess.run(cmd, check=True)

print("\n✅ Sample generation completed for all snapshots")
