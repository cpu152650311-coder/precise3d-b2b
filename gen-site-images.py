"""
gen-site-images.py — GPT Image 2 batch image generator
Uses requests library (not OpenAI SDK) to avoid pydantic conflicts.
Supports both URL and base64 response formats.
Model: gpt-image-2. Quality: low by default.
Automatically falls back to api.inferera.com if aihubmix is unreachable.
"""

import os, sys, json, time, argparse, base64, io
from pathlib import Path
import requests
from PIL import Image

MODEL = "gpt-image-2"
BASE_URLS = [
    "https://aihubmix.com/v1",
    "https://api.inferera.com/v1",
]

def get_api_key():
    for env_var in ("AIHUBMIX_API_KEY",):
        key = os.getenv(env_var, "").strip()
        if key:
            return key
    # Fallback: try reading from .env files
    for env_path in (
        os.path.expandvars(r"%LOCALAPPDATA%\hermes\.env"),
        os.path.expanduser("~/.hermes/.env"),
    ):
        try:
            with open(env_path) as f:
                for line in f:
                    if line.startswith("AIHUBMIX_API_KEY="):
                        return line.strip().split("=", 1)[1].strip("'\"")
        except FileNotFoundError:
            continue
    return ""

def generate_image(api_key, base_url, prompt, size="1024x1024"):
    """Generate image using GPT Image 2, supporting both URL and base64 formats."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': MODEL,
        'prompt': prompt,
        'n': 1,
        'size': size
    }
    
    try:
        response = requests.post(
            f"{base_url}/images/generations",
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            image_data = data['data'][0]
            
            if 'url' in image_data:
                img_response = requests.get(image_data['url'], timeout=60)
                return img_response.content
            elif 'b64_json' in image_data:
                return base64.b64decode(image_data['b64_json'])
            else:
                print(f"  Error: No image data in response")
                return None
        else:
            print(f"  Error: Unexpected response format: {data}")
            return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def save_image(image_bytes, output_path):
    """Save image bytes as WebP format."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.save(output_path, 'WEBP', quality=90)
        return True
    except Exception as e:
        print(f"  Save error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", default="image-prompts.json")
    parser.add_argument("--out", default="./generated")
    parser.add_argument("--manifest", default=None, help="Existing manifest to merge into")
    parser.add_argument("--delay", type=int, default=3)
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("ERROR: AIHUBMIX_API_KEY not set.")
        sys.exit(1)

    prompts_path = Path(args.prompts)
    if not prompts_path.exists():
        print(f"ERROR: {prompts_path} not found")
        sys.exit(1)

    data = json.loads(prompts_path.read_text(encoding="utf-8"))

    if isinstance(data, list):
        images = data
    elif isinstance(data, dict) and "images" in data:
        images = data["images"]
    else:
        images = [data]

    output_dir = Path(args.out)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {}
    if args.manifest and Path(args.manifest).exists():
        manifest = json.loads(Path(args.manifest).read_text())

    success = 0
    failed = 0

    # Find working endpoint
    working_url = None
    for base_url in BASE_URLS:
        try:
            test_headers = {'Authorization': f'Bearer {api_key}'}
            response = requests.get(f"{base_url}/models", headers=test_headers, timeout=10)
            if response.status_code == 200:
                working_url = base_url
                print(f"Connected: {base_url}")
                break
        except:
            continue

    if not working_url:
        print("ERROR: All endpoints unreachable. Check VPN/proxy.")
        sys.exit(1)

    for item in images:
        img_id = item.get("id", f"image-{success+failed}")
        subject = item.get("subject", item.get("prompt", ""))
        size = f"{item.get('width', 1024)}x{item.get('height', 1024)}"

        if size not in ("1024x1024",):
            print(f"  Warning: {img_id} size={size} -> 1024x1024")
            size = "1024x1024"

        print(f"[{img_id}] {subject[:60]}...")
        image_bytes = generate_image(api_key, working_url, subject, size)
        if image_bytes:
            out_path = output_dir / f"{img_id}.webp"
            if save_image(image_bytes, str(out_path)):
                manifest[img_id] = {"local": str(out_path)}
                print(f"  OK {out_path}")
                success += 1
            else:
                failed += 1
        else:
            failed += 1

        if item != images[-1]:
            time.sleep(args.delay)

    # Save manifest
    manifest_path = output_dir / "image-manifest.json"
    json.dump(
        {"generated": success, "failed": failed, "images": manifest},
        open(manifest_path, "w", encoding="utf-8"),
        indent=2,
    )
    print(f"\nDone: {success} ok, {failed} failed -> {manifest_path}")


if __name__ == "__main__":
    main()
