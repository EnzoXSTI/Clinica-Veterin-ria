from flask import Flask, render_template, request, redirect
import fdb

app = Flask(__name__)

con = fdb.connect(
    host='localhost',
    database='C:\Aluno\Downloads\BANCO.FDB',
    user='sysdba',
    password='masterkey'
)

@app.get("/tutores")
def tutores():
    cur = con.cursor()
    cur.execute("SELECT ID_TUTOR, NOME, TELEFONE, EMAIL, ENDERECO FROM TUTOR")
    lista = cur.fetchall()
    return render_template("tutores.html", dados=lista)

@app.get("/excluir_tutor/<int:id>")
def excluir_tutor(id):
    cur = con.cursor()
    cur.execute("DELETE FROM TUTOR WHERE ID_TUTOR = ?", (id,))
    con.commit()
    return redirect("/tutores")

@app.route("/editar_tutor/<int:id>", methods=["GET", "POST"])
def editar_tutor(id):

    cur = con.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        endereco = request.form["endereco"]

        cur.execute("""
            UPDATE TUTOR SET 
            NOME=?, TELEFONE=?, EMAIL=?, ENDERECO=?
            WHERE ID_TUTOR=?
        """, (nome, telefone, email, endereco, id))

        con.commit()
        return redirect("/tutores")

    cur.execute("SELECT NOME, TELEFONE, EMAIL, ENDERECO FROM TUTOR WHERE ID_TUTOR = ?", (id,))
    t = cur.fetchone()

    return render_template("editar_tutor.html", t=t, id=id)

app.run(debug=True)
