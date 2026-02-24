import os
import subprocess

SNAPSHOT_DIR = "stylegan_eval/snapshots"
METRICS_OUT = "stylegan_eval/metrics/results.txt"
DATASET_ZIP = "datasets/celeba64.zip"
PYTHON = "python"

os.makedirs(os.path.dirname(METRICS_OUT), exist_ok=True)

snapshots = sorted([
    f for f in os.listdir(SNAPSHOT_DIR)
    if f.endswith(".pkl")
])

with open(METRICS_OUT, "w") as log:
    for snap in snapshots:
        print(f"\n📊 Computing FID for {snap}")

        cmd = [
            PYTHON, "calc_metrics.py",
            "--metrics=fid50k_full",
            f"--data={DATASET_ZIP}",
            f"--network={os.path.join(SNAPSHOT_DIR, snap)}",
            "--gpus=1"
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True
        )

        log.write(f"\n===== {snap} =====\n")
        log.write(result.stdout)
        log.write(result.stderr)

print("\n✅ FID evaluation completed")
