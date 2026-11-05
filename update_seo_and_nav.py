#!/usr/bin/env python3
"""
Global SEO meta-tag + nav updater for Language Localist website.
Applies correct title tags, meta descriptions, canonical URLs,
Open Graph tags, and updated nav/footer to all HTML pages.
Run after subagents have written index.html, about.html, technology.html,
multilingual-dtp.html, estimate.html.
"""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.languagelocalist.com"

# ── Per-page SEO data ────────────────────────────────────────────────────────
PAGE_SEO = {
    "index.html": {
        "title": "Expert Translation & Multilingual DTP Services | Language Localist",
        "desc":  "Since 2003, Language Localist has provided premium translation and multilingual desktop publishing (DTP) services. Specializing in Indian, Asian, and Middle Eastern languages, we support global agencies and clients across the UK, USA, Europe, Australia, and India.",
        "kw":    "translation services, multilingual DTP, Indian language translation, Arabic translation, Hindi translation, DTP typesetting, localization agency",
        "robots": "index, follow",
    },
    "about.html": {
        "title": "About Language Localist | B2B Translation & DTP Agency Est. 2003",
        "desc":  "Learn about Language Localist. For over two decades, we have been the trusted localization and multilingual typesetting partner for global language agencies and enterprises.",
        "kw":    "about Language Localist, translation agency history, B2B DTP agency, translation outsourcing partner",
        "robots": "index, follow",
    },
    "services.html": {
        "title": "Translation & Localization Expertise | Language Localist",
        "desc":  "Comprehensive language solutions tailored for complex industries — legal, medical, technical, and marketing. Expert translators with 7+ years subject-matter experience.",
        "kw":    "translation services, legal translation, medical translation, technical translation, localization expertise",
        "robots": "index, follow",
    },
    "technology.html": {
        "title": "Translation Technology, CAT & TM Tools | Language Localist",
        "desc":  "We leverage advanced translation technology, including SDL Trados Studio, memoQ, Memsource, and Phrase, to deliver consistent, cost-effective, and high-quality localization.",
        "kw":    "SDL Trados Studio, memoQ, Memsource, Phrase, CAT tools, translation memory, TM tools, localization technology",
        "robots": "index, follow",
    },
    "estimate.html": {
        "title": "Request a Free Translation Quote | Language Localist",
        "desc":  "Request a free, secure project quote for professional translation and multilingual DTP services. File upload supported. Response within 4 business hours.",
        "kw":    "translation quote, free quote, DTP quote, localization estimate",
        "robots": "noindex, nofollow",
    },
    "careers.html": {
        "title": "Translation Careers & Freelance Linguist Jobs | Language Localist",
        "desc":  "Join the Language Localist network. We seek experienced native-speaking translators, DTP specialists, and linguists with 7+ years of subject-matter expertise.",
        "kw":    "translation jobs, freelance translator, linguist careers, DTP jobs, translation agency careers",
        "robots": "index, follow",
    },
    "multilingual-dtp.html": {
        "title": "Multilingual Desktop Publishing & Typesetting | Outsource DTP | Language Localist",
        "desc":  "Expert multilingual DTP and typesetting services. We format Right-to-Left (RTL), Indic, and Asian scripts in InDesign, Illustrator, Canva, and QuarkXPress for global campaigns.",
        "kw":    "multilingual DTP, desktop publishing, typesetting, RTL typesetting, InDesign localization, Arabic typesetting, Hindi typesetting, outsource DTP",
        "robots": "index, follow",
    },
    "translation-services.html": {
        "title": "Asian, Indian & Middle Eastern Translation Services | Language Localist",
        "desc":  "Professional translation and localization services specializing in Indian, Asian, and Middle Eastern languages for B2B, technical, and corporate sectors. Native speakers only.",
        "kw":    "translation services, Indian language translation, Asian translation, Middle Eastern translation, Hindi translation, Arabic translation, Bengali translation",
        "robots": "index, follow",
    },
    "editing-proofreading.html": {
        "title": "Professional Editing & Proofreading Services | Language Localist",
        "desc":  "Rigorous editing and proofreading by native-speaking linguists to verify tone, grammar, terminology consistency, and industry compliance for translated documents.",
        "kw":    "translation editing, proofreading, linguistic QA, translation review, grammar verification",
        "robots": "index, follow",
    },
    "voice-over.html": {
        "title": "Professional Voice-Over & Audio Localization | Language Localist",
        "desc":  "Native voice talent for corporate, commercial, and educational media in 80+ languages. Studio-quality recordings delivered in any format with full post-production.",
        "kw":    "voice over services, audio localization, multilingual voice over, corporate narration, language voice over",
        "robots": "index, follow",
    },
    "transcription-subtitling.html": {
        "title": "Transcription & Subtitling Services | Language Localist",
        "desc":  "Time-synced, culturally nuanced video localization. Professional transcription and subtitling adapted for local broadcast standards and online platforms in SRT/VTT format.",
        "kw":    "transcription services, subtitling, video localization, SRT files, multilingual subtitles, closed captions",
        "robots": "index, follow",
    },
    "website-development.html": {
        "title": "Multilingual Website Development & Localization | Language Localist",
        "desc":  "Complete digital localization for your website. CMS integration, SEO-optimized multilingual content, and UI/UX adaptation for global markets.",
        "kw":    "multilingual website, website localization, CMS translation, multilingual SEO, international website development",
        "robots": "index, follow",
    },
    "medical-translation.html": {
        "title": "Medical Translation Services | Clinical & Pharmaceutical | Language Localist",
        "desc":  "Certified medical translation for clinical trials, regulatory submissions, patient records, and pharmaceutical documentation. ISO 17100 compliant. EMA and FDA terminology.",
        "kw":    "medical translation, clinical trial translation, pharmaceutical translation, healthcare translation, FDA translation, EMA translation",
        "robots": "index, follow",
    },
    "legal-translation.html": {
        "title": "Legal Translation Services | Sworn & Certified | Language Localist",
        "desc":  "Certified legal translation for contracts, M&A documents, court filings, and intellectual property documentation. Sworn translators for official legal standing.",
        "kw":    "legal translation, certified translation, sworn translation, contract translation, court document translation, IP translation",
        "robots": "index, follow",
    },
    "financial-translation.html": {
        "title": "Financial Translation Services | Reports & Compliance | Language Localist",
        "desc":  "Expert financial translation for annual reports, audit documents, compliance filings, and investor communications. Accurate financial terminology in 80+ languages.",
        "kw":    "financial translation, annual report translation, compliance translation, investor relations translation, banking translation",
        "robots": "index, follow",
    },
    "technical-translation.html": {
        "title": "Technical Translation Services | Manuals & Engineering | Language Localist",
        "desc":  "Specialist technical translation for instruction manuals, engineering specifications, safety data sheets, and technical documentation in all world languages.",
        "kw":    "technical translation, manual translation, engineering translation, SDS translation, industrial translation",
        "robots": "index, follow",
    },
    "it-translation.html": {
        "title": "IT & Software Translation Services | UI/UX Localization | Language Localist",
        "desc":  "Professional IT and software translation for UI/UX, API documentation, B2B SaaS platforms, and workplace technology. CAT-tool integrated workflows.",
        "kw":    "IT translation, software localization, UI UX translation, app localization, SaaS translation, API documentation translation",
        "robots": "index, follow",
    },
    "indian-languages.html": {
        "title": "Indian Language Translation Services | Hindi, Bengali, Tamil & More | Language Localist",
        "desc":  "Expert translation for all major Indian languages including Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Kannada, Malayalam, and Punjabi. Native speakers only.",
        "kw":    "Hindi translation, Bengali translation, Tamil translation, Telugu translation, Marathi translation, Gujarati translation, Indian language translation",
        "robots": "index, follow",
    },
    "asian-languages.html": {
        "title": "Asian Language Translation Services | Chinese, Japanese, Korean | Language Localist",
        "desc":  "Professional translation for East and Southeast Asian languages including Chinese (Simplified/Traditional), Japanese, Korean, Vietnamese, Thai, and Indonesian.",
        "kw":    "Chinese translation, Japanese translation, Korean translation, Vietnamese translation, Thai translation, Asian language translation",
        "robots": "index, follow",
    },
    "middle-eastern-languages.html": {
        "title": "Middle Eastern Language Translation | Arabic, Farsi, Hebrew | Language Localist",
        "desc":  "Specialized RTL translation for Middle Eastern languages including Arabic, Persian (Farsi), Hebrew, Turkish, and Kurdish. Expert RTL typesetting available.",
        "kw":    "Arabic translation, Farsi translation, Hebrew translation, Turkish translation, RTL translation, Middle Eastern language translation",
        "robots": "index, follow",
    },
    "european-languages.html": {
        "title": "European Language Translation Services | Spanish, French, German | Language Localist",
        "desc":  "Comprehensive European language translation including Spanish, French, German, Italian, Portuguese, Dutch, Russian, Polish, Swedish, and Greek.",
        "kw":    "Spanish translation, French translation, German translation, Italian translation, Portuguese translation, European language translation",
        "robots": "index, follow",
    },
    "african-languages.html": {
        "title": "African Language Translation Services | Swahili, Zulu, Hausa | Language Localist",
        "desc":  "Professional African language translation for Swahili, Amharic, Zulu, Xhosa, Hausa, Yoruba, Igbo, and Afrikaans. In-country native linguists.",
        "kw":    "Swahili translation, Zulu translation, Hausa translation, Yoruba translation, African language translation",
        "robots": "index, follow",
    },
    "quality.html": {
        "title": "Quality Statement | Language Localist",
        "desc":  "Our quality commitment: highest standards in translation and DTP, ISO-compliant processes, and continual improvement in all business practices.",
        "kw":    "translation quality, ISO translation, quality assurance translation",
        "robots": "index, follow",
    },
    "terms.html": {
        "title": "Terms & Conditions | Language Localist",
        "desc":  "Terms and conditions for using Language Localist services and website.",
        "kw":    "",
        "robots": "noindex, follow",
    },
    "disclaimer.html": {
        "title": "Disclaimer | Language Localist",
        "desc":  "Legal disclaimer for Language Localist website and services.",
        "kw":    "",
        "robots": "noindex, follow",
    },
    "privacy-policy.html": {
        "title": "Privacy Policy | Language Localist",
        "desc":  "Privacy policy for Language Localist website and services. We respect and protect your personal information.",
        "kw":    "",
        "robots": "noindex, follow",
    },
}

