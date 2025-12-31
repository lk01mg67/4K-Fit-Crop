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
    
    source_dir = '.'
    output_dir = 'output'
    target_width = 3840
    target_height = 2160

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 현재 디렉토리의 jpg 파일 목록
    files = [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg') and os.path.isfile(f)]
    
    for f in files:
        if f == 'optimize_4k.py': continue
        
        # 파일명 정리
        clean_name = re.sub(r'(-?14000|-?10000|-?px)', '', os.path.splitext(f)[0])
        output = os.path.join(output_dir, f"{clean_name}-4K.jpg")

        try:
            # 이미지 크기 확인
            dim = subprocess.check_output([im_cmd, 'identify', '-format', '%w %h', f]).decode().split()
            w, h = int(dim[0]), int(dim[1])

            if w < h:
                # [세로형] 1px 스트레치 + 블러 배경
                cmd = [
                    im_cmd, f,
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
                    im_cmd, f, 
                    '-resize', f'{target_width}x{target_height}^', 
                    '-gravity', 'center', 
                    '-extent', f'{target_width}x{target_height}', 
                    output
                ]
                method = "Center Crop"

            subprocess.run(cmd, check=True)
            print(f"✅ 성공: {f} -> {output} [{method}]")
        except Exception as e:
            print(f"❌ 오류: {f} ({e})")

if __name__ == "__main__":
    optimize_images()