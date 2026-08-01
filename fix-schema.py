#!/usr/bin/env python3
"""为38篇无Schema文章插入 JSON-LD BlogPosting"""
import re, glob, os, json

sm = open('sitemap.xml', encoding='utf-8').read()
lastmods = {}
for m in re.finditer(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', sm):
    lastmods[m.group(1).rstrip('/').split('/')[-1]] = m.group(2)

no_schema = []
for f in glob.glob('blog/*.html'):
    if 'blog-page' in f: continue
    html = open(f, encoding='utf-8').read()
    if '"@type"' not in html:
        no_schema.append(f)

def esc(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').strip()

done = 0
for f in no_schema:
    html = open(f, encoding='utf-8').read()
    slug = os.path.basename(f).replace('.html', '')
    # 提取数据
    og_title = re.search(r'property="og:title" content="([^"]*)"', html)
    og_desc = re.search(r'property="og:description" content="([^"]*)"', html)
    meta_desc = re.search(r'name="description" content="([^"]*)"', html)
    headline = og_title.group(1) if og_title else ''
    description = (og_desc or meta_desc)
    description = description.group(1) if description else ''
    if not headline:
        t = re.search(r'<title>([^<]+)</title>', html)
        headline = t.group(1).replace(' — Precise3D Blog', '').strip() if t else slug
    date = lastmods.get(slug, '2026-08-01')

    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": description[:200],
        "datePublished": date,
        "dateModified": date,
        "author": {"@type": "Organization", "name": "Precise3D"},
        "publisher": {"@type": "Organization", "name": "Precise3D", "url": "https://ems-3dp.com"}
    }
    ld = '<script type="application/ld+json">\n' + json.dumps(schema, indent=2, ensure_ascii=False) + '\n</script>'
    # 在 </head> 前插入
    if '</head>' in html and '<script type="application/ld+json">' not in html:
        html = html.replace('</head>', ld + '\n</head>', 1)
        open(f, 'w', encoding='utf-8').write(html)
        done += 1
    else:
        print(f"跳过: {f}")

print(f"插入Schema: {done}/{len(no_schema)}")

# 验证
remain = 0
for f in glob.glob('blog/*.html'):
    if 'blog-page' in f: continue
    if '"@type"' not in open(f, encoding='utf-8').read():
        remain += 1
print(f"剩余无Schema: {remain}")
