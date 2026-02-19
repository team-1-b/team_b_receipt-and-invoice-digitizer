"""
INTELLIGENT TEMPLATE PARSER ENGINE
----------------------------------
✔ Spatial OCR
✔ Vendor template learning
✔ Layout matching
✔ Financial field extraction
✔ Template accuracy scoring
✔ Standard vs Template comparison
"""

import pytesseract
import pandas as pd
import numpy as np
import cv2
import json
import os
import re

TEMPLATE_DB = "templates.json"

FIELDS = ["vendor", "date", "amount", "tax", "subtotal"]


# =========================================================
# SAFE FLOAT
# =========================================================

def safe_float(value):
    try:
        if isinstance(value, str):
            value = value.replace("₹", "").replace(",", "").strip()
            value = re.sub(r"[^\d.]", "", value)
        return float(value)
    except:
        return 0.0


# =========================================================
# SPATIAL OCR
# =========================================================

def extract_spatial_data(image):
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    data = pytesseract.image_to_data(img_cv, output_type=pytesseract.Output.DATAFRAME)
    data = data.dropna()
    data = data[data['text'].str.strip() != ""]

    spatial_df = data[['text', 'left', 'top', 'width', 'height', 'conf']]
    spatial_df.columns = ['text', 'x', 'y', 'w', 'h', 'conf']

    return spatial_df


# =========================================================
# TEMPLATE STORAGE
# =========================================================

def load_templates():
    if not os.path.exists(TEMPLATE_DB):
        return {}
    with open(TEMPLATE_DB, "r") as f:
        return json.load(f)


def save_template(vendor, template):
    templates = load_templates()
    templates[vendor] = template
    with open(TEMPLATE_DB, "w") as f:
        json.dump(templates, f, indent=4)


def get_template(vendor):
    templates = load_templates()
    return templates.get(vendor)


# =========================================================
# FIELD EXTRACTION USING SPATIAL LOGIC
# =========================================================

def extract_fields_spatial(spatial_df, template=None):

    result = {}

    if spatial_df.empty:
        return result

    # Vendor detection
    top_zone = spatial_df[spatial_df['y'] < 200]
    vendor_words = top_zone.sort_values(by='conf', ascending=False).head(6)
    result['vendor'] = " ".join(vendor_words['text'].tolist())

    # Total detection
    bottom_zone = spatial_df[spatial_df['y'] > spatial_df['y'].max() * 0.7]
    amount_candidates = bottom_zone[bottom_zone['text'].str.contains(r'\d+\.\d+', regex=True)]

    numbers = []
    for txt in amount_candidates['text']:
        matches = re.findall(r'\d+\.\d+', txt)
        for m in matches:
            numbers.append(float(m))

    if numbers:
        result['amount'] = max(numbers)

    # Template override only if missing
    if template:
        for field, coords in template.items():
            if field not in result:
                zone = spatial_df[
                    (spatial_df['x'] > coords['x1']) &
                    (spatial_df['x'] < coords['x2']) &
                    (spatial_df['y'] > coords['y1']) &
                    (spatial_df['y'] < coords['y2'])
                ]
                result[field] = " ".join(zone['text'].tolist())

    return result


# =========================================================
# ACCURACY CALCULATION
# =========================================================

def calculate_accuracy(data):

    score = 0
    total = len(FIELDS)

    for field in FIELDS:
        if data.get(field):
            score += 1

    return int((score / total) * 100)


# =========================================================
# TEMPLATE PIPELINE WITH ACCURACY
# =========================================================

def template_parse_pipeline(image, parsed_data):

    spatial_df = extract_spatial_data(image)

    vendor = parsed_data.get("vendor", "unknown")
    template = get_template(vendor)

    # standard data snapshot
    standard_data = parsed_data.copy()

    # spatial extraction
    spatial_fields = extract_fields_spatial(spatial_df, template)

    # merge safely
    for k, v in spatial_fields.items():
        if not parsed_data.get(k) or parsed_data.get(k) == 0:
            parsed_data[k] = v

    template_data = parsed_data

    # accuracy scoring
    standard_accuracy = calculate_accuracy(standard_data)
    template_accuracy = calculate_accuracy(template_data)

    # confidence score
    confidence = 0.0
    if template:
        confidence += 0.3
    if template_data.get("amount"):
        confidence += 0.4
    if template_data.get("vendor"):
        confidence += 0.3

    confidence = round(confidence, 2)

    # auto learn template
    if not template and vendor != "unknown":
        learn_template(vendor, spatial_df)

    return {
        "standard_data": standard_data,
        "template_data": template_data,
        "standard_accuracy": standard_accuracy,
        "template_accuracy": template_accuracy,
        "confidence": confidence
    }


# =========================================================
# AUTO TEMPLATE LEARNING
# =========================================================

def learn_template(vendor, spatial_df):

    if spatial_df.empty:
        return

    bottom_zone = spatial_df[spatial_df['y'] > spatial_df['y'].max() * 0.7]

    template = {
        "amount": {
            "x1": int(bottom_zone['x'].min()),
            "x2": int(bottom_zone['x'].max()),
            "y1": int(bottom_zone['y'].min()),
            "y2": int(bottom_zone['y'].max())
        }
    }

    save_template(vendor, template)
