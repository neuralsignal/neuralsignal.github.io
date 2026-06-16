# neuralsignal.github.io

Personal site of Matthias Christenson. A small, static, multi-page
[Jekyll](https://jekyllrb.com/) site (originally based on the
[al-folio](https://github.com/alshedivat/al-folio) theme, since trimmed down).

## Run locally

```bash
./serve.sh          # build + serve with live reload at http://127.0.0.1:4000
./serve.sh build    # one-off build into _site/
```

The script handles `rbenv` + `bundler` and installs gems on first run.

## Structure

- `_pages/` — about, projects, resume (the top-level pages)
- `_projects/` — one markdown file per project (collection, served at `/projects/<name>/`)
- `_posts/` — blog posts (served at `/blog/<year>/<title>/`)
- `_bibliography/papers.bib` — publications; "Selected Works" on the resume pulls entries with `selected={true}`
- `_data/cv.yml` — resume content
- `_sass/` — styles (`_base.scss` holds the shared primitives)
- `_layouts/`, `_includes/` — templates

## Add a blog post

Create `_posts/YYYY-MM-DD-some-title.md`. It appears on `/blog/` automatically
(newest first). Only `title` and `date` are required — `layout: post` is applied
automatically via `_config.yml`:

```markdown
---
title: My post title
date: 2026-06-16
description: One-line summary shown in the blog list (optional).
tags: optional space-separated tags
---

Write your post here in Markdown.
```

## Deploy

Pushes to the default branch deploy to GitHub Pages via GitHub Actions.

## License

Theme is MIT-licensed ([al-folio](https://github.com/alshedivat/al-folio/blob/master/LICENSE)). Site content © Matthias Christenson.
