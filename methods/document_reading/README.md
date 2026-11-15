# Document Reading

`document_reading` reads a document page by page for a caller who will not see it, a person or an agent, and lists every rule, value, threshold, name and constraint each page states or shows, in its exact words. Each page is read from both the text an OCR service extracted from it and a picture of the whole page, so what only a figure, a chart, a diagram, a photograph or a stamp shows is read as well as the text. The method lists what each page holds and leaves relevance to its caller: it never summarizes, ranks or drops anything.

```
github.com/Pipelex/methods/document_reading
```

## What it takes

`read_document`, the package's entry pipe, takes one input:

| Input | Concept | What to give |
|---|---|---|
| `document` | `Document` | A PDF, an image, or a Word or PowerPoint file. A runtime with a document converter reads an Office file through its PDF. |

The sample [`inputs.json`](inputs.json) points at a three-page mutual non-disclosure agreement.

`read_pages`, the second exported pipe, takes `pages`, a list of `Page`, and runs only the reading. It reads again pages that an earlier run of `read_document` extracted, taken from that run's working memory, with no second extraction: a caller uses it to read a page again whose first answer came back thin.

## What it returns

A list of `PageReading`, **one per page, in the order of the pages**. A page answer carries no page number of its own, because the model reading a page is not told its position: the page of an answer is its position in the list, and the caller stamps it. A document's own printed page numbers are kept separately, in `printed_page_number`.

### `PageReading`

| Field | Type | Meaning |
|---|---|---|
| `findings` | list of `Finding` | Every rule, value, threshold, name and constraint the page states or shows. |
| `unreadable` | list of text | What on the page could not be read with confidence, and why. Empty when there is none. |
| `not_looked_at` | list of text | What the page holds that was not shown, not read or not listed in full, such as small print or a table given in part. Empty only when the findings cover the whole page. |
| `printed_page_number` | text | The page number printed in the page's header or footer, when there is one; never a section or chapter number. |

### `Finding`

| Field | Type | Meaning |
|---|---|---|
| `quote` | text | The page's exact words, copied character for character; for what a picture only shows, an exact description of one visible element. |
| `kind` | choice | `rule`, `value`, `threshold`, `name`, `constraint` or `other`. |
| `source` | choice | `text` when the OCR text holds it, `picture` when only the page's picture shows it, `both` when both do. |
| `note` | text | What the finding applies to when its quote does not say it, the picture's reading of a figure the text reads otherwise, or a doubt about the reading. |

## How a page is read

- **Every table row is one finding**, quoted with its column headers, as `Header: value; Header: value`, a merged cell repeated in every row it covers. Every footnote is a finding of its own, with the marker that ties it to what it qualifies.
- **What only a picture shows is listed element by element**: one finding for each visible element that carries a rule, a value or a name, with its source `picture`. A value read from a drawn chart is an estimate and is quoted with "about", as `about 30`.
- **Where the text and the picture disagree on a figure, a word or a name, the text's reading is kept**, since the picture, at 100 dpi, is coarser than the scan the text was read from; the note gives the picture's reading and `unreadable` names the doubt. The picture is trusted for the marks, symbols and layout the text cannot carry, such as a footnote marker or where an element sits.
- **A page answered in part says so** in `not_looked_at`, so a caller can tell a thin answer from a page that holds little. A caller can also compare a page's quotes with its OCR text and read a thin page again with `read_pages`.

## What it costs

One OCR extraction a page, `@default-extract-document`, and one call a page to `claude-5.5-sonnet` at temperature 0, with up to 32,000 output tokens. Measured on Pipelex's hosted API in November 2026, a page cost about $0.035 at the median, about $0.05 on a page of dense prose and up to about $0.09 on a page of dense tables, the model's answer being most of it. The page calls run in parallel, so a document of up to 15 pages took under a minute to about 4 minutes, 50 pages about 6.5 minutes and 150 pages about 12 to 13 minutes.

## What it does not read

- **What no page shows**: a Word document's comments, a deck's speaker notes, a workbook's hidden sheets. The method reads the pages a document prints. A converted Word document shows a tracked deletion beside the current text as if both were current.
- **A workbook as data.** A workbook read through its PDF loses its hidden sheets and breaks its tables across pages; read it as structured data instead.
- **A page range.** The method reads every page of the document it is given; to read chosen pages, give it a document cut down to them.

## Running it

```bash
pipelex run bundle methods/document_reading -i methods/document_reading/inputs.json
```

Or by its address on the hosted API, pinned to a library tag, as the [library's README](../../README.md#running-a-method-by-address) describes.
