#!/usr/bin/env python3
"""Generate 5 blog images for nozzle/hotend article — precise3d-b2b"""
import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

OUT_DIR = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{OUT_DIR}/blog-cover-nozzle-tech.webp",
        "prompt": (
            "close-up macro photo of an assortment of 3D printer brass nozzles arranged on a dark navy workbench surface, "
            "different nozzle diameters visible, one nozzle partially installed in a silver heater block with blue silicone sock, "
            "precision engineering detail lit by cool LED overhead light, electric blue accent reflections on brass surfaces, "
            "industrial workshop background with subtle teal glow, photorealistic product photography style, "
            "deep navy background, no brands, no logos, no text, no people faces"
        )
    },
    {
        "path": f"{OUT_DIR}/blog-diagram-nozzle-tech-1.webp",
        "prompt": (
            "macro comparison shot of four 3D printer nozzles on a neutral dark surface under studio lighting, "
            "showing progressive wear: new shiny brass nozzle, slightly worn nozzle with subtle bore enlargement, "
            "heavily worn nozzle with visible tip deformation, and pristine hardened steel nozzle for contrast, "
            "each nozzle next to a small printed test swatch showing surface quality differences, "
            "deep navy background with electric blue accent edge lighting, photorealistic macro photography depth of field, "
            "no brands, no logos, no text, no people faces"
        )
    },
    {
        "path": f"{OUT_DIR}/blog-diagram-nozzle-tech-2.webp",
        "prompt": (
            "3D printer hotend assembly partially disassembled on a dark workshop surface, "
            "titanium heat break removed from aluminum heater block, interchangeable brass nozzles lined up nearby, "
            "hex wrenches and maintenance tools visible, silicone sock pulled back revealing heater cartridge, "
            "professional workshop lighting with cool blue undertones, deep navy background, "
            "identifiable 3D printer components in engineering context, photorealistic detail, "
            "no brands, no logos, no text, no people faces"
        )
    },
    {
        "path": f"{OUT_DIR}/blog-diagram-nozzle-tech-3.webp",
        "prompt": (
            "photorealistic 3D cross-section render of a 3D printer all-metal hotend, "
            "cutaway view revealing internal structure: titanium heat break with sharp thermal transition zone, "
            "aluminum heater block, brass nozzle threaded in place, internal filament path visible as a smooth bore, "
            "metallic surfaces with realistic machining marks, distinct color coding for different metals, "
            "dark navy studio background with electric blue rim lighting, technical product visualization style, "
            "no brands, no logos, no text, no people faces"
        )
    },
    {
        "path": f"{OUT_DIR}/blog-diagram-nozzle-tech-4.webp",
        "prompt": (
            "four 3D printer nozzles of different diameters arranged in a row on dark textured surface, "
            "from smallest to largest: 0.2mm, 0.4mm, 0.6mm, 0.8mm, "
            "each nozzle next to a small 3D printed test cube showing increasing layer line thickness, "
            "calipers partially visible measuring one nozzle tip, shallow depth of field focusing on nozzle tips, "
            "deep navy background with subtle cool teal accent lighting, industrial product photography, "
            "no brands, no logos, no text, no people faces"
        )
    },
]

for i, img in enumerate(images, 1):
    print(f"[{i}/{len(images)}] Generating {os.path.basename(img['path'])}...")
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
    print(f"  -> saved ({size_kb:.0f} KB)")
    time.sleep(1)

# Verify all files exist
print("\n=== Verify ===")
for img in images:
    if os.path.exists(img["path"]):
        sz = os.path.getsize(img["path"]) / 1024
        print(f"  OK: {os.path.basename(img['path'])} ({sz:.0f} KB)")
    else:
        print(f"  MISSING: {os.path.basename(img['path'])}")
