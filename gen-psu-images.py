#!/usr/bin/env python3
"""Generate blog images for PSU quality article using GPT Image 2 (AIHUBMIX)."""
import base64, os, subprocess, sys, time
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AIHUBMIX_API_KEY"],
    base_url="https://aihubmix.com/v1"
)

OUT_DIR = "/home/ubuntu/projects/precise3d-b2b/generated"
os.makedirs(OUT_DIR, exist_ok=True)

# Precise3D brand: deep navy (#0B1120) background, electric blue (#2563EB) accent, cool teal (#06B6D4)
BRAND = "deep navy (#0B1120) background, electric blue (#2563EB) accent highlights, cool teal (#06B6D4) secondary accents, tech-forward aesthetic, neutral studio lighting or industrial workspace"

IMAGES = [
    {
        "id": "blog-cover-psu-quality",
        "prompt": f"Close-up macro shot of a certified Mean Well LRS-350-24 switching power supply on a dark technical workbench inside a 3D printer, visible UL/CE certification labels on the aluminum case, green LED indicator glowing, screw terminals with thick wires connected, professional electronics engineering photography, {BRAND}, no people faces, no text, no logos"
    },
    {
        "id": "blog-diagram-psu-1",
        "prompt": f"Interior view of an open 3D printer electronics enclosure showing the power supply unit with visible capacitor banks and transformer, blue LED indicator lit, cooling fan visible, ribbon cables connecting to the 3D printer mainboard, professional industrial photography, {BRAND}, no people faces, no text, no logos"
    },
    {
        "id": "blog-diagram-psu-2",
        "prompt": f"Side-by-side comparison on an anti-static electronics workbench: authentic Mean Well LRS-350 power supply with dense certification label on the left, generic no-name silver PSU with sparse markings on the right, visible quality difference in case finish and terminal block construction, 3D printer parts in background, macro product comparison shot, {BRAND}, no people faces, no text, no logos"
    },
    {
        "id": "blog-diagram-psu-3",
        "prompt": f"Factory quality control testing station: Mean Well PSU connected to an electronic load tester and multimeter on a workbench, thermal imaging camera display showing heat distribution across the PSU enclosure during full-load burn-in testing, cables and probes visible, industrial electronics lab setting with 3D printer visible in background, {BRAND}, no people faces, no text, no logos"
    },
]

print(f"Generating {len(IMAGES)} images...")
for i, img in enumerate(IMAGES, 1):
    raw_path = os.path.join(OUT_DIR, f"{img['id']}_raw.webp")
    final_path = os.path.join(OUT_DIR, f"{img['id']}.webp")
    
    print(f"[{i}/{len(IMAGES)}] {img['id']}...", end=" ", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        
        # Compress with cwebp
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            check=True, capture_output=True
        )
        os.remove(raw_path)
        size_kb = os.path.getsize(final_path) / 1024
        print(f"OK ({size_kb:.0f}KB)")
    except Exception as e:
        print(f"FAILED: {e}")
    
    if i < len(IMAGES):
        time.sleep(1.5)

# Verify
print("\nVerification:")
for img in IMAGES:
    p = os.path.join(OUT_DIR, f"{img['id']}.webp")
    if os.path.exists(p):
        print(f"  ✅ {img['id']}.webp ({os.path.getsize(p)/1024:.0f}KB)")
    else:
        print(f"  ❌ {img['id']}.webp MISSING")
