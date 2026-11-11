import re

with open("D:/PORTFOLIO_NEO_BRUTALISM/scripts/build_english_financial_portal.py", "r", encoding="utf-8") as f:
    text = f.read()

# Add image_url to HTML_TEMPLATE in article
# Find <p class="lead-summary">{summary}</p> and add image below it
text = text.replace(
    '<p class="lead-summary">{summary}</p>\n    </article>',
    '<p class="lead-summary">{summary}</p>\n      <div style="margin-top:20px;border:1px solid var(--border);overflow:hidden;background:#050505;"><img src="{image_url}" alt="{title}" style="width:100%;height:380px;object-fit:cover;display:block;" loading="lazy"></div>\n    </article>'
)

# In article generation call, add image_url=art.get("image_url", "...")
text = text.replace(
    'reading_time=art["reading_time"],\n            body_html=body_html\n        )',
    'reading_time=art["reading_time"],\n            image_url=art.get("image_url", "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80"),\n            body_html=body_html\n        )'
)

# In homepage featured card, add image
text = text.replace(
    '<p class="featured-summary">{lead_art[\'summary\']}</p>',
    '<div style="margin:12px 0;border:1px solid var(--border);overflow:hidden;max-height:340px;"><img src="{lead_art.get(\'image_url\', \'https://images.unsplash.com/photo-1610375461246-83df859d849d?auto=format&fit=crop&w=1200&q=80\')}" alt="{lead_art[\'title\']}" style="width:100%;height:340px;object-fit:cover;display:block;" loading="lazy"></div>\n        <p class="featured-summary">{lead_art[\'summary\']}</p>'
)

# In homepage news-card grid, add card image
text = text.replace(
    '<article class="news-card">\n      <div class="card-meta">',
    '<article class="news-card">\n      <div style="margin:-24px -24px 16px -24px;overflow:hidden;height:160px;border-bottom:1px solid var(--border);"><img src="{a.get(\'image_url\', \'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80\')}" alt="{a[\'title\']}" style="width:100%;height:100%;object-fit:cover;display:block;" loading="lazy"></div>\n      <div class="card-meta">'
)

with open("D:/PORTFOLIO_NEO_BRUTALISM/scripts/build_english_financial_portal.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Injected images into templates.")
