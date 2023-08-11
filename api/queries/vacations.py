from pydantic import BaseModel
from typing import Optional, List,Union
from datetime import date
from queries.pool import pool

## this will create a list inside a list
# class Thoughts(BaseModel):
#     private_thoughts:str
#     public_thoughts:str

#customize error message
class Error(BaseModel):
    mssg:str

class VacationIn(BaseModel):
    name:str
    from_date:date
    to_date:date
    thoughts: Optional[str]


class VacationOut(BaseModel):
    id:int
    name:str
    from_date:date
    to_date:date
    thoughts: Optional[str]


class VacationRepository:
    def create(self,vacation:VacationIn):

        #connect the database
        #what this code does, it will create a connection
        # and makesure if exception thrown, it will give
        #connection back to the pool (so we dont have to do alot try and catch )
        with pool.connection() as conn:

            #get a cursor (somethong to run SQL with)
            with conn.cursor() as db:

                #Run our INSERT STATEMENT
                result=db.execute(
                    '''
                    INSERT INTO vacations
                    (name, from_date, to_date, thoughts)
                    VALUES
                        (%s, %s, %s, %s)
                    RETURNING id;
                    ''',
                    [
                        vacation.name,
                        vacation.from_date,
                        vacation.to_date,
                        vacation.thoughts
                    ]
                )
                # i think this can be used to patching different api into one
                id=result.fetchone()[0]
                ## every pydantic models has dic property in it
                old_data=vacation.dict()

                new_vacation=VacationOut(id=id,**old_data)
                print(new_vacation,'--VacationOut--')

                #Return new Data which is vacation out
                return new_vacation

    ## this instance method will return all the data in the database
    def get_all(self) -> Union[Error,list[VacationOut]]:
        ## need to create all the connection oncemore
        try:
            ## conect the database
            with pool.connection() as conn:
                ## get a cursor(something to run SQL with)
                with conn.cursor() as db:
                    ## Run Select statement
                    result=db.execute(
                    """
                    SELECT id, name,from_date, to_date, thoughts
                    FROM vacations
                    ORDER BY from_date
                    """
                    )


                    result=[]
                    ## if you iterate db, it will list all the data that is
                    ##stated depending on what u stated in cursor
                    for record in db:
                        print(record)
                        vacation=VacationOut(
                            id=record[0],
                            name=record[1],
                            from_date=record[2],
                            to_date=record[3],
                            thoughts=record[4]
                        )
                        result.append(vacation)

                    return result

        ## e means state the problem
        except Exception as e:
            return {"mssg":f"{e}edatabase cannot get all the vacations"}
