#!/usr/bin/env python3
"""Generate blog images for stepper drivers article — Precise3D"""
import os, base64, time, subprocess
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/precise3d-b2b/generated"
os.makedirs(out_dir, exist_ok=True)

images = [
    {
        "path": f"{out_dir}/blog-cover-stepper-drivers.webp",
        "prompt": (
            "Close-up macro photograph of a Trinamic TMC2209 stepper driver chip on a 3D printer motherboard, "
            "gold contact pads and tiny surface-mount components visible, subtle blue LED glow from nearby power indicator, "
            "deep navy (#0B1120) dark background with electric blue (#2563EB) accent reflections on PCB traces, "
            "industrial precision electronics photography, shallow depth of field, no brands no logos no text no people faces"
        ),
    },
    {
        "path": f"{out_dir}/blog-diagram-stepper-1.webp",
        "prompt": (
            "Extreme macro shot of a stepper driver chip on a 3D printer control board, "
            "TMC driver IC with visible chip markings and fine pitch pins soldered to PCB, "
            "surrounding capacitors and resistors in sharp focus, cool teal (#06B6D4) accent from nearby status LED, "
            "dark navy (#0B1120) background, premium electronics product photography, "
            "3D printer motherboard context clearly visible with stepper motor connectors, no brands no logos no text no people faces"
        ),
    },
    {
        "path": f"{out_dir}/blog-diagram-stepper-2.webp",
        "prompt": (
            "Three different Trinamic stepper driver chips arranged on an anti-static mat: TMC2208, TMC2209, and TMC5160, "
            "each with aluminum heatsink attached, pin headers visible, macro photography showing size comparison, "
            "next to a 3D printer mainboard partially visible with stepper motor wiring, "
            "dark industrial workbench setting, deep navy (#0B1120) shadows, electric blue (#2563EB) accent light, "
            "precision electronics lab aesthetic, no brands no logos no text no people faces"
        ),
    },
    {
        "path": f"{out_dir}/blog-diagram-stepper-3.webp",
        "prompt": (
            "Modern 32-bit 3D printer motherboard with STM32 ARM processor visible, integrated TMC2209 stepper drivers, "
            "multiple fan headers and thermistor connectors, clean PCB design with organized silkscreen sections, "
            "connected to stepper motors and ribbon cables leading to a 3D printer frame visible in background, "
            "deep navy (#0B1120) dark background, electric blue (#2563EB) accent from power LED, "
            "industrial product photography of electronics, no brands no logos no text no people faces"
        ),
    },
    {
        "path": f"{out_dir}/blog-diagram-stepper-4.webp",
        "prompt": (
            "3D printer mid-print creating a complex geometric lattice model, close-up of print head moving smoothly over build plate, "
            "pristine first layer with perfect adhesion visible, filament extruding cleanly from nozzle, "
            "dimly lit studio setting with deep navy (#0B1120) ambiance, electric blue (#2563EB) accent from printer status LED, "
            "silent operation aesthetic conveyed through smooth motion blur, professional 3D printing photography, "
            "no brands no logos no text no people faces"
        ),
    },
]

for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating: {os.path.basename(img['path'])}")
    resp = client.images.generate(
        model="gpt-image-2",
        prompt=img["prompt"],
        n=1, size="1024x1024", quality="low"
    )
    b64 = resp.data[0].b64_json
    # Write raw PNG first (GPT Image 2 returns PNG even when named .webp)
    raw_path = img["path"].replace(".webp", "_raw.png")
    with open(raw_path, "wb") as f:
        f.write(base64.b64decode(b64))
    # Convert to WebP with compression
    subprocess.run(
        ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", img["path"]],
        check=True, capture_output=True
    )
    # Remove raw PNG
    os.remove(raw_path)
    # Check size
    size_kb = os.path.getsize(img["path"]) / 1024
    print(f"  -> {img['path']} ({size_kb:.0f} KB)")
    time.sleep(1.5)

print("\nDone. Verifying files:")
for img in images:
    exists = os.path.exists(img["path"])
    size_kb = os.path.getsize(img["path"]) / 1024 if exists else 0
    print(f"  {'✓' if exists else '✗'} {os.path.basename(img['path'])} ({size_kb:.0f} KB)")
