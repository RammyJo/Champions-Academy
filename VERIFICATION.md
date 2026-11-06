# Source audit and launch review

Historical record from the initial build. Later revisions and the current deployment are described in README.md. The site has since been deployed to Cloudflare Pages; the original verification below is not a fresh test of every later change.

Audited November 5, 2026 (Asia/Manila). The reference was the public Champions Academy WordPress site.

| Area | Source and decision |
| --- | --- |
| Brand | The official site icon contains the school’s shield. Preserved the published PNG. The school’s signage artwork combines blue and red with white. The redesign uses navy #082C5C and red #BF1E2D sampled from the institutional artwork, with crest blue #042E60. The legacy theme uses a sans-serif-led WordPress layout. The new site uses a system sans serif for reading and Georgia for editorial headings. |
| Mission and values | The [About graphics](https://champions.edu.ph/about/) supplied vision, mission, and the formal five values. The [homepage](https://champions.edu.ph/) separately presents five character traits. Both lists are labeled by source. |
| Philosophy and programs | The [academic overview](https://champions.edu.ph/program/), [Preschool](https://champions.edu.ph/preschool/), [Grade School](https://champions.edu.ph/home/gradeschool/), and [Junior High](https://champions.edu.ph/junior-high-school/) supplied teaching themes, program structure, and published entry guidance. |
| History | The [school history](https://champions.edu.ph/history/) documents the Christian community, Make Kids Smile outreach, and initial growth. |
| Faculty | The [legacy roster](https://champions.edu.ph/faculty/) contains leadership, administration, and teacher names and portraits. Several images date from 2021–2023. Current assignments and permission are pending. The public directory supports approved records and currently directs families to the office. |
| Admissions | The [Academics](https://champions.edu.ph/program/) checklist and [Pre-register](https://champions.edu.ph/pre-register/) embed were inspected. The linked Google form returned a learner information page over HTTPS. No learner data was entered or submitted. The school needs to confirm current intake, placement rules, document applicability, response access, and turnaround. |
| Contact | The [Contact page](https://champions.edu.ph/contact/) publishes the two telephone numbers and four emails. Office hours are published on Academics. Directions use the place identifier in the school’s published Maps embed. Facebook and Instagram URLs came from official site links. The school should confirm current hours, contact ownership, and reception. |
| Summer and Zoom | Summer has a separate legacy Google Form, with no verified active intake. The route directs families to Admissions. The existing Zoom menu URL has a meeting credential. Staff should confirm the link, meeting access policy and distribution channel before restoring it. |
| News | [Legacy Blog](https://champions.edu.ph/blog/) links to 2017 articles. Three are summarized under their original dated routes. The nursery preview timed out during review and redirects to Preschool. |
| Media | The [public media endpoint](https://champions.edu.ph/wp-json/wp/v2/media) and page assets supplied the crest and photos below. Public source provenance identifies the school. Obtain institutional approval and confirm safeguarding permissions for identifiable minors before public launch. |

## Asset inventory

| Local asset stem | Original path under the school’s WordPress uploads |
| --- | --- |
| crest | 2019/06/cropped-logo-270x270.png |
| celebration | 2025/06/DSCF4803-scaled.jpg |
| student-performance | 2025/06/DSCF4810-scaled.jpg |
| school-event | 2025/06/DSCF4814-scaled.jpg |
| junior-high | 2025/06/IMG_9264-1-scaled.jpg |
| campus | 2021/06/facade-2.jpg |
| preschool | 2021/06/preschhol.jpg |

## Privacy review

The redesign has no student-data fields, embedded form, tracking script, or submission storage. It links out to the school’s existing Google Form. Before cutover, have the school’s privacy lead verify the form’s purpose, lawful basis and parent or guardian notice, the need for each field, access to responses and exports, retention, and data-subject request handling. Approve the website privacy copy and the form notice together. See the [National Privacy Commission implementing rules](https://privacy.gov.ph/implementing-rules%20regulations-data-privacy-act-2012/) and [right to be informed](https://privacy.gov.ph/the-right-to-be-informed/).

## Legacy WordPress security

Unrelated software crack and APK links were present in Academics. Multiple dated blog articles also contained unexpected external links in ordinary prose. These findings warrant investigation. The redesign uses independently written static files and imports only selected, decoded images and approved public facts.

Have the legacy host preserve backups and logs, review WordPress core, themes, plugins, database content, administrator and service accounts, and check for unauthorized modifications, persistence, and SEO spam. Scan for malware, rotate affected credentials after containment, and validate a clean restore and rollback procedure. Coordinate DNS cutover with that work.

## Local QA results

- The production build generated 20 routes plus a 404 page. The navigation script passed Node syntax checking. The build uses Python and browser JavaScript.
- Chromium loaded all 20 routes at 360, 390, 768, 1024 and 1440 pixels. The checks covered horizontal overflow, internal destinations, one main heading and canonical per route, and decoding every rendered image. Keyboard checks exercised the skip link, mobile navigation and dropdown dismissal. No console errors were observed in the test run.
- Axe reported zero violations in the tested WCAG A/AA rules across the 20 routes at 390 pixels. This is an automated check. Manual assistive-technology testing and Lighthouse scoring remain open.
- The original Google Form opened over HTTPS. The Facebook, Instagram and Maps URLs returned HTTP 200. Social page visibility and Maps pin rendering may depend on browser and account state. Telephone and email links were inspected without calling or sending a message.
- Production DNS, school-owned Cloudflare Pages and Google Forms administration were outside the preview environment.

## Added classroom photographs

Source: https://www.facebook.com/sfchampionsacademy/photos/

- `classroom-activity`: Facebook photo ID 1745987494194503.
- `classroom-together`: Facebook photo ID 1745987454194507.

Both use 480px and 940px WebP variants. Additional photo candidates are in `media-library/facebook-shortlist/` with source URLs and are not part of the generated site.
