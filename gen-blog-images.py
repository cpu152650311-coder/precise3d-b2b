import base64, os, time
from openai import OpenAI

client = OpenAI(api_key=os.environ["AIHUBMIX_API_KEY"], base_url="https://aihubmix.com/v1")

DEST = "/home/ubuntu/projects/precise3d-b2b/generated"
BRAND = "dark industrial style, deep navy #0B1120 background, electric blue #2563EB and teal #06B6D4 accents, high contrast, precision-focused, cool blue tones, rim lighting, no people faces, no text, no logos"

images = [
    # === Article 1: CoreXY vs Bedslinger ===
    {
        "path": f"{DEST}/blog-cover-corexy-vs-bedslinger.webp",
        "prompt": f"A dramatic split-view technical illustration: on the left, a CoreXY 3D printer mechanism showing the crossed belt path and stationary bed with glowing teal accent lines tracing the motion path; on the right, a bedslinger printer showing the moving bed mechanism with blue motion trails. {BRAND}. Clean geometric composition with negative space for text overlay in the center."
    },
    {
        "path": f"{DEST}/blog-diagram-corexy-bedslinger-1.webp",
        "prompt": f"A clean technical cutaway diagram comparing two 3D printer kinematic systems side by side. Left: CoreXY architecture showing crossed belt path, stationary bed, 4 stepper motors, compact frame. Right: bedslinger/Cartesian architecture showing moving Y-bed with motion arrows, 3 stepper motors, linear rail system. {BRAND}. Infographic style with clear labels, glowing accent lines tracing motion paths."
    },
    {
        "path": f"{DEST}/blog-diagram-corexy-bedslinger-2.webp",
        "prompt": f"A customer segment mapping visualization: three tiers stacked vertically. Top: enthusiast/prosumer icon with CoreXY printer silhouette. Middle: hobbyist/first-time buyer with bedslinger silhouette. Bottom: print farm/business with multiple CoreXY units. {BRAND}. Clean infographic style, teal-to-blue gradient connecting tiers, minimalist icons."
    },
    {
        "path": f"{DEST}/blog-diagram-corexy-bedslinger-3.webp",
        "prompt": f"A convergence timeline visualization showing two converging lines: CoreXY cost curve declining and bedslinger performance curve rising, intersecting around 2027-2028. X-axis: 2024-2028 years. Y-axis unlabeled for visual impact. {BRAND}. Futuristic data visualization, glowing gradient lines, minimal grid background."
    },
    # === Article 2: Enclosed vs Open-Frame ===
    {
        "path": f"{DEST}/blog-cover-enclosed-vs-open.webp",
        "prompt": f"A split comparison: on the left, a fully enclosed 3D printer with transparent panels revealing a glowing hotend inside, dark chamber with teal ambient glow; on the right, an open-frame printer with exposed mechanics, blue accent highlights on the frame. {BRAND}. Dramatic lighting, product-photography quality, negative space for text overlay."
    },
    {
        "path": f"{DEST}/blog-diagram-enclosed-open-1.webp",
        "prompt": f"A technical cutaway diagram of an enclosed 3D printer showing internal airflow patterns: heated air rising from the bed in warm orange gradients, HEPA filter with particulate capture visualization, noise wave patterns being absorbed by enclosure walls. {BRAND}. Engineering diagram style, labeled components with glowing accent callouts."
    },
    {
        "path": f"{DEST}/blog-diagram-enclosed-open-2.webp",
        "prompt": f"A horizontal bar chart comparing noise levels: three bars for Pro X1 enclosed (44dB in teal), Creator C1 open-frame (48dB in blue), Start S1 open-frame (55dB in lighter blue). Background shows a subtle waveform visualization. {BRAND}. Clean data visualization, minimalist chart design, logarithmic scale indicated visually."
    },
    {
        "path": f"{DEST}/blog-diagram-enclosed-open-3.webp",
        "prompt": f"A branching decision tree diagram: starting from 'What does your customer print?' branching to 5 customer segments: Classroom (enclosed recommended), Home Hobbyist PLA-only (open-frame OK), Home Enthusiast multi-material (enclosure recommended), Office/Prototyping (enclosed mandatory), Print Farm (enclosed mandatory). {BRAND}. Flowchart style, teal and blue node connections, minimalist icons for each segment."
    },
]

print(f"Generating {len(images)} images...")
for i, img in enumerate(images):
    name = os.path.basename(img["path"])
    print(f"[{i+1}/{len(images)}] {name}")
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
        print(f"  OK: {size_kb:.0f}KB")
    except Exception as e:
        print(f"  FAIL: {e}")
    time.sleep(1)

print("\nDone. File sizes:")
for img in images:
    name = os.path.basename(img["path"])
    if os.path.exists(img["path"]):
        kb = os.path.getsize(img["path"]) / 1024
        print(f"  {name}: {kb:.0f}KB")
