#!/usr/bin/env python3
"""Generate blog images for 3D Printer Safety Features article — Precise3D (ems-3dp.com)"""
import base64, os, subprocess, time
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AIHUBMIX_API_KEY"],
    base_url="https://aihubmix.com/v1",
    timeout=600
)

OUT = "/home/ubuntu/projects/precise3d-b2b/generated"
BRAND = "deep navy (#0B1120) background with electric blue (#2563EB) accent highlights, cool teal (#06B6D4) secondary accents, tech-forward aesthetic, neutral studio lighting, no people faces, no text, no logos, no brands"

IMAGES = [
    {
        "id": "cover-safety-features",
        "prompt": (
            f"Professional product photography of a modern enclosed 3D printer in a dark studio environment, "
            f"the printer's chamber illuminated by electric blue LED glow, a thermal imaging effect overlay on the hotend area showing heat distribution in orange/red, "
            f"the printer on a clean desk surface, dramatic rim lighting emphasizing the safety-focused engineering, "
            f"no people, no text, no brand logos, {BRAND}"
        )
    },
    {
        "id": "diagram-safety-1",
        "prompt": (
            f"Extreme macro close-up photograph of a 3D printer hotend assembly, "
            f"a glass bead thermistor visible pressed against the aluminum heater block, the thin thermistor wires clearly shown, "
            f"the heater cartridge also visible beside it, precision engineering detail shot with shallow depth of field, "
            f"metallic surfaces reflecting cool blue light, industrial inspection photography style, "
            f"no people, no text, no brand logos, {BRAND}"
        )
    },
    {
        "id": "diagram-safety-2",
        "prompt": (
            f"Side-by-side comparison on an electronics workbench: a Mean Well LRS-350-24 certified power supply unit on the left with visible CE and UL certification markings, "
            f"and a generic unbranded silver PSU on the right, the contrast highlighting the quality gap between certified and uncertified components, "
            f"3D printer electronics context visible in background, industrial safety testing environment, "
            f"no people, no text on products, no brand logos except certification marks, {BRAND}"
        )
    },
    {
        "id": "scene-safety-edu",
        "prompt": (
            f"A clean modern classroom or makerspace with multiple enclosed 3D printers on a long workbench, "
            f"each printer actively printing with filament visible, the room well-lit with natural light from windows, "
            f"organized safety signage context implied by the professional workspace layout, educational institution setting, "
            f"prints on the build plates visible mid-print, showing real classroom use of 3D printing technology, "
            f"no people faces visible, no text, no brand logos, {BRAND}"
        )
    },
    {
        "id": "cta-safety",
        "prompt": (
            f"Abstract technology atmosphere background: a darkened industrial workspace with subtle electric blue light trails suggesting precision engineering, "
            f"a 3D printer silhouette visible in the background, the focus on the ambient lighting and mood rather than the equipment detail, "
            f"deep navy darkness with cyan-teal accent glow, designed for text overlay, "
            f"clean minimal composition with 60% dark negative space in the center-right area, "
            f"no people, no text, no brand logos, {BRAND}"
        )
    },
]

print(f"Generating {len(IMAGES)} images for blog-safety-features...")
for i, img in enumerate(IMAGES):
    start = time.time()
    print(f"[{i+1}/{len(IMAGES)}] {img['id']}...", end=" ", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        raw_path = f"{OUT}/blog-{img['id']}-raw.webp"
        final_path = f"{OUT}/blog-{img['id']}.webp"
        with open(raw_path, "wb") as f:
            f.write(base64.b64decode(b64))
        # Compress with subprocess cwebp (check=True avoids silent file loss)
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            check=True, capture_output=True
        )
        os.remove(raw_path)
        elapsed = time.time() - start
        size_kb = os.path.getsize(final_path) / 1024
        print(f"OK ({elapsed:.0f}s, {size_kb:.0f}KB)")
    except Exception as e:
        print(f"FAILED: {e}")
    time.sleep(1.5)

print("\nDone. Verifying:")
for img in IMAGES:
    fp = f"{OUT}/blog-{img['id']}.webp"
    if os.path.exists(fp):
        print(f"  ✓ {fp} ({os.path.getsize(fp)/1024:.0f}KB)")
    else:
        print(f"  ✗ {fp} MISSING")
