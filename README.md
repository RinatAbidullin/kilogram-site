# Kilogram website for GitHub Pages

Static website prepared for GitHub Pages. No build tools, Jekyll, npm or dependencies are required.

## Pages

- `/` — main page / Marketing URL
- `/privacy/` — Privacy Policy URL
- `/terms/` — Terms of Use
- `/support/` — Support URL
- `/data-sources/` — food data attribution
- `/licenses/` — third-party notices

## 1. Replace placeholders before publishing

Search the repository for these values:

- `DEVELOPER_NAME_OR_COMPANY`
- `PRIVACY_EMAIL`
- `SUPPORT_EMAIL`
- `OFF_DERIVATIVE_DATABASE_URL_OR_REMOVE`
- `OPEN_SOURCE_NOTICES`

Also review all policy text and remove statements that do not match the released app.

A quick search from Terminal:

```bash
grep -R "PLACEHOLDER\|DEVELOPER_NAME_OR_COMPANY\|PRIVACY_EMAIL\|SUPPORT_EMAIL\|OFF_DERIVATIVE_DATABASE_URL_OR_REMOVE\|OPEN_SOURCE_NOTICES" .
```

## 2. Create a GitHub repository

Recommended repository name:

```text
kilogram-site
```

For the simplest GitHub Pages setup, make it public.

## 3. Push the site

```bash
git init
git add .
git commit -m "Add Kilogram website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kilogram-site.git
git push -u origin main
```

## 4. Enable GitHub Pages

Repository → **Settings** → **Pages**

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/(root)`

After publishing, the URL will normally be:

```text
https://YOUR_USERNAME.github.io/kilogram-site/
```

App Store URLs:

```text
Privacy Policy URL:
https://YOUR_USERNAME.github.io/kilogram-site/privacy/

Support URL:
https://YOUR_USERNAME.github.io/kilogram-site/support/

Marketing URL:
https://YOUR_USERNAME.github.io/kilogram-site/
```

## Optional custom domain

If you later buy a domain such as `kilogramapp.com`, configure it in GitHub Pages and then use stable URLs such as:

```text
https://kilogramapp.com/privacy/
https://kilogramapp.com/support/
```

## Important

This repository contains starter legal text, not legal advice. Before App Store submission, make sure the text matches:

- actual data collection and storage;
- App Store Privacy Nutrition Labels;
- HealthKit usage;
- subscriptions / Kilogram Pro;
- all third-party services;
- food database licenses and attribution;
- account deletion flow, if accounts exist.
