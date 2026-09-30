# Zero's archive

Preserve the original writing unless Zero explicitly asks to edit it. Keep the black theme, Gengar home cover, and nested left sidebar. Do not add dates, upload timestamps, marketing sections, or placeholder writing. Empty imported pages are intentional.

Edit `site/content/` and the shared source, then run `python3 scripts/build.py`. All pages must remain in `site/pages.json`; its order and slug hierarchy define the sidebar. Validate with `python3 scripts/validate.py` when local assets are available. Assets belong in `docs/assets/`. Do not replace artwork with generated imagery. The public hosting source is `main` `/docs`.
