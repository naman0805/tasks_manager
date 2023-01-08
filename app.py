from ast import excepthandler
import re
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        todo_obj = Todo(content=task_content)
        try:
            db.session.add(todo_obj)
            db.session.commit()
            return redirect('/')
        except:
            return "Could not add the task you requested for"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    todo_obj = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo_obj)
        db.session.commit()
        return redirect('/')
    except:
        return "Could not add the task you requested for"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    todo_obj = Todo.query.get_or_404(id)
    if request.method=='GET':
        return render_template("update.html", task_id=todo_obj.id, content=todo_obj.content)
    
    else:
        content = request.form['content']
        todo_obj.content = content
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return "Faild to update the content of todo"



if __name__ == "__main__":
    app.run(debug=True)
