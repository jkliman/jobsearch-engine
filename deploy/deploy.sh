#!/usr/bin/env bash
# Usage: ./deploy/deploy.sh <bucket-name> <cloudfront-distribution-id>
#
# Publishes the ANONYMIZED build only. build_public.py strips real company
# names and salary figures out of the page source, so nothing confidential is
# ever uploaded — not even in "view source". Your local index.html keeps the
# full Public/Private toggle for private use and is never deployed.
set -euo pipefail
BUCKET="${1:?bucket name required}"
DIST="${2:?cloudfront distribution id required}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Building anonymized public copy ..."
python3 "$ROOT/build_public.py"   # writes $ROOT/public/index.html (fails if any confidential token survives)

echo "Syncing anonymized site to s3://$BUCKET ..."
aws s3 sync "$ROOT/public" "s3://$BUCKET" --delete

echo "Invalidating CloudFront cache ..."
aws cloudfront create-invalidation --distribution-id "$DIST" --paths "/*" >/dev/null
echo "Done. Live in ~1-2 min."
