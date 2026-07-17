import os, base64, time, sys
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

images = [
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-cover-dd-bowden.webp",
        "prompt": "Close-up split composition: left side shows a direct drive 3D printer extruder assembly on print head with exposed dual gears and motor, right side shows a Bowden tube routing from frame-mounted extruder to hotend. Dark industrial studio lighting with rim highlights. Brand colors: dark blue (#0B2447) accents with gold (#D4A017) highlights on metallic components. Precision engineering aesthetic. no brands, no logos, no text, no people faces"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-dd-bowden-1.webp",
        "prompt": "Macro close-up of two 3D printer hotend assemblies side by side on dark workbench. Left: direct drive extruder with motor mounted directly above hotend, compact integrated design. Right: Bowden setup showing PTFE tube entering hotend from frame-mounted extruder. Deep shadows, cool blue industrial lighting. Factory QC inspection setting with calipers nearby. no brands, no logos, no text, no people faces"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-dd-bowden-2.webp",
        "prompt": "Two identical flexible TPU 3D printed test objects on dark slate surface under studio lighting. Left print shows clean surface finish with sharp details from direct drive printer. Right print shows slight stringing and surface artifacts characteristic of Bowden retraction challenges. Gold (#D4A017) accent rim light on the successful print. Professional product photography style. no brands, no logos, no text, no people faces"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-dd-bowden-3.webp",
        "prompt": "Three 3D printers on display in a modern trade show booth setting, each representing a different tier: compact open-frame Bowden printer on left, mid-size enclosed printer center, large professional CoreXY direct drive printer on right with filament spools visible. Dark booth with spot lighting on each printer. Brand-consistent dark blue (#0B2447) background with gold (#D4A017) accent strips. no brands, no logos, no text, no people faces"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-diagram-dd-bowden-4.webp",
        "prompt": "Rows of identical enclosed 3D printers operating in a print farm, LED-lit build chambers glowing, finished parts visible on build plates. Clean industrial workspace with organized filament storage shelves. Blue ambient lighting from printer displays reflecting on dark floor. Professional production environment. no brands, no logos, no text, no people faces"
    },
    {
        "path": "/home/ubuntu/projects/precise3d-b2b/generated/blog-cta-dd-bowden.webp",
        "prompt": "Abstract dark blue (#0B2447) gradient with subtle gold (#D4A017) geometric accent lines suggesting precision engineering and technical sophistication. Low contrast texture pattern like brushed metal surface. Moody industrial atmosphere suitable as background for text overlay. No distinct objects, pure texture and atmosphere. no brands, no logos, no text, no people faces"
    },
]

success_count = 0
for i, img in enumerate(images):
    print(f"[{i+1}/{len(images)}] Generating {os.path.basename(img['path'])}...", flush=True)
    try:
        resp = client.images.generate(
            model="gpt-image-2", prompt=img["prompt"],
            n=1, size="1024x1024", quality="low"
        )
        b64 = resp.data[0].b64_json
        with open(img["path"], "wb") as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(img["path"]) / 1024
        print(f"  -> OK ({size_kb:.0f} KB)", flush=True)
        success_count += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)
    if i < len(images) - 1:
        time.sleep(1.5)

print(f"\nDone: {success_count}/{len(images)} images generated", flush=True)
