#!/usr/bin/env python3
"""Generate blog images for heated chamber article — Precise3D ems-3dp.com"""
import os, base64, time, subprocess, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
OUT = "/home/ubuntu/projects/precise3d-b2b/generated"
os.makedirs(OUT, exist_ok=True)

images = [
    {
        "path": f"{OUT}/blog-cover-heated-chamber.webp",
        "prompt": (
            "Enclosed 3D printer with transparent acrylic panels and visible heated chamber interior "
            "glowing warm orange, dark navy (#0B1120) studio background with electric blue rim lighting "
            "on printer edges, engineering precision aesthetic, macro detail showing temperature display "
            "reading 65C on printer screen, cool industrial studio lighting, photorealistic product photography, "
            "no people faces, no text, no logos, no brands, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-heated-chamber-active.webp",
        "prompt": (
            "Extreme macro close-up of PTC ceramic heater element with warm red-orange glow inside 3D printer chamber, "
            "thermistor wire and metal mounting bracket visible, dark navy background, electric blue LED accent "
            "glow reflecting off metal components, printed ASA part on build plate in foreground with smooth "
            "surface finish, precision engineering shot, shallow depth of field, photorealistic industrial macro photography, "
            "no people faces, no text, no logos, no brands, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-heated-chamber-filament.webp",
        "prompt": (
            "Assortment of engineering-grade 3D printer filament spools arranged on dark industrial surface, "
            "black ABS spool, gray ASA spool, clear PC spool, white Nylon spool, enclosed 3D printer with "
            "glowing heated chamber visible in background, dark navy tones with electric blue accent highlights "
            "on printer edges, cool studio lighting, dramatic product photography for industrial catalog, "
            "no people faces, no text, no logos, no brands, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-heated-chamber-comparison.webp",
        "prompt": (
            "Side-by-side display of enclosed 3D printer with digital temperature controller showing 65C "
            "next to open-frame CoreXY 3D printer on dark reflective surface, engineering filament spools "
            "and calibration print parts between them, dark navy environment with electric blue accent "
            "lighting, industrial workshop setting, professional product comparison shot, "
            "no people faces, no text, no logos, no brands, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-heated-chamber-cta.webp",
        "prompt": (
            "Modern 3D printer showroom with multiple enclosed printers of varying sizes on illuminated "
            "dark display podiums, engineering filament spools on metal shelving in background, warm orange "
            "glow from heated chambers contrasting with dark navy room tones, electric blue accent strip "
            "lighting along display edges, professional industrial aesthetic, wide angle shot, "
            "no people faces, no text, no logos, no brands, no arrows, no diagrams, no charts"
        )
    },
]

for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating {os.path.basename(img['path'])}...")
    try:
        resp = client.images.generate(
            model="gpt-image-2", prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        raw_path = img["path"].replace(".webp", "_raw.webp")
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        raw_kb = os.path.getsize(raw_path) / 1024

        # Compress with cwebp
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", img["path"]],
            check=True, capture_output=True, timeout=30
        )
        os.remove(raw_path)
        final_kb = os.path.getsize(img["path"]) / 1024
        print(f"  -> OK: {raw_kb:.0f}KB raw -> {final_kb:.0f}KB compressed ({img['path']})")
    except Exception as e:
        print(f"  -> FAILED: {e}")
    if i < len(images) - 1:
        time.sleep(2)

print("\n=== Result ===")
for img in images:
    if os.path.exists(img["path"]):
        kb = os.path.getsize(img["path"]) / 1024
        print(f"  {os.path.basename(img['path'])}: {kb:.0f} KB")
    else:
        print(f"  {os.path.basename(img['path'])}: MISSING")
