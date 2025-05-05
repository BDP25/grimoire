#!/usr/bin/env bash
set -e

REPOSITORIES=(
  "https://github.com/JohnTrunix/swisstination"
)

mkdir -p test_projects

for REPO in "${REPOSITORIES[@]}"; do
  DIR="test_projects/$(basename "$REPO" .git)"

  if [ -d "$DIR/.git" ]; then
    echo "Updating existing repo: $DIR"
    git -C "$DIR" pull origin main
  else
    echo "Cloning new repo: $REPO"
    git clone "$REPO" --branch main "$DIR"
  fi
done
