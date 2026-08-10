# jobsearch.engine() — a job search, engineered

A data & AI platform leader's job search, run like a data platform and documented in the open.
Live site sources roles programmatically, scores each for fit, tracks everything, and mines the
professional network for warm intros — with a **Public / Private toggle** so nothing sensitive
ships to the public build.

**Live site:** _add your CloudFront/custom-domain URL here_

## What's inside
- `index.html` — the entire site (self-contained: inline CSS/JS, no build step). Each section
  flips to reveal the code behind it. A live toggle switches between:
  - **Private** — real companies, compensation, and contacts.
  - **Public** — companies collapsed to industry, compensation hidden, contacts anonymized.
- `src/` — the (illustrative) engine the site is about:
  - `pipeline.py` — source → score → track → act.
  - `score.py` — transparent, rules-based fit scoring (no black box).
  - `search.py` — multi-angle sourcing + de-dupe + ranking.
  - `networking.py` — connections × live openings → ranked warm paths.
  - `positioning.py` — the résumé repositioning logic behind section 05.
- `data/applications.sample.json` — a genericized sample of the tracker data.
- `build_public.py` — emits `public/index.html`, a deploy-safe copy with real
  company names and salaries **stripped from the source**. It fails loudly if any
  confidential token survives, so a bad build can't be published.
- `deploy/` — AWS hosting (S3 + CloudFront) via CloudFormation and a one-command deploy script.

## Run locally
Just open `index.html` in a browser. There is no build step.

## Deploy to AWS (S3 + CloudFront)
Static site, hosted privately in S3 and served over HTTPS by CloudFront.

**1. One-time infrastructure (CloudFormation):**
```bash
aws cloudformation deploy \
  --template-file deploy/cloudformation.yaml \
  --stack-name jobsearch-engine \
  --parameter-overrides BucketName=YOUR-UNIQUE-BUCKET-NAME \
  --capabilities CAPABILITY_NAMED_IAM
```
This creates a private S3 bucket, a CloudFront distribution (Origin Access Control, HTTPS,
default root `index.html`), and prints the distribution domain in the stack outputs.

**2. Publish content (repeat on every update):**
```bash
./deploy/deploy.sh YOUR-UNIQUE-BUCKET-NAME YOUR-CLOUDFRONT-DISTRIBUTION-ID
```
This runs `build_public.py`, then syncs **only** the anonymized `public/` build to S3 and
invalidates the CloudFront cache. The full-detail `index.html` is never uploaded.

> Custom domain: add an ACM cert (us-east-1) + a Route 53 alias record to the distribution.

## Privacy
Two layers protect confidential data:
1. **At render time** — in public mode the site shows industry labels + a "confidential" marker
   instead of company names and salaries.
2. **At build time** — `build_public.py` strips those values out of the deployed file's *source*,
   so even "view source" on the live site reveals nothing. This is the copy that gets published.

The networking section shows only **aggregate counts** (totals, seniority mix, industry spread) —
individual names and employers are never emitted to the page. The full ranked contact lists live
in separate `*.private.html` files that are git-ignored and never deployed.

## License
MIT — see [LICENSE](LICENSE).
