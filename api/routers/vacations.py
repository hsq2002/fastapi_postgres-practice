from fastapi import APIRouter,Depends,Response
from typing import Union
from queries.vacations import VacationIn, VacationRepository,VacationOut, Error

router=APIRouter()

## the response_model parameters is just telling the fastAPI to
## show the correct response type in the FASTapi/docs
## the Union allow the function return 2 types of base
@router.post("/vacations",response_model=Union[VacationOut,Error])

## the depende will create instance of the VacationRepository
def create_vacations(vacation:VacationIn,response:Response,repo:VacationRepository = Depends()):
    print(repo,'--repo--')

    ## the response status is to alter the response status in the code
    # response.status_code=400

    ## this code will create the vacation and return the basemodel that is desired
    return repo.create(vacation)


## get all the vacation

@router.get("/vacations",response_model=Union[VacationOut,Error])
def get_all(repo:VacationRepository=Depends()):
    return repo.get_all()
