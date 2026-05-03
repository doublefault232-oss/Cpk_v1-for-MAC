# Cpk 분석 및 보고서 생성 프로그램

## 프로젝트 개요
이 프로그램은 엑셀 파일을 업로드하여 공정능력지수(Cpk)를 분석하고, 보고서를 생성합니다. 주요 기능은 다음과 같습니다:

- Cpk 계산 및 분석
- USL/LSL 표시
- IMR 차트 생성
- 미니탭 스타일의 그래프 및 보고서 출력
- 엑셀 파일의 시트별 분석

## 설치 및 실행 방법

1. Python 가상 환경 생성 및 활성화 (선택 사항):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. 필수 라이브러리 설치:
   ```bash
   pip install pandas openpyxl numpy matplotlib streamlit
   ```

3. Streamlit 웹 애플리케이션 실행:
   ```bash
   streamlit run app.py
   ```
   또는 (가상 환경을 사용하지 않는 경우):
   ```bash
   /usr/local/bin/python3 -m streamlit run app.py
   ```

   앱이 실행되면 웹 브라우저에서 `http://localhost:8501`로 접속하여 확인할 수 있습니다.

## 파일 구조
- `main.py`: 프로그램의 진입점
- `cpk_analysis.py`: Cpk 계산 및 분석 로직
- `report_generator.py`: 보고서 생성 로직
- `requirements.txt`: 필요한 라이브러리 목록

## 배포
다른 사용자도 쉽게 사용할 수 있도록 패키징 및 배포 가능합니다.