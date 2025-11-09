# Refund Canvas Taxpayer Registration

본 프로젝트는 국세청의 웹서비스인 홈택스에 동적 크롤링을 통해 공동인증서로 로그인한 뒤, 수임계약 요청을 한 납세자를 자동으로 등록해주는 프로그램입니다.

1. 홈택스 공동인증서 로그인
2. 세무법인 관리자 로그인
3. 수임계약 요청 납세자 등록

위 3단계의 수임 요청 프로세스를 자동화하기 위한 목적으로 설계되었습니다.

# 디렉토리 구조
```
├── schemas/
│   └── taxpayer.py                 # 납세자 스키마 정의
├── service/
│   ├── hometax-login.py            # 홈택스 공동인증서 로그인
│   └── taxpayer-registration.py    # 수임요청 납세자 등록
│   └── workflow.py                 # 전체 플로우 구성
├── main.py                    
├── requirements.txt           
└── README.md                  
```

# 납세자 정보 스키마
```
TaxPayer(
    # 사업자 유형 구분 (개인/법인/비사업자)
    client_type="individual_business",

    # 사업자등록번호 (XXX-XX-XXXXX 형식의 숫자 조합 정규식)
    business_registration_number="123-45-67890",
    
    # 주민등록번호 (XXXXXX-XXXXXXX 형식 정규식)
    resident_registration_number="900101-1234567",  # 주민등록번호
    
    # 성명 (2글자 이상 20글자 미만)
    name="김납세",
    
    # 전화번호 (XX-XXXX-XXXX 또는 XXX-XXX-XXXX 형식 정규식)
    phone_number="02-123-4567",
    
    # 휴대 전화번호 (01X-XXXX-XXXX 형식 정규식)
    mobile_number="010-9876-5432",
    
    # 유효한 이메일 형식
    email="nskim@example.com",
    
    # 수임 일자 (YYYY-MM-DD 형식 정규식)
    contract_date="2025-11-05"

    # 해임 일자 (YYYY-MM-DD 형식 정규식)
    dismissal_date: "2026-01-05"
)
```

### 사업자 유형 구분 관련

```
1. "individual_business" → 개인사업자"
2. "corporate_business" → 법인사업자
3. "non_business" → 비사업자
```

위 총 3가지 유형만 가능합니다.

# API 응답 코드
- 200: 정상 처리. 신규 등록이 완료되었거나 이미 등록된 납세자로 확인된 경우입니다.
- 400: 입력값 오류. 주민등록번호 또는 사업자등록번호가 잘못된 경우에 반환합니다.
- 500: 서버 내부 오류. 처리 중 예기치 못한 문제가 발생하면 `Internal Server Error` 와 함께 반환됩니다.


# 설치 및 실행방법

### 1. 사전 요구사항

- Python 3.11 이상
- pip

### 2. 프로젝트 클론

```bash
git clone <repository-url>
```

### 3. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

### 5. Playwright 브라우저 설치

```bash
playwright install chromium
```

### 6. 환경 변수 설정

`env.example` 을 참고하여 `.env` 파일을 생성합니다.

```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

### 7. 수임요청 자동화 서버 실행

```bash
python main.py
```