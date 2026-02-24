import uuid
from pathlib import Path
import pickle
import torch
from PIL import Image
from tqdm import trange
import sys
from pathlib import Path

# --------------------------------------------------
# Make StyleGAN2-ADA importable
# --------------------------------------------------
STYLEGAN_ROOT = Path(r"F:\stylegan2ada\stylegan2-ada-pytorch")
sys.path.insert(0, str(STYLEGAN_ROOT))


# --------------------------------------------------
# CONFIG
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = PROJECT_ROOT / "models" / "personix_stylegan64.pkl"
OUTPUT_DIR = PROJECT_ROOT / "faces" / "_incoming"

NUM_IMAGES = 100                 # how many faces to generate per run
SEED = None                      # set int for reproducibility, None = random
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

IMAGE_SIZE = 64                  # sanity check

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOAD MODEL (ONCE)
# --------------------------------------------------
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

print(f"🔌 Loading GAN model from {MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

G = data["G_ema"].to(DEVICE)
G.eval()

print(f"✅ Model loaded on {DEVICE}")

# --------------------------------------------------
# OPTIONAL: GLOBAL SEED
# --------------------------------------------------
if SEED is not None:
    torch.manual_seed(SEED)

# --------------------------------------------------
# IMAGE GENERATION
# --------------------------------------------------
print(f"🎨 Generating {NUM_IMAGES} synthetic faces...")

for _ in trange(NUM_IMAGES):
    z = torch.randn([1, G.z_dim], device=DEVICE)

    with torch.no_grad():
        img = G(z, None)

    # Post-process [-1,1] → [0,255]
    img = (img.clamp(-1, 1) + 1) / 2
    img = img.permute(0, 2, 3, 1)
    img = (img * 255).byte().cpu().numpy()[0]

    # Safety check
    if img.shape[0] != IMAGE_SIZE or img.shape[1] != IMAGE_SIZE:
        raise ValueError("Unexpected image resolution")

    filename = f"img_{uuid.uuid4().hex}.png"
    Image.fromarray(img, "RGB").save(OUTPUT_DIR / filename)

print(f"✅ Done. Images saved to: {OUTPUT_DIR}")
