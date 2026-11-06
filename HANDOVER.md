# Champions Academy website

The site is a dependency-free static build. Python renders standalone pages with native HTML navigation and a small enhancement script. The school’s existing Google Form handles the registration workflow.

## Run locally

From this directory, run:

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8765/. The local Python server serves pages and assets. Cloudflare Pages interprets the generated `_redirects` and `_headers` files.

## Routes

| Route | Purpose |
| --- | --- |
| `/` | School introduction, programs, formation, school life and admissions |
| `/about/` | Philosophy and institutional overview |
| `/history/` | The school’s origins and milestones |
| `/values/` | Official vision and mission and the two published values lists |
| `/faculty/` | Faculty overview and directory for approved profiles |
| `/program/` | Academic overview and program comparison |
| `/preschool/` | Nursery, Kindergarten and entry guidance |
| `/grade-school/` | Grades 1–6 |
| `/junior-high-school/` | Grades 7–10 |
| `/admissions/` | Four-step admissions journey |
| `/requirements/` | Published document checklist and conditional guidance |
| `/pre-register/` | Handoff to the existing Google Form |
| `/school-life/` | Campus and activity photos |
| `/news/` | Current updates and clearly dated archive links |
| `/contact/` | Office hours, phone numbers, email directory and directions |
| `/privacy/` | Public-site and registration privacy information for families |
| `/summer-class/` | Contact Admissions for current availability |
| Three original dated blog URLs | Short archive summaries |

The build emits permanent redirects for the previous Grade School URL, the Blog index, the Home alias and the unavailable nursery preview article. See `REDIRECTS` in `build.py`. Preserve these when migrating.

## Optional future Git integration

The live project currently uses direct upload; see README.md for its current deployment process. The following instructions describe creating a separate Git-integrated project, not changing the existing project.

1. Create a school-owned GitHub repository. Add the source from this folder. Remove the Sites-specific `.openai` directory for a Cloudflare-only repository.
2. In Cloudflare Workers & Pages, create a Pages project and import the repository. Choose the school’s production branch, the repository root, and no framework preset.
3. Set the build command to `python3 build.py` and output directory to `dist`. If the selected build image lacks Python, commit a freshly generated `dist` directory and use `exit 0` as the build command.
4. The default metadata origin is `https://champions.edu.ph`. Set `SITE_ORIGIN` to the agreed canonical origin when deploying under a different production hostname. Test the Pages preview before connecting any school domain.
5. Verify the enrollment link, response settings, image permissions, privacy notice, redirects, and access to the prior site backup before DNS cutover. Keep a rollback path to the previous deployment. Coordinate any legacy WordPress archive or redirect plan with the school's hosting administrator.

See [Cloudflare Pages static HTML deployment](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) and [Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/).

If the school keeps WordPress, migrate the approved copy and optimized images into clean page and post templates on a remediated or fresh installation. Preserve the route map, Google Form handoff, and metadata. Recheck plugins and imported content before moving data.

## Update content

- **Programs and requirements.** Edit `PROGRAMS` and `REQUIREMENTS` in `content.py`. Confirm school-year details with Admissions first.
- **News.** Add entries to `ANNOUNCEMENTS` with an ISO date, title, and summary. The newest date appears first. Keep historical material in `ARCHIVE`.
- **Staff.** Add verified entries to `FACULTY` with group, name, role, and an optional portrait filename. Put approved portraits in `static/assets/`. Use square, optimized files and review current permission.
- **Photos.** Use approved school originals. Export responsive WebP variants at 480, 960 and 1440 pixels where the source allows. Update `PHOTOS` with accurate alternative text and aspect ratio. Retain asset provenance and photo permissions in school records.
- **Contact and forms.** Update the school constants in `content.py` and the public contact copy in `build.py` as needed. Confirm the target is the institution’s active form for the correct intake before publishing changes.

Run the build, inspect a preview, then commit the approved changes. Branding tokens live in `static/styles.css`.
