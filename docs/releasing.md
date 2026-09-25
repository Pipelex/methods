# Releasing the method library

This library publishes no package. The repository is the distribution channel, and a release is a git tag: an address pinned to it, `github.com/Pipelex/methods/<name>@vX.Y.Z`, runs every package exactly as it was at that tag. So **the annotated `vX.Y.Z` tag is the release artifact**, and everything on this page exists to make sure a tag is only ever created on a commit whose manifests and changelog agree with it.

## The scheme

- **The version lives in every `methods/*/METHODS.toml`**, as the `[package]` table's `version`, with no `v` prefix. The library versions in lockstep: a package's version is the library's version, so every manifest moves with every release, including those of packages the release did not touch. There is no `VERSION` file and no second place the number is written.
- **`CHANGELOG.md`** is the release record, one `## [vX.Y.Z] - YYYY-MM-DD` entry per release, with work in progress gathered under `## [Unreleased]` until it ships. An entry speaks to a caller who pins a tag: which package, pipe or sample changed, and what running it at the new tag changes for them.
- **Annotated `vX.Y.Z` tags on `main`**, created by a workflow on the release pull request's merge commit, never by hand.
- **`main` is the default branch**, and an address without a tag runs it at its head. It can therefore move ahead of the last tag between releases, so what a release carries is everything since the last tag, not the difference between `dev` and `main`.

The `v` prefix appears in branch names, changelog headings and tags, never in a manifest.

## What counts as breaking

The library is pre-1.0, so a breaking change is a **minor** and everything else a **patch**. A change is breaking when it breaks a caller who moves an address from the previous tag to the new one: a package renamed or removed, an exported pipe renamed, removed or no longer exported, a `main_pipe` changed, or the inputs or output concept of an exported pipe changed. A new package, a new pipe, a better prompt, a model moved to a deck alias or a fixed sample is a patch. Pre-release forms (`-rc.1`) are not used: a tag is something any address can pin.

## Cutting a release

A release is a `release/vX.Y.Z` branch cut from `dev` and merged into `main` by pull request, with a merge commit.

1. On the release branch, set the version in every manifest: `perl -pi -e 's/^version = ".*"/version = "X.Y.Z"/' methods/*/METHODS.toml`. Then `grep -h '^version = ' methods/*/METHODS.toml | sort -u` must print exactly one line, the version being released.
2. In the same commit, turn the `## [Unreleased]` section of `CHANGELOG.md` into the release's entry, `## [vX.Y.Z] - YYYY-MM-DD`, leaving no `[Unreleased]` heading behind.
3. Before committing, check the bundles: `plxt fmt --check` and `plxt lint` over every `.mthds` and `METHODS.toml`, and `pipelex validate bundle methods/<name>/` for every package.
4. Check that every sample resolves: `.claude/skills/release/scripts/check-samples.sh` reads every `url` in every `methods/*/inputs.json`, refuses a placeholder on a reserved domain such as `.invalid` and a `raw.githubusercontent.com` link whose ref is not a `v*` tag of its repository, whether linked directly or reached by a redirect such as a `github.com/…/raw/…` link, asks every other URL for its first byte, spends no inference, and must print `✓` for every one. Validation never fetches a sample, and a tag freezes its samples for good, so this is the one moment a dead sample link can be caught before it ships. A sample file hosted on GitHub is a house-owned asset linked at one of the cookbook's tags, never at a branch and never at a tag of this repository, so it cannot change under a library tag.
5. Open the pull request into `main`. Its checks refuse a manifest that does not declare the branch's version, and a changelog without the entry.
6. The merge creates the tag and the GitHub Release. Once the tag exists, check that every package runs by its address at it: `.claude/skills/release/scripts/check-addresses.sh vX.Y.Z`, with `PIPELEX_API_KEY` set, asks the hosted API to fetch and validate each package at the tag, spends no inference, and must print `✓` for every one.

The Pipelex team runs these steps with the repository's `/release` skill for Claude Code, [`.claude/skills/release/SKILL.md`](../.claude/skills/release/SKILL.md), inside the workspace release play that every Pipelex repository shares.

