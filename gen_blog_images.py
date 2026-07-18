#!/usr/bin/env python3
"""Generate blog images for linear-rails-vs-vwheels article"""
import base64, os, time, subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{out_dir}/blog-cover-linear-rails-vwheels.webp",
        "prompt": (
            "Professional corporate marketing photo of a high-end enclosed 3D printer with visible linear rails on the gantry, "
            "precision engineering aesthetic, deep navy (#0B1120) background with electric blue (#2563EB) accent lighting on the rail system, "
            "cool teal (#06B6D4) secondary highlights, tech-forward industrial workspace, "
            "the linear rails are the focal point gleaming under workshop lighting, "
            "no people faces, no text, no logos, no brands"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-linear-rails-vwheels-1.webp",
        "prompt": (
            "extreme macro close-up photography side by side: on the left a worn POM V-wheel from a 3D printer with visible flat spot "
            "and groove deformation on the polymer contact surface, on the right a pristine hardened steel MGN12H linear rail with bearing block "
            "showing mirror-smooth ground raceways, precision engineering comparison shot, "
            "deep navy (#0B1120) background, electric blue (#2563EB) accent rim light on the steel rail, "
            "industrial inspection lighting, 3D printer parts visible in context, "
            "no people faces, no text, no logos, no brands, no arrows, no labels"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-linear-rails-vwheels-2.webp",
        "prompt": (
            "laboratory inspection photography: a worn POM V-wheel from a 3D printer with visible flat deformation spot "
            "placed under inspection magnifier showing surface degradation at 40x, next to a pristine steel linear rail bearing block "
            "with perfect ball bearings visible through the end cap, engineering quality control lab setting, "
            "deep navy (#0B1120) background with electric blue (#2563EB) accent lighting, "
            "caliper and measurement tools in soft focus background, "
            "no people faces, no text, no logos, no brands, no arrows, no diagrams"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-linear-rails-vwheels-3.webp",
        "prompt": (
            "engineering workbench overhead photography: a tray of brand new POM V-wheels with eccentric nuts, spacers, and hex shims "
            "laid out on the left side, three MGN12H linear rails with bearing blocks arranged on the right side, "
            "bill of materials comparison for a 3D printer motion system, micrometer and engineering drawings in background, "
            "deep navy (#0B1120) workbench surface, electric blue (#2563EB) accent on the linear rail steel, "
            "professional factory lighting, components are the sole subject, "
            "no people faces, no text, no logos, no brands"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-linear-rails-vwheels-4.webp",
        "prompt": (
            "split scene maintenance photography: left half shows hands using an Allen key to adjust the eccentric nut "
            "on a V-wheel of an open-frame 3D printer, right half shows hands wiping a clean linear rail with a microfiber cloth "
            "on an enclosed 3D printer, maintenance comparison context, workshop environment, "
            "deep navy (#0B1120) tones with electric blue (#2563EB) accent on the printer frames, "
            "both printers visible in their respective halves, practical how-to aesthetic, "
            "no faces shown (hands only, head cropped out), no text, no logos, no brands"
        )
    },
]

success = 0
for i, img in enumerate(images):
    print(f"[{i+1}/5] Generating {os.path.basename(img['path'])}...")
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
        tmp = img["path"] + ".tmp"
        subprocess.run(["cwebp", "-q", "75", "-m", "6", img["path"], "-o", tmp], check=True)
        os.rename(tmp, img["path"])
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  ✓ Saved ({size_kb:.0f} KB)")
        success += 1
    except Exception as e:
        print(f"  ✗ Failed: {e}")
    time.sleep(1.5)

print(f"\nDone: {success}/{len(images)} images generated and compressed")