# ── New nav HTML (shared across all pages) ──────────────────────────────────
NEW_NAV_DESKTOP = '''\
  <nav class="hidden md:flex items-center space-x-8" id="navLinks">
    <a class="font-label text-[13px] text-neutral-500 hover:text-brand-navy transition-colors tracking-wide" href="index.html#why-us">The Difference</a>
    <a class="font-label text-[13px] text-neutral-500 hover:text-brand-navy transition-colors tracking-wide" href="about.html">About Us</a>
    <a class="font-label text-[13px] text-neutral-500 hover:text-brand-navy transition-colors tracking-wide" href="services.html">Expertise</a>
    <a class="font-label text-[13px] text-neutral-500 hover:text-brand-navy transition-colors tracking-wide" href="technology.html">Technology</a>
    <a class="font-label text-[13px] text-neutral-500 hover:text-brand-navy transition-colors tracking-wide" href="careers.html">Careers</a>
    <a class="bg-brand-navy hover:bg-brand-gold text-white font-label text-[11px] uppercase tracking-widest font-semibold px-7 py-3 rounded-full transition-all duration-300 shadow-md hover:shadow-lg" href="estimate.html">Get a Quote</a>
  </nav>
  <button class="md:hidden p-2" onclick="document.getElementById(\'mobileMenu\').classList.toggle(\'hidden\')" aria-label="Open menu">
    <span class="material-symbols-outlined text-brand-navy">menu</span>
  </button>'''

