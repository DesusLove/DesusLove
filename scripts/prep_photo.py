"""Boost local contrast with CLAHE and brighten, save as source-prepped.png."""

import sys
import cv2
import numpy as np
from PIL import Image

CLIP_LIMIT = 4.0
BRIGHTNESS_BOOST = 1.8
GRID_SIZE = (8, 8)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <path-to-photo> [output.png]")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"

    img = Image.open(src).convert("RGB")
    arr = np.array(img)

    lab = cv2.cvtColor(arr, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=GRID_SIZE)
    l = clahe.apply(l)
    l = np.clip(l.astype(np.float32) * BRIGHTNESS_BOOST, 0, 255).astype(np.uint8)
    lab = cv2.merge([l, a, b])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    Image.fromarray(result).save(dst)
    print(f"Saved prepped photo to {dst}")


if __name__ == "__main__":
    main()
