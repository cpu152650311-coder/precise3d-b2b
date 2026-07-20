#!/usr/bin/env python3
"""Generate blog images for industrial materials article (ems-3dp.com)."""
import os, sys, base64, time, subprocess
from openai import OpenAI

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
if not API_KEY:
    print("ERROR: AIHUBMIX_API_KEY not set")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url="https://aihubmix.com/v1")
OUTDIR = "/home/ubuntu/projects/precise3d-b2b/generated"
os.makedirs(OUTDIR, exist_ok=True)

# Brand colors: deep navy #0B1120, electric blue #2563EB, teal #06B6D4
IMAGES = [
    {
        "id": "blog-cover-industrial-materials",
        "prompt": "PEEK and PEI industrial-grade 3D printer filament spools on a dark warehouse shelf, translucent amber and gold spools, precision engineering environment, deep navy background with electric blue accent lighting, no people faces, no text, no logos, 3D printer context visible"
    },
    {
        "id": "blog-diagram-ind-mat-1",
        "prompt": "close-up macro shot of PEEK filament spool with translucent amber color, industrial 3D printer nozzle in background, high-temperature engineering aesthetic, deep navy (#0B1120) ambient with electric blue (#2563EB) rim light, no people faces, no text, no logos"
    },
    {
        "id": "blog-diagram-ind-mat-2",
        "prompt": "close-up of industrial 3D printer all-metal hot end assembly with ceramic heater block and ruby-tipped nozzle, high-temperature components visible, engineering macro photography, deep navy background with electric blue and teal accent lighting, no people faces, no text, no logos"
    },
    {
        "id": "blog-diagram-ind-mat-3",
        "prompt": "collection of 3D printed industrial parts on dark technical workbench: aerospace bracket, medical implant guide, oil and gas valve component, chemical processing seal ring, made from PEEK and PEI polymer, professional studio lighting, deep navy background with electric blue highlights, no people faces, no text, no logos"
    },
    {
        "id": "blog-diagram-ind-mat-4",
        "prompt": "side-by-side comparison of three 3D printed test coupons made from PPSU, PEI, and PEEK on a dark engineering workbench surface, showing surface finish and amber/translucent color differences between the three materials, macro detail shot, deep navy background, cool teal accent lighting, no text, no logos"
    },
    {
        "id": "blog-scene-industrial-materials",
        "prompt": "industrial-grade enclosed 3D printer actively printing a PEEK aerospace component, orange heated chamber glow visible through transparent door, professional laboratory setting, precision engineering environment, deep navy ambient with electric blue accent highlights, no people faces, no text, no logos"
    },
]

for i, img in enumerate(IMAGES):
    img_id = img["id"]
    raw_path = os.path.join(OUTDIR, f"{img_id}_raw.webp")
    final_path = os.path.join(OUTDIR, f"{img_id}.webp")
    
    # Skip if final already exists
    if os.path.exists(final_path):
        print(f"[{i+1}/{len(IMAGES)}] SKIP {img_id} (already exists)")
        continue
    
    print(f"[{i+1}/{len(IMAGES)}] Generating {img_id}...")
    
    # Try aihubmix first, then inferera
    for endpoint_base in ["https://aihubmix.com/v1", "https://api.inferera.com/v1"]:
        try:
            c = OpenAI(api_key=API_KEY, base_url=endpoint_base)
            resp = c.images.generate(
                model="gpt-image-2",
                prompt=img["prompt"],
                n=1,
                size="1024x1024",
                quality="low"
            )
            # Handle both b64_json and url responses
            if hasattr(resp.data[0], 'b64_json') and resp.data[0].b64_json:
                b64 = resp.data[0].b64_json
                with open(raw_path, "wb") as f:
                    f.write(base64.b64decode(b64))
                break
            elif hasattr(resp.data[0], 'url') and resp.data[0].url:
                import urllib.request
                urllib.request.urlretrieve(resp.data[0].url, raw_path)
                break
            else:
                print(f"  WARN: unexpected response format from {endpoint_base}")
                continue
        except Exception as e:
            print(f"  FAIL {endpoint_base}: {e}")
            continue
    else:
        print(f"  ERROR: all endpoints failed for {img_id}")
        continue
    
    # Compress with cwebp
    try:
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            check=True, capture_output=True, timeout=120
        )
        os.remove(raw_path)
        size_kb = os.path.getsize(final_path) / 1024
        print(f"  OK {img_id}.webp ({size_kb:.0f} KB)")
    except Exception as e:
        print(f"  COMPRESS FAIL {img_id}: {e}")
        # Keep raw if compression fails
        os.rename(raw_path, final_path)
    
    time.sleep(1)

# Verify
print("\n=== Generated files ===")
for img in IMAGES:
    fp = os.path.join(OUTDIR, f"{img['id']}.webp")
    if os.path.exists(fp):
        print(f"  {img['id']}.webp  {os.path.getsize(fp)/1024:.0f} KB")
    else:
        print(f"  {img['id']}.webp  MISSING!")
