import os, base64, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{out_dir}/blog-cover-build-volume.webp",
        "prompt": "Three 3D printers of different sizes arranged side by side on illuminated display platforms, from compact 180mm to large 400mm, dark industrial showroom with blue ambient lighting, precision engineering aesthetic, brand colors dark blue accents with gold highlights, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-build-volume-compact.webp",
        "prompt": "Compact 180mm 3D printer on classroom desk, colorful 3D printed geometric shapes and toys displayed nearby, bright modern education setting, safety enclosure visible, brand colors dark blue with gold, tech-forward clean aesthetic, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-build-volume-prosumer.webp",
        "prompt": "Large format 3D printer printing a full-size detailed cosplay helmet in one continuous piece on build plate, well-lit professional workshop, filament spools on shelf behind, layer lines visible, precision engineering, dark blue and gold brand tones, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-build-volume-margin.webp",
        "prompt": "Three 3D printers of graduated sizes on illuminated podiums at trade show exhibition booth, product specification brochures on stand, professional corporate lighting, dark blue backdrop with warm gold accent lights, premium industrial aesthetic, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-build-volume-printfarm.webp",
        "prompt": "Close-up of a large detailed 3D print emerging from printer build plate, intricate layer lines visible under LED lighting, rows of identical 3D printers operating in background print farm, industrial workspace, dark blue and gold ambient tones, tech-forward aesthetic, no people faces, no text, no logos"
    },
    {
        "path": f"{out_dir}/blog-build-volume-cta-bg.webp",
        "prompt": "3D printers of varying sizes arranged in modern warehouse showroom, pallets and shipping crates in defocused background, professional industrial lighting with dark blue ambient tones and subtle gold warmth, clean organized space, premium B2B atmosphere, no people faces, no text, no logos"
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
    with open(img["path"], "wb") as f:
        f.write(base64.b64decode(b64))
    size_kb = os.path.getsize(img["path"]) / 1024
    print(f"  -> Saved ({size_kb:.0f} KB)")
    time.sleep(1)

print("DONE: All 6 images generated")
