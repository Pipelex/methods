#!/usr/bin/env bash
# Validate every package's address at a release tag on the hosted API.
#
#   check-addresses.sh vX.Y.Z
#
# Run from any checkout of the repository. It fetches the tags, lists the
# packages the tag itself carries — so a package added on `dev` after the cut
# is not asked for — and for each METHODS.toml reads the manifest's `address`
# and `name`, which are the package's identity, then asks POST /v1/validate to
# fetch <address>/<name>@vX.Y.Z and validate it. No call spends inference.
# Prints one line per package and exits non-zero when any address is not both
# valid and runnable, or when the API answers without a verdict.
#
# Needs git, curl, jq and PIPELEX_API_KEY; PIPELEX_BASE_URL overrides the API host.

set -euo pipefail

TAG="${1:-}"
if [[ ! "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "usage: $0 vX.Y.Z" >&2
  exit 2
fi
if [ -z "${PIPELEX_API_KEY:-}" ]; then
  echo "PIPELEX_API_KEY is not set: the check validates on the hosted API, so it needs a key (create one at https://app.pipelex.com)" >&2
  exit 2
fi
for tool in git curl jq; do
  command -v "$tool" >/dev/null || { echo "$tool is required" >&2; exit 2; }
done

BASE_URL="${PIPELEX_BASE_URL:-https://api.pipelex.com}"
failures=0

# The first `<key> = "…"` (or '…') line of a manifest, or nothing. It must not
# fail when the key is absent: `name` is optional in the MTHDS schema, and a
# package without one is exactly what this check has to report.
field() {
  printf '%s\n' "$2" | sed -nE "/^$1 = /{s/^$1 = [\"']([^\"']*)[\"'].*/\1/p;q;}"
}

git fetch --quiet --tags origin
if ! git rev-parse -q --verify "refs/tags/$TAG" >/dev/null; then
  echo "$TAG is not a tag on origin yet: the release workflow has not tagged it" >&2
  exit 1
fi

manifests=$(git ls-tree -r --name-only "$TAG" -- methods/ | grep '/METHODS\.toml$')
for manifest in $manifests; do
  text=$(git show "$TAG:$manifest")
  name=$(field name "$text")
  address=$(field address "$text")
  if [ -z "$name" ] || [ -z "$address" ]; then
    echo "✗ $manifest — declares no name or no address, so no address reaches the package"
    failures=$((failures + 1))
    continue
  fi
  method_ref="$address/$name@$TAG"
  body=$(jq -n --arg ref "$method_ref" '{method_ref: $ref}')
  response=$(curl -sS -X POST "$BASE_URL/v1/validate" \
    -H "Authorization: Bearer $PIPELEX_API_KEY" \
    -H 'Content-Type: application/json' \
    -w '\n%{http_code}' \
    -d "$body") || { echo "✗ $method_ref — the API could not be reached"; failures=$((failures + 1)); continue; }
  status=$(printf '%s' "$response" | tail -n 1)
  verdict=$(printf '%s' "$response" | sed '$d')
  if [ "$status" != "200" ]; then
    detail=$(printf '%s' "$verdict" | jq -r '.detail // .title // empty' 2>/dev/null || true)
    echo "✗ $method_ref — HTTP $status: ${detail:-$(printf '%s' "$verdict" | head -c 300)}"
    failures=$((failures + 1))
    continue
  fi
  valid=$(printf '%s' "$verdict" | jq -r '.is_valid' 2>/dev/null || true)
  runnable=$(printf '%s' "$verdict" | jq -r '.is_runnable' 2>/dev/null || true)
  if [ "$valid" = "true" ] && [ "$runnable" = "true" ]; then
    echo "✓ $method_ref"
  else
    message=$(printf '%s' "$verdict" | jq -r '.message // "no message"' 2>/dev/null || echo "an answer that is not JSON")
    echo "✗ $method_ref — is_valid ${valid:-?}, is_runnable ${runnable:-?}: $message"
    failures=$((failures + 1))
  fi
done

if [ "$failures" -ne 0 ]; then
  echo "$failures address(es) at $TAG failed validation" >&2
  exit 1
fi
