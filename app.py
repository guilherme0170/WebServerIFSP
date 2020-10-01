from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
import yaml
import os
import uuid

app = Flask(__name__)

app.secret_key = "12345"
app.config['UPLOAD_FOLDER'] = 'static/_imagens'

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

@app.route('/projeto/<id>')
def projeto(id):
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM PROJETOS WHERE ID_PROJ = %d" % int(id))
    results = cur.fetchall()

    return render_template('projeto.html', results = results)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        proj_logo = request.files['logo']
        proj_salario = request.form['salario']
        proj_titulo = request.form['titulo']
        proj_endereco = request.form['endereco']
        proj_contato = request.form['contato']
        proj_desc = request.form['descricao']
        
        nome_img = str(uuid.uuid4().hex) + proj_logo.filename

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO PROJETOS (ID_EMPRESA, TITULO, CONTATO, SALARIO, ENDERECO, DESCRICAO, IMAGEM) VALUES (1, %s, %s, %s, %s, %s, %s)", (proj_titulo, proj_contato, proj_salario, proj_endereco, proj_desc, nome_img))
        mysql.connection.commit()
        cur.close()
        
        path = os.path.join(app.config['UPLOAD_FOLDER'], nome_img)
        proj_logo.save(path)

        flash("Projeto '%s' criado com sucesso!" % proj_titulo)
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
    cur.execute("SELECT * FROM PROJETOS WHERE ID_PROJ = %d" % int(id))
    results = cur.fetchall()
    
    cur.execute("DELETE FROM PROJETOS WHERE ID_PROJ = %d" % int(id))
    mysql.connection.commit()
    cur.close()

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], results[0]['IMAGEM']))

    flash("Projeto '%s' deletado com sucesso!" % results[0]['TITULO'])
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
        proj_logo = request.files['logo']

        nome_img = str(uuid.uuid4().hex) + proj_logo.filename
        
        cur.execute("UPDATE PROJETOS SET TITULO='%s', CONTATO='%s', SALARIO='%s', ENDERECO='%s', DESCRICAO='%s', IMAGEM='%s' WHERE ID_PROJ=%d" % (proj_titulo, proj_contato, proj_salario, proj_endereco, proj_desc, nome_img, int(id)))
        mysql.connection.commit()
        cur.close()
        
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], results[0]['IMAGEM']))
        
        path = os.path.join(app.config['UPLOAD_FOLDER'], nome_img)
        proj_logo.save(path)

        flash("Projeto '%s' editado com sucesso!" % proj_titulo)
        return redirect(url_for('editar'))
    else:
        return render_template('update.html', results = results)


if __name__ == '__main__':
    app.run(debug=True)
