# Push Prompt for GitHub

Copy the prompt below into GitHub Copilot / your coding assistant after opening the `Zaid7829/Zaid7829` repository.

```text
I am setting up my GitHub profile repository.

Username:
Zaid7829

Repository:
Zaid7829/Zaid7829

I have a prepared profile package. Help me put the package into this repository without inventing personal information.

The final repository should have this structure:

README.md
SETUP.md
avi-ascii.svg
info-card.svg
contrib-heatmap.svg

data/
  contributions.json
  profile.json

scripts/
  fetch_contributions.py
  make_ascii_svg.py
  make_info_card.py
  prep_photo.py
  render_heatmap_svg.py
  requirements.txt
  requirements-local.txt

.github/
  workflows/
    update-profile-art.yml

.gitignore

Requirements:

1. README.md must be at the repository root.
2. Present Zaid7829 as a Full Stack Developer / Software Engineer / Builder.
3. Keep the terminal-style aesthetic.
4. Include sections for:
   - About Me
   - What I Build
   - Programming Languages
   - Frontend
   - Backend & APIs
   - Databases
   - Cloud & DevOps
   - Testing
   - AI / ML
   - Tools
   - Architecture
   - Engineering Principles
   - Currently
   - Development Workflow
   - Project Philosophy
   - GitHub Activity
   - Open Source Mindset
   - What I'm Improving
   - Contact
5. Keep the broad technology toolbox, but explicitly describe it as a technology radar rather than claiming expert-level knowledge of every technology.
6. Preserve the generated ASCII portrait and animated SVG developer card.
7. Preserve the animated contribution heatmap.
8. Do not add JavaScript to the README.
9. Do not add personal access tokens, API keys, passwords, .env files, private photos, or other secrets.
10. Do not replace the self-hosted contribution system with a third-party GitHub statistics service.
11. Keep the contribution workflow using GitHub Actions and the repository GITHUB_TOKEN.
12. The workflow should request contents: write permission and run daily plus support workflow_dispatch.
13. Do not invent projects, employers, education, awards, follower counts, contribution counts, or other personal achievements.
14. Preserve all existing working Python scripts unless a change is required to fix a real problem.
15. Validate Python syntax with:
    python -m py_compile scripts/*.py
16. Check that every README image path exists.
17. Check that .github/workflows/update-profile-art.yml is in the correct location.
18. Check that the repository is ready for GitHub's profile README renderer.

Do not use a generic template instead of the supplied files. Use the prepared package as the source of truth.

After everything is in place, give me the exact commands to commit and push.

Use this commit message:

feat: build terminal-style developer profile

The final push command should target:

origin main
```

## If using Git locally instead

Run:

```bash
git clone https://github.com/Zaid7829/Zaid7829.git
cd Zaid7829
```

Copy the package contents into that folder, then:

```bash
git add .
git commit -m "feat: build terminal-style developer profile"
git push origin main
```

After pushing, open:

```text
https://github.com/Zaid7829
```

Then go to:

**Repository → Actions → Update profile art → Run workflow**

to test the contribution updater once.
