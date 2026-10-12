#!/usr/bin/env python3
"""Explainable CSV invoice-to-PO matcher prototype. No payment actions."""
import argparse, csv, json
from pathlib import Path

def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [{str(k).strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in rows]

def norm(value): return " ".join((value or "").casefold().split())

def match(invoice_path, po_path, tolerance=0.02):
    invoices, orders = load(invoice_path), load(po_path)
    by_id = {r.get("po_id", ""): r for r in orders if r.get("po_id")}
    results = []
    for inv in invoices:
        po = by_id.get(inv.get("po_id", ""))
        reasons = []
        if not inv.get("invoice_id"): reasons.append("missing invoice_id")
        if not po: reasons.append("purchase order not found")
        else:
            if norm(inv.get("supplier")) != norm(po.get("supplier")): reasons.append("supplier mismatch")
            try:
                amount_inv, amount_po = float(inv.get("amount", "")), float(po.get("amount", ""))
                if abs(amount_inv - amount_po) > tolerance: reasons.append(f"amount mismatch: invoice={amount_inv:.2f}, PO={amount_po:.2f}")
            except ValueError: reasons.append("amount missing or invalid")
        results.append({"invoice_id": inv.get("invoice_id", ""), "po_id": inv.get("po_id", ""), "status": "review" if reasons else "matched", "reasons": reasons})
    seen, duplicates = set(), set()
    for inv in invoices:
        key = inv.get("invoice_id", "")
        if key and key in seen: duplicates.add(key)
        seen.add(key)
    for row in results:
        if row["invoice_id"] in duplicates:
            row["status"] = "review"
            row["reasons"].append("duplicate invoice_id in input")
    return {"invoice_count": len(invoices), "po_count": len(orders), "results": results, "notice": "Prototype matching only. Review every flagged and matched record; this tool does not approve invoices or initiate payments."}

def main():
    p = argparse.ArgumentParser(description="Match invoice CSV rows to PO CSV rows")
    p.add_argument("invoices_csv")
    p.add_argument("purchase_orders_csv")
    p.add_argument("--tolerance", type=float, default=0.02)
    p.add_argument("--out")
    a = p.parse_args()
    result = match(a.invoices_csv, a.purchase_orders_csv, a.tolerance)
    output = json.dumps(result, indent=2)
    if a.out: Path(a.out).write_text(output + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__": main()
