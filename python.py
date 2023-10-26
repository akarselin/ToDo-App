from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/todoapp'  # PostgreSQL bağlantı URL'sini buraya girin
db = SQLAlchemy(app)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.id

# Ana sayfa
@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# Todo ekleme
@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

# Todo silme
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Todo güncelleme
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    todo = Todo.query.get_or_404(id)
    todo.content = request.form['content']
    db.session.commit()
    return redirect(url_for('index'))

if _name_ == '__main__':
    app.run(debug=True)
