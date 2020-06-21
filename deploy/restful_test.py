from flask import Flask
from flask_restful import reqparse,abort,Api,Resource
app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1':{'task':'build on API'},
    'todo2':{'task':'haha'},
    'todo3':{'task':'profit'}
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404,message='TODO {} doesn\'t exist'.format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Todo(Resource):
    def get(self, todo_id):
        print('get')
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '',204

    def put(self, todo_id):
        print('put')
        # args = parser.parse_args()
        args = parser.parse_args()
        print(args['task'])
        task ={'task':args['task']}
        TODOS[todo_id] = task
        print(TODOS[todo_id])
        return task,201

class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo'))+1
        todo_id = 'todo%i'%todo_id
        print('post',todo_id)
        TODOS[todo_id]={'task':args['task']}
        return TODOS[todo_id],201

api.add_resource(TodoList,'/todos')
api.add_resource(Todo,'/todos/<todo_id>')

if __name__ == "__main__":
    app.run("0.0.0.0",5000,debug=True)