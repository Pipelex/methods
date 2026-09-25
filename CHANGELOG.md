# Changelog

## [Unreleased]

### Added

- **`CHANGELOG.md`**: the library's release history, from `v0.1.0` on. Each GitHub Release's notes are its version's entry here.

### Changed

- **Every model goes through the standard model deck**: `image_generation`'s image pipes use `@default-general` instead of `nano-banana-2`, `slide_designer`'s mockup renderer uses `@default-premium` instead of `nano-banana-pro`, and `documents`' markdown extraction uses `@default-extract-document` instead of `azure-document-intelligence`, so no method in the library names a model outright.

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
