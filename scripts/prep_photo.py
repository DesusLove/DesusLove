"""Remove background with rembg, boost local contrast with CLAHE, save as source-prepped.png."""

import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

CLIP_LIMIT = 3.0
GRID_SIZE = (8, 8)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <path-to-photo> [output.png]")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"

    img = Image.open(src).convert("RGB")
    img_no_bg = remove(img, post_process_mask=True)
    no_bg_arr = np.array(img_no_bg.convert("RGB"))

    lab = cv2.cvtColor(no_bg_arr, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=CLIP_LIMIT, tileGridSize=GRID_SIZE)
    l = clahe.apply(l)
    lab = cv2.merge([l, a, b])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    Image.fromarray(result).save(dst)
    print(f"Saved prepped photo to {dst}")


if __name__ == "__main__":
    main()
