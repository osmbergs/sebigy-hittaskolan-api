from datetime import datetime
from typing import Optional, Dict, Union, List

from pydantic import BaseModel, json, Field

from app.models.school import SchoolType, SchoolStatus


class SchoolRequestBaseSchema(BaseModel):

    pass






class SchoolRequestCreateSchema(SchoolRequestBaseSchema):

    school_unit_code: Optional[str] = Field(None)

    name: Optional[str] = Field(None)

class SchoolRequestUpdateSchema(SchoolRequestBaseSchema):
    status: Optional[SchoolStatus] = Field(None)
    types: Union[Optional[Dict], List[Optional[Dict]], List[Optional[str]]]
    school_unit_code: Optional[str] = Field(None)
    created: Optional[datetime] = Field(None)
    updated: Optional[datetime] = Field(None)

    name: Optional[str] = Field(None)
    display_name: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    headmaster: Optional[str] = Field(None)
    municipality_code: Optional[str] = Field(None)

    visit_address_street: Optional[str] = Field(None)
    visit_address_postal_code: Optional[str] = Field(None)
    visit_address_locality: Optional[str] = Field(None)
    geo_lat: Optional[str] = Field(None)
    geo_long: Optional[str] = Field(None)





class SchoolResponseBaseSchema(BaseModel):
    status: Optional[SchoolStatus] = Field(None)
    types: Optional[dict] = Field(None)
    school_unit_code: Optional[str] = Field(None)
    created: Optional[datetime] = Field(None)
    updated: Optional[datetime] = Field(None)

    name: Optional[str] = Field(None)
    display_name: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    headmaster: Optional[str] = Field(None)
    municipality_code: Optional[str] = Field(None)

    visit_address_street: Optional[str] = Field(None)
    visit_address_postal_code: Optional[str] = Field(None)
    visit_address_locality: Optional[str] = Field(None)
    geo_lat: Optional[str] = Field(None)
    geo_long: Optional[str] = Field(None)


class Config:
        orm_mode = True


class SchoolResponseListSchema(SchoolResponseBaseSchema):
    pass






class SchoolResponseFullSchema(SchoolResponseBaseSchema):
    pass


SchoolResponseBaseSchema.update_forward_refs()

class SchoolRefreshData(BaseModel):
    no_created:int
    no_updated:int