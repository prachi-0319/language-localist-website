#!/usr/bin/env python3
"""
End-to-end link integrity tester for Language Localist website.
Checks every internal href in every HTML file to ensure no 404s.
"""
import os, re, glob, sys
from pathlib import Path

BASE = Path(os.path.dirname(os.path.abspath(__file__)))

# All pages that should exist
EXPECTED_PAGES = [
    "index.html", "about.html", "services.html", "technology.html",
    "estimate.html", "careers.html",
    "multilingual-dtp.html", "translation-services.html",
    "editing-proofreading.html", "voice-over.html",
    "transcription-subtitling.html", "website-development.html",
    "medical-translation.html", "legal-translation.html",
    "financial-translation.html", "technical-translation.html",
    "it-translation.html",
    "indian-languages.html", "asian-languages.html",
    "middle-eastern-languages.html", "european-languages.html",
    "african-languages.html",
    "quality.html", "terms.html", "disclaimer.html", "privacy-policy.html",
]

# Required SEO elements per page
REQUIRED_SEO = ["<title>", '<meta name="description"', '<link rel="canonical"', 'og:title']

def get_internal_links(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Find all href values
    hrefs = re.findall(r'href=["\']([^"\'#?]+)["\']', content)
    # Filter to local .html files only
    local = [h for h in hrefs if h.endswith(".html") and not h.startswith("http")]
    return set(local), content

def check_seo(filepath, content):
    issues = []
    for tag in REQUIRED_SEO:
        if tag not in content:
            issues.append(f"Missing: {tag}")
    # Check title is not generic
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match and title_match.group(1).strip() in ["", "Language Localist"]:
        issues.append("Generic/empty title tag")
    return issues

def main():
    print("=" * 60)
    print("LANGUAGE LOCALIST — END-TO-END SITE AUDIT")
    print("=" * 60)

    all_files = {f.name for f in BASE.glob("*.html")}
    errors = []
    warnings = []

    # ── 1. Check all expected pages exist ───────────────────────────────────
    print("\n📄 Checking required pages exist...")
    missing_pages = []
    for page in EXPECTED_PAGES:
        path = BASE / page
        if path.exists():
            print(f"  ✓ {page}")
        else:
            print(f"  ✗ MISSING: {page}")
            missing_pages.append(page)
            errors.append(f"Missing page: {page}")

    # ── 2. Check all internal links resolve ─────────────────────────────────
    print("\n🔗 Checking internal links in all pages...")
    link_errors = []
    for filepath in sorted(BASE.glob("*.html")):
        links, content = get_internal_links(filepath)
        broken = [l for l in links if l not in all_files]
        if broken:
            for b in broken:
                print(f"  ✗ {filepath.name} → broken link: {b}")
                link_errors.append(f"{filepath.name} → {b}")
                errors.append(f"Broken link in {filepath.name}: {b}")
        else:
            print(f"  ✓ {filepath.name} ({len(links)} links OK)")

    # ── 3. SEO audit ────────────────────────────────────────────────────────
    print("\n🔍 SEO audit (title, description, canonical, og:title)...")
    seo_errors = []
    for filepath in sorted(BASE.glob("*.html")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        issues = check_seo(filepath, content)
        if issues:
            for issue in issues:
                print(f"  ⚠ {filepath.name}: {issue}")
                warnings.append(f"{filepath.name}: {issue}")
        else:
            print(f"  ✓ {filepath.name}")

    # ── 4. Check nav contains new links on key pages ────────────────────────
    print("\n🧭 Checking nav links on core pages...")
    nav_check_pages = ["index.html", "services.html", "careers.html", "estimate.html"]
    for page in nav_check_pages:
        path = BASE / page
        if not path.exists():
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        nav_ok = True
        for link in ["about.html", "technology.html", "estimate.html"]:
            if link not in content:
                print(f"  ✗ {page}: nav missing link to {link}")
                errors.append(f"{page} nav missing: {link}")
                nav_ok = False
        if nav_ok:
            print(f"  ✓ {page}")

    # ── 5. Check footer on core pages ───────────────────────────────────────
    print("\n🦶 Checking footer on core pages...")
    for page in ["index.html", "services.html", "careers.html"]:
        path = BASE / page
        if not path.exists():
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        footer_links = ["about.html", "technology.html", "quality.html",
                        "terms.html", "disclaimer.html", "privacy-policy.html"]
        missing_fl = [l for l in footer_links if l not in content]
        if missing_fl:
            print(f"  ✗ {page}: footer missing links: {missing_fl}")
            errors.append(f"{page} footer missing: {missing_fl}")
        else:
            print(f"  ✓ {page}")

    # ── Summary ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Pages checked:  {len(list(BASE.glob('*.html')))}")
    print(f"  Errors:         {len(errors)}")
    print(f"  Warnings:       {len(warnings)}")

    if errors:
        print("\n❌ ERRORS (must fix):")
        for e in errors:
            print(f"   • {e}")
    if warnings:
        print("\n⚠  WARNINGS (should fix):")
        for w in warnings:
            print(f"   • {w}")
    if not errors and not warnings:
        print("\n✅ ALL CHECKS PASSED. Site is ready.")
    elif not errors:
        print("\n✅ No critical errors. Only warnings remain.")

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())

