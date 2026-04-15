# econhangyu.com — Personal Academic Website

Personal website of **Hang Yu**, Assistant Professor of Economics at the National School of Development, Peking University. Development economist; field experiments in Sub-Saharan Africa.

Public URL (once DNS is migrated): `https://econhangyu.com`
Build URL (GitHub Pages default): `https://econhangyu.github.io`
GitHub repo: `https://github.com/econhangyu/econhangyu.github.io`

This README documents the key decisions, architecture, and maintenance workflow for this site. **Read this file first** if you are the author returning after a break, or an AI assistant picking up the project mid-stream.

---

## Current status (as of 2026-04-15)

**Phase: Skeleton deployed, architecture approved, content migration not yet started.**

- [x] AcademicPages template cloned into `website/` and stripped of upstream git history
- [x] Fresh local git repo initialized on `main` branch
- [x] `.git/` marked `com.dropbox.ignored` to prevent Dropbox/Git conflicts
- [x] Pre-existing files (`logo/`, `website.docx`) preserved and gitignored
- [x] Initial commit made and pushed to `github.com/econhangyu/econhangyu.github.io`
- [x] GitHub Pages enabled; placeholder template is live
- [x] Peer-site research complete (20 mid-career dev economists surveyed)
- [x] Design principles confirmed with author
- [x] Site architecture approved
- [ ] `_config.yml` customized (site name, bio, nav, socials)
- [ ] Unused collections removed (`_talks/`, `_posts/`, `_drafts/`, default `_portfolio/`)
- [ ] Nav restructured to 5 items (Home / Research ▾ / Teaching / Gallery / CV)
- [ ] Research sub-pages created (Publications / Working Papers / Works in Progress)
- [ ] Custom Publications layout with `<details>`-based expand mechanism
- [ ] Gallery page with lightbox and country-year grouping
- [ ] Custom domain `econhangyu.com` wired to GitHub Pages (DNS flip from Google Sites)
- [ ] Real content migrated from [old Google Site](https://www.econhangyu.com)
- [ ] Old Google Site kept alive as dormant backup after migration

---

## Key decisions

### Platform
**AcademicPages** (a Jekyll theme), hosted on **GitHub Pages**, deployed to the custom domain `econhangyu.com`. Chosen over alternatives (al-folio, Quarto, Squarespace, WordPress, Google Sites) after surveying 20 peer sites of mid-career development economists. Rationale:

- Matches the dominant pattern among economists (Dean Yang, Jonathan Weigel, and many others use AcademicPages or similar Jekyll themes).
- Simpler under the hood than al-folio; easier for a Git beginner to maintain.
- BibTeX-style publication management via Markdown files, with per-paper category fields — handles the English/Chinese/edited-volume split cleanly.
- Free, version-controlled, and platform-independent (no vendor lock-in).

### Design principles (approved 2026-04-15)

The author explicitly stated these principles — **respect them when adding new features or proposing changes:**

1. **No thematic grouping of papers.** Author feels the paper count doesn't justify themes. Use plain reverse-chronological order within each sub-page.
2. **Traditional multi-sub-page structure.** Research has sub-pages, not a single long scroll.
3. **Clean, minimalist paper listing** with optional per-paper expand to reveal a fieldwork photo, key chart, or longer description. Entries with no expandable content should not show an expand control at all.
4. **Real gallery design** — the fieldwork gallery is the one place where design effort is warranted. It is the site's distinctive asset; no peer site surveyed has a comparable gallery.
5. **Everything else: traditional, restrained.** Follow Dean Yang and James Allen IV's lead. Author's exact words: *"making it fancy only serves to shame myself."* No hero videos, animations, accent colors beyond default link blue, custom fonts, or visual flourishes.

### Architecture

**Top-level navigation (5 items):**

```
Home  |  Research ▾  |  Teaching  |  Gallery  |  CV
```

- **Home**: headshot + short bio (2–3 sentences) + "Recent" news list (5–7 bullets) + contact links row (Scholar, Email, CV, Bluesky, GitHub).
- **Research**: parent page with a short agenda description (3–4 sentences) and links down to three sub-pages.
  - **Publications**: peer-reviewed journal articles (English + Chinese) + edited volumes, reverse chronological.
  - **Working Papers**: WP with PDFs, R&R status, trial registry links, reverse chronological.
  - **Works in Progress**: titles + coauthors + status, sometimes no PDF.
- **Teaching**: plain list grouped by level (Undergraduate / Doctoral / MPA), each entry as "Course Name — years taught." No syllabi on the public site.
- **Gallery**: fieldwork photos, grouped by country-year (Mozambique 2017–2019 / Ethiopia 2023 / Mozambique 2023), responsive grid with click-to-lightbox and full captions.
- **CV**: direct link to PDF in `files/cv.pdf`. No intermediate page.

**Explicitly removed from default AcademicPages template**: Talks, Portfolio, Blog/Posts, and the default About-page hero layout.

### Publication entry format (the expand mechanism)

Each paper lives as a Markdown file in `_publications/`, with frontmatter:

```yaml
---
title: "..."
authors: "..."
venue: "..."            # e.g., "Journal of Development Economics, 161: 103035"
year: 2023
category: published     # published | chinese | edited | working | wip
pdf: /files/publications/xxx.pdf
replication: https://...
media: https://...      # VoxDev link, etc.
image: /images/papers/xxx.jpg    # optional: fieldwork photo or chart
description: |          # optional: 2–4 sentence abstract
  ...
---
```

The custom Publications layout iterates these files and wraps each in a native HTML `<details>` element. Papers without `image:` or `description:` render without an expand control — the design scales naturally from minimal to enriched entries.

**Why `<details>` over JavaScript**: built into HTML, no framework, accessible, works offline, no dependencies. Custom CSS hides the default browser triangle and adds a subtle "▸ more" / "▾ less" indicator.

### Gallery format

- Jekyll collection `_gallery/` with one Markdown file per country-year section.
- Each section loops over images in `images/gallery/<section-name>/` and renders a responsive CSS grid (3 / 2 / 1 columns on desktop / tablet / mobile).
- Lightbox: single small JS library (GLightbox or similar, ~10 KB). This is the **only** JS dependency added beyond AcademicPages defaults.
- Image pipeline: originals stored in `images/gallery/originals/` (gitignored), optimized derivatives stored at `images/gallery/<section>/` (committed). Thumbnails ~600px wide, full-size ~1600px wide, WebP with JPEG fallback.

---

## Directory structure

```
website/                              ← this folder, Git repo root
├── .git/                              Git database (Dropbox-ignored)
├── .gitignore                         Ignores _site/, logo/, website.docx, etc.
├── README.md                          ← YOU ARE HERE
├── _config.yml                        Site-wide config (name, bio, nav, socials)
├── _data/                             Navigation menu, author info, UI strings
│   ├── navigation.yml
│   └── authors.yml
├── _pages/                            Top-level pages
│   ├── about.md                       Homepage
│   ├── research.md                    Research landing page
│   ├── publications.html              Custom layout listing _publications/
│   ├── working-papers.html            Custom layout listing working papers
│   ├── works-in-progress.html         Custom layout listing WIP
│   ├── teaching.md                    Teaching list
│   └── gallery.html                   Gallery with lightbox
├── _publications/                     One .md per paper
├── _gallery/                          One .md per country-year section
├── _includes/                         Theme partials (nav, footer, head)
├── _layouts/                          Theme page skeletons
├── _sass/                             Theme stylesheets (SCSS)
├── assets/                            Compiled CSS/JS
├── files/                             Public-facing PDFs (CV, papers)
│   ├── cv.pdf
│   ├── publications/*.pdf
│   └── working-papers/*.pdf
├── images/                            Public-facing images
│   ├── headshot.jpg
│   ├── papers/                        Per-paper images for expand view
│   └── gallery/                       Fieldwork photos
│       ├── originals/                 Unoptimized masters (gitignored)
│       ├── mozambique-2017-2019/
│       ├── ethiopia-2023/
│       └── mozambique-2023/
├── logo/                              Pre-existing, gitignored, not published
└── website.docx                       Pre-existing, gitignored, not published
```

**Removed from the cloned template** (explicitly, because they're not used):
- `_posts/`, `_drafts/`, `_talks/` collections
- `talkmap.py`, `talkmap.ipynb`, `talkmap_out.ipynb`, `talkmap/`
- `markdown_generator/` (the BibTeX-to-Markdown script — we're writing Markdown files by hand)
- `.devcontainer/`, `Dockerfile`, `docker-compose.yaml` (we don't need containerized dev)

---

## Dropbox + Git coexistence

**This repo lives inside a Dropbox folder** at `/Users/hangyu/Library/CloudStorage/Dropbox/_professional documents/website/`. This is deliberate — the author keeps all working materials in Dropbox and wants this project proximate to sibling folders (`CVs/`, `papers/`, etc.).

To prevent Dropbox from corrupting the Git database, the `.git/` directory has the macOS extended attribute `com.dropbox.ignored = 1` set. This tells Dropbox to skip it entirely. Set once, persists across machines, set via:

```bash
xattr -w com.dropbox.ignored 1 ".git"
```

**If you ever re-clone this repo** (e.g., on a new machine, or after deleting and re-downloading from GitHub), you must **re-run that `xattr` command** on the fresh `.git/` folder. Otherwise Dropbox will start syncing Git internals, which can cause subtle corruption across machines. The same applies to any new nested Git repo you might create inside `website/`.

Verify the flag is in place with:
```bash
xattr -l .git
# should show: com.dropbox.ignored: 1
```

Content files in the repo (`_publications/*.md`, `images/*`, etc.) **are** synced by Dropbox, which gives you a free backup. Git manages version history via GitHub.

---

## Relationship to sibling folders

The repo is **self-contained** — everything published on the site must live inside `website/`. But the sibling folders (`CVs/`, `papers/`, `statements/`, `photos/`, etc.) serve as **source-of-truth working materials**. The flow is:

| Source of truth (sibling folder) | What flows into the repo | Destination inside `website/` |
|---|---|---|
| `CVs/CV_eng 202604.docx` | Exported PDF | `files/cv.pdf` |
| `papers/1-publications/*.pdf` | Individual PDFs | `files/publications/*.pdf` |
| `papers/2-working papers/*.pdf` | Current WP versions | `files/working-papers/*.pdf` |
| `photos/headshot/` | Cropped + resized headshot | `images/headshot.jpg` |
| `photos/` (fieldwork photos) | Optimized derivatives | `images/gallery/<section>/*.webp` |

**Do not symlink across this boundary** — GitHub Pages builds on GitHub's servers where sibling folders don't exist. Duplication is the correct answer. It also enforces a clean "private working / public published" distinction.

When updating a file: edit the source, export/optimize if needed, copy into `website/`, commit, push.

---

## Maintenance workflow

The author uses **GitHub Desktop** (not command-line Git). All routine updates should go through this visual workflow.

### Routine content update (new PDF, fixed typo, new publication entry)

1. Edit or add the relevant file in the `website/` folder using any editor (VS Code, plain text editor, even Finder for drag-and-drop of PDFs and images).
2. Open GitHub Desktop. It shows the changed files in the left panel.
3. Type a one-line commit summary at the bottom-left (e.g., `Add 2026 working paper PDF` or `Fix typo in bio`).
4. Click **Commit to main**.
5. Click **Push origin** at the top.
6. Wait 1–3 minutes. GitHub Actions rebuilds the site; the new version is live.

Verify build success in the repo's **Actions** tab on GitHub.com. A green check = live; red X = build failure (click in to see the error).

### Adding a new publication

1. Create a new Markdown file in `_publications/` named like `2026-paper-short-title.md`.
2. Copy frontmatter from an existing file in the same category; fill in title, authors, venue, year, pdf, category.
3. Drop the PDF into `files/publications/`.
4. Optional: drop an image into `images/papers/`, add `image:` and `description:` frontmatter fields. This triggers the expand control.
5. Commit and push as above.

### Adding a new gallery section

1. Create a subfolder in `images/gallery/originals/` with the new country-year name; drop in the full-resolution photos.
2. Run the image optimization command (documented in `scripts/optimize-gallery.sh` once created) to produce the web-ready versions in `images/gallery/<section>/`.
3. Create a new Markdown file in `_gallery/` with the section title and caption metadata.
4. Commit and push.

### Design/layout change

Design changes affect many visitors at once, so use a branch to preview before merging:

1. In GitHub Desktop: **Branch → New Branch**, name it something like `design-tweak-accent-color`.
2. Make the edits on that branch, commit, push.
3. On GitHub.com, open a Pull Request from the branch to `main`.
4. GitHub Pages builds a preview (check the Actions tab).
5. Once satisfied, merge the PR; site goes live.

For content edits, the branch workflow is overkill — commit straight to `main`.

### Emergency rollback

Git preserves full history. If a bad change breaks the site:

1. On GitHub.com, find the most recent working commit in the repo's commit list.
2. Copy its hash.
3. In GitHub Desktop: **History → right-click the bad commit → Revert this commit**.
4. Push. The site rebuilds to the previous state within minutes.

---

## For future Claude agents picking this up

**First steps before making any changes:**

1. Read this README completely — it contains the design principles the author explicitly approved. Do not deviate from them without asking.
2. Check `git log --oneline` to see the most recent commits and understand what phase the project is in.
3. Check the [Current status](#current-status-as-of-2026-04-15) checklist above to see what has and has not been done. Update it after your session.
4. Look at [old Google Site](https://www.econhangyu.com) for the source content that will eventually be migrated. It is built on Google Sites and JavaScript-rendered, so WebFetch will capture homepages but not subpages well — ask the author to paste subpage content if needed.
5. The author's GitHub username is `econhangyu`. The repo must be named exactly `econhangyu.github.io` for GitHub Pages user-site routing to work.

**Important caveats:**

- The author is a **Git beginner** (per their `~/.claude/CLAUDE.md`) but a **Stata expert and Python beginner**. Explain Git concepts when they come up; do not assume familiarity.
- The author's time is scarce — **do not rebuild from scratch or introduce abstractions beyond what the task requires**. Respect the existing decisions and work incrementally.
- Do not modify files in sibling folders (`../CVs/`, `../papers/`, etc.) without explicit permission. Those are the author's private working materials.
- Do not fill in real publication, teaching, or gallery content until the design skeleton is complete and the author has reviewed it. The author explicitly asked to review the design *before* content migration.
- The author maintains memory at `/Users/hangyu/.claude/projects/.../memory/`. Check there for ongoing context.

**Where to start new work**: look at the first unchecked item in the [Current status](#current-status-as-of-2026-04-15) checklist. That is the active front.

---

## Useful references

- [Peer sites surveyed](https://github.com/econhangyu/econhangyu.github.io/issues) — not yet documented; see conversation history. Key comparables: Dean Yang, James Allen IV, Jonathan Weigel, Gautam Rao, Namrata Kala, Stefano Caria.
- AcademicPages upstream: https://github.com/academicpages/academicpages.github.io
- Jekyll docs: https://jekyllrb.com/docs/
- GitHub Pages docs: https://docs.github.com/en/pages

---

*Last updated: 2026-04-15. Update the status checklist and the "as of" date whenever the project state changes meaningfully.*
