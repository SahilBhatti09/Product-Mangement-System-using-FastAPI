from pydantic import (BaseModel, # Base class for all models
Field, # Field class for all fields
AnyUrl, # AnyUrl class for all URLs
field_validator, # field_validator class for all field validators - used to validate individual fields
model_validator, # model_validator class for all model validators - used to validate the entire model
computed_field, # computed_field class for all computed fields - used to compute the value of a field
EmailStr, # EmailStr class for all email addresses
)
from typing import Annotated, Literal, Optional, List
from uuid import UUID
from datetime import datetime

#============================================== CREATE PRODUCT PYDANTIC MODEL ==============================================
class Seller(BaseModel):
    seller_id: UUID
    seller_name: Annotated [
        str,
        Field(
            min_length=2, 
            max_length=60, 
            title="Seller Name", 
            description="Name of the seller", 
            example="Mi Store")]
    seller_email: Annotated [
        EmailStr,
        Field(
            min_length=3, 
            max_length=100, 
            title="Seller Email", 
            description="Seller email address", 
            example="support@xiaomi.com")]
    seller_website: Annotated [
        AnyUrl,
        Field(
            min_length=3, 
            max_length=100, 
            title="Seller Website", 
            description="Seller website URL", 
            example="https://www.xiaomi.com")]
 
@field_validator("seller_email")
@classmethod
def validate_seller_email_domain(cls, value: EmailStr):
    allowed_domains = {
        "email.com",
        "gmail.com",
        "fccollege.edu.pk",
        "formanite.fccollege.edu.pk"
    }

    domain = value.split("@")[-1]

    if domain not in allowed_domains:
        raise ValueError(
            f"Email domain '{domain}' not allowed. Allowed: {allowed_domains}"
        )
    return value


class Dimensions(BaseModel):
    length: Annotated [
        float,
        Field(gt=0, strict=True, description="Length of the product in cm")]
    width: Annotated [
        float,
        Field(gt=0, strict=True, description="Width of the product in cm")]
    height: Annotated [
        float,
        Field(gt=0, strict=True, description="Height of the product in cm")]


class Product(BaseModel):
    id: UUID 
    #sku: str = "2323-2323-2323"
    sku: Annotated [
        str,
        Field(
            min_length=6, 
            max_length=100, 
            title="SKU", 
            description="The stock keeping unit of the product", 
            example="XIAO-359GB-001")]
    name: Annotated [
        str,
        Field(
            min_length=3, 
            max_length=100, 
            title="Product Name", 
            description="Readable product name", 
            example="Xiaomi Model Pro")]
    description: Annotated [
        str,
        Field(min_length=6, 
        max_length=100, 
        title="SKU", 
        description="Short Product description")]
    category: Annotated [
        str,
        Field(min_length=3, 
        max_length=100, 
        title="Category", 
        example="electronics")]
    brand: Annotated [
        str,
        Field(min_length=3, 
        max_length=100, 
        title="Brand Name", 
        example="Apple Inc.")]
    price: Annotated [
        float,
        Field(ge=0, description="Base price in PKR", example=2000.00)]
    currency: Literal["PKR"] = "PKR"
    discount_percent: Annotated [
        int,
        Field(ge=0, le=90, description="The discount percent of the product",)]=0
    stock: Annotated [
        int,
        Field(ge=0, description="Available stock of the product",)]
    is_active: Annotated [
        bool,
        Field(description="Is the product is active or not",)]
    rating: Annotated [
        float,
        Field(ge=0, le=5, strict=True, description="The rating of the product out of 5",)]=0
    tags: Annotated [
        Optional[List[str]],
        Field(default=None,
        max_items=10, 
        description="Upto 10 tags for the product",)]
    image_urls: Annotated [
        List[AnyUrl],
        Field(max_length=1, 
        description="Atleast 1 image URL for the product",)]
    dimensions_cm: Dimensions
    seller: Seller
    created_at: datetime

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku(cls, value:str):
        if "-" not in value:
            raise ValueError("SKU must contain a hyphen '-'.")

        last = value.split("-")[-1]
        if not len(last) == 3 and last.isdigit():
            raise ValueError("SKU must end with 3 digits sequence like '001'.")

        return value

    @model_validator(mode="after")
    @classmethod
    def validate_bussiness_rules(cls, model:"Product"):
        if model.stock == 0 and model.is_active:
            raise ValueError("Stock is 0, is_active must be fasle.")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discount product must have a rating.")

        return model

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)

    @computed_field
    @property
    def product_volume(self) -> float:
        return (self.dimensions_cm.length * self.dimensions_cm.width * self.dimensions_cm.height)

#============================================== UPDATE PRODUCT PYDANTIC MODEL ==============================================
class SellerUpdate(BaseModel):
    seller_name: Optional[str] = None
    seller_email: Optional[EmailStr] = None
    seller_website: Optional[AnyUrl] = None


class DimensionsUpdate(BaseModel):
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    discount_percent: Optional[int] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    rating: Optional[float] = None
    tags: Optional[list[str]] = None
    image_urls: Optional[list[AnyUrl]] = None
    dimensions_cm: Optional[DimensionsUpdate] = None
    seller: Optional[SellerUpdate] = None
