---
name: release
description: >
  Cut a release of methods, the public MTHDS method library at
  github.com/Pipelex/methods: the release/vX.Y.Z worktree, the lockstep bump of
  every methods/*/METHODS.toml, the changelog entry, the format, lint,
  validation and sample gates, one commit, and a pull request to main whose
  merge creates the annotated vX.Y.Z tag every pinned address resolves against.
  Use when the user says "release", "cut a release", "bump version", "prepare a
  release", "new version", "make a release", "ship it", "create release
  branch", "promote dev to main", "tag the library", "snapshot the library", or
  wants a change reachable at a new @vX.Y.Z address. Changelog content passed
  inline ("/release Added a contract review method") becomes the entry. The
  merge is landed by /ledger-land, never by this skill.
---

# Releasing the method library

The procedure is the workspace release play, [`docs/workspace/releasing.md`](../../../../docs/workspace/releasing.md) at the workspace root — `../docs/workspace/releasing.md` from this repo's own root, which resolves the same from the main checkout and from any worktree. Read it first, then run it with what follows. The repo key is `methods`, the base is `dev`, and the pull request targets `main`. The release worktree is `_methods--release`, made with `wt add methods release --branch release/vX.Y.Z`. The repo declares no `.worktree.toml`, no `.worktreeinclude` and no Makefile, so `wt` resolves the base from `origin/dev` and provisions nothing: the gates run with the `pipelex`, `plxt`, `curl` and `jq` installed on the machine. The repo's own account of the scheme, the workflows and why they are built as they are is [`docs/releasing.md`](../../../docs/releasing.md).

## What ships

Nothing is published to a package registry: the repository is the distribution channel, and what the merge to `main` produces is the annotated `vX.Y.Z` tag that every address pinned to the release resolves against, `github.com/Pipelex/methods/<name>@vX.Y.Z`, with a GitHub Release beside it. Both are created by `.github/workflows/github-release.yml`, which fires on the push to `main`, and on a `workflow_dispatch` for a re-run, which it refuses from any branch but `main`:

- It reads the version every `methods/*/METHODS.toml` declares, and fails when they do not all declare the same one, so a manifest left behind tags nothing.
- It is guarded on what already exists, because `main` moves between releases without a version bump: with the tag and the Release both there it reports that the push carried no bump and stops, and with the tag there and no Release it creates only the Release.
- It tags the release pull request's merge commit, which it asks GitHub for as the pull request from `release/vX.Y.Z` merged into `main`, never the commit its own run checked out. So a release run cancelled while pending behind another push, a failed run followed by a routine push, and a re-dispatch after `main` moved all tag the same commit. It refuses when no such pull request was merged.
- It refuses to tag when `CHANGELOG.md` at that commit has no `## [vX.Y.Z] - ` heading. Otherwise it creates the tag with `git tag -a` on the merge commit, message `Library snapshot vX.Y.Z`, pushes it, and calls `gh release create --verify-tag` with the notes sliced from the changelog: everything between the version's heading and the next `## [v…] - ` heading. Never create the tag by hand first; the workflow tags.

The landing verifies the publish from the run, the tag and the Release:

```bash
gh run list --workflow=github-release.yml --branch main --limit 3 --json conclusion,headSha,url   # the run whose headSha is the merge SHA: success, or a later one if it was cancelled
git -C <main> fetch --tags --prune origin && git -C <main> rev-list -n 1 vX.Y.Z                 # the tag, on the merge SHA
gh release view vX.Y.Z                                                                           # the Release and its notes
```

Once the tag exists, the landing proves what the release is for: every package runs by its address at the tag. From `<main>`, with `PIPELEX_API_KEY` set, run `.claude/skills/release/scripts/check-addresses.sh vX.Y.Z`. It lists the packages the tag itself carries, asks the hosted API's `POST /v1/validate` to fetch and validate each one at `<address>/<name>@vX.Y.Z`, and spends no inference. Every line must read `✓`. A `✗` is a release that did not do its job, since the hosted fetch refuses that package at its own tag: report it with the line the script printed, and file the fix against `methods` as a bug discovered from the release item.

If the run failed, read its log before anything else. Its deliberate refusals, manifests that disagree and a missing changelog entry, are also what the pull request's checks assert, so either one reaching `main` means a check was bypassed. A failure from outside the repository is re-run with `gh run rerun <run id> --failed`, or, once `main` has moved on, with `gh workflow run github-release.yml --ref main`. The guards make either safe, since the tag lands on the merge commit whichever run creates it.

## Version files and the lock

- **Every `methods/*/METHODS.toml`** — the `[package]` table's `version`, with no `v` prefix. The library versions in lockstep: a package's version is the library's version, so every manifest moves with every release, including the manifests of packages the release did not touch. Each manifest opens exactly one line with `version = `, so one command sets them all: `perl -pi -e 's/^version = ".*"/version = "X.Y.Z"/' methods/*/METHODS.toml`, using perl because the in-place flag of `sed -i` differs between macOS and GNU. `mthds_version`, the version of the standard a package requires, is a different field and never moves with a release.
- **No lock.** Nothing is installed, and nothing records the version a second time.
- **Also stamped:** nothing. There is no `VERSION` file, no badge and no version literal. The README's example addresses illustrate the grammar and stay as they are, and a sample `inputs.json` pins the cookbook's tags, never this repo's.

## Gates

Run at the root of the worktree, in this order. Every one is blocking.

