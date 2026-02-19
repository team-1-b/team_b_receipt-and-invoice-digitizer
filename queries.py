from db import get_db
from template_parser import safe_float


# ================= SAVE RECEIPT =================
def save_receipt(data):
    """
    Save receipt to database.
    Handles noisy OCR/template values safely.
    """

    db = get_db()

    # Ensure required keys exist
    if "subtotal" not in data:
        data["subtotal"] = 0.0

    if "tax" not in data:
        data["tax"] = 0.0

    if "amount" not in data:
        data["amount"] = 0.0

    if "category" not in data:
        data["category"] = "Uncategorized"

    # SAFE numeric conversion
    amount = safe_float(data.get("amount"))
    tax = safe_float(data.get("tax"))
    subtotal = safe_float(data.get("subtotal"))

    db.execute(
        """
        INSERT INTO receipts (bill_id, vendor, date, amount, tax, subtotal, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("bill_id"),
            data.get("vendor"),
            data.get("date"),
            amount,
            tax,
            subtotal,
            data.get("category"),
        ),
    )

    db.commit()


# ================= DUPLICATE CHECK =================
def receipt_exists(bill_id):
    db = get_db()
    cur = db.execute(
        "SELECT 1 FROM receipts WHERE bill_id = ?",
        (bill_id,)
    )
    return cur.fetchone() is not None


# ================= FETCH ALL RECEIPTS =================
from typing import List, Dict, Any

def fetch_all_receipts() -> List[Dict[str, Any]]:
    db = get_db()

    try:
        cur = db.execute(
            "SELECT bill_id, vendor, date, amount, tax, subtotal, category FROM receipts ORDER BY date DESC"
        )
    except:
        cur = db.execute(
            "SELECT bill_id, vendor, date, amount, tax, 0.0 as subtotal, 'Uncategorized' as category FROM receipts ORDER BY date DESC"
        )

    rows = cur.fetchall()

    return [
        {
            "bill_id": r["bill_id"],
            "vendor": r["vendor"],
            "date": r["date"],
            "amount": safe_float(r["amount"]),
            "tax": safe_float(r["tax"]),
            "subtotal": safe_float(r["subtotal"]),
            "category": r["category"] if r["category"] else "Uncategorized",
        }
        for r in rows
    ]


# ================= DELETE ONE RECEIPT =================
def delete_receipt(bill_id):
    db = get_db()
    db.execute(
        "DELETE FROM receipts WHERE bill_id = ?",
        (bill_id,)
    )
    db.commit()


# ================= CLEAR ALL RECEIPTS =================
def clear_all_receipts():
    db = get_db()
    db.execute("DELETE FROM receipts")
    db.commit()
