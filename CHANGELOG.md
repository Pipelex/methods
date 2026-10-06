# Changelog

## [v0.1.7] - 2026-10-06

### Changed

- **`invoice_extraction` declares no dotted input name**: the internal pipe `extract_invoice_data` drops its redundant input key `"invoice_page.page_view" = "Image"` and keeps `invoice_page = "Page"`, while its prompt still reads the page view through the root as `$invoice_page.page_view`. The root already set the input's concept, so the method runs exactly as before, and it keeps validating once Pipelex refuses dotted input names with `invalid_input_name`. At `v0.1.6` and earlier the package still declares the dotted key and stops validating under that refusal: run it at `@v0.1.7` or later.

## [v0.1.6] - 2026-10-03

### Added

- **`image_card`**: generates an image from a text description with the deck's small image generation model, `@default-small`, and presents the image and its description side by side in an HTML page. Its entry pipe, `generate_image_card`, takes a `description` text, like `image_generation_fast`'s `generate_image`, and returns an `Html` page. The page links the image by its storage URL, so where signed URLs are configured the image stops showing once the link expires.

## [v0.1.5] - 2026-10-03

### Added

- **`image_generation_fast`**: generates an image directly from a text description with the deck's small image generation model, `@default-small`, trading quality for speed and cost. Its entry pipe, `generate_image`, takes a `description` text and returns an `Image`, like `image_generation`'s pipe of the same name, so the two are interchangeable.

## [v0.1.4] - 2026-09-25

### Fixed

- **`doc_summarizer`'s sample document**: its `inputs.json` links a real document, the cookbook's CatOps pitch deck at the cookbook's `v0.18.0` tag, where it named a placeholder host that never resolves. At `v0.1.3` and earlier the sample does not run: run it at `@v0.1.4` or later.

## [v0.1.3] - 2026-09-25

### Added

- **`CHANGELOG.md`**: the library's release history, from `v0.1.0` on. Each GitHub Release's notes are its version's entry here.

### Changed

- **Every model goes through the standard model deck**: `image_generation`'s image pipes use `@default-general` instead of `nano-banana-2`, `slide_designer`'s mockup renderer uses `@default-premium` instead of `nano-banana-pro`, and `documents`' markdown extraction uses `@default-extract-document` instead of `azure-document-intelligence`, so no method in the library names a model outright. Run at `@v0.1.3`, these pipes use whichever model the deck assigns to each alias, which can differ from the model they named at `v0.1.2`.

## [v0.1.2] - 2026-09-25

### Changed

- **`invoice_extraction`'s sample invoice is pinned**: its `inputs.json` links the invoice at the cookbook's `v0.18.0` tag rather than its `main`, so the sample cannot change under a library tag.

### Fixed

- **`table_extraction`'s sample table image**: its `inputs.json` links the image under the cookbook's `assets/` at the cookbook's `v0.18.0` tag. The old link, under the cookbook's `examples/` tree, stops resolving once the cookbook removes that tree from its `main`, so from then on the sample does not resolve at `v0.1.1` and earlier: run it at `@v0.1.2` or later.
- **Every package manifest states the library's version**: each `METHODS.toml` declares `0.1.2`, where the manifests at `v0.1.1` still declared `0.1.0` or `0.2.0`. A package's version is the library's version, and every manifest moves with each release.

## [v0.1.1] - 2026-08-29

### Added

- **`text_stats`**: deterministic text statistics computed by a sandboxed Python function, with no LLM: counts, vocabulary richness, the most frequent words, and estimated reading and speaking times, as a Markdown report. It is the library's first package carrying a PipeFunc.

## [v0.1.0] - 2026-08-29

### Highlights

**The first curated snapshot of the public method library.** Every package is self-contained and runs on the hosted API by its address, `github.com/Pipelex/methods/<name>@v0.1.0`, and every manifest follows the MTHDS packaging rules.

### Added

- **The first methods**: `documents`, `doc_summarizer`, `cv_analyzer`, `invoice_extraction`, `table_extraction`, `slide_designer`, `image_generation` and `tweet_optimizer`, each a directory of `.mthds` bundles under a `METHODS.toml` manifest, most with a sample `inputs.json` that runs as it is.
- **The library's front page**: the README, which lists the methods, the address grammar, how to run a method by its address and how to contribute one, and the MIT license.
