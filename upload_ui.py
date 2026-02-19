import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import numpy as np
import cv2

from text_parser import parse_receipt
from validation_ui import validate_receipt
from queries import save_receipt, receipt_exists
from translations import get_text
from template_parser import template_parse_pipeline, safe_float
from item_extractor import extract_items_from_receipt


# =========================================================
# OCR PREPROCESSING
# =========================================================

def preprocess_for_ocr(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh


# =========================================================
# MAIN UPLOAD UI
# =========================================================

def render_upload_ui():

    lang = st.session_state.get("language", "en")
    st.header(get_text(lang, "upload_receipt_header"))

    uploaded = st.file_uploader(
        get_text(lang, "upload_label"),
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if not uploaded:
        st.info(get_text(lang, "upload_info"))
        return

    # =====================================================
    # LOAD IMAGE / PDF
    # =====================================================

    if uploaded.type == "application/pdf":
        from ocr.pdf_processor import pdf_to_images
        pdf_images = pdf_to_images(uploaded.read())

        if not pdf_images:
            st.error("Failed to process PDF")
            return

        img = pdf_images[0]
    else:
        img = Image.open(uploaded)

    # =====================================================
    # DISPLAY IMAGES
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        st.image(img, caption=get_text(lang, "original_image"), use_container_width=True)

    with col2:
        st.image(img.convert("L"), caption=get_text(lang, "processed_image"), use_container_width=True)

    st.divider()

    # =====================================================
    # EXTRACT BUTTON
    # =====================================================

    if not st.button(get_text(lang, "extract_save_btn"), use_container_width=True):
        return

    data = None
    items = []

    # =====================================================
    # OCR TEXT EXTRACTION
    # =====================================================

    gray_preprocessed = preprocess_for_ocr(img)
    text = pytesseract.image_to_string(gray_preprocessed)

    if not text.strip():
        st.error("No text detected from receipt.")
        return

    # =====================================================
    # BASIC TEXT PARSER
    # =====================================================

    try:
        data, items = parse_receipt(text)
    except Exception as e:
        st.error(f"Text parser failed: {e}")
        return

    # =====================================================
    # SMART ITEM EXTRACTION (SPATIAL AI)
    # =====================================================

    try:
        spatial_items = extract_items_from_receipt(img)

        if spatial_items and len(spatial_items) > 0:
            items = spatial_items
            st.success(f"{len(items)} items detected using AI extractor")

    except Exception as e:
        st.warning(f"Item extractor failed: {e}")

    # =====================================================
    # TEMPLATE PARSING ENGINE
    # Template Accuracy + Confidence
    # =====================================================

    try:
        template_result = template_parse_pipeline(img, data)

        data = template_result["template_data"]

        st.info(f"Template Confidence Score: {template_result['confidence']}")
        st.caption(f"Standard Accuracy: {template_result['standard_accuracy']}%")
        st.caption(f"Template Accuracy: {template_result['template_accuracy']}%")

    except Exception as e:
        st.warning(f"Template parser failed: {e}")

    st.session_state["LAST_EXTRACTED_RECEIPT"] = data

    # =====================================================
    # RECEIPT SUMMARY
    # =====================================================

    st.subheader(get_text(lang, "receipt_summary"))

    summary_df = pd.DataFrame([{
        get_text(lang, "bill_id"): data.get("bill_id"),
        get_text(lang, "vendor"): data.get("vendor"),
        get_text(lang, "category"): data.get("category", "Uncategorized"),
        get_text(lang, "date"): data.get("date"),
        get_text(lang, "subtotal_inr"): round(safe_float(data.get("subtotal")), 2),
        get_text(lang, "tax_inr"): round(safe_float(data.get("tax")), 2),
        get_text(lang, "amount_inr"): round(safe_float(data.get("amount")), 2),
    }])

    st.dataframe(summary_df, use_container_width=True)

    # =====================================================
    # ITEM DETAILS
    # =====================================================

    st.subheader(get_text(lang, "item_details"))

    if items and len(items) > 0:
        st.dataframe(items, use_container_width=True)
    else:
        st.info(get_text(lang, "no_item_details"))

    st.divider()

    # =====================================================
    # DUPLICATE CHECK
    # =====================================================

    if data.get("bill_id") and receipt_exists(data["bill_id"]):
        st.error(get_text(lang, "duplicate_error"))
        return

    # =====================================================
    # VALIDATION
    # =====================================================

    validation = validate_receipt(data)
    st.session_state["LAST_VALIDATION_REPORT"] = validation

    # =====================================================
    # SAVE RECEIPT
    # =====================================================

    try:
        save_receipt(data)
    except Exception as e:
        st.error(f"Database Save Failed: {e}")
        return

    # =====================================================
    # RESULT STATUS
    # =====================================================

    if validation.get("passed"):
        st.success(get_text(lang, "validation_passed_save"))
    else:
        st.error(get_text(lang, "validation_failed"))
