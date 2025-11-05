# Refund Canvas Taxpayer Registration
홈택스 자동 납세자 등록 프로그램

본 프로젝트는 국세청의 웹서비스인 홈택스에 동적 크롤링을 통해 로그인한 뒤, 수임계약 요청을 한 납세자를 자동으로 등록해주는 프로그램입니다.
즉, 자동으로 로그인 → 수임계약 요청 확인 → 납세자 등록까지의 흐름을 자동화하는 목적으로 설계되어 있습니다.

# 디렉토리 구조
```
├── schemas/
│   └── taxpayer.py                 # 납세자 스키마 정의
├── service/
│   ├── hometax-login.py            # 홈택스 로그인 자동화 코드
│   └── taxpayer-registration.py    # 납세자 등록 자동화 코드
│   └── workflow.py                 # 1번과 2번 통합 코드
├── main.py                    
├── requirements.txt           
└── README.md                  
```

# 납세자 정보 스키마
```
TaxPayer(
    # 사업자 유형 구분 (개인/법인/비사업자)
    client_type="individual_business",

    # 사업자등록번호 (XXX-XX-XXXXX 형식의 숫자 조합정규식)
    business_registration_number="123-45-67890",
    
    # 주민등록번호 (XXXXXX-XXXXXXX 형식)
    resident_registration_number="900101-1234567",  # 주민등록번호
    
    # 성명 (2글자 이상 20글자 미만)
    name="김납세",
    
    # 전화번호 (XXX-XXXX-XXXX 또는 XX-XXX-XXXX 형식 정규식)
    phone_number="02-123-4567",
    
    # 휴대 전화번호 (01X-XXXX-XXXX 형식 정규식)
    mobile_number="010-9876-5432",
    
    # 유효한 이메일 형식
    email="abc@example.com",
    
    # 수임 일자 (YYYY-MM-DD 형식)
    contract_date="2025-11-05"
)
```

### 사업자 유형 구분 관련

```
1. "individual_business" → 개인사업자"
2. "corporate_business" → 법인사업자
3. "non_business" → 비사업자
```

위 총 3가지 유형만 가능합니다.


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

`env.example`을 참고하여 `.env` 파일을 생성합니다:

```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```