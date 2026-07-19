#!/usr/bin/env python3
"""Generate blog images for filament drying article on ems-3dp.com"""
import base64, time, subprocess, os, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

IMAGES = [
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-cover-filament-drying.webp",
        "prompt": "close-up of 3D printer filament spools inside a sealed dry storage box with digital humidity display showing 15%, silica gel orange beads visible through transparent lid, PLA and PETG spools in dark navy (#0B1120) environment with electric blue (#2563EB) accent lighting, professional studio shot, industrial aesthetic, tech-forward, no people faces, no text, no logos, no brands, no arrows, no charts, no infographics"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-filament-drying-1.webp",
        "prompt": "photorealistic macro close-up of two 3D printer filament strands side by side on dark surface — left strand dry and glossy with smooth surface, right strand moisture-damaged showing surface bubbles and micro-cracks, 3D printer nozzle visible in soft background bokeh, engineering lab setting, deep navy (#0B1120) background with electric blue (#2563EB) accent, cool teal (#06B6D4) secondary highlights, no people faces, no text, no logos, no charts, no infographics"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-filament-drying-2.webp",
        "prompt": "assortment of vacuum-sealed 3D printer filament storage bags with reusable desiccant packets and blue moisture indicator cards showing dry status, organized on industrial warehouse shelving, multiple spool colors visible through clear bags, professional industrial lighting, deep navy (#0B1120) background, electric blue (#2563EB) accent, cool teal (#06B6D4) highlights, no people faces, no text, no logos, no brands, no charts, no infographics"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-filament-drying-3.webp",
        "prompt": "3D printer filament dryer unit with transparent lid on workbench, spool visible inside rotating slowly, digital temperature display showing 50 degrees Celsius, slight condensation forming on lid interior, PTFE tube extending from dryer to nearby 3D printer extruder, industrial workshop setting, studio lighting, deep navy (#0B1120) background with electric blue (#2563EB) accent highlights, tech-forward aesthetic, no people faces, no text, no logos, no brands, no charts, no infographics"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-cta-filament-drying.webp",
        "prompt": "rows of 3D printer filament spools on industrial shelving in climate-controlled warehouse, organized by material type and color gradient, professional lighting, clean organized environment, deep navy (#0B1120) background with electric blue (#2563EB) accent, tech-forward industrial aesthetic, wide angle establishing shot, no people faces, no text, no logos, no brands, no charts, no infographics"
    },
]

generated = 0
failed = []

for img in IMAGES:
    fname = os.path.basename(img["path"])
    print(f"[{generated+1}/{len(IMAGES)}] Generating {fname}...", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low"
        )
        b64 = resp.data[0].b64_json
        raw_path = img["path"] + ".raw"
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))

        # Compress immediately with cwebp
        result = subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", img["path"]],
            capture_output=True, text=True, check=True
        )
        os.remove(raw_path)
        
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  ✓ {fname} — {size_kb:.0f} KB", flush=True)
        generated += 1
        time.sleep(2)
    except Exception as e:
        print(f"  ✗ {fname} FAILED: {e}", flush=True)
        failed.append(fname)
        # Try to clean up raw file
        raw_path = img["path"] + ".raw"
        if os.path.exists(raw_path):
            os.remove(raw_path)

print(f"\nDone. Generated: {generated}/{len(IMAGES)}")
if failed:
    print(f"Failed: {', '.join(failed)}")
    sys.exit(1)
