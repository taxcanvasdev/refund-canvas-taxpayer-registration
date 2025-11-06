from pydantic import BaseModel, Field, EmailStr
from typing import Literal
from datetime import date

class TaxPayer(BaseModel):
    """세무대리의뢰인 등록 요청 스키마"""
    
    # 사업자 유형구분
    client_type: Literal["individual_business", "corporate_business", "non_business"] = Field(
        ...,
        description="유형구분: individual_business(개인사업자), corporate_business(법인사업자), non_business(비사업자)"
    )
    
    # 사업자등록번호 (개인/법인사업자인 경우)
    business_registration_number: str = Field(
        "000-00-00000",
        description="사업자등록번호 (XXX-XX-XXXXX 형식)",
        pattern=r"^\d{3}-\d{2}-\d{5}$"
    )
    
    # 주민등록번호
    resident_registration_number: str = Field(
        ...,
        description="주민등록번호 (XXXXXX-XXXXXXX 형식)",
        pattern=r"^\d{6}-\d{7}$"
    )
    
    # 성명
    name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="성명"
    )
    
    # 전화번호
    phone_number: str = Field(
        description="전화번호 (XXX-XXXX-XXXX 형식)",
        pattern=r"^\d{2,4}-\d{3,4}-\d{4}$"
    )
    
    # 휴대전화번호
    mobile_number: str = Field(
        ...,
        description="휴대전화번호 (XXX-XXXX-XXXX 형식)",
        pattern=r"^01[0-9]-\d{3,4}-\d{4}$"
    )
    
    # 이메일주소
    email: EmailStr = Field(
        ...,
        description="이메일주소"
    )
    
    # 신고대리 세목 (증여세/양도소득세 중 택1)
    tax_type: Literal["gift_tax", "capital_gains_tax"]

    # 수임일자(YYYY-MM-DD 형식)
    contract_date: str

    # 해임일자(YYYY-MM-DD 형식)
    dismissal_date: str