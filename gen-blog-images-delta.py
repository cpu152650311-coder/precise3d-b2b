#!/usr/bin/env python3
"""Generate images for delta kinematics blog — inline fallback"""
import os, base64, time, subprocess, sys
from openai import OpenAI

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
if not API_KEY:
    print("ERROR: AIHUBMIX_API_KEY not set", file=sys.stderr)
    sys.exit(1)

OUT = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "slug": "blog-cover-delta-kinematics",
        "prompt": "Wide cinematic shot of a delta 3D printer in operation inside a dark studio, triangular aluminum frame with three vertical towers, effector platform with hotend suspended by six carbon fiber arms, printing a tall cylindrical vase at high speed, LED strip lighting illuminating the build plate, layer lines visible on the part, deep navy (#0B1120) background with electric blue (#2563EB) accent lighting on the towers, tech-forward aesthetic, no people faces, no text, no logos, no brands, no abstract diagrams, photorealistic 3D printer photography"
    },
    {
        "slug": "blog-diagram-delta-1",
        "prompt": "Close-up action shot of a delta 3D printer effector platform in mid-print, carbon fiber arms with magnetic ball joints visible, hotend nozzle depositing filament on a tall cylindrical part, motion blur on the arms conveying speed, build plate stationary below, triangular tower structure visible in soft background, industrial studio lighting, deep navy (#0B1120) tones with electric blue (#2563EB) LED accents on the effector, cool teal (#06B6D4) ambient glow, no people faces, no text, no logos, no abstract diagrams, macro engineering photography style"
    },
    {
        "slug": "blog-diagram-delta-2",
        "prompt": "Extreme close-up macro photograph of a delta 3D printer effector, six carbon fiber rods converging at a central aluminum hub, magnetic ball joints with visible metallic bearing surfaces, hotend heatsink with cooling fins, 0.4mm brass nozzle tip visible, precision mechanical engineering detail shot, dark studio background with subtle electric blue (#2563EB) rim lighting, deep navy (#0B1120) shadow tones, no people faces, no text, no logos, no arrows, no diagrams, product photography style"
    },
    {
        "slug": "blog-diagram-delta-3",
        "prompt": "Studio product photography of multiple finished 3D printed objects arranged on a dark reflective surface — tall spiral vases in marble PLA, cylindrical lamp shades with geometric patterns, a decorative column, all showing clean layer lines and smooth surfaces characteristic of delta printer output, side lighting with electric blue (#2563EB) and cool teal (#06B6D4) accents, deep navy (#0B1120) background, premium product display aesthetic, no people faces, no text, no logos, no abstract graphics"
    },
    {
        "slug": "blog-diagram-delta-4",
        "prompt": "3D printer trade show booth setting, a delta 3D printer prominently displayed on a pedestal with triangular frame and carbon arms visible, printed sample parts arranged around the base — helmets, vases, architectural models, LED-backlit display panels with deep navy (#0B1120) tones, electric blue (#2563EB) accent lighting strips on the booth structure, professional exhibition photography, no faces visible, no text, no logos, no brands, no people as main subject, no abstract infographics"
    },
]

os.makedirs(OUT, exist_ok=True)

ENDPOINTS = ["https://aihubmix.com/v1", "https://api.inferera.com/v1"]

for i, img in enumerate(images):
    final_path = os.path.join(OUT, f"{img['slug']}.webp")
    if os.path.exists(final_path):
        print(f"[{i+1}/{len(images)}] SKIP {img['slug']}.webp (exists)")
        continue

    print(f"[{i+1}/{len(images)}] Generating {img['slug']}...", flush=True)
    success = False
    raw_path = final_path + ".raw"

    for endpoint in ENDPOINTS:
        try:
            c = OpenAI(api_key=API_KEY, base_url=endpoint)
            resp = c.images.generate(
                model="gpt-image-2", prompt=img["prompt"],
                n=1, size="1024x1024", quality="low"
            )
            if hasattr(resp.data[0], 'b64_json') and resp.data[0].b64_json:
                with open(raw_path, "wb") as f:
                    f.write(base64.b64decode(resp.data[0].b64_json))
                success = True
                break
            elif hasattr(resp.data[0], 'url') and resp.data[0].url:
                import urllib.request
                urllib.request.urlretrieve(resp.data[0].url, raw_path)
                success = True
                break
        except Exception as e:
            print(f"  FAIL {endpoint}: {e}")
            continue

    if not success:
        print(f"  -> ALL ENDPOINTS FAILED for {img['slug']}")
        continue

    try:
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            check=True, capture_output=True, timeout=120
        )
        os.remove(raw_path)
        kb = os.path.getsize(final_path) / 1024
        print(f"  OK {img['slug']}.webp ({kb:.0f} KB)")
    except Exception as e:
        print(f"  COMPRESS FAIL: {e}")
        os.rename(raw_path, final_path)

    if i < len(images) - 1:
        time.sleep(1)

print(f"\nDone. Files in {OUT}/")
