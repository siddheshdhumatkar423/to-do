from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/todoapp"
mongo = PyMongo(app)
collection = mongo.db.tasks

@app.route("/")
def mytodo():
    tasks = collection.find()
    return render_template('index.html', tasks=tasks)


@app.route("/add", methods=["POST", 'GET'])
def add_task():
    task = {'task': request.form['Task'],
            'description': request.form["desc"]
            }
    collection.insert_one(task)
    return redirect('/')


@app.route('/delete/<task_id>')
def delete_task(task_id):
    collection.delete_one({'_id': ObjectId(task_id)})
    return redirect('/')


@app.route('/update/<task_id>', methods=['POST', 'GET'])
def update_task(task_id):
    if request.method == "POST":
        task_title = request.form.get('Task')
        task_description = request.form.get('desc')

        collection.update_one({'_id': ObjectId(task_id)}, {'$set': {
            'task': task_title,
            'description': task_description
        }})
        return redirect(url_for('mytodo'))
    existing_task = collection.find_one({'_id': ObjectId(task_id)})
    return render_template("update.html", task_id=task_id, existing_task=existing_task)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
