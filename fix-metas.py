#!/usr/bin/env python3
"""meta description 截短到 ≤230 字符(单词边界截断)"""
import re, glob

def truncate_desc(desc, max_len=225):
    desc = desc.strip()
    if len(desc) <= max_len:
        return desc
    cut = desc[:max_len-1]
    sp = cut.rfind(' ')
    if sp > max_len * 0.6:
        return cut[:sp].rstrip(',;:.') + '…'
    return cut.rstrip() + '…'

changed = 0
for f in glob.glob('blog/*.html'):
    if 'blog-page' in f: continue
    html = open(f, encoding='utf-8').read()
    m = re.search(r'name="description" content="([^"]*)"', html)
    if not m: continue
    if len(m.group(1)) <= 230: continue
    new_desc = truncate_desc(m.group(1))
    html = html.replace(f'name="description" content="{m.group(1)}"',
                        f'name="description" content="{new_desc}"', 1)
    open(f, 'w', encoding='utf-8').write(html)
    changed += 1

print(f"修改meta: {changed} 篇")
# 验证
over = 0
for f in glob.glob('blog/*.html'):
    if 'blog-page' in f: continue
    m = re.search(r'name="description" content="([^"]*)"', open(f, encoding='utf-8').read())
    if m and len(m.group(1)) > 230:
        over += 1
        if over <= 5: print(f"  ❌ 仍超: {len(m.group(1))}字")
print(f"剩余超长meta: {over}")
