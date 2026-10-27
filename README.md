# RIDI PAPER PRO · Chromium M58 WebView

RIDI Android 8 제품의 커스텀 WebView 소스입니다. Chromium 58.0.3029.125 기반으로
Android O 연동과 RIDI E Ink의 소프트웨어 우선 렌더링 경로를 보존합니다.

**전체 프로젝트:** [메인 manifest 저장소](https://github.com/INO-33/ridi-paper-pro)

## 보관 범위

- `android_webview/`: WebView 본체와 Android 연동
- `content/`: RIDI 제품 경로에 필요한 Chromium 변경
- `ridi-dependencies/`: Breakpad·SwiftShader의 RIDI 변경 패키지
- `docs/UPSTREAM_README.md`: 원본 Chromium 소스 안내

제품 소스와 두 의존성 변경을 이 저장소 하나로 관리합니다. 원본 커밋은
`c254b52f7661657df3d56ff997030fc36988c9cd`이며, 실제 사용할 제품 커밋은 메인
`release-lock.json`에 고정됩니다. 기존 upstream-tree 기준과 과거 이력도 보존합니다.

## 소스 준비와 빌드

먼저 메인 저장소에서 Android 작업 폴더와 `env.sh`를 준비한 뒤, 메인 저장소
폴더에서 실행합니다.

```sh
python3 prepare-chromium.py "$RIDI_WORKSPACE"
CHROMIUM_SRC_ROOT="$RIDI_WORKSPACE/chromium-m58/src" \
DEPOT_TOOLS_ROOT="$RIDI_WORKSPACE/depot_tools" \
"$RIDI_WORKSPACE/tools/chromium-m58-build/build_m58_xenial_arm.sh"
```

x86은 `build_m58_xenial_x86.sh`를 사용합니다. 빌드 스크립트와 Ubuntu Xenial용
Dockerfile은 [빌드 도구 저장소](https://github.com/INO-33/ridi-paper-pro-dev-tools)의
`tools/chromium-m58-build/`에 있습니다. Docker와 외부 Chromium 의존성 다운로드가
필요하며 로그는 작업 폴더의 `.orchestrator/logs/`에 남습니다.

준비 스크립트는 고정 depot_tools/DEPS 원본을 받고 두 의존성 변경을 적용한 뒤
소스 트리를 검사합니다. 독립 의존성 보관 저장소를 별도로 받을 필요는 없습니다.

## Android 제품과의 관계

Android 이미지 빌드는 기기 저장소에 보존한 WebView APK를 사용합니다. 이 소스의
재빌드 결과와 그 APK의 일치는 별도 검증 대상이며, 소스 체크포인트 업로드가
새 APK 빌드/설치를 의미하지는 않습니다. 이번 작업에서 렌더러 동작이나 제품
그래픽 기본 경로를 추가로 변경하지 않았습니다.

체크포인트: **2026-10-27**. 오래된 DEPS·컨테이너 패키지의 장기 보존 및 새 환경
전체 재빌드는 추가 검증 항목입니다. Chromium 라이선스는 [`LICENSE`](LICENSE)를
따릅니다.

## 개발환경과 공개 전 자산 검토

처음 구성하는 개발자는 메인 저장소의 [개발환경 구축 안내](https://github.com/INO-33/ridi-paper-pro/blob/checkpoint-20261016/DEVELOPMENT.md)를 따릅니다.
공개 전 제외·확인 대상은 [공개 자산 목록](https://github.com/INO-33/ridi-paper-pro/blob/checkpoint-20261016/PUBLIC_ASSETS.md)에 있습니다.


## 사용 대상과 라이선스

기존 리디 페이퍼 프로 사용자를 위한 프로젝트입니다. [LICENSING.md](LICENSING.md)와
[DEVICE_ASSETS.md](DEVICE_ASSETS.md)를 확인하세요. 타 기기 포팅에서는 기기 유래 자산을 제외합니다.
기존 코드·드라이버·폰트의 오픈소스 라이선스는 그대로 유지합니다.
과거 포팅 기록과 설명이 다를 경우 이 라이선스 문서와 메인 PUBLIC_ASSETS.md의 최신 검토를 기준으로 합니다.