1. **Lockstep** — `grep -h '^version = ' methods/*/METHODS.toml | sort -u` must print exactly one line. Before the bump that line is the previous release's version, and a second line means a package reached `dev` declaring another one; the bump cures it, since it rewrites every manifest. **After the bump** it runs again and must print exactly `version = "X.Y.Z"`.
2. **Format and lint** — `plxt fmt --check`, then `plxt lint`, over every `.mthds` bundle and `METHODS.toml`. The repo carries no `plxt` configuration, so `plxt` reads the machine's own, `~/.pipelex/plxt.toml` when there is one. A red format check is cured by `plxt fmt`, which rewrites, and whatever it touched joins the release commit. A red lint is a bundle to fix on `dev` through an ordinary branch before the release is cut again.
3. **Every package validates** — `for d in methods/*/; do pipelex validate bundle "$d" >/dev/null || echo "✗ $d"; done` prints nothing when every package passes; re-run a failing one without the redirect to read why. It is the static validation and dry run the README asks of every contribution, and it spends no inference. A red package is fixed on `dev` through an ordinary branch, never inside the release commit.
4. **Every sample resolves** — `.claude/skills/release/scripts/check-samples.sh` reads every `url` in every `methods/*/inputs.json` and must print `✓` for each one. It refuses by name a host under a reserved domain (`.invalid`, `.test`, `.example`, `.localhost`, `example.com` and its siblings), which is what a generated inputs template leaves behind, and a `raw.githubusercontent.com` link whose ref is not a `v*` tag; it asks every other URL for its first byte and wants a `2xx`. It needs `curl` and `jq`, no API key, and spends no inference. Validation never fetches a sample, which is how `doc_summarizer` shipped a placeholder from `v0.1.0` to `v0.1.3`, and a tag freezes its samples for good. A red sample is fixed on `dev` through an ordinary branch, never inside the release commit.

## The release commit

`CHANGELOG.md` and every `methods/*/METHODS.toml`, plus each file `plxt fmt` rewrote, staged by name: `git add CHANGELOG.md methods/*/METHODS.toml`, the shell spelling the glob out into names.

## CI on the release pull request

- `version-check.yml` — every `methods/*/METHODS.toml` declares the version in the `release/vX.Y.Z` branch name, and the failure names each manifest that does not.
- `changelog-check.yml` — `CHANGELOG.md` carries `## [vX.Y.Z] - …` for that version, and no `[Unreleased]` heading survives.

Both act only on a head matching `^release/v([0-9]+\.[0-9]+\.[0-9]+)$` and pass trivially on any other pull request into `main`. Nothing in CI formats, lints or validates a bundle, or checks a sample link: the gates above run here and nowhere else.

## Particulars

- **`main` is the default branch, and it moves between releases.** An address without a tag runs `main` at its head, so `main` is fast-forwarded to `dev` when a change should reach those callers before a tag does, and `origin/main..dev` can then be empty while work is still unreleased. What a release carries is everything since the last tag: in the play's step 1, read `git -C <main> log $(git -C <main> describe --tags --abbrev=0)..dev --oneline` rather than `origin/main..dev`. The release pull request still targets `main` and still merges with a merge commit, whether or not `main` had already caught up.
- **What counts as breaking.** The bump follows the play's pre-1.0 rule, read for a method library: a change that breaks a caller moving an address from the previous tag to this one is a **minor** — a package renamed or removed, an exported pipe renamed, removed or no longer exported, a `main_pipe` changed, or the inputs or output concept of an exported pipe changed. Everything else is a **patch**: a new package, a new pipe, a better prompt, a model moved to a deck alias, a sample fixed. `v0.1.1`, which added `text_stats`, was a patch.
- **The changelog entry speaks to a caller who pins a tag.** Name the package and the pipe or the sample, and say what running it at the new tag changes. When a change makes something stop resolving at older tags, such as a sample link that moved in `v0.1.2`, say so and name the tag to run instead. The headings carry the `v`, `## [vX.Y.Z] - YYYY-MM-DD`, which is what `changelog-check.yml` greps for and what `github-release.yml` slices the Release notes from.
- **No pre-release form.** Both pull-request checks skip a head like `release/v0.2.0-rc.1` rather than failing it, and `github-release.yml` tags whatever the manifests declare, so an `rc` would ship as a tag any address could pin. Ship a plain `X.Y.Z`, which is also the tag form the address grammar recommends.
- **The tags are annotated.** `v0.1.0` to `v0.1.2` were created by hand, each with a one-line summary as its message; from the release that first carries `github-release.yml`, the workflow creates them with the message `Library snapshot vX.Y.Z`. A lightweight `v0.0.1` also exists, on a commit after `v0.1.0`; `git describe --tags` from `dev` answers the nearest release tag and is not misled by it.
- **The pull request body names the manifests.** The repo has no single version file, so the play's "Bumps version" line reads "Bumps every package manifest from `A.B.C` to `X.Y.Z`."
- **Consumers pin library tags, and a release moves none of them.** The cookbook, both starters, the method-app template, the plugins and the MCP name addresses at tags of this library in their docs, samples and tests. When a release fixes something one of them pins, as `v0.1.2` did for `table_extraction`'s sample, file the move against that repo; whether and when it moves is that repo's call.
- **The skill, the docs page and the workflows move together.** This skill, `docs/releasing.md` and the workflows in `.github/workflows/` state the same rules; a change to one of them changes the others in the same commit.
- **No release follow-ups are armed.** `ledger.toml` declares no `release_followups` for `methods`, so filing the release item materializes no blocked tasks; anything a release owes another repo is filed by hand beside it.
