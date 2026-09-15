#!/usr/bin/env bash
# Deploy hrapp (and pinned vendor apps) to a site on this bench.
#
# Usage: ./scripts/deploy.sh <site-name> [branch]
#   branch defaults to "main"
#
# Run from the bench root (the directory containing apps/, sites/, Procfile).

set -euo pipefail

SITE="${1:?Usage: deploy.sh <site-name> [branch]}"
BRANCH="${2:-main}"
BENCH_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

cd "$BENCH_ROOT"

echo "==> Backing up ${SITE} (db + files) before deploy"
bench --site "$SITE" backup --with-files

echo "==> Enabling maintenance mode on ${SITE}"
bench --site "$SITE" set-maintenance-mode on
trap 'bench --site "$SITE" set-maintenance-mode off' EXIT

echo "==> Updating apps/hrapp to origin/${BRANCH}"
git -C apps/hrapp fetch origin
git -C apps/hrapp checkout "$BRANCH"
git -C apps/hrapp pull --ff-only origin "$BRANCH"

echo "==> Running migrations and fixture sync for ${SITE}"
bench --site "$SITE" migrate

echo "==> Rebuilding assets"
bench build --app hrapp

echo "==> Restarting processes"
if command -v supervisorctl >/dev/null 2>&1; then
	sudo supervisorctl restart all
else
	echo "supervisorctl not found — restart the bench processes manually (systemctl or bench restart)."
fi

echo "==> Deploy complete. Maintenance mode will now be disabled."