NEW_MOBILE_MENU = '''\
<div id="mobileMenu" class="hidden md:hidden bg-brand-sand border-t border-black/5 px-6 py-6 flex flex-col space-y-4">
  <a class="font-label text-[14px] text-neutral-600 hover:text-brand-navy" href="about.html">About Us</a>
  <a class="font-label text-[14px] text-neutral-600 hover:text-brand-navy" href="services.html">Expertise</a>
  <a class="font-label text-[14px] text-neutral-600 hover:text-brand-navy" href="technology.html">Technology</a>
  <a class="font-label text-[14px] text-neutral-600 hover:text-brand-navy" href="careers.html">Careers</a>
  <a class="inline-block bg-brand-navy text-white font-label text-[11px] uppercase tracking-widest font-semibold px-6 py-3 rounded-full text-center" href="estimate.html">Get a Quote</a>
</div>'''

# ── New 5-column footer ──────────────────────────────────────────────────────
NEW_FOOTER_COLS = '''\
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 mb-16">
      <!-- Col 1 -->
      <div>
        <h4 class="font-headline text-brand-gold text-lg mb-6">Translation Services</h4>
        <ul class="space-y-3 font-label text-[13px] text-white/70">
          <li><a href="translation-services.html" class="hover:text-white transition-colors">Translation</a></li>
          <li><a href="multilingual-dtp.html" class="hover:text-white transition-colors">Multilingual DTP</a></li>
          <li><a href="editing-proofreading.html" class="hover:text-white transition-colors">Editing &amp; Proofreading</a></li>
          <li><a href="voice-over.html" class="hover:text-white transition-colors">Voice-Over</a></li>
          <li><a href="transcription-subtitling.html" class="hover:text-white transition-colors">Transcription &amp; Subtitling</a></li>
          <li><a href="website-development.html" class="hover:text-white transition-colors">Website Development</a></li>
        </ul>
      </div>
      <!-- Col 2 -->
      <div>
        <h4 class="font-headline text-brand-gold text-lg mb-6">Languages Translated</h4>
        <ul class="space-y-3 font-label text-[13px] text-white/70">
          <li><a href="indian-languages.html" class="hover:text-white transition-colors">Indian Languages</a></li>
          <li><a href="asian-languages.html" class="hover:text-white transition-colors">Asian Languages</a></li>
          <li><a href="middle-eastern-languages.html" class="hover:text-white transition-colors">Middle Eastern Languages</a></li>
          <li><a href="european-languages.html" class="hover:text-white transition-colors">European Languages</a></li>
          <li><a href="african-languages.html" class="hover:text-white transition-colors">African Languages</a></li>
        </ul>
      </div>
      <!-- Col 3 -->
      <div>
        <h4 class="font-headline text-brand-gold text-lg mb-6">Specialised Translations</h4>
        <ul class="space-y-3 font-label text-[13px] text-white/70">
          <li><a href="medical-translation.html" class="hover:text-white transition-colors">Medical Translation</a></li>
          <li><a href="legal-translation.html" class="hover:text-white transition-colors">Legal Translation</a></li>
          <li><a href="financial-translation.html" class="hover:text-white transition-colors">Financial Translation</a></li>
          <li><a href="technical-translation.html" class="hover:text-white transition-colors">Technical Translation</a></li>
          <li><a href="it-translation.html" class="hover:text-white transition-colors">IT Translation</a></li>
        </ul>
      </div>
      <!-- Col 4 -->
      <div>
        <h4 class="font-headline text-brand-gold text-lg mb-6">Company</h4>
        <ul class="space-y-3 font-label text-[13px] text-white/70">
          <li><a href="about.html" class="hover:text-white transition-colors">About Us</a></li>
          <li><a href="technology.html" class="hover:text-white transition-colors">Technology</a></li>
          <li><a href="careers.html" class="hover:text-white transition-colors">Careers</a></li>
          <li><a href="estimate.html" class="hover:text-white transition-colors">Get a Quote</a></li>
          <li><a href="quality.html" class="hover:text-white transition-colors">Quality Statement</a></li>
        </ul>
      </div>
      <!-- Col 5 -->
      <div>
        <a class="flex items-center mb-6" href="index.html">
          <img src="https://languagelocalist.com/images/logo.png" alt="Language Localist" class="h-10 w-auto brightness-0 invert opacity-90" />
        </a>
        <p class="font-body text-[13px] text-white/50 leading-relaxed mb-4">
          Premium translation &amp; localization for global sectors. Certified, human-verified, zero-tolerance precision. Est. 2003.
        </p>
        <a class="text-[14px] font-label text-brand-gold hover:text-white transition-colors" href="mailto:inquiries@languagelocalist.com">inquiries@languagelocalist.com</a>
      </div>
    </div>'''

