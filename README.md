# Pipelex Methods — the public method library

This repository is the public library of packaged [MTHDS](https://mthds.ai) methods, maintained by the [Pipelex](https://pipelex.com) team. Every package here is a directory of `.mthds` bundles governed by a `METHODS.toml` manifest, and the repository itself is the distribution channel: publishing is pushing a git tag, and running a method is naming its address. There is no build step, no upload, and no registry account between you and any method in this library.

## The methods

| Method | What it does | Entry pipe |
|---|---|---|
| [`documents`](methods/documents/) | Document extraction toolbox: text pages, markdown pages, page contents with images and page views, single-text concatenation | `extract_document_markdown` |
| [`doc_summarizer`](methods/doc_summarizer/) | Deep document summarization: profile the document and extract importance-ranked key points in parallel, then synthesize a structured summary with themes and open questions | `summarize_document` |
| [`cv_analyzer`](methods/cv_analyzer/) | End-to-end candidate screening: match a CV against a job offer, then generate tailored interview questions or draft a courteous refusal email | `screen_candidate` |
| [`invoice_extraction`](methods/invoice_extraction/) | Classify each page as bill or receipt, then extract structured invoice data (amounts, VAT, vendor, buyer) from OCR text and page views | `process_invoice` |
| [`table_extraction`](methods/table_extraction/) | Turn a screenshot of a table into faithful HTML, with a vision review pass to correct text and formatting | `extract_html_table_and_review` |
| [`slide_designer`](methods/slide_designer/) | Turn a rough slide-deck brief into design proposals: multiple visual themes, a rendered mockup image for each, and an HTML report presenting them all | `generate_design_proposals_from_rough_brief` |
| [`image_generation`](methods/image_generation/) | Generate images from text: render a description directly, or refine it into an optimized image prompt first | `illustrate` |
| [`tweet_optimizer`](methods/tweet_optimizer/) | Score a draft tech tweet for fluffiness, cringiness, humblebragging and vagueness, then rewrite it in your own writing style | `optimize_tweet_sequence` |
| [`text_stats`](methods/text_stats/) | Deterministic text statistics computed by a sandboxed Python function (PipeFunc, no LLM): counts, vocabulary richness, most frequent words, and estimated reading and speaking times, as a Markdown report | `analyze_text` |

Each package directory carries its manifest, its bundles, and where practical a sample `inputs.json` you can run as-is.

## Addresses

A method in this library is addressed as:

```
github.com/Pipelex/methods/<method_name>[@<tag>]
```

The address without a tag means this repository's default branch at HEAD; `@vX.Y.Z` means the repository at that git tag. The identity comes from each package's manifest — `address = "github.com/Pipelex/methods"` plus its `name` — not from its directory path. Examples:

```
github.com/Pipelex/methods/doc_summarizer
github.com/Pipelex/methods/invoice_extraction@v0.1.0
```

## Running a method by address

Run-by-address is rolling out across the Pipelex toolchain right now; the address grammar above is the contract every surface converges on. Where each surface stands:

- **CLI** — `pipelex run method github.com/Pipelex/methods/<method_name>[@<tag>]`, and the `validate` twin. The fetch honors the tag, locates the package by manifest identity, and runs its `main_pipe` unless you name another pipe.
- **Hosted API** — `POST /v1/start` and `/v1/execute` on `api.pipelex.com` accept the address as `method_ref`; the server fetches the repository itself, so every client shares one implementation and one security model, and every run records the address, the tag, and the resolved commit SHA.
- **SDKs** — `@pipelex/sdk` (TypeScript) and `pipelex-sdk` (Python) pass `method_ref` through the same hosted routes.
- **MCP** — the Pipelex console MCP servers accept the address on their run, validate, and inputs-template tools, so an agent in ChatGPT or Claude can run any method here by pasting its address.

Until the surface you use has shipped its `method_ref` leg, the always-available path is to clone this repository and run locally:

```bash
git clone https://github.com/Pipelex/methods.git
cd methods
pipelex run bundle methods/tweet_optimizer -i methods/tweet_optimizer/inputs.json
```

## Including a method in your own methods

A pipe from this library can be referenced from your own bundles by its address:

```toml
steps = [
  { pipe = "github.com/Pipelex/methods/documents->documents.extract_page_contents_and_views", result = "pages" },
]
```

Today this resolves against packages installed in your project's `.mthds/methods/` directory (copy or clone the package directory in); automatic fetch-on-miss, which makes the reference work on a fresh machine with no install step, is landing in the Pipelex runtime. Only pipes listed in a package's `[exports]` are referenceable across packages.

## Versioning and tags

Repository-level snapshot tags, `vX.Y.Z`: a tag pins the whole library at a commit, and `<address>@<tag>` runs any package exactly as it was at that snapshot. Every package also carries a `version` in its `METHODS.toml`, and the standing convention is **lockstep**: that version is the repository's version, so a package manifest always states the release line it belongs to rather than a count of its own edits. A manifest declaring a version its tag does not carry is a bug — nothing reads the field today, but the moment it becomes authoritative (cache keys, registry indexing, conflict resolution) a manifest disagreeing with its tag resolves silently to the wrong artifact.

Per-package tag prefixes — tagging and versioning one package's release independently of the rest of the library — are the anticipated direction and a planned refinement of the MTHDS packaging spec. That decision is still open; lockstep is the interim convention and holds until it is settled.

### Cutting a release

Before pushing a tag `vX.Y.Z`:

1. Set `version = "X.Y.Z"` in **every** `methods/*/METHODS.toml` — all of them, including the packages that did not change in this release. Lockstep means no manifest is left behind.
2. Commit that version sync, and tag **that commit**, so the tag and the manifests it contains agree.
3. Verify before tagging: `grep -h '^version = ' methods/*/METHODS.toml | sort -u` must print exactly one line, and it must be the version you are about to tag.

## Contributing a method

Contributions are welcome. A submission is a package directory under `methods/`: one `METHODS.toml` manifest and one or more `.mthds` bundles.

**The hosted execution constraint — read this first.** Hosted execution accepts MTHDS concepts and sandboxed PipeFuncs, not in-process Python. Concretely:

- `.mthds` content is always acceptable — it is data, interpreted by the runtime. Define your types as MTHDS concepts (`[concept.X.structure]` tables), which is also what makes them visible to validation, forms, and documentation.
- PipeFunc Python is acceptable: it executes inside a network-blocked sandbox, never in the server process.
- Python structure classes (`structures/*.py` defining `StructuredContent` subclasses) are refused for fetched packages, because structures are imported in-process by the runner. A package carrying them cannot run by address on the hosted platform. Express those types as MTHDS concepts instead.

Beyond that rule:

- **Self-contained packages only, for now.** A package must not reference pipes from other packages (including this library's own `documents`): hosted execution of cross-package closures is gated on upcoming runtime work. Inline what you need.
- **Manifest identity**: `address = "github.com/Pipelex/methods"`, a snake_case `name` matching your directory, a concise `description`, a `version`, and a `main_pipe` where the package has a natural entry point (most should).
- **Exports**: list the pipes you mean callers to use in `[exports.<domain>]`; unlisted pipes stay private to the package.
- **It must validate**: `pipelex validate bundle methods/<your_method>/` must pass before you open a PR.
- **Quality over quantity**: a method that actually runs, with a sample `inputs.json` where practical, beats a pile of stubs. Keep binary assets out of the package — link to hosted samples instead.

## License

MIT — see [LICENSE](LICENSE). Method manifests state their license individually; everything here is MIT.
