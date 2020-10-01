from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

app.secret_key = "12345"

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_PORT'] = db['mysql_port']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM PROJETOS")
    results = cur.fetchall()
    return render_template('index.html', results = results)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        proj_salario = request.form['salario']
        proj_titulo = request.form['titulo']
        proj_endereco = request.form['endereco']
        proj_contato = request.form['contato']
        proj_desc = request.form['descricao']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO PROJETOS (ID_EMPRESA, TITULO, CONTATO, SALARIO, ENDERECO, DESCRICAO, IMAGEM) VALUES (1, %s, %s, %s, %s, %s, %s)", (proj_titulo, proj_contato, proj_salario, proj_endereco, proj_desc, "img a add"))
        mysql.connection.commit()
        cur.close()
    return render_template('criar.html')

@app.route('/editar')
def editar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM PROJETOS")
    results = cur.fetchall()
    return render_template('editar.html', results = results)

@app.route('/deletar/<id>')
def deletar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM PROJETOS WHERE ID_PROJ = %d" % int(id))
    mysql.connection.commit()
    cur.close()
    flash("Projeto deletado com sucesso!")
    return redirect(url_for('editar'))

@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM PROJETOS WHERE ID_PROJ = %d" % int(id))
    results = cur.fetchall()

    if request.method == 'POST':
        proj_salario = request.form['salario']
        proj_titulo = request.form['titulo']
        proj_endereco = request.form['endereco']
        proj_contato = request.form['contato']
        proj_desc = request.form['descricao']

        cur.execute("UPDATE PROJETOS SET TITULO='%s', CONTATO='%s', SALARIO='%s', ENDERECO='%s', DESCRICAO='%s', IMAGEM='a adicionar' WHERE ID_PROJ=%d" % (proj_titulo, proj_contato, proj_salario, proj_endereco, proj_desc, int(id)))
        mysql.connection.commit()
        cur.close()

        flash("Projeto '%s' editado com sucesso!" % proj_titulo)
        return redirect(url_for('editar'))
    else:
        return render_template('update.html', results = results)




if __name__ == '__main__':
    app.run(debug=True)
