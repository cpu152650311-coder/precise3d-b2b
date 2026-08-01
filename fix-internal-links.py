#!/usr/bin/env python3
"""为13篇内链不足的文章插入自然锚文本内链"""
import re, os, json

LINKS = {
 '10-questions-oem-partner-3d-printer': [
   ('private-label-3d-printer-brand-oem-sourcing-guide-distributor', 'private label sourcing'),
   ('3d-printer-oem-pricing-negotiation-chinese-factories-distributor-guide', 'OEM pricing negotiation'),
   ('3d-printer-moq-payment-terms-china-oem-negotiation-distributor-guide', 'MOQ and payment terms'),
   ('3d-printer-oem-production-line-factory-tour-distributor-guide', 'factory tour guide'),
   ('3d-printer-certification-compliance-distributor-guide', 'certification compliance'),
   ('3d-printer-factory-audit-qc-checklist-distributor-guide', 'factory audit checklist'),
 ],
 '3d-printer-maintenance-distributor-guide': [
   ('3d-printer-maintenance-plans-extended-warranty-distributor-guide', 'maintenance plans and warranties'),
   ('3d-printer-after-sales-support-distributor-strategy', 'after-sales support'),
   ('3d-printer-nozzle-hotend-technology-distributor-guide', 'nozzle and hotend technology'),
   ('3d-printer-bed-adhesion-consumables-distributor-guide', 'bed adhesion'),
   ('3d-printer-customer-training-onboarding-distributor-guide', 'customer training'),
   ('filament-drying-storage-guide-distributor-2026', 'filament drying and storage'),
 ],
 'ai-slicers-changing-consumer-3d-printing': [
   ('multi-color-consumer-3d-printing-2026', 'multi-color printing'),
   ('3d-printer-software-ecosystem-slicers-farm-management-distributor-guide', 'slicer software ecosystem'),
   ('marlin-vs-klipper-vs-reprap-firmware-distributor-guide', 'firmware comparison'),
   ('3d-printer-remote-monitoring-cloud-connectivity-distributor-guide', 'remote monitoring'),
   ('multi-material-3d-printing-ams-cfs-mmu-distributor-guide', 'multi-material printing'),
 ],
 'engineering-filaments-distributor-guide': [
   ('polycarbonate-pc-filament-3d-printer-distributor-guide', 'polycarbonate filament'),
   ('nylon-pa-filament-3d-printing-distributor-guide', 'nylon filament'),
   ('carbon-fiber-filled-filaments-3d-printing-distributor-guide', 'carbon fiber filaments'),
   ('pla-petg-abs-tpu-filament-stocking-guide-distributor-2026', 'filament stocking guide'),
   ('flexible-filaments-tpu-tpe-tpc-distributor-guide', 'flexible filaments'),
   ('filament-drying-storage-guide-distributor-2026', 'filament drying'),
 ],
 'fdm-vs-resin-2026': [
   ('resin-3d-printer-distribution-guide-2026', 'resin printer distribution'),
   ('sla-vs-dlp-vs-msla-resin-3d-printer-technology-distributor-guide', 'SLA vs DLP vs MSLA'),
   ('engineering-filaments-distributor-guide', 'engineering filaments'),
   ('water-washable-vs-standard-resin-margin-comparison-distributor-guide', 'water-washable resin'),
   ('resin-3d-printer-troubleshooting-common-failures-distributor-guide', 'resin troubleshooting'),
 ],
 'multi-color-consumer-3d-printing-2026': [
   ('multi-material-3d-printing-ams-cfs-mmu-distributor-guide', 'AMS/CFS/MMU multi-material systems'),
   ('idex-dual-extrusion-3d-printers-distributor-guide', 'IDEX dual extrusion'),
   ('ai-slicers-changing-consumer-3d-printing', 'AI slicers'),
   ('3d-printer-software-ecosystem-slicers-farm-management-distributor-guide', 'slicer software'),
   ('3d-printing-consumer-electronics-distributor-guide', 'consumer electronics'),
 ],
 'print-farm-economics-2026': [
   ('print-farm-operations-scale-distributor-guide', 'scaling print farm operations'),
   ('3d-printer-software-ecosystem-slicers-farm-management-distributor-guide', 'farm management software'),
   ('3d-printer-remote-monitoring-cloud-connectivity-distributor-guide', 'remote monitoring'),
   ('3d-printer-energy-consumption-operating-cost-distributor-guide', 'energy and operating costs'),
   ('3d-printer-tco-roi-calculator-distributor-guide', 'TCO/ROI calculator'),
 ],
 '3d-print-annealing-heat-treatment-distributor-guide': [
   ('polycarbonate-pc-filament-3d-printer-distributor-guide', 'polycarbonate filament'),
   ('3d-printer-post-processing-finishing-distributor-guide', 'post-processing'),
   ('3d-printer-heated-chamber-distributor-guide', 'heated chambers'),
   ('3d-printer-enclosure-temperature-control-distributor-guide', 'enclosure temperature control'),
   ('engineering-filaments-distributor-guide', 'engineering filaments'),
 ],
 '3d-printer-accessories-revenue-multiplier-distributor-guide': [
   ('3d-printer-consumables-accessories-bundling-strategy-distributor', 'consumables bundling'),
   ('3d-printer-upgrades-aftermarket-revenue-distributor-guide', 'aftermarket upgrades'),
   ('multi-material-3d-printing-ams-cfs-mmu-distributor-guide', 'multi-material accessories'),
   ('3d-scanner-3d-printer-bundle-strategy-distributor-guide', '3D scanner bundles'),
   ('filament-drying-storage-guide-distributor-2026', 'filament storage accessories'),
 ],
 '3d-printer-certification-compliance-distributor-guide': [
   ('3d-printer-import-china-hs-codes-tariffs-customs-guide', 'import tariffs and HS codes'),
   ('food-safe-3d-printing-distributor-regulatory-guide', 'food-safe regulations'),
   ('3d-printer-fume-extraction-filtration-distributor-guide', 'fume extraction compliance'),
   ('shipping-3d-printers-from-china-logistics-guide', 'shipping from China'),
   ('3d-printer-factory-audit-qc-checklist-distributor-guide', 'factory QC audit'),
 ],
 '3d-printer-trade-show-strategy-distributor-guide': [
   ('3d-printer-distributor-digital-marketing-strategy-guide', 'digital marketing'),
   ('3d-printer-demo-lab-setup-distributor-guide', 'demo lab setup'),
   ('3d-printer-b2b-rfq-proposal-playbook-distributor-guide', 'B2B proposal playbook'),
   ('3d-printer-b2b-sales-demo-playbook-distributor-guide', 'B2B sales demo'),
   ('3d-printer-customer-training-onboarding-distributor-guide', 'customer onboarding'),
 ],
 'resin-3d-printer-distribution-guide-2026': [
   ('fdm-vs-resin-2026', 'FDM vs resin'),
   ('sla-vs-dlp-vs-msla-resin-3d-printer-technology-distributor-guide', 'SLA vs DLP vs MSLA'),
   ('water-washable-vs-standard-resin-margin-comparison-distributor-guide', 'water-washable resin margins'),
   ('resin-3d-printer-troubleshooting-common-failures-distributor-guide', 'resin troubleshooting'),
   ('3d-printer-resin-types-selection-distributor-guide', 'resin types'),
 ],
 'shipping-3d-printers-from-china-logistics-guide': [
   ('3d-printer-crating-packaging-international-shipping-distributor-guide', 'crating and packaging'),
   ('3d-printer-import-china-hs-codes-tariffs-customs-guide', 'import tariffs and HS codes'),
   ('3d-printer-certification-compliance-distributor-guide', 'certification compliance'),
   ('3d-printer-distributor-inventory-management-sku-planning-guide', 'inventory planning'),
   ('3d-printer-distributor-cash-flow-management-guide', 'cash flow management'),
 ],
}

