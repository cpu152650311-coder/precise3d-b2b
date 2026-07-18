import base64, os, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")
out_dir = "/home/ubuntu/projects/precise3d-b2b/generated"

images = [
    {
        "path": f"{out_dir}/blog-cover-abl-tech.webp",
        "prompt": (
            "Close-up industrial product photography of a 3D printer hotend with integrated probe sensor "
            "hovering millimeters above a textured build plate, dramatic rim lighting on dark navy background, "
            "precision engineering aesthetic, cool blue tones with electric blue accent highlights, "
            "identifiable 3D printer frame visible in shallow depth of field, macro lens perspective, "
            "no people faces, no text, no logos, no brands"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-abl-1.webp",
        "prompt": (
            "Extreme macro photograph of a 3D printer nozzle tip making contact with a PEI build plate surface, "
            "visible gap between nozzle and bed showing precise measurement, LED indicator light glowing red on probe, "
            "metallic nozzle reflecting ambient light, dark navy background, technical precision aesthetic, "
            "identifiable 3D printer toolhead assembly partially visible, industrial photography style, "
            "no people faces, no text, no logos, no brands"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-abl-2.webp",
        "prompt": (
            "Macro detail of a BLTouch-style plunger probe tip extended and touching textured build plate surface, "
            "plastic pin tip visible in sharp focus, red LED indicator on probe body, metallic mounting bracket, "
            "3D printer hotend and part cooling fan visible in the background, dark workshop setting, "
            "precision measurement aesthetic, cool blue ambient lighting with warm accent on the contact point, "
            "no people faces, no text, no logos, no brands"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-abl-4.webp",
        "prompt": (
            "Professional product photography of a 3D printer hotend assembly with integrated strain gauge sensor "
            "mounted on precision aluminum bracket, visible sensor wiring and mounting screws, "
            "CoreXY motion system rails visible in background, dark navy blue background with rim lighting, "
            "industrial engineering aesthetic, sharp focus on the sensor component, "
            "identifiable 3D printer mechanical components, cool technical lighting, "
            "no people faces, no text, no logos, no brands"
        )
    },
    {
        "path": f"{out_dir}/blog-diagram-abl-5.webp",
        "prompt": (
            "Row of identical 3D printers operating simultaneously in a print farm configuration, "
            "LED-lit print chambers glowing, build plates visible with first layer being printed on each machine, "
            "industrial workspace setting with organized cable management, modern manufacturing aesthetic, "
            "multiple 3D printers in perspective rows, dark environment with printer LED glow, "
            "cool blue tones with warm amber LED accents from printer chambers, "
            "no people faces, no text, no logos, no brands"
        )
    },
]

print(f"Generating {len(images)} images...")
for i, img in enumerate(images):
    fname = os.path.basename(img["path"])
    print(f"[{i+1}/{len(images)}] {fname}...")
    try:
        resp = client.images.generate(
            model="gpt-image-2", prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(img["path"], "wb") as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  OK: {size_kb:.0f} KB")
    except Exception as e:
        print(f"  FAIL: {e}")
    time.sleep(1)

print("Done.")
