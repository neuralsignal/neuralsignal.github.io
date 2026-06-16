#!/usr/bin/env bash
#
# Run the site locally.
#
#   ./serve.sh            # build + serve with live reload at http://127.0.0.1:4000
#   ./serve.sh build      # one-off build into _site/ (no server)
#
# Requires rbenv (Ruby 3.3.x) + bundler. First run will install gems.

set -euo pipefail

cd "$(dirname "$0")"

# Activate rbenv if available so we use the project's Ruby, not system Ruby 2.6.
if command -v rbenv >/dev/null 2>&1; then
  eval "$(rbenv init - bash)"
fi

# Install dependencies if they're missing.
if ! bundle check >/dev/null 2>&1; then
  echo "Installing gems..."
  bundle install
fi

case "${1:-serve}" in
  build)
    echo "Building site into _site/ ..."
    bundle exec jekyll build
    ;;
  serve)
    echo "Serving at http://127.0.0.1:4000 (Ctrl-C to stop)"
    bundle exec jekyll serve --livereload
    ;;
  *)
    echo "Usage: ./serve.sh [serve|build]" >&2
    exit 1
    ;;
esac
