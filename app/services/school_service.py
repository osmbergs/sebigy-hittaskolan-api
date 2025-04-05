import logging
import time

import requests
from fastapi import Depends, HTTPException, Security
from fastapi_pagination import Params
from psycopg import connect
from sqlalchemy import text

from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from requests.adapters import HTTPAdapter, Retry

from app.core import dt_utils
from app.core.auth_util import auth, RequestContext

from app.core.id_generator import new_id


from app.core.deps import get_db


from app.models.school import School, SchoolType, SchoolStatus
from app.schemas.school import SchoolRequestCreateSchema, SchoolRefreshData, SchoolRequestUpdateSchema
from app.services.base_service import BaseService





def get_school_service(
    db: Session = Depends(get_db),
    ctx=Security(auth.verify),
) -> "SchoolService":
    schoolService = SchoolService(db,ctx)

    return schoolService

class SchoolService(BaseService):




    def __init__(
        self,
        db: Session,
        ctx:RequestContext
    ):
        super().__init__(db,ctx)


    def get_school_by_id(self, id: str) -> School:
        school = self._db.query(School).filter(School.id == id).first()
        if not school:
            raise HTTPException(status_code=404, detail="Not found")
        return school




    def _get_school_type_code(school_type:SchoolType):
        if school_type==SchoolType.Preliminary:
            return "FKLASS"
        if school_type==SchoolType.Elementary:
            return "GR"
        if school_type==SchoolType.ElementaryOther:
            return "GRAN"
        if school_type==SchoolType.Recreational:
            return "FTH"
        if school_type==SchoolType.RecreationalOpen:
            return "OPPFTH"
        if school_type==SchoolType.Special:
            return "SP"
        if school_type==SchoolType.Minority:
            return "SAM"
        if school_type == SchoolType.Secondary:
            return "GY"
        if school_type==SchoolType.SecondaryOther:
            return "GYAN"
        if school_type==SchoolType.Adult:
            return "VUX"




        raise Exception("Illegal school type "+str(school_type)+" passed")



    def _get_school_type(self,school_type_code:str):
        if school_type_code=="FKLASS":
            return str(SchoolType.Preliminary)
        if school_type_code=="GR":
            return str(SchoolType.Elementary)
        if school_type_code=="GRAN":
            return str(SchoolType.ElementaryOther)
        if school_type_code=="FTH":
            return str(SchoolType.Recreational)
        if school_type_code=="OPPFTH":
            return str(SchoolType.RecreationalOpen)
        if school_type_code=="SP":
            return str(SchoolType.Special)
        if school_type_code=="SAM":
            return str(SchoolType.Minority)
        if school_type_code=="GY":
            return str(SchoolType.Secondary)
        if school_type_code=="GYAN":
            return str(SchoolType.SecondaryOther)
        if school_type_code=="VUX":
            return str(SchoolType.Adult)





    def get_schools(self,     pagination_params: Params, municipality_code:str,school_type:SchoolType):


        query = self._db.query(School)

        query = query.filter(School.municipality_code==municipality_code)