## The workflows

| Workflow | Fires on | Enforces |
|---|---|---|
| `version-check.yml` | pull request → `main` | every `methods/*/METHODS.toml` declares the version in the `release/vX.Y.Z` branch name |
| `changelog-check.yml` | pull request → `main` | `CHANGELOG.md` has `## [vX.Y.Z] - …` for that version, and no `[Unreleased]` heading survives |
| `github-release.yml` | push to `main`, and `workflow_dispatch` from `main` | creates the annotated tag on the release pull request's merge commit, and the GitHub Release |

The pull-request checks act only on a head matching `release/vX.Y.Z` exactly and pass trivially on anything else. They read the branch name from an environment variable rather than splicing it into their script, since in a public repository anyone can open a pull request from a branch named with shell syntax. Nothing in CI formats, lints or validates a bundle, or checks a sample link: steps 3 and 4 above run on the releaser's machine and nowhere else. A check of the sample links in CI would also catch a dead link on an ordinary pull request, but it would make every pull request depend on third-party hosts answering, and the release is the moment a sample becomes immutable.

### Why the tagger creates the tag itself

`gh release create vX.Y.Z` creates a *lightweight* tag when the tag does not exist yet. Because the tag here is the artifact rather than a pointer at a published package, `github-release.yml` creates it with `git tag -a` (message `Library snapshot vX.Y.Z`) on the merge commit and pushes it, then calls `gh release create --verify-tag`, which aborts rather than substituting a lightweight tag if the annotated one is somehow missing.

### Which commit the tag goes on

The tag goes on the release pull request's merge commit, which the workflow finds by asking GitHub for the pull request from `release/vX.Y.Z` merged into `main`, and never on the commit its own run checked out. The two are the same when the run is the merge's own. They differ when the merge's run was cancelled while pending, since a concurrency group keeps a single pending run and cancels it when another push queues; when the merge's run failed before tagging and a later push to `main` ran; and when the workflow was dispatched again after `main` moved on. In each case, tagging the run's own commit would pin a commit carrying work the release does not. The workflow refuses to tag when no such pull request was merged or when its merge commit is not in `main`'s history, and it reads the changelog entry at that commit, so the Release's notes are the ones the tag carries.

A dispatch from any branch other than `main` is refused before anything runs. On a release branch it would otherwise tag the branch's head before the merge, and the merge's own run would then find the tag taken and leave it where it was.

### Idempotency

Pushes to `main` that carry no version bump are routine, since `main` moves ahead between releases, so every step is guarded on what already exists:

- The version is read from the manifests first, and the workflow fails when they do not all declare the same one, so a manifest left behind tags nothing.
- Tag and Release both exist: the workflow reports that the push carried no bump and stops.
- Neither exists: it finds the release pull request's merge commit, verifies the changelog entry there, tags that commit, then releases.
- The tag exists and the Release does not, after a partial earlier run: it leaves the tag alone and creates only the Release.

The changelog check runs before any tag is written, so a version bump that reached `main` without a changelog entry fails the workflow instead of producing a tag with no release notes. A failure from outside the repository is re-run with `gh run rerun <run id> --failed`, or by dispatching the workflow from `main`, and these guards make either safe: the tag lands on the merge commit however far `main` has moved since.

### Release notes

A Release's body is the changelog entry for its version: everything between its `## [vX.Y.Z] - …` heading and the next `## [v…] - …` heading, heading excluded. Nothing is generated from commit messages, so the changelog is the single source of release notes.

## History

`v0.1.0`, `v0.1.1` and `v0.1.2` were tagged and released by hand, before the changelog and the workflows existed; their tag messages carry a one-line summary of each release, and their changelog entries were written afterwards from those tags and the `v0.1.2` Release. A lightweight `v0.0.1` tag also exists, on a commit after `v0.1.0`. It marks no release, and `git describe --tags` from `dev` answers the nearest release tag regardless.
