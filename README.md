# 고해상도 이미지 4K 최적화 (Python)

> **Vibe Coding**으로 생성된 프로젝트입니다.

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

_설치 시 **"Install legacy utilities (e.g. convert)"** 및 **"Add to PATH"** 옵션 체크를 권장합니다._

### 3. Python 패키지 설치 (선택 사항)

스크립트 실행을 위한 환경을 설정합니다. (표준 라이브러리만 사용하므로 필수 단계는 아닙니다.)

```bash
# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 의존성 패키지 설치
pip install -r requirements.txt
```

## 폴더 구조 및 처리 방식

### 📁 입력: `Models`

스크립트는 `Models` 폴더를 재귀적으로 탐색하여 모든 이미지 파일(`.jpg`, `.jpeg`, `.png`)을 찾습니다.

- **구조**: `Models/이름/앨범명/이미지` (예: `Models/Name/Album/Number.jpg`)
- **처리**: 하위 폴더의 모든 이미지를 자동으로 찾아 처리합니다.

### 📁 출력: `output`

최적화된 이미지는 `output` 폴더에 저장됩니다.

- **파일명 생성 규칙**: `출력폴더/이름-앨범명-파일명-4K.jpg`
- **충돌 방지**: 중복된 파일명을 방지하기 위해 **상위 폴더 구조(이름 및 앨범명)**가 파일명 앞에 자동으로 붙습니다.
- **예시**: `Models/Name/Album/Number.jpg` -> `output/Name-Album-Number-4K.jpg`

## 사용 방법

```bash
# 1. 스크립트 실행
python3 optimize_4k.py

# 2. 생성된 output 폴더 확인
```

## 라이선스

이 프로젝트는 [MIT](LICENSE) 라이선스에 따라 라이선스가 부여됩니다.
