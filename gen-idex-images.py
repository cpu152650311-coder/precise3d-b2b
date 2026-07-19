#!/usr/bin/env python3
"""Generate IDEX dual extrusion blog images — ems-3dp.com"""
import os, base64, time, subprocess, sys
from openai import OpenAI

API_KEY = os.environ["AIHUBMIX_API_KEY"]
client = OpenAI(api_key=API_KEY, base_url="https://aihubmix.com/v1")
OUT = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{OUT}/blog-cover-idex-dual-extrusion.webp",
        "prompt": "Professional corporate marketing photo of an IDEX 3D printer with two independent toolheads visible on linear rail, both hotends active, printing a complex multi-material part on build plate, dark navy (#0B1120) background with electric blue (#2563EB) accent LED lighting, precision engineering aesthetic, cool teal secondary accents (#06B6D4), tech-forward industrial workspace, no brands, no logos, no text, no people faces"
    },
    {
        "path": f"{OUT}/blog-diagram-idex-1.webp",
        "prompt": "Extreme macro close-up photograph of an IDEX 3D printer dual toolhead mechanism, two independent hotends with nozzles mounted on linear rail, precision alignment between nozzles visible, metallic copper heat blocks and brass nozzles, focus on the mechanical gap between the two toolheads, studio lighting on dark navy background, no brands, no logos, no text"
    },
    {
        "path": f"{OUT}/blog-diagram-idex-2.webp",
        "prompt": "Multi-material 3D printed part emerging from an IDEX 3D printer build plate: rigid white PLA body with flexible black TPU hinge integrated in a single print, both materials visible at the junction, partially dissolved PVA support structure in wash station beside the printer, engineering workbench setting with caliper tool nearby, dark navy (#0B1120) background, professional lighting, no brands, no logos, no text"
    },
    {
        "path": f"{OUT}/blog-diagram-idex-3.webp",
        "prompt": "Row of three identical IDEX 3D printers in a print farm configuration, both toolheads on each printer operating in mirror mode producing identical duplicate parts, LED-lit build chambers, finished parts collection area with batch of completed prints, industrial workspace with organized shelving, dark navy (#0B1120) background with electric blue (#2563EB) accent lighting from printer LEDs, no brands, no logos, no text"
    }
]

results = []
for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating {os.path.basename(img['path'])}...", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(img["path"], "wb") as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  -> Written ({size_kb:.0f} KB)", flush=True)
        
        # Compress immediately (trap 18a — do in Python, not shell loop)
        tmp = img["path"] + ".tmp"
        subprocess.run(["cwebp", "-q", "75", "-m", "6", img["path"], "-o", tmp], check=True)
        os.replace(tmp, img["path"])
        size_kb2 = os.path.getsize(img["path"]) / 1024
        print(f"  -> Compressed ({size_kb:.0f} -> {size_kb2:.0f} KB)", flush=True)
        results.append({"file": os.path.basename(img["path"]), "size_kb": size_kb2, "status": "ok"})
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)
        results.append({"file": os.path.basename(img["path"]), "size_kb": 0, "status": str(e)})
    time.sleep(1)

print("\n=== RESULTS ===", flush=True)
for r in results:
    print(f"  {r['file']}: {r['size_kb']:.0f}KB - {r['status']}", flush=True)
print(f"Total: {len([r for r in results if r['status']=='ok'])}/{len(images)} generated", flush=True)
