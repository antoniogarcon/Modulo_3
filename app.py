from flask import Flask, request, jsonify
from models.task import Task

#__name__ = '__main__'
app = Flask(__name__)

#CRUD
#Create, Read, Update, Delete
#Tabela tarefa

#lista de tarefas
tasks = []
task_id_control = 1
#Criação / CREATE
@app.route('/tasks', methods=['POST'])
def create_task(): 
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso","id":new_task.id})

#Leitura / READ
@app.route('/tasks',methods=['GET'])
def get_tasks():
    """ Modo mais verboso
        task_list = []
        for task in tasks:
            task_list.append(task.to_dict())
    """
    task_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }

    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict()),200

  return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

#Atualizar / UPDATE
@app.route('/tasks/<int:id>',methods=['PUT'])
def update_task(id):
   
   task = None
   for t in tasks:
      if t.id == id:
         task = t
      
   if task == None:
       return jsonify({"message": "Não foi possível encontrar a atividade"}), 404

   data = request.get_json()
   task.title = data['title']
   task.description = data['description']
   task.completed = data['completed']
   return jsonify({"message": "Tarefa atualizada com sucesso!"}), 200

#Deletar / DELETE
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
   task = None
   for t in tasks:
      if t.id == id:
         task = t
         break
      
   if not task:
       return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
      
   tasks.remove(task)
   return jsonify({"message": "Tarefa deletada com sucesso"}), 200
   
# Para exibir log, usado para desenvolvimento local
if __name__ == '__main__':
    app.run(debug=True)