NEW_FOOTER_BOTTOM = '''\
    <div class="border-t border-white/10 pt-8 flex flex-col lg:flex-row justify-between items-center gap-6">
      <p class="font-label text-[12px] text-white/40">© 2026 Language Localist. All rights reserved.</p>
      <div class="flex flex-wrap justify-center gap-6">
        <a class="text-[12px] font-label text-white/60 hover:text-brand-gold transition-colors" href="quality.html">Quality Statement</a>
        <a class="text-[12px] font-label text-white/60 hover:text-brand-gold transition-colors" href="terms.html">Terms &amp; Conditions</a>
        <a class="text-[12px] font-label text-white/60 hover:text-brand-gold transition-colors" href="disclaimer.html">Disclaimer</a>
        <a class="text-[12px] font-label text-white/60 hover:text-brand-gold transition-colors" href="privacy-policy.html">Privacy Policy</a>
      </div>
    </div>'''


def build_seo_block(filename):
    seo = PAGE_SEO.get(filename, {})
    title = seo.get("title", "Language Localist")
    desc  = seo.get("desc", "")
    kw    = seo.get("kw", "")
    robots = seo.get("robots", "index, follow")
    slug = filename.replace(".html", "")
    canonical = BASE_URL + "/" + filename if filename != "index.html" else BASE_URL + "/"
    og_url = canonical

    block = f'<title>{title}</title>\n'
    block += f'<meta name="description" content="{desc}"/>\n'
    if kw:
        block += f'<meta name="keywords" content="{kw}"/>\n'
    block += f'<meta name="robots" content="{robots}"/>\n'
    block += f'<link rel="canonical" href="{canonical}"/>\n'
    block += f'<meta property="og:type" content="website"/>\n'
    block += f'<meta property="og:url" content="{og_url}"/>\n'
    block += f'<meta property="og:title" content="{title}"/>\n'
    block += f'<meta property="og:description" content="{desc}"/>\n'
    block += f'<meta property="og:site_name" content="Language Localist"/>\n'
    block += f'<meta name="twitter:card" content="summary"/>\n'
    block += f'<meta name="twitter:title" content="{title}"/>\n'
    block += f'<meta name="twitter:description" content="{desc}"/>\n'
    return block


