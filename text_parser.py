import re
from datetime import datetime
import random


# ---------- HELPERS ----------

def _clean_amount(val):
    try:
        clean_val = val.replace(",", "")
        return float(clean_val)
    except Exception:
        return 0.0


def _round2(val):
    return int(val * 100 + 0.5) / 100.0


def _default_bill_id():
    return f"BILL-{random.randint(100000, 999999)}"


def _extract_date(text):
    patterns = [
        r"\b(\d{4}-\d{2}-\d{2})\b",
        r"\b(\d{2}/\d{2}/\d{4})\b",
        r"\b(\d{2}-\d{2}-\d{4})\b",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            raw = m.group(1)
            try:
                if "-" in raw and raw.count("-") == 2:
                    return datetime.strptime(raw, "%Y-%m-%d").strftime("%Y-%m-%d")
                if "/" in raw:
                    return datetime.strptime(raw, "%d/%m/%Y").strftime("%Y-%m-%d")
            except Exception:
                pass

    return datetime.today().strftime("%Y-%m-%d")


# ---------- MAIN PARSER ----------

def parse_receipt(text: str):

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # ---------- BILL ID ----------
    bill_id = None
    for l in lines:
        m = re.search(r"(?i)(bill|invoice|receipt|txn|#)\s*[:.-]?\s*([a-zA-Z0-9/-]+)", l)
        if m:
            bill_id = m.group(2)
            break

    if not bill_id:
        bill_id = _default_bill_id()

    # ---------- VENDOR ----------
    vendor = "Unknown Vendor"
    for line_text in lines[:4]:
        if len(line_text) > 3:
            vendor = line_text
            break

    # ---------- DATE ----------
    date = _extract_date(text)

    # ---------- FINANCIALS (KEYWORD PRIORITY) ----------
    total = 0.0
    tax = 0.0
    subtotal = 0.0

    for l in lines:

        line_lower = l.lower()

        # ignore tips/percentages
        if "tip" in line_lower or "%" in line_lower:
            continue

        if re.search(r"\b(total|amount due|grand total|payable)\b", line_lower):
            nums = re.findall(r"\d+\.\d+", l)
            if nums:
                total = max(_clean_amount(n) for n in nums)

        if re.search(r"\b(subtotal|sub total|net amount)\b", line_lower):
            nums = re.findall(r"\d+\.\d+", l)
            if nums:
                subtotal = max(_clean_amount(n) for n in nums)

        if re.search(r"\b(tax|gst|vat|cgst|sgst)\b", line_lower):
            nums = re.findall(r"\d+\.\d+", l)
            if nums:
                tax += max(_clean_amount(n) for n in nums)

    # fallback detection
    if total == 0:
        nums = re.findall(r"\d+\.\d+", text)
        if nums:
            total = max(_clean_amount(n) for n in nums if _clean_amount(n) > 1)

    if subtotal == 0 and total > 0:
        subtotal = total - tax

    # ---------- ITEMS ----------
    items = []
    for l in lines:

        if re.search(r"(?i)(total|subtotal|tax|cash|card|change)", l):
            continue

        m = re.match(r"(.+?)\s+(\d+\.\d+)$", l)
        if m:
            name = m.group(1).strip()
            price = _clean_amount(m.group(2))
            if 0 < price < total:
                items.append({
                    "Item": name,
                    "Price": price
                })

    # ---------- CATEGORY ----------
    def _extract_category(text, vendor):
        text_lower = text.lower()
        vendor_lower = vendor.lower()

        keywords = {
            "Food": ["restaurant", "cafe", "hotel", "pho", "kitchen"],
            "Medical": ["hospital", "clinic", "pharmacy"],
            "Travel": ["fuel", "uber", "ola"],
            "Shopping": ["mall", "store", "mart"],
        }

        for cat, kw in keywords.items():
            if any(k in vendor_lower for k in kw):
                return cat

        for cat, kw in keywords.items():
            if any(k in text_lower for k in kw):
                return cat

        return "Uncategorized"

    category = _extract_category(text, vendor)

    data = {
        "bill_id": bill_id,
        "vendor": vendor,
        "date": date,
        "amount": _round2(total),
        "tax": _round2(tax),
        "subtotal": _round2(subtotal),
        "category": category
    }

    return data, items
