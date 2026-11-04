# Studio Sleepy Giraffe

This repository houses the code and tools for my personal website. Having gone through many variations and much history I finally decided to start over fresh, primarily for security/privacy reasons. After years of hosting on my own RPi I've also shifted paradigm to hosting on CloudFlare pages instead to avoid having my personal website dependant on my ever changing home network. 

## Building the site

Published posts live in `content/posts/YYYY-MM-DD/`, with `post.md`, `info.json`,
and optional `cover.jpg` and supplemental files listed in the metadata. Other
folders in `content/posts/` are not included in the published post list.

From the repository root:

```sh
python3 -m venv venv
venv/bin/python -m pip install -r requirements
venv/bin/python src/freeze.py
```

The freezer reads this repository's content and writes the static site to `dist/`.
Paths are resolved relative to the source files, so it can also be invoked from
another working directory. Review and commit the generated `dist/` changes to
publish them through the deployment pipeline below.

## Deployment

The site now targets **Cloudflare Workers Static Assets**, using Wrangler to
publish the checked-in `dist/` directory. No Worker script or Python runtime is
needed on Cloudflare. Generating `dist/` is still a separate, local Frozen-Flask
step; commit the updated output when publishing content.

### Local preview and validation

Use Node.js 22 or newer (the Cloudflare build version is set in `.node-version`).
From the repository root:

```sh
npm ci
npm run dev
```

Open the local URL printed by Wrangler. To validate the deployment configuration
without publishing:

```sh
npm run check:deploy
```

Wrangler serves `/` from `dist/index.html`. HTML URLs such as
`/post/2025-07-27.html` redirect to their extensionless equivalent and serve the
same file, as with Cloudflare Pages. Missing paths return 404 rather than the
homepage. Images, fonts, and downloadable files are uploaded from `dist/` too.

### Automatic deployments with Cloudflare Workers Builds

Connect `Narcolapser/ssgwebsite` through the Cloudflare dashboard's
**Workers & Pages** Git repository integration, creating a Worker with these
settings:

| Setting | Value |
| --- | --- |
| Worker name | `ssgwebsite` (must match `wrangler.jsonc`) |
| Production branch | `master` |
| Root directory | Repository root |
| Build command | `npm ci && npm run check:deploy` |
| Deploy command | `npm run deploy` |
| Preview command, if branch previews are enabled | `npx wrangler preview` |

Cloudflare provides deployment authentication through Workers Builds. Pushes to
`master` publish the committed `dist/`; branch previews do not promote to
production. No Flask build command or sibling blog checkout is required.

For migration from the existing Pages project, first verify the new Worker on
its `workers.dev` URL. Then move the site's custom domain from Pages to the
Worker under **Settings > Domains & Routes**, and disable the old Pages automatic
deployments. Creating the Worker does not automatically migrate the Pages domain.

### Manual deployment

```sh
npx wrangler login
npm run deploy
```

For a separate CI system, supply `CLOUDFLARE_ACCOUNT_ID` and
`CLOUDFLARE_API_TOKEN` (with Workers Scripts edit permission for the target account)
as CI secrets instead of interactive login, then run `npm ci` and `npm run deploy`.

See the [Workers Static Assets guide](https://developers.cloudflare.com/workers/static-assets/get-started/)
and [Workers Builds settings](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/).
