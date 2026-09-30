# Zero's World

Zero's personal archive of mathematics, medicine, history, art, and games.

Migrated from https://sites.google.com/view/zerofpa/home. All 66 publicly linked pages are included, with their original writing, artwork, typography, and hierarchy. The black sidebar has expandable categories. The home page retains the Gengar background. Search covers page titles and writing. Blank original pages remain blank.

## Publish

In this repository's **Settings → Pages**, choose **Deploy from a branch**, then **main**, **/docs**, and **Save**. Wait for the archive workflow to finish first so the artwork is present. GitHub will show the live address on that settings page.

## Editing with an AI assistant

- `site/content/` contains the writing and layout for each page as HTML, arranged in the original category folders.
- `site/pages.json` controls titles, order, and nested navigation. A page's parent is its enclosing slug path.
- `site/shared/archive.css` controls the sidebar, black theme, mobile menu, and search.
- `site/shared/archive.js` controls expansion, search, and the mobile menu.
- `site/themes/` preserves the original Google Sites page styling.
- `docs/assets/` stores original images and the captured layout stylesheet locally after the first workflow run. These are real repository files, not image hotlinks.

Ask the assistant to edit the relevant source and run `python3 scripts/build.py`. The archive workflow rebuilds `docs/` after source changes. The public site contains no upload timestamps and no Google Sites editor, tracking scripts, or cookies banner.

## Local preview

Run `python3 scripts/import_assets.py` once to download the original public artwork, then `python3 scripts/build.py`, `python3 scripts/validate.py`, and `python3 -m http.server --directory docs 8000`.

The original repository contents remain recoverable in Git history. Google Sites has not been deleted or modified. Only published pages were migrated; unpublished drafts and restricted files cannot be discovered from the public website. The site's displayed author is **Zero**; the GitHub account username is unchanged.
