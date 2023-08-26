steps=[
    [
        """
        CREATE TABLE vacations(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(1000) NOT NULL,
        from_date DATE NOT NULL,
        to_date DATE NOT NULL,
        thoughts TEXT
        );
        """,
        """
        DROP TABLE vacations;
        """
    ]
    ,
      [
        """
        CREATE TABLE costumer(
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(1000) NOT NULL,
        lastName VARCHAR(1000) NOT NULL
        );
        """,
        """
        DROP TABLE vacations;
        """
    ]
]
