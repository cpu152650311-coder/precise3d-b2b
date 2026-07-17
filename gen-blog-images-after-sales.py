#!/usr/bin/env python3
"""Generate blog images for after-sales support article using GPT Image 2."""
import os, base64, time, sys
from openai import OpenAI

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
if not API_KEY:
    print("ERROR: AIHUBMIX_API_KEY not set", file=sys.stderr)
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url="https://aihubmix.com/v1")
OUT = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{OUT}/blog-cover-after-sales-support.webp",
        "prompt": (
            "Professional photography of a precision 3D printer on a clean modern workbench, "
            "diagnostic tools and calibration equipment nearby, warm studio lighting with blue accent, "
            "depth of field focusing on printer extruder assembly, "
            "industrial design aesthetic, dark background with soft rim light, "
            "no people faces, no text, no logos, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-after-sales-1.webp",
        "prompt": (
            "Macro photograph of electronic quality control testing station, "
            "circuit board undergoing automated optical inspection under bright LED ring light, "
            "precision probe touching test points, digital measurement readout reflecting on surface, "
            "clean room environment with anti-static mat, shallow depth of field, "
            "no people faces, no text, no logos, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-after-sales-2.webp",
        "prompt": (
            "Organized industrial spare parts storage with labeled compartments, "
            "various 3D printer components neatly arranged: hotend assemblies, build plates, "
            "fan modules, stepper motors, each in dedicated foam-cut slots, "
            "warehouse shelving with warm LED lighting, professional inventory management aesthetic, "
            "no people faces, no text, no logos, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-after-sales-3.webp",
        "prompt": (
            "Close-up photography of skilled hands working on precision 3D printer calibration, "
            "adjusting extruder assembly with hex tool, focus on mechanical details, "
            "well-lit technical workshop environment, metallic components reflecting soft light, "
            "professional service atmosphere, shallow depth of field on adjustment point, "
            "no faces visible, no text, no logos, no diagrams, no charts"
        )
    },
    {
        "path": f"{OUT}/blog-diagram-after-sales-4.webp",
        "prompt": (
            "Industrial product photography of packaged 3D printer boxes stacked on wooden pallets "
            "in a clean modern shipping facility, quality inspection stickers visible on boxes, "
            "forklift in distant background blurred, bright even warehouse lighting, "
            "professional logistics environment, cardboard boxes with minimal branding marks obscured, "
            "no people faces, no text, no logos, no diagrams, no charts"
        )
    },
]

for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating: {os.path.basename(img['path'])}")
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(img["path"], "wb") as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  ✓ Saved ({size_kb:.0f} KB)")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
    time.sleep(1.5)

print("\nAll done. File sizes:")
for img in images:
    if os.path.exists(img["path"]):
        sz = os.path.getsize(img["path"]) / 1024
        print(f"  {os.path.basename(img['path']):50s} {sz:7.0f} KB")
