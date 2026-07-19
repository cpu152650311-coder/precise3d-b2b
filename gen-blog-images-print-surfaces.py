#!/usr/bin/env python3
"""Generate blog images for print surfaces article — Precise3D ems-3dp.com"""
import os, base64, time, subprocess, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
OUT = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{OUT}/blog-cover-print-surfaces.webp",
        "prompt": (
            "Close-up macro photograph of a pristine gold PEI spring steel build plate on a 3D printer, "
            "dark navy studio background with dramatic rim lighting from the side, the textured surface catching the light, "
            "precision engineering aesthetic, cool blue tone grading, high contrast, product photography style, "
            "no people faces, no text, no logos, no arrows, no diagrams"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-print-surfaces-1.webp",
        "prompt": (
            "Macro comparison photograph on a dark workbench: a heavily worn scratched PEI print surface on the left "
            "showing visible gouge marks, scraper damage, and a polished-smooth worn central area, "
            "next to a factory-fresh textured PEI sheet on the right showing pristine matte gold surface, "
            "both are 235x235mm spring steel sheets with subtle magnetic backing visible at edges, "
            "dark studio lighting with cool industrial tones, depth of field focusing on the surface texture contrast, "
            "no people faces, no text, no logos, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-print-surfaces-2.webp",
        "prompt": (
            "Four different 3D printer build plates arranged in a grid on a dark matte surface, each with a small "
            "printed calibration cube on it: smooth gold PEI spring steel sheet, textured dark gray PEI sheet, "
            "black G10 Garolite fiberglass plate showing subtle weave pattern, and a carborundum-coated glass bed "
            "with micro-porous dark surface, studio product photography with even cool lighting, "
            "dark navy background, precision engineering aesthetic, the calibration cubes show first-layer finish, "
            "no people faces, no text, no logos, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-print-surfaces-3.webp",
        "prompt": (
            "Close-up of a carborundum-coated glass 3D printer bed with a black PLA printed object beginning to "
            "self-release after cooling — a visible gap forming between the print and the bed surface, "
            "the micro-porous ceramic coating texture visible at macro level, warm amber bed heating glow fading, "
            "dark studio background with rim lighting from above, the printed part has a clean flat bottom surface, "
            "no people faces, no text, no logos, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-print-surfaces-4.webp",
        "prompt": (
            "Macro photograph of a G10 Garolite fiberglass-epoxy build plate surface showing the distinct woven "
            "fabric texture of the laminate material, with a freshly 3D printed nylon PA6 calibration cube sitting "
            "on it that has cleanly released, the matte black-green surface has a subtle industrial sheen, "
            "dark workshop setting with focused side lighting that emphasizes the laminate weave pattern, "
            "the nylon print has a characteristic slightly rough matte surface typical of PA6, "
            "no people faces, no text, no logos, no arrows, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-print-surfaces-5.webp",
        "prompt": (
            "Side-by-side close-up comparison of two PEI spring steel sheets angled toward camera: "
            "textured PEI on the left showing fine matte grain surface with a PETG print successfully detaching, "
            "smooth PEI on the right showing mirror-like glossy gold reflective finish, "
            "both sheets partially lifted off a dark magnetic base to show the spring steel flexibility, "
            "dark navy studio background, cool blue rim lighting, precision product photography, "
            "no people faces, no text, no logos, no arrows, no diagrams, no charts"
        )
    },
]

print(f"Generating {len(images)} images for print surfaces article...")
for i, img in enumerate(images):
    fname = os.path.basename(img["path"])
    print(f"[{i+1}/{len(images)}] {fname}...")
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(img["path"], "wb") as f:
            f.write(base64.b64decode(b64))
        # Compress immediately
        raw_size = os.path.getsize(img["path"])
        result = subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", img["path"], "-o", f"{img['path']}.tmp"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            os.rename(f"{img['path']}.tmp", img["path"])
            final_size = os.path.getsize(img["path"])
            print(f"  ✓ {raw_size//1024}KB → {final_size//1024}KB compressed")
        else:
            print(f"  ⚠ compression failed: {result.stderr[:100]}")
            if os.path.exists(f"{img['path']}.tmp"):
                os.remove(f"{img['path']}.tmp")
        time.sleep(2)
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        continue

# Verify all files
print("\n=== Verification ===")
for img in images:
    fname = os.path.basename(img["path"])
    if os.path.exists(img["path"]):
        size_kb = os.path.getsize(img["path"]) // 1024
        status = "✓" if size_kb < 200 else "⚠ OVER 200KB"
        print(f"  {status} {fname}: {size_kb}KB")
    else:
        print(f"  ✗ MISSING: {fname}")

print(f"\nTotal files: {sum(1 for img in images if os.path.exists(img['path']))}/{len(images)}")
