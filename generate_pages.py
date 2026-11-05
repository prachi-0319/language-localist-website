import os
import glob
import re

# Template data
pages = [
    {
        "filename": "translation-services.html",
        "title": "Translation Services",
        "icon": "translate",
        "category": "Linguistics & Verification",
        "headline": "Professional Document Translation.",
        "paragraph": "We engage highly qualified, subject-specific native speakers with a minimum of 7 years of specialized experience to guarantee accuracy across all industries.",
        "bullets": [
            "<strong>Native Fluency:</strong> Linguists translating exclusively into their mother tongue.",
            "<strong>Subject Matter Experts:</strong> Specialists in legal, medical, and technical fields.",
            "<strong>ISO Certified workflows:</strong> Rigorous quality assurance processes."
        ]
    },
    {
        "filename": "multilingual-dtp.html",
        "title": "Multilingual DTP",
        "icon": "design_services",
        "category": "Digital & Design",
        "headline": "Flawless Multilingual DTP.",
        "paragraph": "Dedicated in-house typesetters and professional operators with extensive experience across all major design suites (InDesign, Illustrator, etc.).",
        "bullets": [
            "<strong>Complex Layouts:</strong> Handling right-to-left languages and intricate formatting.",
            "<strong>Print-Ready Files:</strong> Delivered exactly to your specifications.",
            "<strong>Font Management:</strong> Extensive library of global typography."
        ]
    },
    {
        "filename": "editing-proofreading.html",
        "title": "Editing & Proofreading",
        "icon": "spellcheck",
        "category": "Linguistics & Verification",
        "headline": "Meticulous Editing & Proofreading.",
        "paragraph": "Rigorous secondary QA checks to verify tone, grammar, and industry compliance for translations produced internally or by third parties.",
        "bullets": [
            "<strong>Grammar & Syntax:</strong> Ensuring natural flow and perfect mechanics.",
            "<strong>Terminology Consistency:</strong> Verifying against approved glossaries.",
            "<strong>Cultural Nuance:</strong> Adapting tone for the target demographic."
        ]
    },
    {
        "filename": "voice-over.html",
        "title": "Voice-Over",
        "icon": "mic",
        "category": "Audio & Visual Localization",
        "headline": "Professional Voice-Over Talent.",
        "paragraph": "Native voice talent for corporate, commercial, and educational media, recorded in state-of-the-art studios.",
        "bullets": [
            "<strong>Extensive Talent Pool:</strong> Diverse ages, accents, and vocal styles.",
            "<strong>Studio Quality:</strong> High-fidelity recordings delivered in any format.",
            "<strong>Post-Production:</strong> Full audio mixing and syncing services."
        ]
    },
    {
        "filename": "transcription-subtitling.html",
        "title": "Transcription & Subtitling",
        "icon": "subtitles",
        "category": "Audio & Visual Localization",
        "headline": "Accurate Transcription & Subtitling.",
        "paragraph": "Time-synced, culturally nuanced video localization adapted for local broadcast standards and online platforms.",
        "bullets": [
            "<strong>Time-Coded Precision:</strong> Perfectly synced with on-screen action.",
            "<strong>Readability Optimization:</strong> Adapted for character limits and reading speeds.",
            "<strong>Multiple Formats:</strong> SRT, VTT, and broadcast-ready files."
        ]
    },
    {
        "filename": "website-development.html",
        "title": "Website Development",
        "icon": "language",
        "category": "Digital & Design",
        "headline": "Multilingual Website Development.",
        "paragraph": "Complete digital localization mapping your CMS to international markets. We handle text extraction, translation, and seamless reintegration.",
        "bullets": [
            "<strong>CMS Integration:</strong> Working directly with WordPress, Drupal, and custom platforms.",
            "<strong>SEO Optimization:</strong> Localized keywords and metadata for global search.",
            "<strong>UI/UX Adaptation:</strong> Ensuring layouts accommodate text expansion."
        ]
    },
    # Language Pages
    {
        "filename": "indian-languages.html",
        "title": "Indian Languages",
        "icon": "public",
        "category": "Languages Translated",
        "headline": "Indian Subcontinent Languages.",
        "paragraph": "Expert translation for the diverse linguistic landscape of India, ensuring regional nuances and dialects are perfectly captured.",
        "bullets": [
            "<strong>Major Languages:</strong> Hindi, Bengali, Telugu, Marathi, Tamil, Urdu, Gujarati, Kannada, Malayalam, Odia, Punjabi.",
            "<strong>Regional Dialects:</strong> Deep understanding of localized terminology.",
            "<strong>Script Expertise:</strong> Flawless rendering of complex Indic scripts."
        ]
    },
    {
        "filename": "asian-languages.html",
        "title": "Asian Languages",
        "icon": "public",
        "category": "Languages Translated",
        "headline": "East & Southeast Asian Languages.",
        "paragraph": "Navigating the complexities of Asian character sets and tonal languages with native precision for high-growth markets.",
        "bullets": [
            "<strong>Major Languages:</strong> Chinese (Simplified/Traditional), Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Tagalog.",
            "<strong>Character Sets:</strong> Perfect handling of Hanzi, Kanji, Kana, and Hangul.",
            "<strong>Cultural Context:</strong> Ensuring appropriate levels of formality and honorifics."
        ]
    },
    {
        "filename": "middle-eastern-languages.html",
        "title": "Middle Eastern Languages",
        "icon": "public",
        "category": "Languages Translated",
        "headline": "Middle Eastern Languages.",
        "paragraph": "Specialized localization for right-to-left (RTL) languages, requiring both linguistic mastery and technical layout expertise.",
        "bullets": [
            "<strong>Major Languages:</strong> Arabic, Hebrew, Persian (Farsi), Turkish, Kurdish.",
            "<strong>RTL Formatting:</strong> Ensuring interfaces and documents flow correctly.",
            "<strong>Regional Variations:</strong> Distinguishing between Gulf, Levantine, and North African Arabic."
        ]
    },
    {
        "filename": "european-languages.html",
        "title": "European Languages",
        "icon": "public",
        "category": "Languages Translated",
        "headline": "European Languages.",
        "paragraph": "Comprehensive coverage of the European Union and broader continent, facilitating seamless cross-border commerce.",
        "bullets": [
            "<strong>Major Languages:</strong> Spanish, French, German, Italian, Portuguese, Dutch, Russian, Polish, Swedish, Greek.",
            "<strong>Regulatory Compliance:</strong> Familiarity with EU directives and terminology.",
            "<strong>Market Localization:</strong> Adapting between variants (e.g., European vs. Latin American Spanish)."
        ]
    },
    {
        "filename": "african-languages.html",
        "title": "African Languages",
        "icon": "public",
        "category": "Languages Translated",
        "headline": "African Languages.",
        "paragraph": "Connecting you with the rapidly emerging markets of Africa through precise translation of widely spoken and regional languages.",
        "bullets": [
            "<strong>Major Languages:</strong> Swahili, Amharic, Zulu, Xhosa, Hausa, Yoruba, Igbo, Afrikaans.",
            "<strong>Local Expertise:</strong> In-country linguists with deep cultural immersion.",
            "<strong>Development & Commerce:</strong> Supporting both NGO and commercial enterprise expansion."
        ]
    }
]

