#!/usr/bin/env python3
"""Generate 5 images for data center article."""
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
    {
        "id": "blog-cover-datacenter",
        "prompt": "Professional hero shot of a 3D printed PA12 liquid cooling manifold with quick-connect fittings mounted in a data center server rack, coolant tubing routed to GPU servers, deep navy background with electric blue LED accent lighting, photorealistic industrial photography, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-datacenter-1",
        "prompt": "3D printed PA12 liquid cooling manifold with quick-connect fittings on a data center rack, coolant tubing routed to GPU servers, blue LED server lighting, photorealistic macro detail of fittings, no text, no logos",
    },
    {
        "id": "blog-diagram-datacenter-2",
        "prompt": "Stack of 3D printed flame-retardant blanking panels installed in a server rack, cold aisle containment in the background, data center corridor with blue LED lighting, photorealistic, no people faces, no text, no logos",
    },
    {
        "id": "blog-diagram-datacenter-3",
        "prompt": "3D printed PA12-CF GPU mounting bracket holding a graphics card in a server chassis, drive bays visible, engineering workspace with digital calipers, electric blue accents, photorealistic macro detail, no text, no logos",
    },
    {
        "id": "blog-diagram-datacenter-4",
        "prompt": "Rack of 3D printed cable management D-rings and fiber routing troughs on server racks, neatly organized cabling, blue LED data center aisle lighting, photorealistic, no people faces, no text, no logos",
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
