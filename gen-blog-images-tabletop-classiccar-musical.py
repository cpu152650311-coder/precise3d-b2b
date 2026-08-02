#!/usr/bin/env python3
"""Generate 15 images for 3 new articles (tabletop/classiccar/musical). Precise3D brand rules."""
import os, sys, time, base64, subprocess

API_KEY = os.environ.get("AIHUBMIX_API_KEY")
if not API_KEY:
    print("ERROR: AIHUBMIX_API_KEY not set", file=sys.stderr)
    sys.exit(1)

from openai import OpenAI

clients = [
    OpenAI(api_key=API_KEY, base_url="https://aihubmix.com/v1", timeout=600),
    OpenAI(api_key=API_KEY, base_url="https://api.inferera.com/v1", timeout=600),
]

OUT_DIR = "/home/ubuntu/projects/precise3d-b2b/generated"
os.makedirs(OUT_DIR, exist_ok=True)

IMAGES = [
    # ── Tabletop Gaming & Miniatures ──
    {
        "id": "blog-cover-tabletop",
        "prompt": "Hero shot of a resin 3D printer with amber UV protective cover printing small tabletop miniature figures on the build plate, paint brushes and paint pots beside it on a dark hobby workbench, deep navy background with electric blue accent lighting, photorealistic product photography, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-tabletop-1",
        "prompt": "Close-up of a resin 3D printer with amber UV cover printing detailed tabletop miniature figures, wash and cure station machines beside it on a hobby workshop desk, blue accent rim lighting, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-tabletop-2",
        "prompt": "Freshly printed unpainted grey resin miniature figures standing on a build plate, a wash basket with isopropyl alcohol and a UV cure station turntable visible in the hobby workshop background, photorealistic macro shot, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-tabletop-3",
        "prompt": "Print-on-demand game club station with multiple resin 3D printers running rows, shelves of resin bottles and finished painted miniatures on display nearby, LED-lit workshop, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-tabletop-4",
        "prompt": "Retail shelf display in a game shop featuring a resin 3D printer, wash and cure station, and colorful resin bottles, finished painted miniatures on a display shelf above, warm retail lighting with navy accents, photorealistic, no people faces, no text, no logos",
    },
    # ── Classic Car Restoration ──
    {
        "id": "blog-cover-classiccar",
        "prompt": "Hero shot of a classic 1970s sports car in a restoration workshop, a 3D printer printing a dashboard vent louver part in the foreground, tools and parts on the bench, deep navy background with electric blue accent lighting, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-classiccar-1",
        "prompt": "Close-up of hands-free workshop bench scene: a classic car dashboard with a printed vent louver replacement part held beside it, worn original part next to the new printed part, restoration shop lighting with blue accents, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-classiccar-2",
        "prompt": "Flat lay of 3D printed classic car interior parts on a dark workshop bench: vent louver, switch bezel, door panel clips and a sun visor bracket, next to one worn original part, macro detail, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-classiccar-3",
        "prompt": "Engine bay of a classic car with 3D printed PA12 fluid cap and hose bracket installed, vintage engine block with chrome details, workshop lighting, photorealistic close-up, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-classiccar-4",
        "prompt": "Restoration workshop scene: a 3D printer printing a trim piece in the foreground, a monitor showing scanned 3D models of classic car parts in the background, parts shelf with printed components, photorealistic, no people faces, no text, no logos",
    },
    # ── Musical Instruments ──
    {
        "id": "blog-cover-musical",
        "prompt": "Hero shot of an electric guitar on a luthier workbench with 3D printed pickup rings and knobs being fitted, printed parts and tools around it, deep navy background with electric blue accent lighting, photorealistic product photography, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-musical-1",
        "prompt": "Close-up of a luthier workbench: electric guitar body with a 3D printed pickup ring being fitted, printed knobs and switch tips laid out, workshop tools, photorealistic macro, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-musical-2",
        "prompt": "Flat lay of 3D printed guitar parts in matte black and cream on a dark workbench: knobs, pickup rings, control plate and caps, one knob fitted on a guitar body corner, studio lighting, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-musical-3",
        "prompt": "Luthier workshop with a 3D printer printing a guitar part, printed fret radius jigs and clamping fixtures on the bench, stringed instruments hanging on the wall, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-musical-4",
        "prompt": "Collection of 3D printed instrument accessories arranged on a dark surface: picks, thumb rests, mic clips, cable clips and a stand adapter, soft studio lighting with blue accent glow, photorealistic, no people faces, no text, no logos",
    },
]


def generate_one(client, img, attempt=1):
    try:
        resp = client.images.generate(
            model="gpt-image-2",
            prompt=img["prompt"],
            n=1,
            size="1024x1024",
            quality="low",
        )
        if hasattr(resp.data[0], 'b64_json') and resp.data[0].b64_json:
            raw_data = base64.b64decode(resp.data[0].b64_json)
        elif hasattr(resp.data[0], 'url') and resp.data[0].url:
            import urllib.request
            raw_data = urllib.request.urlopen(resp.data[0].url).read()
        else:
            raise ValueError(f"Unknown response format: {resp.data[0]}")

        raw_path = os.path.join(OUT_DIR, f"{img['id']}_raw.webp")
        with open(raw_path, "wb") as f:
            f.write(raw_data)
        raw_size = os.path.getsize(raw_path)
        print(f"  [{img['id']}] generated: {raw_size//1024}KB raw")

        final_path = os.path.join(OUT_DIR, f"{img['id']}.webp")
        subprocess.run(
            ["cwebp", "-q", "75", "-m", "6", raw_path, "-o", final_path],
            capture_output=True, text=True, check=True
        )
        final_size = os.path.getsize(final_path)
        print(f"  [{img['id']}] compressed: {final_size//1024}KB")
        os.remove(raw_path)
        return True
    except Exception as e:
        print(f"  [{img['id']}] FAILED (attempt {attempt}): {e}")
        return False


def main():
    total = len(IMAGES)
    success = 0
    failed = []
    for i, img in enumerate(IMAGES):
        print(f"[{i+1}/{total}] Generating {img['id']}...")
        ok = generate_one(clients[0], img)
        if not ok:
            print(f"  [{img['id']}] Trying fallback endpoint...")
            ok = generate_one(clients[1], img, attempt=2)
        if ok:
            success += 1
        else:
            failed.append(img['id'])
        time.sleep(1.5)
    print(f"\n=== SUMMARY: {success}/{total} generated ===")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    print("\n=== VERIFICATION ===")
    for img in IMAGES:
        fp = os.path.join(OUT_DIR, f"{img['id']}.webp")
        if os.path.exists(fp):
            sz = os.path.getsize(fp)
            print(f"  OK  {img['id']}.webp — {sz//1024}KB")
        else:
            print(f"  MISS  {img['id']}.webp — NOT FOUND")


if __name__ == "__main__":
    main()
