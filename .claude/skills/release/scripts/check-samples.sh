#!/usr/bin/env bash
# Check that every URL a sample inputs.json links answers.
#
#   check-samples.sh [inputs.json ...]
#
# With no argument it reads every methods/*/inputs.json of the checkout the
# script lives in, wherever it is run from; name files to check those instead.
# It takes every `url` value in each file, at any depth, and refuses one that
# is not an http(s) URL, one whose host is under a domain reserved for
# documentation and testing (.invalid, .test, .example, .localhost, and
# example.com, example.net, example.org), which is what a generated inputs
# template's placeholder looks like, and a raw.githubusercontent.com URL whose
# ref is not a v* tag, since a sample must not change under a library tag. A
# bare ref (<owner>/<repo>/<ref>/<file>) is looked up with git ls-remote, since
# a branch can be named like a version: it must be a tag of that repository
# and not also a branch. Every other URL must answer a request for its first
# byte with a 2xx, and a URL that redirects is held to the same rules where it
# lands, which is how github.com's /raw/ and ?raw=true links are checked. No
# call spends inference. Prints one line per URL, and one per file jq cannot
# read, and exits non-zero when any line is a failure.
#
# Needs curl, git and jq.

set -euo pipefail

for arg in "$@"; do
  if [[ "$arg" == -* ]]; then
    echo "usage: $0 [inputs.json ...]" >&2
    exit 2
  fi
  [ -f "$arg" ] || { echo "$arg: no such file" >&2; exit 2; }
done
for tool in curl git jq; do
  command -v "$tool" >/dev/null || { echo "$tool is required" >&2; exit 2; }
done

if [ "$#" -eq 0 ]; then
  cd "$(dirname "$0")/../../../.."
  shopt -s nullglob
  set -- methods/*/inputs.json
  shopt -u nullglob
fi

errors=$(mktemp)
trap 'rm -f "$errors"' EXIT
failures=0

# Why a URL is refused before anything fetches it, or nothing when it is not.
refusal() {
  local url=$1 rest host owner repo ref kind name spelled_as_tag refs
  if [[ ! "$url" =~ ^[Hh][Tt][Tt][Pp][Ss]?:// ]]; then
    echo "not an http(s) URL, so the hosted API cannot fetch it"
    return
  fi
  rest=${url#*://}
  host=${rest%%[/?#]*}
  host=${host##*@}
  host=${host%:*}
  host=$(printf '%s' "$host" | tr '[:upper:]' '[:lower:]')
  host=${host%.}
  case "$host" in
    invalid | *.invalid | test | *.test | example | *.example)
      echo "$host is under a reserved top-level domain that never resolves: a placeholder, not a sample"
      return
      ;;
    localhost | *.localhost)
      echo "$host is the machine making the request, never a public host: a placeholder, not a sample"
      return
      ;;
    example.com | *.example.com | example.net | *.example.net | example.org | *.example.org)
      echo "$host is a reserved example domain: a placeholder, not a sample"
      return
      ;;
  esac
  if [ "$host" = raw.githubusercontent.com ]; then
    # The path is /<owner>/<repo>/<ref>/<file>, the ref possibly spelled refs/tags/<tag>.
    IFS=/ read -r owner repo ref kind name _ <<<"${rest#*/}"
    spelled_as_tag=false
    if [ "$ref" = refs ]; then
      if [ "$kind" != tags ]; then
        echo "names refs/$kind/$name, which is not a tag, so the file can change under a library tag: link it at a v* tag of $owner/$repo"
        return
      fi
      ref=$name
      spelled_as_tag=true
    fi
    if [[ ! "$ref" =~ ^v[0-9] ]]; then
      echo "names the ref '$ref', which is not a v* tag, so the file can change under a library tag: link it at a v* tag of $owner/$repo"
      return
    fi
    # A bare ref is whatever GitHub resolves the name to, and a branch can be
    # named like a version, so ask GitHub which one it is.
    if [ "$spelled_as_tag" = false ]; then
      if ! refs=$(GIT_TERMINAL_PROMPT=0 git ls-remote "https://github.com/$owner/$repo.git" "refs/tags/$ref" "refs/heads/$ref" 2>"$errors"); then
        echo "cannot list the refs of $owner/$repo on GitHub: $(head -n 1 "$errors")"
        return
      fi
      if [ -z "$(awk -v want="refs/tags/$ref" '$2 == want' <<<"$refs")" ]; then
        echo "names '$ref', which is not a tag of $owner/$repo, so the file can change under a library tag: link it at a v* tag"
        return
      fi
      if [ -n "$(awk -v want="refs/heads/$ref" '$2 == want' <<<"$refs")" ]; then
        echo "names '$ref', which is both a tag and a branch of $owner/$repo: spell it refs/tags/$ref so the tag is what is served"
        return
      fi
    fi
  fi
}

for file in "$@"; do
  if ! urls=$(jq -r '.. | objects | .url? | strings' "$file" 2>"$errors"); then
    echo "✗ $file — not valid JSON: $(head -n 1 "$errors")"
    failures=$((failures + 1))
    continue
  fi
  while IFS= read -r url; do
    [ -n "$url" ] || continue
    reason=$(refusal "$url")
    if [ -n "$reason" ]; then
      echo "✗ $file: $url — $reason"
      failures=$((failures + 1))
      continue
    fi
    if ! fetched=$(curl -sSL -r 0-0 --max-time 30 --retry 2 -o /dev/null \
      -w '%{http_code} %{num_redirects} %{url_effective}' "$url" 2>"$errors"); then
      echo "✗ $file: $url — $(head -n 1 "$errors")"
      failures=$((failures + 1))
      continue
    fi
    read -r code redirects effective <<<"$fetched"
    if [[ "$code" != 2?? ]]; then
      echo "✗ $file: $url — HTTP $code"
      failures=$((failures + 1))
      continue
    fi
    # A link can reach raw GitHub through a redirect, as github.com's /raw/ and
    # ?raw=true links do, so where it lands is held to the same rules.
    if [ "$redirects" -gt 0 ]; then
      reason=$(refusal "$effective")
      if [ -n "$reason" ]; then
        echo "✗ $file: $url — redirects to $effective, which fails: $reason"
        failures=$((failures + 1))
        continue
      fi
    fi
    echo "✓ $file: $url"
  done <<<"$urls"
done

if [ "$failures" -ne 0 ]; then
  echo "$failures sample check(s) failed" >&2
  exit 1
fi
