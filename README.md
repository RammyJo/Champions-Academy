# Champions Academy

Source and generated pages for the Champions Academy school website.

**Live site:** https://champions-bte.pages.dev/

## Build and preview

Requires Python 3. No packages or frontend build tools are needed.

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8765/.

## Project structure

- `build.py`: HTML templates, routes, redirects and sitemap generation.
- `content.py`: school content, programs, official registration link and image metadata.
- `static/`: styles, navigation/gallery behavior, headers and responsive school images.
- `dist/`: generated website, included for direct deployment.
- `media-library/`: additional Facebook photo candidates and source links; these are not published by the build.
- `HANDOVER.md`: editing and deployment guidance.
- `VERIFICATION.md`: original source audit and recorded verification.

## Current deployment

The existing Cloudflare Pages project is named `champions` and serves https://champions-bte.pages.dev/. It currently uses direct uploads. Creating this repository does not change hosting or automatically connect GitHub deployments.

After building, upload the **contents** of `dist/` (or a ZIP containing those contents at its root) as a production deployment in the existing Pages project. Preserve `_headers` and `_redirects`.

The default canonical origin is `https://champions.edu.ph`. To intentionally change it, build with `SITE_ORIGIN=https://your-domain.example python3 build.py`.

## Latest revisions

The current snapshot includes the simplified homepage, soft dimensional styling, animated navigation and interaction feedback, manual hero gallery, reduced-motion support, and two newer classroom photographs from the official Facebook page. Extra shortlisted media are retained separately.

School branding and photographs remain the property of their respective owners. No open-source license is granted for those assets by this repository.
