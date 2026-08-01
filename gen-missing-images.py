#!/usr/bin/env python3
"""补生成14张缺失的博客配图(ems-3dp.com), alt文本作为prompt"""
import os, re, base64, time, glob
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

STYLE = ("Professional B2B photography, photorealistic, high detail, "
         "warm industrial lighting, shallow depth of field, no text overlay, no watermark, no charts, no diagrams")

# (文件名, alt描述)
TARGETS = {
    "blog-diagram-abl-3.webp": "3D printer build plate being scanned by probe, close-up detail of probe tip traveling across heated bed surface, precision auto bed leveling process",
    "blog-diagram-rfq-1.webp": "Professional B2B proposal document on modern office desk, 3D printer specifications and pricing table visible, pen and calculator nearby",
    "blog-diagram-rfq-2.webp": "Modern corporate meeting room with large screen displaying 3D printer specifications, buyers and suppliers discussing RFQ",
    "blog-diagram-sales-4.webp": "Professional sample kit display case with 12 different 3D printed parts organized in foam inserts, sales demo showcase",
    "blog-diagram-brand-landscape-3.webp": "Pallet of boxed 3D printers in a distribution warehouse, shipping labels and barcodes on cartons, brand comparison context",
    "blog-diagram-inventory-1.webp": "Well-organized 3D printer distributor warehouse with shelved printer boxes, filament spools and accessories in neat rows",
    "blog-diagram-inventory-2.webp": "Warehouse worker with tablet scanning barcode on 3D printer box, pallet racking in background, inventory management",
    "blog-diagram-ecommerce-3.webp": "Smartphone displaying 3D printer product listing on mobile e-commerce app with shopping cart icon, online marketplace",
    "blog-diagram-import-1.webp": "Shipping container being loaded with pallets of 3D printer boxes at Chinese port, customs import logistics",
    "blog-diagram-import-2.webp": "Close-up of customs declaration form on clipboard with HS code highlighted, import tariff documents on desk",
    "blog-diagram-software-4.webp": "3D printer connected to Raspberry Pi with OctoPrint interface visible on tablet, print farm software monitoring",
    "blog-diagram-tco-4.webp": "Professional distributor workspace with dual monitors displaying TCO spreadsheet and ROI calculator, financial analysis",
    "blog-diagram-injmold-3.webp": "3D printed injection mold insert on inspection bench alongside molded plastic parts, hybrid manufacturing comparison",
    "blog-diagram-private-label-3.webp": "Premium unboxing experience of a 3D printer, retail packaging box opened with custom brand label, white label product",
}

os.makedirs("generated", exist_ok=True)
for fname, alt in TARGETS.items():
    path = f"generated/{fname}"
    if os.path.exists(path):
        print(f"跳过(已存在): {fname}")
        continue
    prompt = f"{alt}. {STYLE}"
    try:
        resp = client.images.generate(model="gpt-image-2", prompt=prompt, n=1, size="1024x1024", quality="low")
        raw = base64.b64decode(resp.data[0].b64_json)
        with open(path, "wb") as f:
            f.write(raw)
        # 压缩
        os.system(f'cwebp -q 75 "{path}" -o "{path}.tmp" 2>/dev/null && mv "{path}.tmp" "{path}"')
        size = os.path.getsize(path) // 1024
        print(f"✅ {fname} ({size}KB)")
    except Exception as e:
        print(f"❌ {fname}: {str(e)[:120]}")
    time.sleep(1.2)

print("\n完成。验证:")
for fname in TARGETS:
    print(f"  {'✅' if os.path.exists('generated/'+fname) else '❌'} {fname}")
