from flask import Flask, render_template, request
from librairie_chartjs import *

app = Flask(__name__)



@app.route("/", methods=['POST', 'GET'])
def courbeweibull():
    beta = 2
    sigma = 7
    c = 0
    alpha = 0.98

    if request.method == 'POST':
        beta = float(request.form['beta'])
        sigma = float(request.form['sigma'])
        c = float(request.form['c'])
        alpha = float(request.form['alpha'])

    data = Weibull_densite(beta,sigma,c, alpha)

    Nom_script="Graphscript"
    ID_graphe="Graphid"
    Fichier_js="static/js/"+str(Nom_script)+".js"

    graphe = Ecrire_Chartjs_graph(Nom_script,ID_graphe,"Densité de la loi Weibull", data)

    return render_template("weibull.html", 
                            beta = beta,
                            sigma = sigma,
                            c = c,
                            alpha = alpha,
                            graphe = graphe,
                            Nom_script=Nom_script,
                            ID_graphe=ID_graphe,
                            Fichier_js=Fichier_js)

if __name__ == "__main__":
    #import webbrowser
    #webbrowser.open("http://127.0.0.1:5000/")
    #app.run(debug=True)
    app.run()