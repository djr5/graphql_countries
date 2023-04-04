import falcon
from falcon_cors import CORS
import graphene
from graphql import GraphQLError
import json
from queries import Query
from mutations import Mutation

cors = CORS(
    allow_all_origins=True,
    allow_all_headers=True,
    allow_all_methods=True
)

app = falcon.App(middleware=[cors.middleware])

schema = graphene.Schema(query=Query, mutation=Mutation)


#Class for rendering the home page
class HomePageResource:
    
    def on_get(self, req, resp):
        with open('graphql_countries\static\html\index.html', 'r') as f:
            html = f.read()
        resp.content_type = 'text/html'
        resp.text = html
        resp.status = falcon.HTTP_200

# It takes a POST request with a JSON body containing a GraphQL query and variables, executes the query, and returns the result as JSON
class GraphQLResource:

    def on_post(self, req, resp):
        try:
            data = json.loads(req.bounded_stream.read().decode('utf-8'))
            action = data['query'] if 'query' in data else data['mutation']
            result = schema.execute(action, variable_values=data.get('variables'))
            resp.media = result.data
        except (ValueError, KeyError, TypeError, GraphQLError, SyntaxError) as ex:
            resp.media = {"errors": [{"message": str(ex)}]}
            resp.status = falcon.HTTP_400
        else:
            if result.errors:
                resp.status = falcon.HTTP_400
                try:
                    error = result.errors[0].message
                except Exception:
                    error = "Something Went Wrong"
                resp.media = {"errors": [{"message": error}]}
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'

app.add_route("/", HomePageResource())
app.add_route("/graphql", GraphQLResource())

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("localhost", 8000, app)
    print("Development server running at http://127.0.0.1:8000/")
    httpd.serve_forever()