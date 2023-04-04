
# GraphQL implementation 

GraphQL API using Python falcon web framework and graphene.


## Authors

- [@rakendkr](https://github.com/djr5)


## How to run

Prerequisites : Python 3.x, MongoDB (latest version)

Clone the repo, create python virtual enviornment.

```bash
  git clone https://github.com/djr5/graphql_countries.git

  cd graphql_countries
  
  python -m venv venv
```
After sucessful virtual enviornment creation, make sure to activate newly created venv. install all packages from requirements.txt file

in Windows:
```bash
  venv/Scripts/activate
  pip install -r requirements.txt
```

in Linux and Mac:
```bash
  source venv/bin/activate
  pip install -r requirements.txt
```

Check if all packages are install using

```bash
  pip freeze
```

Create an Env file in the graphql_countries folder with name .env

add the variables just like .sample.env file and change values accordingly.


To run the server: 
execute the run.bat file in Windows system and start.sh file in Linux or Mac systems respectively.

```bash
  run.bat
```

Make the script executable using the chmod command: (for Linux and Mac)

```bash
  chmod +x start.sh
  ./start.sh
```
Then in terminal you will be able see like this:

Development server running at http://127.0.0.1:8000/
## API Reference

#### Get Home Page

```http
  GET /
```
Endpoint for Home page.

#### Get Graphql Endpoint

```http
  POST /graphql
```
Endpoint to handle graphql service.