def insert_links(html, links):
    """在正文段落末尾的自然句子后插入链接"""
    added = 0
    used_anchors = []
    for slug, anchor in links:
        if added >= 5:
            break
        # 找到正文中还没被插入过的 <p> 段落(排除含链接的)
        paras = list(re.finditer(r'<p>(.*?)</p>', html, re.S))
        # 从长段落开始找(有足够上下文)
        for m in reversed(paras):
            p_text = m.group(1)
            plain = re.sub(r'<[^>]+>', '', p_text)
            if len(plain) < 200:
                continue
            if '/blog/' in p_text:
                continue
            # 在段落末尾句号前插入
            insert_at = p_text.rfind('</')  # 找最后一个闭合标签前
            if insert_at < 0:
                continue
            # 在段落文本末尾加一句带链接的话
            sentence = f' For distributors evaluating this area, our <a href="/blog/{slug}.html">{anchor}</a> guide covers it in depth.'
            new_p = p_text[:insert_at] + sentence + p_text[insert_at:]
            html = html.replace(m.group(0), f'<p>{new_p}</p>', 1)
            added += 1
            used_anchors.append((slug, anchor))
            break
    return html, added, used_anchors

results = []
for target, links in LINKS.items():
    path = f'blog/{target}.html'
    html = open(path, encoding='utf-8').read()
    new_html, added, used = insert_links(html, links)
    open(path, 'w', encoding='utf-8').write(new_html)
    results.append((target, added, len(used)))
    print(f"{target}: 插入{added}条")

# 验证
print("\n=== 验证 ===")
for target, added, _ in results:
    html = open(f'blog/{target}.html', encoding='utf-8').read()
    internal = set(re.findall(r'href="(/blog/[^"]+?)(?:\.html)?"', html))
    internal.discard(f'/blog/{target}')
    print(f"{'✅' if len(internal) >= 5 else '❌'} {target}: {len(internal)}条唯一内链")