base_dir = "/Users/prachikansal/Desktop/stuff/brain juice/language_localist/"

# Read template
with open(os.path.join(base_dir, "medical-translation.html"), "r") as f:
    template = f.read()

# Extract parts from template to replace
head_match = re.search(r'(<title>).*?(</title>)', template)
icon_match = re.search(r'(<span class="material-symbols-outlined text-\[14px\]">).*?(</span>)', template)
cat_match = re.search(r'</span>(.*?)</div>', template)
h1_match = re.search(r'(<h1 class="font-headline text-5xl lg:text-6xl text-brand-navy mb-6 leading-tight">).*?(</h1>)', template)
p_match = re.search(r'(<p class="font-body text-\[16px\] text-neutral-500 font-light leading-relaxed mb-8 max-w-lg">).*?(</p>)', template, flags=re.DOTALL)
ul_match = re.search(r'(<ul class="space-y-4 font-light text-\[14px\] text-neutral-600">).*?(</ul>)', template, flags=re.DOTALL)

for page in pages:
    content = template
    content = content.replace(head_match.group(0), f'<title>{page["title"]} | Language Localist</title>')
    
    # Very specific targeted replacements to avoid breaking HTML structure
    content = re.sub(r'<span class="material-symbols-outlined text-\[14px\]">.*?</span>', f'<span class="material-symbols-outlined text-[14px]">{page["icon"]}</span>', content)
    
    # Replace category text which comes right after the icon
    content = re.sub(r'(<span class="material-symbols-outlined text-\[14px\]">.*?</span>)[^<]+(</div>)', r'\g<1> ' + page["category"] + r' \g<2>', content)
    
    content = re.sub(r'<h1 class="font-headline text-5xl lg:text-6xl text-brand-navy mb-6 leading-tight">.*?</h1>', f'<h1 class="font-headline text-5xl lg:text-6xl text-brand-navy mb-6 leading-tight">{page["headline"]}</h1>', content)
    
    content = re.sub(r'<p class="font-body text-\[16px\] text-neutral-500 font-light leading-relaxed mb-8 max-w-lg">.*?</p>', f'<p class="font-body text-[16px] text-neutral-500 font-light leading-relaxed mb-8 max-w-lg">\n        {page["paragraph"]}\n      </p>', content, flags=re.DOTALL)
    
    # Rebuild bullets
    bullets_html = '<ul class="space-y-4 font-light text-[14px] text-neutral-600">\n'
    for b in page["bullets"]:
        bullets_html += f'''           <li class="flex items-start gap-3">
             <span class="material-symbols-outlined text-brand-gold text-xl">check_circle</span>
             <span>{b}</span>
           </li>\n'''
    bullets_html += '         </ul>'
    
    content = re.sub(r'<ul class="space-y-4 font-light text-\[14px\] text-neutral-600">.*?</ul>', bullets_html, content, flags=re.DOTALL)
    
    # Replace H3 Title for bullets
    content = re.sub(r'<h3 class="font-headline text-2xl text-brand-navy mb-6">.*?</h3>', f'<h3 class="font-headline text-2xl text-brand-navy mb-6">Why Language Localist?</h3>', content)
    
    with open(os.path.join(base_dir, page["filename"]), "w") as f:
        f.write(content)

