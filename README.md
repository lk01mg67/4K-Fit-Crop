# 고해상도 이미지 4K 최적화 (Python)

이 스크립트는 `ImageMagick`을 활용하여 고해상도 이미지를 4K(3840x2160) 월페이퍼로 최적화합니다.  
**macOS**, **Linux**, **Windows** 환경을 모두 지원합니다.

## 기능
- **가로형 이미지**: 16:9 비율로 중앙 크롭 (Center Crop)
- **세로형 이미지**: 좌우 1px을 늘려 배경을 만들고 원본을 중앙에 배치 (1px Stretch + Blur)
- **파일명 정리**: `14000`, `10000`, `px` 등 불필요한 문자열 제거
- **자동 감지**: 시스템에 설치된 ImageMagick 버전(`magick` 또는 `convert`)을 자동으로 감지하여 실행

## 요구 사항 및 설치

### 1. Python (v3.10+)
스크립트는 **Python 3.10** 이상의 환경에서 테스트되었습니다.

### 2. ImageMagick (v7.1+)
이미지 프로세싱을 위해 ImageMagick이 필요합니다.
- **권장**: v7.1.0 이상 (`magick` 명령어 사용)
- **최소**: v6.9.0 이상 (`convert` 명령어 사용)

**macOS:**
```bash
brew install imagemagick
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install imagemagick
```

**Windows:**
```powershell
winget install ImageMagick.ImageMagick
```
*설치 시 **"Install legacy utilities (e.g. convert)"** 및 **"Add to PATH"** 옵션 체크를 권장합니다.*

## 사용 방법

```bash
# 1. 스크립트 실행
python3 optimize_4k.py

# 2. 생성된 Wallpaper 폴더 확인
```

## 폴더 구조 및 처리 방식

### 📁 입력: `Models`
스크립트는 `Models` 폴더를 재귀적으로 탐색하여 모든 `.jpg` 파일을 찾습니다.
- **구조**: `Models/이름/앨범명/사진.jpg` (예: `Models/Name/Album/001.jpg`)
- **처리**: 하위 폴더의 모든 이미지를 자동으로 찾아 처리합니다.

### 📁 출력: `output`
최적화된 이미지는 `output` 폴더에 저장됩니다.
- **파일명 생성 규칙**: `출력폴더/앨범명-파일명-4K.jpg`
- **충돌 방지**: 중복된 파일명을 방지하기 위해 **앨범명(상위 폴더명)**이 파일명 앞에 자동으로 붙습니다.
- **예시**: `Models/Name/Album/001.jpg` -> `output/Album-001-4K.jpg`

---
본 도구는 [optimize_4k.py](./optimize_4k.py) 스크립트를 통해 실행됩니다.