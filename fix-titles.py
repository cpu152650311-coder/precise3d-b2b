#!/usr/bin/env python3
"""title 截短到 ≤70 字符:去品牌后缀,超长按单词边界截断"""
import re, glob, html as html_mod

def truncate_title(title, max_len=70):
    """截断到max_len,尽量在单词边界"""
    if len(title) <= max_len:
        return title
    # 在max_len-3处找单词边界
    cut = title[:max_len-1]
    # 找最后一个空格
    sp = cut.rfind(' ')
    if sp > max_len * 0.6:  # 边界不要太靠前
        return cut[:sp].rstrip(',;:') + '…'
    return cut.rstrip() + '…'

changed = 0
for f in glob.glob('blog/*.html'):
    if 'blog-page' in f: continue
    html = open(f, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', html, re.S)
    if not m: continue
    title = m.group(1).strip()
    if len(title) <= 70:
        continue
    # 去品牌后缀
    base = re.sub(r'\s*[—|]\s*(Precise3D( Blog)?)\s*$', '', title)
    # 如果base还是太长,用og:title? 先看og:title
    og = re.search(r'property="og:title" content="([^"]*)"', html)
    if og and len(og.group(1)) < len(base):
        base = og.group(1).strip()
    # 清理多余空格
    base = re.sub(r'\s+', ' ', base).strip()
    new_title = truncate_title(base)
    # 加回简短品牌(若空间允许)
    if len(new_title) + 12 <= 70:
        new_title = f"{new_title} | Precise3D"
    html = html.replace(m.group(0), f'<title>{new_title}</title>', 1)
    open(f, 'w', encoding='utf-8').write(html)
    changed += 1

print(f"修改title: {changed} 篇")
# 验证
over = 0
for f in glob.glob('blog/*.html'):
    if 'blog-page' in f: continue
    t = re.search(r'<title>(.*?)</title>', open(f, encoding='utf-8').read())
    if t and len(t.group(1)) > 70:
        over += 1
        if over <= 5: print(f"  ❌ 仍超: {len(t.group(1))}字 {t.group(1)[:80]}")
print(f"剩余超长title: {over}")