#        query = query.filter(School.type == self._get_school_type_code(school_type))

        ret=paginate(query,pagination_params)



        return ret







    def create_school(self,create_data:SchoolRequestCreateSchema ) -> School:


        new_school = School()
        new_school.id = new_id()

        new_school.status=SchoolStatus.active

        if create_data.name:
            new_school.name = create_data.name


        if create_data.school_unit_code:
            new_school.school_unit_code=create_data.school_unit_code



        new_school.created = dt_utils.now()
        new_school.updated = dt_utils.now()


        self.save(new_school)

        return new_school



    def update_school(self, id:str, update_data: SchoolRequestUpdateSchema) -> School:


        school=self.get_school_by_id(id)




        if update_data.display_name:
            school.display_name = update_data.display_name


        if update_data.types:
            school.types = update_data.types

        if update_data.school_unit_code:
            school.school_unit_code = update_data.school_unit_code

        if update_data.url:
            school.url = update_data.url

        if update_data.email:
            school.email = update_data.email

        if update_data.phone:
            school.phone = update_data.phone

        if update_data.municipality_code:
            school.municipality_code = update_data.municipality_code

        if update_data.headmaster:
            school.headmaster = update_data.headmaster

        if update_data.visit_address_postal_code:
            school.visit_address_postal_code = update_data.visit_address_postal_code

        if update_data.visit_address_street:
            school.visit_address_street = update_data.visit_address_street

        if update_data.visit_address_locality:
            school.visit_address_locality = update_data.visit_address_locality

        if update_data.geo_lat:
            school.geo_lat = update_data.geo_lat
        if update_data.geo_long:
            school.geo_long = update_data.geo_long

        school.full_data=True

        school.updated = dt_utils.now()

        self.save(school)

        return school


    def admin_refresh_incomplete(self):

        query = self._db.query(School)

        query = query.filter(School.full_data == False)

        for school in query.all():
            self.admin_refresh_one(school.id)





    def admin_refresh_one(self,id:str) -> SchoolRefreshData:


        logging.info("Refreshing for id "+id)
        API_URL = "https://api.skolverket.se/skolenhetsregistret/v2"

        headers = {
            "Content-Type": "application/json",

        }

        school=self.get_school_by_id(id)




        res = requests.get(API_URL + "/school-units/" + school.school_unit_code,headers=headers)

        details = res.json()["data"]["attributes"]

        school_types = []
        for stc in details["schoolTypes"]:
            school_types.append(self._get_school_type(stc))

        update_data = SchoolRequestUpdateSchema(
            types=school_types,
            display_name=details["displayName"],
            url=details["url"] if "url" in details else None,
            email=details["email"] if "email" in details else None,
            phone=details["phoneNumber"],
            headmaster=details["headMaster"] if "headMaster" in details else None,
            visit_address_postal_code=details["addresses"][0]["postalCode"],
            visit_address_street=details["addresses"][0]["streetAddress"],
            visit_address_locality=details["addresses"][0]["locality"],
            geo_lat=details["addresses"][0]["geoCoordinates"]["latitude"] if "geoCoordinates" in
                                                                             details["addresses"][
                                                                                 0] and "latitude" in
                                                                             details["addresses"][0][
                                                                                 "geoCoordinates"] else None,
            geo_long=details["addresses"][0]["geoCoordinates"]["longitude"] if "geoCoordinates" in
                                                                               details["addresses"][
                                                                                   0] and "longitude" in
                                                                               details["addresses"][0][
                                                                                   "geoCoordinates"] else None,

            )
        self.update_school(id,update_data)


        return school

    def admin_recreate_all(self) -> SchoolRefreshData:

        self._db.execute(text('TRUNCATE TABLE school'))

        API_URL="https://api.skolverket.se/skolenhetsregistret/v2"



        headers = {
            "Content-Type": "application/json",

        }
        all_schools = requests.get(
            API_URL+"/school-units?status=AKTIV"

        )
        no_created=0
        for school in all_schools.json()["data"]["attributes"]:
            logging.info("Saving school "+str(school["name"]))





            create_data=SchoolRequestCreateSchema(
                name=school["name"],
             #   types=school_types,
                school_unit_code=school["schoolUnitCode"],
              #  display_name=details["displayName"],
               # url=details["url"] if "url" in details else None,
                #email=details["email"],
              #  phone=details["phoneNumber"],
              #  headmaster=details["headMaster"] if "headMaster" in details else None,
               # municipality_code=details["municipalityCode"],
               # visit_address_postal_code=details["addresses"][0]["postalCode"],
              #  visit_address_street=details["addresses"][0]["streetAddress"],
              #  visit_address_locality=details["addresses"][0]["locality"],
              #  geo_lat=details["addresses"][0]["geoCoordinates"]["latitude"] if "geoCoordinates" in details["addresses"][0] and "latitude" in details["addresses"][0]["geoCoordinates"] else None,
              #  geo_long=details["addresses"][0]["geoCoordinates"]["longitude"] if "geoCoordinates" in details["addresses"][0] and "longitude" in details["addresses"][0]["geoCoordinates"] else None,

            )
            self.create_school(create_data)
            no_created=no_created+1

        return SchoolRefreshData(no_created=no_created,no_updated=no_created)



    def save(self, data: School) -> None:
        self._db.add(data)
        self._db.commit()


