# Assets Directory

This directory contains all static assets for the Sutra-Atlas project documentation.

## Screenshots

Save your application screenshots with these exact filenames in the `screenshots/` subdirectory:

### Required Screenshot Files:

1. **login.png** - Login page with dark theme
2. **register.png** - Registration page with password requirements  
3. **collections-dashboard.png** - Main collections overview
4. **create-collection.png** - Create new collection form
5. **collections-search.png** - Search functionality with no results
6. **add-resource.png** - Add new resource form
7. **resources-list.png** - Resources list with status badges
8. **user-profile.png** - User profile page
9. **faq.png** - FAQ page with accordion sections

### File Requirements:
- Format: PNG (recommended for screenshots)
- Naming: Exact filenames as listed above (lowercase, hyphens for spaces)
- Location: `/assets/screenshots/`

### After Adding Screenshots:
```bash
git add assets/screenshots/*.png
git commit -m "Add application screenshots for documentation"
git push origin main
```

The screenshots will then display properly in the GitHub README.md file.