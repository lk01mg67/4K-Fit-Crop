import os
import subprocess
import re
import shutil
import sys
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed

def get_imagemagick_cmds():
    """Detect ImageMagick version and return appropriate commands for processing and identification."""
    if shutil.which("magick"):
        # ImageMagick v7+: Use 'magick' for processing and 'magick identify' for metadata.
        return "magick", ["magick", "identify"]
    
    if shutil.which("convert") and shutil.which("identify"):
        # ImageMagick v6: 'convert' and 'identify' are separate standalone binaries.
        return "convert", ["identify"]
    
    print("❌ Error: ImageMagick not found in system PATH.")
    print("\nPlease install the required tools:")
    print(" - macOS: brew install imagemagick")
    print(" - Ubuntu/Debian: sudo apt install imagemagick")
    print(" - Fedora: sudo dnf install ImageMagick")
    print(" - Windows: winget install ImageMagick.ImageMagick")
    print("\nVisit https://imagemagick.org/script/download.php for more info.")
    sys.exit(1)


def process_image(root, filename, source_dir, output_dir, target_w, target_h, im_cmd, ident_cmd, ext):
    """
    Process a single image: horizontal images are center-cropped, 
    vertical images get a blurred 1px-stretched background.
    """
    valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
    if not filename.lower().endswith(valid_exts):
        return None

    input_path = os.path.join(root, filename)
    
    # Clean up filename (remove common bulk tags)
    base_name = os.path.splitext(filename)[0]
    clean_name = re.sub(r'(-?14000|-?10000|-?px)', '', base_name)
    
    # Generate prefix based on directory structure (Name-Album-File)
    rel_path = os.path.relpath(root, source_dir)
    if rel_path != '.':
        prefix = rel_path.replace(os.path.sep, '-')
        clean_name = f"{prefix}-{clean_name}"
    
    output_path = os.path.join(output_dir, f"{clean_name}-4K.{ext}")

    try:
        # Get image dimensions
        identify_res = subprocess.check_output(ident_cmd + ['-format', '%w %h', input_path])
        w, h = map(int, identify_res.decode().split())

        if w < h:
            # Vertical image: create blurred background from edges
            cmd = [
                im_cmd, input_path,
                '(', '-clone', '0', '-resize', 'x216',
                '(', '-clone', '0', '-gravity', 'West', '-crop', '1x0+0+0', '-resize', '1920x216!', ')',
                '(', '-clone', '0', '-gravity', 'East', '-crop', '1x0+0+0', '-resize', '1920x216!', ')',
                '-delete', '0', '-background', 'none', '+append', '-blur', '0x20', '-resize', f'{target_w}x{target_h}!', ')',
                '(', '-clone', '0', '-resize', f'x{target_h}', ')',
                '-delete', '0', '-gravity', 'center', '-compose', 'over', '-composite', '+repage',
                output_path
            ]
            method = "1px Stretch"
        else:
            # Horizontal image: center crop
            cmd = [
                im_cmd, input_path, 
                '-resize', f'{target_w}x{target_h}^', 
                '-gravity', 'center', 
                '-extent', f'{target_w}x{target_h}', 
                output_path
            ]
            method = "Center Crop"

        subprocess.run(cmd, check=True)
        return f"✅ {filename} -> {os.path.basename(output_path)} [{method}]"
    except Exception as err:
        return f"❌ {filename} Error: {err}"


def main():
    """Main execution entry point."""
    parser = argparse.ArgumentParser(description="Parallel 4K Image Optimizer using ImageMagick")
    parser.add_argument("--input", default="Models", help="Input directory (default: Models)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    parser.add_argument("--width", type=int, default=3840, help="Target width (default: 3840)")
    parser.add_argument("--height", type=int, default=2160, help="Target height (default: 2160)")
    parser.add_argument("--format", default="jpg", choices=["jpg", "png", "webp"], help="Format (default: jpg)")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers (default: 4)")
    
    args = parser.parse_args()

    im_cmd, ident_cmd = get_imagemagick_cmds()
    print(f"🚀 Initializing optimization: {args.width}x{args.height} [{args.format}]")
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Collect all valid image paths
    image_tasks = []
    for root, _, files in os.walk(args.input):
        for f in files:
            image_tasks.append((root, f))

    if not image_tasks:
        print(f"⚠️ No images found in '{args.input}'.")
        return

    print(f"� Found {len(image_tasks)} items. Processing in parallel...")
    
    processed_count = 0
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(
                process_image, r, f, args.input, args.output, 
                args.width, args.height, im_cmd, ident_cmd, args.format
            ): f for r, f in image_tasks
        }
        
        for future in as_completed(futures):
            res = future.result()
            if res:
                print(res)
                if "✅" in res:
                    processed_count += 1

    print(f"\n✨ Successfully optimized {processed_count} images.")


if __name__ == "__main__":
    main()
