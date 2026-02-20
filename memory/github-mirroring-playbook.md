# GitHub Mirroring Playbook (ThePipis -> kaimirroring)

Last updated: 2026-02-20

## Objective
Automate repository mirroring from `ThePipis/<repo>` to `kaimirroring/<repo-or-repo-mirror>` with scheduled sync and manual trigger.

## Standard Architecture
- Destination repo lives in `kaimirroring`.
- GitHub Actions workflow in destination repo performs `git clone --mirror` from source and `git push --mirror` to destination.
- Source read token stored as repository secret in destination repo: `SOURCE_REPO_TOKEN`.
- Workflow runs on cron (`*/30 * * * *`) + `workflow_dispatch`.

## Required Tokens
### 1) Destination token (kaimirroring) for setup automation
Fine-grained PAT (resource owner: `kaimirroring`, repo access: All repositories), permissions:
- Metadata: Read-only (required)
- Contents: Read and write
- Workflows: Read and write
- Administration: Read and write
- Actions: Read and write
- Secrets: Read and write (recommended for API secret management)

### 2) Source token (ThePipis) for read access
Fine-grained PAT with access only to source repo(s):
- Metadata: Read-only
- Contents: Read-only

## Workflow File
Path: `.github/workflows/mirror.yml`

```yaml
name: Mirror from ThePipis/OpenClaw

on:
  schedule:
    - cron: '*/30 * * * *'
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: mirror-sync
  cancel-in-progress: true

jobs:
  mirror:
    runs-on: ubuntu-latest
    steps:
      - name: Mirror source -> destination
        env:
          SRC_TOKEN: ${{ secrets.SOURCE_REPO_TOKEN }}
          DEST_REPO: ${{ github.repository }}
        run: |
          set -euo pipefail

          if [ -z "${SRC_TOKEN:-}" ]; then
            echo "ERROR: Missing secret SOURCE_REPO_TOKEN"
            exit 1
          fi

          git clone --mirror "https://x-access-token:${SRC_TOKEN}@github.com/ThePipis/OpenClaw.git" source.git
          cd source.git
          git push --mirror "https://x-access-token:${{ github.token }}@github.com/${DEST_REPO}.git"
```

## Repository Settings Needed
- Settings -> Actions -> General -> Workflow permissions: **Read and write permissions**
- Settings -> Secrets and variables -> Actions -> add secret:
  - Name: `SOURCE_REPO_TOKEN`
  - Value: source read-only token

## Verification Checklist
1. Run workflow manually (`workflow_dispatch`) and confirm HTTP 204 if triggered via API.
2. Confirm run status: `completed` + `success`.
3. Confirm refs mirrored (branches/tags).
4. Confirm scheduled run appears every 30 minutes.

## Known Failure Modes
- `403 Resource not accessible by personal access token` when dispatching workflow:
  - Missing `Actions: Read and write` on destination PAT.
- Cannot push `.github/workflows/*`:
  - Missing `Workflows: Read and write` (or classic PAT without `workflow` scope).
- Source clone 403/404:
  - Source token lacks read permission or collaborator access to source repo.

## Operational Rule
When user asks to mirror a repo from ThePipis to kaimirroring:
1. Ensure destination repo exists.
2. Add/update mirror workflow.
3. Ensure `SOURCE_REPO_TOKEN` secret exists.
4. Trigger initial run.
5. Validate success and share run URL.
