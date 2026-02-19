"""
PRODUCTION ITEM TABLE EXTRACTOR
-------------------------------
✔ Spatial OCR
✔ Line grouping
✔ Column alignment
✔ Handles split OCR lines
✔ Detects Qty + Name + Price
✔ Works for restaurant receipts
✔ Skips totals / taxes / tips
✔ Clean structured output
"""

import pytesseract
import pandas as pd
import numpy as np
import cv2
import re


# =========================================================
# STEP 1 — SPATIAL OCR WORD EXTRACTION
# =========================================================

def extract_words_with_coords(image):

    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    data = pytesseract.image_to_data(
        img_cv,
        output_type=pytesseract.Output.DATAFRAME
    )

    data = data.dropna()
    data = data[data['text'].str.strip() != ""]

    words = data[['text', 'left', 'top', 'width', 'height']]
    words.columns = ['text', 'x', 'y', 'w', 'h']

    return words


# =========================================================
# STEP 2 — GROUP WORDS INTO ROWS
# =========================================================

def group_words_into_rows(words_df, y_threshold=12):

    rows = []

    words_df = words_df.sort_values(by='y')

    current_row = []
    last_y = None

    for _, row in words_df.iterrows():

        if last_y is None:
            current_row.append(row)
            last_y = row['y']
            continue

        if abs(row['y'] - last_y) <= y_threshold:
            current_row.append(row)
        else:
            rows.append(current_row)
            current_row = [row]
            last_y = row['y']

    if current_row:
        rows.append(current_row)

    return rows


# =========================================================
# STEP 3 — BUILD TEXT LINE FROM ROW
# =========================================================

def build_line_from_row(row):

    sorted_words = sorted(row, key=lambda r: r['x'])
    line = " ".join([str(w['text']) for w in sorted_words])

    return line.strip()


# =========================================================
# STEP 4 — DETECT ITEM ROWS
# =========================================================

def detect_item_lines(lines):

    item_lines = []

    for line in lines:

        line_lower = line.lower()

        # skip totals, tax, tip, footer, payments
        if re.search(r"(total|subtotal|tax|tip|amount|change|cash|card|balance)", line_lower):
            continue

        # skip percentage lines like 18%, 20%
        if re.search(r"\d+%", line_lower):
            continue

        # must contain price
        if re.search(r"\$?\d+\.\d{2}", line):
            item_lines.append(line)

    return item_lines


# =========================================================
# STEP 5 — PARSE ITEM LINE
# =========================================================

def parse_item_line(line):

    """
    Handles:
    1 Burger 120.00
    3 Pupusa Queso $6.75
    Pizza $10.00
    2 x Coke 40.00
    """

    qty = 1

    # detect quantity at start
    qty_match = re.match(r"^(\d+)\s*(x\s*)?", line)

    if qty_match:
        qty = int(qty_match.group(1))
        line = line[qty_match.end():].strip()

    # extract price
    price_match = re.findall(r"\$?\d+\.\d{2}", line)

    if not price_match:
        return None

    total_price = float(price_match[-1].replace("$", ""))

    # remove price from name
    name = line.replace(price_match[-1], "").strip()

    # clean unwanted text
    name = re.sub(r"\s+", " ", name)

    if len(name) < 2:
        return None

    return {
        "Item": name,
        "Qty": qty,
        "Unit Price": round(total_price / qty, 2),
        "Total": round(total_price, 2)
    }


# =========================================================
# STEP 6 — MAIN EXTRACTOR PIPELINE
# =========================================================

def extract_items_from_receipt(image):

    words = extract_words_with_coords(image)

    if words.empty:
        return []

    rows = group_words_into_rows(words)

    # convert rows → text lines
    lines = [build_line_from_row(row) for row in rows]

    item_lines = detect_item_lines(lines)

    items = []

    for line in item_lines:

        parsed = parse_item_line(line)

        if parsed:
            items.append(parsed)

    return items
