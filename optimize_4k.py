import os
import subprocess
import re
import shutil
import sys

def get_imagemagick_cmd():
    """ImageMagick 명령어 감지 (v7: magick, v6: convert)"""
    if shutil.which("magick"):
        return "magick"
    elif shutil.which("convert"):
        return "convert"
    else:
        print("❌ 오류: ImageMagick이 설치되어 있지 않습니다.")
        sys.exit(1)

def optimize_images():
    im_cmd = get_imagemagick_cmd()
    print(f"ℹ️  감지된 ImageMagick 명령어: {im_cmd}")
    
    source_dir = 'Models'
    output_dir = 'output'
    target_width = 3840
    target_height = 2160

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Models 폴더 재귀 탐색
    count = 0
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if not f.lower().endswith('.jpg'): continue
            
            input_path = os.path.join(root, f)
            
            # 파일명 정리
            clean_name = re.sub(r'(-?14000|-?10000|-?px)', '', os.path.splitext(f)[0])
            
            # 충돌 방지를 위해 앨범명(부모 폴더)을 파일명에 포함
            album_name = os.path.basename(root)
            if album_name and album_name != source_dir:
                clean_name = f"{album_name}-{clean_name}"
            
            output = os.path.join(output_dir, f"{clean_name}-4K.jpg")

            try:
                # 이미지 크기 확인
                dim = subprocess.check_output([im_cmd, 'identify', '-format', '%w %h', input_path]).decode().split()
                w, h = int(dim[0]), int(dim[1])

                if w < h:
                    # [세로형] 1px 스트레치 + 블러 배경
                    cmd = [
                        im_cmd, input_path,
                        '(', '-clone', '0', '-resize', 'x216',
                        '(', '-clone', '0', '-gravity', 'West', '-crop', '1x0+0+0', '-resize', '1920x216!', ')',
                        '(', '-clone', '0', '-gravity', 'East', '-crop', '1x0+0+0', '-resize', '1920x216!', ')',
                        '-delete', '0', '-background', 'none', '+append', '-blur', '0x20', '-resize', '3840x2160!', ')',
                        '(', '-clone', '0', '-resize', f'x{target_height}', ')',
                        '-delete', '0', '-gravity', 'center', '-compose', 'over', '-composite', '+repage',
                        output
                    ]
                    method = "1px Stretch Background"
                else:
                    # [가로형] 중앙 크롭
                    cmd = [
                        im_cmd, input_path, 
                        '-resize', f'{target_width}x{target_height}^', 
                        '-gravity', 'center', 
                        '-extent', f'{target_width}x{target_height}', 
                        output
                    ]
                    method = "Center Crop"

                subprocess.run(cmd, check=True)
                print(f"✅ 성공: {f} -> {output} [{method}]")
                count += 1
            except Exception as e:
                print(f"❌ 오류: {f} ({e})")

    if count == 0:
        print("⚠️  처리할 JPG 이미지를 찾지 못했습니다.")
    else:
        print(f"✨ 총 {count}장의 이미지가 최적화되었습니다.")

if __name__ == "__main__":
    optimize_images()
