# Rider Counsel Journal

This repository builds the Rider Counsel Journal static blog. The build uses Python 3 and its standard library.

## Cloudflare Pages

Connect the GitHub repository in Cloudflare Pages. Use the following settings.

| Setting | Value |
| --- | --- |
| Production branch | `main` |
| Framework | None |
| Root directory | Repository root |
| Build command | `python3 build_blog.py` |
| Output directory | `dist` |

Pages supplies the project address through `CF_PAGES_URL`. The build uses the stable project hostname for canonical links, article metadata, the sitemap and robots.txt. After a custom domain is serving the site over HTTPS, set `SITE_ORIGIN` to its full HTTPS origin and redeploy.

## Local preview

Run `python3 build_blog.py`, then `python3 -m http.server 8000 --directory dist`. Open `http://localhost:8000/`. A local build uses localhost in its search metadata. To build for a different host outside Cloudflare, supply its verified public origin in `SITE_ORIGIN`.

The build verifies local links, article anchors, structured-data URLs, canonical URLs and sitemap coverage. It generates a top-level 404.html for missing routes. Ads are inactive in this edition.
