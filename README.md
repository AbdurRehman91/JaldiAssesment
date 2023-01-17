# Assignment

This is a Python web app using the Flask framework and PostgreSQL relational database service.


### Steps for running the server: 

1. create a Python virtual environment (https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate that.

2. Install the requirements:

```shell
pip install -r requirements.txt
```

3. Create an `.env` file using `.env.sample` as a guide. Set the value of `DBNAME` to the name of an existing database in your local PostgreSQL instance. Set the values of `DBHOST`, `DBUSER`, and `DBPASS` as appropriate for your local PostgreSQL instance.

4. Run the migrations:

```shell
flask db upgrade
```

5. Run the local server:

```shell
flask run
```

### Apis urls

1. To create new user, the endpoint will be:

````
curl --location --request POST 'http://127.0.0.1:5000/user' \
--header 'Content-Type: application/json' \
--data-raw '{"name":"tester", "email":"tester@app.com","password":"abc123456", "phone_number":"", "user_address":""}'
````
2. For user login, the endpoint will be:

```
curl --location --request POST 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{"email":"user1@app.com","password":"1234567"}'
```
3. To get user details, the endpoint will be:

```
curl --location --request GET 'http://127.0.0.1:5000/user/user1@app.com' \
--header 'access_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI4NjI3M2Y0Yy04ZTlkLTQ3NTMtOTgwNS02YjM1NTkyNGU2OTgiLCJleHAiOjE2NzM4OTE4Mzh9.SOH49cNfu0sGviGZRelMvVeQcROppE2Aw_SrdYRvS8A'
```

4. To create listing, endpoint will be:

```
curl --location --request POST 'http://127.0.0.1:5000/user/listing' \
--header 'access_token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOm51bGwsImV4cCI6MTY3Mzk3MjYyOH0.-xwBSp397qUrdG4R-vr5iMV6XgPV9JkM1xxzggYTbAQ' \
--header 'Content-Type: application/json' \
--data-raw '[{"email":"user@app.com","description":"farm house","price":50000000,"address":"lahore"},
{"email":"user@app.com","description":"farm house", "price":50000000,"address":"islmabad"}]'
```

5. To get all the listings, endpoint will be:

```
curl --location --request GET 'http://127.0.0.1:5000/user/listing/user1@app.com'
```

6. To update user, endpoint will be:

```
curl --location --request GET 'http://127.0.0.1:5000/user/listing/user1@app.com'
```
