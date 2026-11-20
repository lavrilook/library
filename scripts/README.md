# LAVRI Cut guides

The site remains static HTML. The Codex guide is generated with:

```sh
python scripts/build_lavri_cut.py
```

Python and `beautifulsoup4` are required only for editing/building, not for visitors.

- `guides/lavri-cut/index.html`: canonical Claude guide and shared work methodology. Keep its existing installation instructions, images and fragment URLs.
- `assets/lavri-cut/faq.json`: common FAQ source; the build refreshes both guides.
- `assets/lavri-cut/codex-install.txt`: complete Codex installation request.
- `scripts/build_lavri_cut.py`: Codex installation sections, platform differences and derivation of common methodology from the Claude guide.
- `guides/lavri-cut-update/index.html`: one canonical update guide for both platforms. Its copyable request matches `assets/lavri-cut/update.txt`; keep these two in sync when editing.
- `assets/lavri-cut/guide.css` and `guide.js`: shared appearance, fragment navigation and copying.

Preserve `/library/` when checking relative URLs. Never add customer archives or numbers, credentials, or internal package notes to these public sources. Product package changes must be validated separately from website changes. The original Claude guide has no PDF download, so these additions do not invent a second PDF source.
