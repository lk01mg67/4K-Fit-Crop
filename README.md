# 고해상도 이미지 4K 최적화 (Python)

이 스크립트는 `ImageMagick`을 활용하여 고해상도 이미지를 4K(3840x2160) 월페이퍼로 최적화합니다.

## 기능
- **가로형 이미지**: 16:9 비율로 중앙 크롭 (Center Crop)
- **세로형 이미지**: 좌우 1px을 늘려 배경을 만들고 원본을 중앙에 배치 (1px Stretch + Blur)
- **파일명 정리**: `14000`, `10000`, `px` 등 불필요한 문자열 제거

## 요구 사항
- Python 3
- ImageMagick (`brew install imagemagick`)

## 코드 (`optimize_4k.py`)

```python
import os
import subprocess
import re

# 대형 이미지 처리를 위해 ImageMagick 사용 (Pillow보다 속도 및 대형 파일 처리에 유리)

def optimize_images():
    source_dir = '.'
    output_dir = 'Wallpaper-4K'
    target_width = 3840
    target_height = 2160

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 현재 디렉토리의 jpg 파일 목록
    files = [f for f in os.listdir(source_dir) if f.lower().endswith('.jpg') and os.path.isfile(f)]
    
    for f in files:
        if f == 'optimize_4k.py': continue
        
        # 파일명 정리: 14000, 10000, px 제거
        clean_name = re.sub(r'(-?14000|-?10000|-?px)', '', os.path.splitext(f)[0])
        output = os.path.join(output_dir, f"{clean_name}-4K.jpg")

        try:
            # 이미지 크기 확인
            dim = subprocess.check_output(['magick', 'identify', '-format', '%w %h', f]).decode().split()
            w, h = int(dim[0]), int(dim[1])

            if w < h:
                # [세로형] 1px 스트레치 + 블러 배경 합성 (가장 자연스러운 결과)
                cmd = [
                    'magick', f,
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
                # [가로형] 중앙 크롭 (16:9 4K 최적화)
                cmd = [
                    'magick', f, 
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
```
