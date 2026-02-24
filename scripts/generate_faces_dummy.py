import os
import uuid
import numpy as np
import cv2

INCOMING_DIR = "faces/_incoming"
NUM_IMAGES = 5   # change later

os.makedirs(INCOMING_DIR, exist_ok=True)

def generate_dummy_faces(n=5):
    for i in range(n):
        # Create random noise image (64x64 RGB)
        img = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)

        image_id = f"img_{uuid.uuid4().hex[:8]}"
        filename = f"{image_id}.png"
        path = os.path.join(INCOMING_DIR, filename)

        cv2.imwrite(path, img)
        print(f"Generated dummy image: {path}")

if __name__ == "__main__":
    generate_dummy_faces(NUM_IMAGES)
