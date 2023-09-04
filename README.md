# Casting-Agency

## Project Description
 Casting Agency models a company that is responsible for creating movies and and actors. There are three different roles in the company Casting Assistant, Casting Director, and Executive Producer. Each of them has a different set of permissions to view, add, update and delete movies and actors in the databse.


## Project Result
Render: https://render-api-example.onrender.com/


## Tech Stack
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Auth0** for authentication management
* **Render** for deployment

## Getting Started


1. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
  This will install all of the required packages we selected within the `requirements.txt` file.


3. Database Setup

  ```
  psql castagency < cast_agencyscript
  ```



## API Reference

### Endpoints

#### GET '/movies'
- General:
    - Return all movies in the database
    - Role Authorized: Assistant, Director, Producer
- Example: ```curl -H "Authorization: Bearer <Token>" https://render-api-example.onrender.com/movies```
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 07 Feb 2020 00:00:00 GMT",
            "title": "Birds of Prey"
        }
    ],
    "success": true
}
```
#### GET '/actors'
- General:
    - Return all actors in the database
    - Role Authorized: Assistant, Director, Producer
- Example: ```curl -H "Authorization: Bearer <Token>" https://render-api-example.onrender.com/actors```
```
{
    "actors": [
        {
            "age": 30,
            "gender": "F",
            "id": 1,
            "name": "Margot Robbie"
        },
       
    ],
    "success": true
}
```

#### POST '/movies'
- General:
    - Add a new movie. The new movie must have all four information. 
    - Role Authorized: Producer
- Example: ```curl -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"title": "Call Me by Your Name", "release_date": "2017-10-20","id":2}' https://render-api-example.onrender.com/movies```
```
{
    "movie": {
        "id": 2,
        "release_date": "Fri, 20 Oct 2017 00:00:00 GMT",
        "title": "Call Me by Your Name"
    },
    "success": true
}
```

#### POST '/actors'
- General:
    - Add a new actor. The new movie must have all four information. 
    - Role Authorized: Director, Producer
- Example: ```curl -X POST - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"name": "Timothée Chalamet", "age": 24, "gender": "M", "id":2}' https://render-api-example.onrender.com/actors```

```
{
    "actor": {
        "age": 24,
        "gender": "M",
        "id": 2,
        "name": "Timothée Chalamet"
    },
    "success": true
}
```

#### PATCH '/movies/<int:id>'
- General:
    - Update some information of a movie based on a payload.
    - Roles authorized : Director, Producer.
- Example: ```curl https://render-api-example.onrender.com/movies/1 -X PATCH -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{ "title": "test", "release_date": "2020-11-01" }'```
```
{
  "movie": {
    "id": 1,
    "release_date": "Sun, 01 NOV 2020 00:00:00 GMT",
    "title": "test"
  },
  "success": true
}
```

#### PATCH '/actors/<int:id>'
- General:
    - Update some information of an actor based on a payload.
    - Roles authorized : Director, Producer.
- Example: ```curl -X PATCH - H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -d '{"name": "test", "age": 88, "": "M"}' https://render-api-example.onrender.com/actors/1```
```
{
  "actor": {"age": 88,
    "gender": "M",
    "id": 1,
    "name": "Leonardo DiCaprio"
  }, 
  "success": true
}
```

#### DELETE '/movies/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Executive Producer.
- Example: ```curl -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -X DELETE https://render-api-example.onrender.com/movies/2```
```
{
  "success": true, 
  "delete": 2
}
```

#### DELETE '/actors/<int:id>'
- General:
    - Deletes a movie by id form the url parameter.
    - Roles authorized : Casting Director, Executive Producer.
- Example: ```curl -H '{"Content-Type: application/json", "Authorization: Bearer <TOKEN>}' -X DELETE https://render-api-example.onrender.com/actors/2```
```
{
    "success": "True",
    "deleted": 2
}
```

### Error Handling
Errors are returned in the following json format:
```
{
    'success': False,
    'error': 404,
    'message': 'Resource not found. Input out of range.'
}
```
The API returns below types of errors:
- 400: bad request
- 404: resource not found
- 500: internal server error
- AuthError: which mainly results in 401 (unauthorized)
