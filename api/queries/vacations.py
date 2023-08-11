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


        ## updatiing the vacations
    def update(vacation_id,vacation)->Union[Error,VacationIn]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result=db.execute(
                        """
                        UPDATE vacations
                        SET name=%s
                        ,   from_date=%s
                        ,   to_date=%s
                        ,   thoughts=%s
                        where id=%s
                        """,
                        [
                        vacation.name,
                        vacation.from_date,
                        vacation.to_date,
                        vacation.thoughts,
                        vacation_id
                        ]
                    )
                    old_data=vacation.dict()
                    return VacationOut(id=vacation_id,**old_data)

        except Exception as e:
            return {"mssg":f"cant update the vacation \n {e}"}


    ## get a vacation with a specific id
    def by_id(self,vacation_id):
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result=db.execute(
                        """
                        SELECT id, name, from_date, to_date, thoughts
                        FROM vacations
                        WHERE id = %s
                        """,
                        [
                            vacation_id
                        ]
                    )
                    record=result.fetchone()
                    if record==None:
                        return None
                    return self.db_to_vacation(record)
        except Exception as e:
            print(e)
            return {'mssg':f'wrong id \n {e}'}


    # create a function for delete:
    def delete(self,vacation_id:int)->Union[Error,bool]:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result=db.execute(
                        """
                        DELETE FROM vacations
                        WHERE id=%s
                        """,
                        [
                            vacation_id
                        ]
                    )
                    return True
        except Exception as e:
            print(e)
            return {'mssg':f'wrong id \n {e}'}









    ## creating a reusable db converter
    def db_to_vacation(self,record):
        vacation_out=VacationOut(
            id=record[0],
            name=record[1],
            from_date=record[2],
            to_date=record[3],
            thoughts=record[4],
        )
        return vacation_out
