import base64, time, subprocess, os, sys

from openai import OpenAI
client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

IMAGES = [
    {
        "prompt": "Professional product photography: premium 3D printer accessory bundle on dark navy background, brass nozzles, PEI spring steel build plate, colorful filament spools, PTFE tubing, silicone socks arranged in elegant composition, studio lighting with electric blue accent rim light, no people faces, no text, no logos, no charts, no arrows, no infographics",
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-cover-accessories-bundling.webp"
    },
    {
        "prompt": "Macro studio product shot: detailed close-up of 3D printer consumables on dark matte surface, brass nozzle with visible 0.4mm aperture, PEI gold textured build plate surface, coiled PTFE tubing, silicone heat block sock, professional lighting highlighting metallic textures, shallow depth of field, no people faces, no text, no logos, no charts, no arrows",
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-accessories-bundling-1.webp"
    },
    {
        "prompt": "Clean commercial product photography: three black matte packaging boxes of different sizes containing 3D printer accessory kits, tiered arrangement Small Medium Large, sleek minimalist packaging design, dark studio background with subtle blue gradient accent light, premium consumer electronics unboxing aesthetic, no people faces, no text on boxes, no logos, no charts, no arrows",
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-accessories-bundling-2.webp"
    },
    {
        "prompt": "Industrial warehouse shelf photography: organized rows of 3D printer filament spools in multiple vibrant colors, grouped by material type with visible spool labels, depth of field focusing on foreground spools with background softly blurred, warm LED warehouse lighting, professional industrial photography style, no people faces, no text, no logos, no charts, no arrows",
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-accessories-bundling-3.webp"
    },
    {
        "prompt": "Abstract dark tech texture: deep navy blue surface with subtle hexagonal grid pattern reminiscent of 3D printer honeycomb infill structure, electric blue light streaks tracing along grid lines, low contrast sophisticated background suitable for section divider, no text, no logos, no people, no objects, purely abstract geometric pattern",
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-accessories-bundling-4.webp"
    },
    {
        "prompt": "Modern e-commerce interface displayed on sleek tablet screen on dark desk: three-tier product bundle comparison with product photography thumbnails, clean minimalist UI design with dark theme and blue accent highlights, professional tech product marketing photography, screen visible at slight angle, ambient studio lighting, no people faces, no text, no logos, no charts with numbers",
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-accessories-bundling-5.webp"
    }
]

results = []
for i, img in enumerate(IMAGES):
    print(f"[{i+1}/{len(IMAGES)}] Generating: {os.path.basename(img['path'])}")
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
        print(f"  -> Saved ({size_kb:.0f} KB)")
        
        # Compress with cwebp
        tmp_path = img["path"] + ".tmp"
        result = subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", img["path"], "-o", tmp_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            os.replace(tmp_path, img["path"])
            compressed_kb = os.path.getsize(img["path"]) / 1024
            print(f"  -> Compressed ({compressed_kb:.0f} KB)")
        else:
            print(f"  -> cwebp failed: {result.stderr[:100]}")
        
        results.append({"file": os.path.basename(img["path"]), "size_kb": int(compressed_kb if result.returncode == 0 else size_kb), "ok": True})
    except Exception as e:
        print(f"  -> FAILED: {e}")
        results.append({"file": os.path.basename(img["path"]), "ok": False, "error": str(e)})
    
    if i < len(IMAGES) - 1:
        time.sleep(1.5)

print("\n=== SUMMARY ===")
for r in results:
    status = f"{r.get('size_kb', '?')}KB" if r["ok"] else f"FAIL: {r.get('error','?')[:60]}"
    print(f"  {'OK' if r['ok'] else 'XX'} {r['file']}: {status}")

all_ok = all(r["ok"] for r in results)
print(f"\nTotal: {sum(1 for r in results if r['ok'])}/{len(results)} succeeded")
sys.exit(0 if all_ok else 1)
