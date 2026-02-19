import os
import sys
import csv
import zipfile
import traceback
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# Make sure project root is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import cv2
from ocr_utils import preprocess_image, extract_text
from parser import parse_receipt


def ensure_unzipped(src_path: str, out_dir: str) -> str:
    """If src_path is a zip file, extract it to out_dir and return folder path.
    If it's a folder, return it.
    """
    p = Path(src_path)
    if p.is_file() and p.suffix.lower() == ".zip":
        target = Path(out_dir) / p.stem
        target.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(p, "r") as z:
            z.extractall(target)
        return str(target)
    if p.is_dir():
        return str(p)
    raise FileNotFoundError(f"Dataset path not found: {src_path}")


def list_images(folder: str):
    exts = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"}
    for p in Path(folder).rglob("*"):
        if p.suffix.lower() in exts:
            yield str(p)


def process_image(path: str):
    """Worker: read image, run preprocess+ocr+parse, return dict or error."""
    try:
        img = cv2.imread(path)
        if img is None:
            return {"filename": os.path.basename(path), "error": "imread_failed"}
        proc = preprocess_image(img)
        text = extract_text(proc, conf_threshold=25)
        parsed = parse_receipt(text)
        # normalize items to a string for CSV
        items = parsed.get("items", [])
        items_str = "; ".join([f"{it.get('name')}|{it.get('price')}" for it in items]) if items else ""
        return {
            "filename": os.path.basename(path),
            "store": parsed.get("store"),
            "date": parsed.get("date"),
            "time": parsed.get("time"),
            "subtotal": parsed.get("subtotal"),
            "tax": parsed.get("tax"),
            "total": parsed.get("total"),
            "payment": parsed.get("payment"),
            "items": items_str,
            "error": "",
        }
    except Exception as e:
        return {"filename": os.path.basename(path), "error": str(e), "traceback": traceback.format_exc()}


def write_csv(rows, out_csv):
    keys = [
        "filename",
        "store",
        "date",
        "time",
        "subtotal",
        "tax",
        "total",
        "payment",
        "items",
        "error",
    ]
    with open(out_csv, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in keys})


def batch_extract(dataset_path: str, out_dir: str = "outputs", workers: int = 4):
    folder = ensure_unzipped(dataset_path, out_dir)
    images = list(list_images(folder))
    if not images:
        print("No images found in dataset folder.")
        return

    os.makedirs(out_dir, exist_ok=True)
    out_csv = Path(out_dir) / "extracted_results.csv"

    results = []
    print(f"Processing {len(images)} images with {workers} workers...")

    with ProcessPoolExecutor(max_workers=workers) as exe:
        futures = {exe.submit(process_image, p): p for p in images}
        for i, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            results.append(res)
            if i % 10 == 0 or i == len(images):
                print(f"Completed {i}/{len(images)}")

    write_csv(results, out_csv)
    print(f"Results written to: {out_csv}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch extract receipts from images using MydigiBill OCR pipeline.")
    parser.add_argument("dataset", help="Path to folder or zip containing images")
    parser.add_argument("--out", help="Output directory", default="outputs")
    parser.add_argument("--workers", help="Number of parallel workers", type=int, default=4)
    args = parser.parse_args()

    batch_extract(args.dataset, args.out, args.workers)
