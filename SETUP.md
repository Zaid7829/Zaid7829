# Zaid7829 GitHub Profile — Complete Setup

This repository contains a terminal-style developer portfolio rendered inside GitHub's profile README environment. It features high-density dot-matrix particle portrait art, an animated typewriter name, an interactive developer card, a technology radar dashboard, technical skill radar visualizations, and an animated GitHub contribution heatmap with a roaming snake.

GitHub displays a profile README when:
1. The repository name exactly matches your username (`Zaid7829/Zaid7829`).
2. The repository is **Public**.
3. A non-empty `README.md` exists in the repository root.

---

## 1. Repository Structure

```text
Zaid7829/
├── README.md                      # Primary profile interface
├── SETUP.md                       # Setup and documentation
├── PROJECT_TEMPLATE.md            # Template for adding verified projects
│
├── avi-dotmatrix.svg              # Animated high-density particle portrait (760x760)
├── hero-name.svg                  # Animated typewriter header (600x64)
├── info-card.svg                  # Terminal developer system card (760x304)
├── toolbox.svg                    # Technology radar dashboard (940x850)
├── skill-radar.svg                # Dual-axis technical skill radar chart (940x440)
├── contrib-heatmap.svg            # Animated GitHub contribution heatmap (940x265)
│
├── data/
│   ├── design.json                # Unified visual design tokens (colors, motion, typography)
│   ├── profile.json               # Primary profile configuration
│   ├── skills.json                # Self-assessed skill radar configuration
│   └── contributions.json         # Cached contribution calendar data
│
├── icons/                         # Brand and category SVGs
│
├── scripts/
│   ├── fetch_contributions.py     # Scrapes public GitHub contribution calendar
│   ├── render_heatmap_svg.py      # Renders animated contribution heatmap SVG
│   ├── render_skill_radar.py      # Renders dual skill radar SVG
│   ├── render_toolbox_svg.py      # Renders standalone toolbox SVG
│   ├── render_name_svg.py         # Renders animated typewriter header SVG
│   ├── make_dotmatrix_svg.py      # Generates dot-matrix particle portrait SVG
│   ├── make_info_card.py          # Generates developer system info card SVG
│   ├── prep_photo.py              # Preprocesses raw photos for portrait generation
│   ├── preview.py                 # Local GitHub markdown browser previewer
│   ├── validate_all.py            # End-to-end repository syntax and security validator
│   ├── requirements.txt           # Lightweight dependencies for daily workflow
│   └── requirements-local.txt     # Local-only dependencies (OpenCV, PIL, rembg)
│
├── .github/
│   └── workflows/
│       └── update-profile-art.yml # Daily GitHub Actions automation
│
└── .gitignore
```

---

## 2. Configuration & Customization

### Profile Information (`data/profile.json`)
Edit `data/profile.json` to customize your role, tagline, focus areas, tech stack, and status message:

```bash
# After editing data/profile.json, regenerate the developer card:
python scripts/make_info_card.py
```

### Skill Radar (`data/skills.json`)
Edit `data/skills.json` to adjust your self-assessed focus and language mix:

```bash
# After editing data/skills.json, regenerate the skill radar:
python scripts/render_skill_radar.py
```

### Technology Toolbox (`toolbox.svg`)
To regenerate the standalone toolbox dashboard:

```bash
python scripts/render_toolbox_svg.py
```

### Portrait Regeneration (`scripts/make_dotmatrix_svg.py`)
To generate a new dot-matrix particle portrait from a photograph:

```bash
# 1. Install local dependencies
pip install -r scripts/requirements-local.txt

# 2. Run the dot-matrix generator
python scripts/make_dotmatrix_svg.py
```

*Note: Never commit private photographs to Git. The `.gitignore` file automatically excludes `*.jpg`, `*.png`, and intermediate portrait files.*

---

## 3. GitHub Contribution Heatmap

The contribution system is completely self-contained and avoids third-party tracking services:

```bash
# Fetch latest public activity from GitHub:
python scripts/fetch_contributions.py

# Render updated animated heatmap SVG:
python scripts/render_heatmap_svg.py
```

---

## 4. Daily Automation (GitHub Actions)

The workflow at `.github/workflows/update-profile-art.yml`:
- Runs daily at 06:17 UTC via cron schedule.
- Supports manual triggering (`workflow_dispatch`) from the Actions tab.
- Uses `GITHUB_TOKEN` with `contents: write` permissions.
- Installs only lightweight dependencies (`requests`, `beautifulsoup4`).
- Refreshes `contrib-heatmap.svg`, `skill-radar.svg`, `toolbox.svg`, and `hero-name.svg` only when changes occur.

---

## 5. Local Validation

To test and compile all Python scripts, JSON schemas, SVGs, and security rules:

```bash
python scripts/validate_all.py
```

---

## 6. Commit & Push

```bash
git add .
git commit -m "feat: unify profile SVG design system"
git push origin main
```