def update_file(filepath):
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # ── 1. Replace/inject SEO block between <head> open and first <link>/<script> ──
    seo_block = build_seo_block(filename)
    # Remove any existing title, meta description, meta keywords, meta robots,
    # canonical, og:*, twitter:* tags first
    html = re.sub(r'<title>.*?</title>', '', html, flags=re.DOTALL)
    html = re.sub(r'<meta\s+name="description"[^>]*/>', '', html)
    html = re.sub(r'<meta\s+name="keywords"[^>]*/>', '', html)
    html = re.sub(r'<meta\s+name="robots"[^>]*/>', '', html)
    html = re.sub(r'<link\s+rel="canonical"[^>]*/>', '', html)
    html = re.sub(r'<meta\s+property="og:[^"]*"[^>]*/>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<meta\s+name="twitter:[^"]*"[^>]*/>', '', html, flags=re.IGNORECASE)
    # Inject right after <head>
    html = re.sub(r'(<head>)', r'\1\n' + seo_block, html, count=1)

    # ── 2. Replace old nav (desktop portion inside header) ───────────────────
    # Match the existing nav block between logo link and end of header inner div
    # We look for the <nav ...> ... </nav> block plus any old mobile button/menu
    html = re.sub(
        r'<nav class="hidden md:flex[^"]*"[^>]*>.*?</nav>(\s*<button[^>]*>.*?</button>)?',
        NEW_NAV_DESKTOP,
        html, count=1, flags=re.DOTALL
    )

    # Remove any existing mobile menu div then append after header closing </div></header>
    html = re.sub(r'<div id="mobileMenu".*?</div>', '', html, flags=re.DOTALL)
    html = re.sub(r'(</header>)', NEW_MOBILE_MENU + r'\n\1', html, count=1)

    # ── 3. Replace old footer grid with new 5-column grid ───────────────────
    # Match old 4-col grid
    html = re.sub(
        r'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-\d+ mb-\d+">.*?</div>\s*(?=<!--\s*Bottom)',
        NEW_FOOTER_COLS + '\n      ',
        html, count=1, flags=re.DOTALL
    )
    # Also handle 5-col if already updated
    html = re.sub(
        r'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-\d+ mb-\d+">.*?</div>\s*(?=<!--\s*Bottom)',
        NEW_FOOTER_COLS + '\n      ',
        html, count=1, flags=re.DOTALL
    )

    # ── 4. Replace footer bottom bar ────────────────────────────────────────
    html = re.sub(
        r'<!--\s*Bottom Bar\s*-->.*?</div>\s*</div>\s*</footer>',
        '<!-- Bottom Bar -->\n' + NEW_FOOTER_BOTTOM + '\n  </div>\n</footer>',
        html, count=1, flags=re.DOTALL
    )

    # ── 5. Fix old email ─────────────────────────────────────────────────────
    html = html.replace('info@languagelocalist.com', 'inquiries@languagelocalist.com')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {filename}")


def main():
    files = glob.glob(os.path.join(BASE, "*.html"))
    # Skip generated_pages.py etc
    files = [f for f in files if f.endswith(".html")]
    print(f"Updating {len(files)} HTML files...\n")
    for filepath in sorted(files):
        try:
            update_file(filepath)
        except Exception as e:
            print(f"  ✗ {os.path.basename(filepath)}: {e}")
    print(f"\nDone. {len(files)} files updated.")

if __name__ == "__main__":
    main()

