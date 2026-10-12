# Invoice Match Auditor

A lightweight tool to extract invoice data and compare it with purchase orders or receipt records, highlighting mismatches for human review.

## MVP goal

Start with CSV inputs and synthetic fixtures. Detect arithmetic differences, duplicate invoice identifiers, supplier mismatches, and quantity/price differences without automatically approving or paying invoices.

## Initial scope

- Import invoice and purchase-order CSV files with a documented schema.
- Normalize supplier names conservatively and show the original values.
- Match records and explain why each match or discrepancy was flagged.
- Export matched, unmatched, and review-needed rows.
- Keep all results explainable and require human approval.

## Open-source foundation and attribution

Research/reference projects: [superintelligenceco/invoice-agent](https://github.com/superintelligenceco/invoice-agent) (Apache-2.0, invoice/PO/receipt matching) and [simeonkolchin/invoice-ocr-framework](https://github.com/simeonkolchin/invoice-ocr-framework) (MIT, template-driven invoice OCR). This repository is a separate MVP scaffold and does **not** currently contain copied upstream source code. Verify upstream license files and dependency terms before importing code; retain required copyright, LICENSE, NOTICE, and modification notices.

## Status and privacy

Early prototype scaffold; not production-ready financial controls. Use synthetic or permissioned data only until access controls, secure storage, retention limits, and audit logs are implemented. Flags are suggestions, not fraud determinations.

## Roadmap

1. Define input schemas and test fixtures.
2. Implement deterministic CSV matching and discrepancy rules.
3. Add report export and tests.
4. Add OCR only after the structured-data workflow is reliable.

## License

Original code in this repository is licensed under the MIT License. Third-party components retain their own licenses and notices. See `LICENSE`.