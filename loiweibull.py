import numpy 
import sys

from flask import Flask, render_template, request
from librairie_chartjs import *

app = Flask(__name__)


def Weibull_densite(beta,sigma,c,alpha):
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    
    nb_point=200
    # max de l'axe des x
    x_max=c+sigma*numpy.power(-numpy.log(1-alpha),1.0/beta)
    
    #intervalle = abscisse
    #y=densité=ordonnée 
    
    intervalle=[c+(x_max-c)*i/(nb_point-1) for i in range(nb_point)]
    
    K=beta/(1.0*sigma)
    y=[K*numpy.power((x-c)/sigma,beta-1)*numpy.exp(-numpy.power((x-c)/sigma,beta)) for x in intervalle]
    
    return intervalle, y

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

