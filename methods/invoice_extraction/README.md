# Invoice Extraction

`invoice_extraction` reads a document holding invoices or receipts and returns what each page says: the vendor and the buyer, the dates, the totals and the tax, the currency the amounts are in, and the purchase line by line. It works from both the text extracted from each page and a picture of the page, so a scanned receipt reads as well as a generated PDF.

```
github.com/Pipelex/methods/invoice_extraction
```

## What it takes

`process_invoice`, the package's entry pipe, takes one input:

| Input | Concept | What to give |
|---|---|---|
| `document` | `Document` | A PDF or an image of one or more invoices or receipts. |

The sample [`inputs.json`](inputs.json) points at a scanned take-out receipt.

## What it returns

A list of `Invoice`, **one per page** of the document. Each page is first classified as a formal bill or a simple receipt, then read on its own, so an invoice whose lines run over two pages comes back as two results, each carrying that page's lines.

### `Invoice`

| Field | Type | Meaning |
|---|---|---|
| `invoice_id` | text | A unique identifier for the invoice. |
| `invoice_number` | text | The invoice number as shown on the document. |
| `issue_date` | date | The date the invoice was issued. |
| `time` | text | The time of the transaction, when the document prints one. |
| `amount_incl_tax` | number | The total including taxes, in `currency`. |
| `amount_excl_tax` | number | The net amount excluding taxes, in `currency`. |
| `vat_amount` | number | The total VAT or tax amount, in `currency`. |
| `currency` | text | The ISO 4217 code of the currency the invoice's totals and lines are expressed in, such as `EUR` or `USD`. Empty when the document does not determine it (see below). |
| `vat_rates` | list of numbers | The VAT rates applied, as percentages: `20` for 20 %. |
| `vendor` | text | The vendor's name. |
| `vendor_address` | text | The vendor's address. |
| `vendor_siret` | text | The vendor's SIRET number, for a French company. |
| `vendor_vat_number` | text | The vendor's VAT registration number. |
| `company_name` | text | The purchasing company's name. |
| `company_address` | text | The purchasing company's address. |
| `description` | text | A one-line summary of what was purchased. |
| `line_items` | list of `InvoiceLineItem` | The priced lines of the invoice, in the order printed (see below). |
| `category` | `InvoiceDetails` | Whether the page is a `bill` or a `receipt`, with the reason. |
| `text` | text | The raw text extracted from the page. |

Every field may be empty when the page does not show it.

### `InvoiceLineItem`

| Field | Type | Meaning |
|---|---|---|
| `label` | text | What the line is for, as printed: the product, service, fee or discount. Always present. |
| `quantity` | number | How many units, or how much, as printed. Fractional for a weighed or measured item. Empty when the line prints no quantity. |
| `unit_price` | number | The price of one unit, in `currency`, when the line prints it. |
| `amount` | number | The line's total, in `currency`, as printed. Negative for a discount or a refund. |

## How the currency is determined

The method reads the currency from the document and never assumes one. It is the currency of the invoice's own amounts, its totals and its lines, and only what qualifies those amounts counts: a converted amount, an exchange rate or a card-payment line printed in another currency, such as a card slip in the cardholder's currency, is ignored. It takes, in this order:

1. a currency code the document gives for those amounts, beside them or in a statement such as "all prices in EUR";
2. otherwise, a symbol printed with them that names one currency only, such as `€` or `₹`;
3. otherwise, for a symbol several currencies share, such as `$`, `£`, `¥` or `kr`, where the document was issued, as the document itself shows it: the vendor's address, a city or a landmark in its name or header, its phone number's format, its tax identifiers or the name its tax goes by.

When none of these settles it, or when the totals and lines are themselves in more than one currency, `currency` stays empty: a missing currency is safer to display than a wrong one. A second currency on the document, such as a converted total, is not represented.

## Which lines are line items

Every priced line of the document, in the order printed: each product or service, and each fee, deposit, surcharge, shipping charge or discount wherever it is printed, a surcharge below the subtotal included. The subtotal, tax, total, payment, tender and change lines are never line items, and neither is a line that only sums lines already listed, such as a subtotal per category: the totals and the tax are the invoice's own amounts, and the payment lines describe how it was paid rather than what was bought. A line's values are taken as printed and never recomputed, so a line that prints no unit price has none, and line amounts are before or after tax exactly as the document itemizes them.

## Running it

```bash
pipelex run bundle methods/invoice_extraction -i methods/invoice_extraction/inputs.json
```

Or by its address on the hosted API, pinned to a library tag, as the [library's README](../../README.md#running-a-method-by-address) describes.
