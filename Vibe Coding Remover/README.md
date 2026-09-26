# Handcrafted Web Standards

A Claude skill that stops websites from looking vibe-coded.

When Claude builds, reviews or launches a website with this skill installed, it follows a fixed set of house rules. It skips the design habits that make a site look AI-generated, it doesn't invent social proof, and it won't call a site ready to launch until the basics are done. The skill also covers research projects: every claim needs a source, and every source is listed at the end.

## Why this exists

Visitors have learned to spot the AI-template look: purple gradients, pill buttons, rocket emoji, "Unlock the future of work" headlines, and a counter claiming 10,000+ happy customers. Once they notice one of these, they stop trusting the rest of the page. This skill turns that list of tells into rules Claude follows every time, and includes a script to check the result.

## What the skill does

**1. Starts with the end user.** Before building, Claude writes an empathy map: who the visitor is, what they search for, what worries them, what device they use, and the one action the page should lead them to. Design and copy decisions are tied back to it in the handoff.

**2. Enforces visual rules.**

| Not allowed | Used instead |
|---|---|
| Purple, violet or indigo gradients | A palette taken from the brand, mostly solid colours |
| Pill-shaped buttons | Square or slightly rounded buttons (0 to 8px) |
| Emoji as icons | A consistent SVG icon set, or no icon |
| AI-generated photos | The owner's real photos, or a type-led layout |
| Custom cursors and cursor effects | The system cursor |
| Parallax, scroll-jacking, fade-in-on-scroll everywhere | Static content, small feedback motion that respects `prefers-reduced-motion` |

**3. Enforces content rules.**
- No fake reviews, testimonials, ratings, logos, metrics or customer counters. If real ones aren't available, the section is left out.
- No vague hero text. The headline must say what this is, who it is for, and what to do next.
- No AI-sounding copy (unlock, elevate, seamless, supercharge and similar words).
- No em dashes.

**4. Checks launch readiness.** Claude won't describe a site as launch-ready until:
- a custom domain is connected (not `*.vercel.app`, `*.lovable.app` and so on)
- a favicon and apple-touch-icon are added
- every "Made with ..." or "Edit with ..." badge is removed
- a privacy policy page exists and is linked in the footer
- a terms and conditions page exists and is linked in the footer

Claude drafts the privacy policy and terms pages based on what the site actually collects. Each draft is marked as needing review by a lawyer.

**5. Holds research to a standard.** For research, Claude only cites sources it actually opened, never makes up a citation, and ends every output with a numbered References section.

**6. Checks its own work.** Before every handoff, Claude:
- runs the checker script
- looks at the page at phone and desktop widths
- verifies every fact on the page
- lists anything still unverified or unfinished instead of saying "done"

## Repository contents

```
handcrafted-web-standards/
├── SKILL.md                 The skill: instructions Claude reads (checker is embedded at the end)
├── scripts/
│   └── check_site.py        Standalone copy of the checker
├── examples/
│   ├── vibe-coded/          A deliberately bad page (the checker reports 14 blockers)
│   └── clean/               A page that passes
└── README.md
```

`SKILL.md` is self-contained: the checker is embedded in it, so the skill works even when uploaded as a single file. `scripts/check_site.py` is the same code, included so you can run it on its own.

## Installation

**Claude apps (web, desktop).** Zip the `handcrafted-web-standards` folder, open Claude's settings, find the Skills section and upload the zip. Skills need to be enabled for your account or organization.

**Claude Code.** Copy the folder into your skills directory:

```bash
# For all your projects
cp -r handcrafted-web-standards ~/.claude/skills/

# For one project only
cp -r handcrafted-web-standards .claude/skills/
```

Once installed, Claude uses the skill automatically for website, landing page, web UI, site copy and research work. You can also ask for it by name.

## Using the checker on its own

The checker needs only Python 3 and has no dependencies.

```bash
python3 scripts/check_site.py path/to/site            # design and content rules
python3 scripts/check_site.py path/to/site --launch   # adds the launch checklist
```

It scans HTML, CSS, JS, TS, JSX, TSX, Vue, Svelte, Astro, Markdown and JSON files and skips `node_modules` and build folders. Results come in two levels:

- **BLOCKER**: a rule is broken and must be fixed (for example an emoji, an em dash, a purple gradient, a pill button or a "Made with" badge). The script exits with code 1, so you can use it in CI.
- **REVIEW**: needs a person to judge (for example a customer count, a testimonial, a scroll-animation library or a temporary domain). A script can't tell a real number from a made-up one.

Try it on the examples:

```bash
python3 scripts/check_site.py examples/vibe-coded --launch
python3 scripts/check_site.py examples/clean --launch
```

Sample output:

```
[BLOCKER] em-dash                              examples/vibe-coded/index.html:8
          <p>Our platform — built for teams — helps you supercharge your workflow.</p>
[BLOCKER] pill-button                          examples/vibe-coded/index.html:3
          .btn-primary { border-radius: 9999px }
[REVIEW] metric-or-counter-needs-source       examples/vibe-coded/index.html:10
          <p>Trusted by 10,000+ happy customers. Rated 4.9 stars ★★★★★</p>
...
1 files scanned: 14 blocker(s), 8 item(s) to review.
```

### Limits

The checker is a safety net, not a replacement for looking at the page. It matches patterns, so it can't:
- tell whether a photo was AI-generated unless the file name or URL gives it away
- judge whether a headline is vague
- confirm that a custom domain's DNS is set up

The skill tells Claude to check those things by hand.

## Customising

The rules live in plain Markdown in `SKILL.md`, so you can edit them directly:
- **Banned words:** edit the list in section 3 of `SKILL.md` and the `SLOP_WORDS` pattern in the checker.
- **Purple detection:** colours with a hue between about 245 and 325 degrees count as purple. Change the range in `hsv_is_purple` if your brand uses a colour near that band.
- **Button radius:** the checker flags radii of 24px or more on buttons and links. Change the threshold in the `PILL_CSS` check.
- **Legal pages:** section 4 names India's DPDP Act 2023 and GDPR. Swap in the laws that apply to you.

If you change the checker, update both `scripts/check_site.py` and the copy at the end of `SKILL.md` so they stay the same.

## Contributing

Issues and pull requests are welcome, especially for:
- new AI-template tells to add to the checker
- false positives found on real sites
- support for more builder platforms and their badges

When you report a false positive, include the smallest snippet that triggers it.

## License

Add your chosen license here (for example MIT) and include a `LICENSE` file in the repository.

## Author

Rakshit Jain
