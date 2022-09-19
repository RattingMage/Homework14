import sqlite3


def connection_db(query):
    with sqlite3.connect("netflix.db") as connection:
        return connection.execute(query).fetchall()


def json_by_title(title):
    query = f"""
                    select * from netflix 
                    where title = '{title}'
                    order by release_year desc 
                    limit 1
                """
    result = connection_db(query)

    return {
        "title": result[0][2],
        "country": result[0][5],
        "release_year": result[0][7],
        "genre": result[0][11],
        "description": result[0][12]
    }


def json_by_realise(from_year, to_year):
    query = f"""
               select * from netflix 
               where release_year between {from_year} and {to_year}
               order by release_year
               limit 100
           """
    answer = connection_db(query)
    result = []

    for movie in answer:
        result.append({
            "title": movie[2],
            "release_year": movie[7]
        })

    return result


def json_by_rating(age):
    my_rating = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    query = f"""
                select * from netflix 
                where rating in {my_rating.get(age)}
            """
    answer = connection_db(query)
    result = []

    for movie in answer:
        result.append({
            "title": movie[2],
            "rating": movie[8],
            "description": movie[12]
        })
    return result


def json_by_genre(genre):
    query = f"""
                select * from netflix 
                where listed_in like '%{genre}%'
                order by release_year desc 
                limit 10
            """
    answer = connection_db(query)
    result = []

    for movie in answer:
        result.append({
            "title": movie[2],
            "description": movie[12]
        })
    return result


def by_actors(name1, name2):
    query = f"""
                select "cast" from netflix 
                where "cast" like '%{name1}%' and "cast" like '%{name2}%'
            """
    answer = connection_db(query)
    names_dict = {}
    res = []
    for movie in answer:
        result = dict(movie)

        names = set(result.get('cast').split(", ")) - {name1, name2}

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1
    for key, value in names_dict.items():
        if value > 2:
            res.append(key)
    return res


def by_something(type, realise_year, genre):
    query = f"""
        SELECT * FROM netflix
        WHERE type = '{type}'
        AND release_year = '{realise_year}'
        AND listed_in = '%{genre}%'
    """

    answer = connection_db(query)
    result = []

    for movie in answer:
        result.append({
            "title": movie[2],
            "description": movie[12]
        })

    return result
