# AGENTS.md

Static redirect service served by GitHub Pages (user site `igugyj.github.io`). Pure Python standard library — no dependencies, no package manager, no Node (despite the `setup-node` step in CI, which is unused; don't add JS tooling).

## Commands

- Generate the site: `py generate.py` (Windows) / `python generate.py` (CI)
- That's the only command. There is no lint, test, typecheck, or format step.

## How it works

- `redirects.json` is the single source of truth: `{ "route": "target-url" }`. Edit it, run the script, done.
- `generate.py` deletes `dist/` entirely, then writes `dist/<route>/index.html` per entry from `template.html` — an interstitial page (`#FFF0F5` background, GIF animation, gradient "art text" of the target) that auto-redirects after 3s.
- `template.html` uses `{{placeholder}}` replacement; `DELAY`, `ASSET_SRC`, and the template path are hardcoded constants at the top of `generate.py` — no config fields anywhere.
- `assets/loading.gif` is copied into every output dir; pages reference it by bare filename so they work at any subpath. It has a white background, so the template relies on `mix-blend-mode: multiply` to blend it into the `#FFF0F5` page — don't remove that or switch to a dark page background without replacing the GIF.
- The "Xiaolai SC" art-text font is loaded at runtime from CDN (`cn-fontsource-xiaolai-sc-regular/font.css` on jsDelivr, linked in `template.html`) — no font file is built or copied. It's an external network dependency of the published pages; the old local `public/font/*.ttf` was removed.
- Route keys have leading/trailing slashes stripped: `"/github"` and `"github"` are equivalent; `"/"` becomes `dist/index.html`.
- Targets are HTML-escaped and JSON-encoded for the JS string, so quotes/`&` in URLs are safe.
- `dist/` is gitignored and rebuilt from scratch every run; never edit or commit it. The working-tree copy may be stale (contains routes no longer in `redirects.json`) — trust the JSON, not `dist/`.
- Only routes listed in `redirects.json` exist; unknown paths get the default GitHub Pages 404 (no custom `404.html`).

## Deploy

- Push to `main` (or manual `workflow_dispatch`) runs `.github/workflows/deploy.yml`: `python generate.py`, then publishes `./dist` to the `gh-pages` branch via `peaceiris/actions-gh-pages` with `force_orphan: true`.
- **Every push to `main` is a live production deploy.** `gh-pages` is generated output — never commit to it manually.

## Repo notes

- `architecture/` holds design diagrams and visual-check artifacts; not part of the build. Marked `linguist-vendored` in `.gitattributes`.
- Commit style: conventional prefixes (`chore:`, `docs:`, `refactor:`) for housekeeping; plain messages like "Update redirects.json" for config edits.