print(f"Generated {len(pages)} landing pages successfully.")

# Now, update ALL html files in the directory to link to these new pages in the footer
# We need to replace the Column 1 and Column 2 in the footer across all files.

new_col1 = """      <div>
        <h4 class="font-headline text-brand-gold text-lg mb-6">Translation Services</h4>
        <ul class="space-y-3 font-label text-[13px] text-white/70">
          <li><a href="translation-services.html" class="hover:text-white transition-colors">Translation</a></li>
          <li><a href="multilingual-dtp.html" class="hover:text-white transition-colors">Multilingual DTP</a></li>
          <li><a href="editing-proofreading.html" class="hover:text-white transition-colors">Editing & Proofreading</a></li>
          <li><a href="voice-over.html" class="hover:text-white transition-colors">Voice-Over</a></li>
          <li><a href="transcription-subtitling.html" class="hover:text-white transition-colors">Transcription & Subtitling</a></li>
          <li><a href="website-development.html" class="hover:text-white transition-colors">Website Development</a></li>
        </ul>
      </div>"""

new_col2 = """      <div>
        <h4 class="font-headline text-brand-gold text-lg mb-6">Languages Translated</h4>
        <ul class="space-y-3 font-label text-[13px] text-white/70">
          <li><a href="indian-languages.html" class="hover:text-white transition-colors">Indian Languages</a></li>
          <li><a href="asian-languages.html" class="hover:text-white transition-colors">Asian Languages</a></li>
          <li><a href="middle-eastern-languages.html" class="hover:text-white transition-colors">Middle Eastern Languages</a></li>
          <li><a href="european-languages.html" class="hover:text-white transition-colors">European Languages</a></li>
          <li><a href="african-languages.html" class="hover:text-white transition-colors">African Languages</a></li>
        </ul>
      </div>"""

all_html_files = glob.glob(os.path.join(base_dir, "*.html"))

for file_path in all_html_files:
    with open(file_path, "r") as f:
        html = f.read()
        
    # Replace Col 1
    html = re.sub(r'<div>\s*<h4 class="font-headline text-brand-gold text-lg mb-6">Translation Services</h4>\s*<ul class="space-y-3 font-label text-\[13px\] text-white/70">.*?</ul>\s*</div>', new_col1, html, flags=re.DOTALL)
    
    # Replace Col 2
    html = re.sub(r'<div>\s*<h4 class="font-headline text-brand-gold text-lg mb-6">Languages Translated</h4>\s*<ul class="space-y-3 font-label text-\[13px\] text-white/70">.*?</ul>\s*</div>', new_col2, html, flags=re.DOTALL)
    
    # Ensure current page in the footer is highlighted (text-brand-gold)
    basename = os.path.basename(file_path)
    # Highlight logic: find the href for this page and add text-brand-gold
    # First, strip existing highlights from the columns in this specific file
    html = re.sub(r'class="text-brand-gold hover:text-white transition-colors"', 'class="hover:text-white transition-colors"', html)
    # Then add it back for the current file
    html = html.replace(f'href="{basename}" class="hover:text-white transition-colors"', f'href="{basename}" class="text-brand-gold hover:text-white transition-colors"')
    
    with open(file_path, "w") as f:
        f.write(html)

print(f"Updated footers in {len(all_html_files)} files.")
