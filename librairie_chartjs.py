from decimal import *

# Moments

def Moment_r(data,r):
    import functools
    data=[x for x in data] # transformation de données en liste
    fonc_r= lambda x : x**r
    S=functools.reduce( lambda x, y: x+y,map(fonc_r,data))
    return S/(1.0*len(data))


#Moments Centrés

def Moment_cr(data,r):
    data=[x for x in data] # transformation de données en liste
    import functools
    m=Moment_r(data,1)
    fonc_r= lambda x : (x-m)**r
    S=functools.reduce(lambda x, y: x+y,map(fonc_r,data))
    return S/(1.0*len(data))

############################################################
# pour chart.js : simuler les rgba pour les couleurs des bars

def RGBA(N):
    def genere_rgba():
        import random
        T=[]
        for i in range(4):
            if i<3:
                T.append(int(10+210*random.random()))
            else:
                T.append(round(random.random(),2))
        return tuple(T)
    
    return ['rgba{}'.format(genere_rgba()) for _ in range(N)]

############################################################

# pour le nombre d'occurrence

def nb_occurrence(data):
    data=list(data)
    Dic={}
    for x in sorted(data):
        Dic[x]=data.count(x)
        
    Valeurs=[t for t in Dic.keys()]
    Effectifs=[t for t in Dic.values()]

    # Pour chart.js:
    # labels: [Valeurs_1,..., Valeurs_k]
    # data: [Effectifs_1,...,Effectifs_k]
    
    return Valeurs,Effectifs

############################################################
# pour le tableau des résultats

def tableau_stats(data):
    import numpy
    Dic_resultats={}
    Dic_resultats["nombre d'observations"]=len(data)
    Dic_resultats["minimum"]=numpy.around(min(data), decimals=4)
    Dic_resultats["maximum"]=numpy.around(max(data), decimals=4)
    Dic_resultats["moyenne empirique"]=numpy.around(Moment_r(data,1), decimals=4)
    Dic_resultats["variance empirique"]=numpy.around(Moment_cr(data,2), decimals=4)
    Dic_resultats["skewness"]=numpy.around(Moment_cr(data,3)/numpy.power(Moment_cr(data,2),1.5), decimals=6)
    Dic_resultats["kurtosis"]=numpy.around(-3+Moment_cr(data,4)/numpy.power(Moment_cr(data,2),2), decimals=6)

    return Dic_resultats

##################################################################
# Ecrire de script d'histogramme en formar char.js  (cas des données discrètes)

def Ecrire_Chartjs_discret(nom_script,nom_histo,data,titre_histo):
    
    Valeurs,Effectifs=nb_occurrence(data)
    
    nom_fich="./static/js/"+str(nom_script)+".js"
    
    f_js = open(nom_fich, "w")
    f_js.write("Chart.pluginService.register({\n")
    f_js.write("beforeDraw: function (chart, easing) {\n")
    f_js.write("                       if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {\n")
    f_js.write("                        var helpers = Chart.helpers;\n")
    f_js.write("			var ctx = chart.chart.ctx;\n")
    f_js.write("			var chartArea = chart.chartArea;\n")

    f_js.write("                        ctx.save();\n")
    f_js.write("			ctx.fillStyle = chart.config.options.chartArea.backgroundColor;\n")
    f_js.write("                        ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);\n")
    f_js.write("ctx.restore();\n")
    f_js.write("}\n")
    f_js.write("}\n")
    f_js.write("});\n")
    f_js.write("const ctx = document.getElementById('{}').getContext('2d'); \n".format(nom_histo))
    f_js.write("Chart.defaults.global.defaultFontFamily = \"Helvetica Neue\"; \n")
    f_js.write("const  %s = new Chart(ctx, { \n"%(nom_histo))
    f_js.write("   type: 'bar', \n")
    f_js.write("     data: {\n")
    f_js.write("         labels: %s, \n"%([str(u) for u in Valeurs]))
    f_js.write("         datasets: [{ \n")
    #f_js.write("         label: \"nombre d'observations\",\n")
    f_js.write("         label: \"\",\n")
    f_js.write("         data: %s,\n"%(Effectifs))
    f_js.write("         backgroundColor:\n")
    f_js.write("         %s,\n"%(RGBA(len(Effectifs))))
    f_js.write("         borderColor: 'rgba(255, 255, 255, 1)',\n")
    f_js.write("         borderWidth: 1,\n")
    f_js.write("         hoverBorderWidth: 2,\n")
    f_js.write("         hoverBorderColor: 'rgba(125, 125, 125, 1)'\n")
    f_js.write("         }]\n")
    f_js.write("       },\n")
    f_js.write("     options: {\n")
    f_js.write("               chartArea: {\n")
    f_js.write("                          backgroundColor: 'rgba(195, 195, 200, 0.25)'\n")
    f_js.write("                          },\n")
    f_js.write("            responsive: true,\n")
    f_js.write("            maintainAspectRatio: false,\n")
    f_js.write("       scales: {\n")
    f_js.write("             y: {\n")
    f_js.write("                 beginAtZero: true\n")
    f_js.write("             },\n")
    f_js.write("             xAxes: [{\n")
    f_js.write("                   ticks: {\n")
    f_js.write("                        autoSkip: false,\n")
    f_js.write("                        maxRotation: 45,\n")
    f_js.write("                        minRotation: 45\n")
    f_js.write("                          },\n")
    ##
    f_js.write("                  scaleLabel: {\n")
    f_js.write("                        display: true,\n")
    f_js.write("                        labelString: \"Valeurs\",\n")
    f_js.write("                        fontFamily: \"Montserrat\",\n")
    f_js.write("                        fontColor: \"black\",\n")
    f_js.write("                        fontSize: 15,\n")
    f_js.write("                             },\n")
    f_js.write("                      }],\n")
    ##
    f_js.write("                     yAxes: [{\n")
    f_js.write("                     	    ticks: {\n")
    f_js.write("                              min: 0,\n")
    #f_js.write("                              max: %s,\n"%(int(max(Effectifs))))
    f_js.write("                            },\n")
    f_js.write("                      scaleLabel: { \n")
    f_js.write("                                display: true, \n")
    f_js.write("                                labelString: \"fr\\u00e9quences\",\n")
    f_js.write("                                fontFamily: \"Montserrat\",\n")
    f_js.write("                                fontColor: \"black\",\n")
    f_js.write("                                fontSize: 15,\n")
    f_js.write("                                 },\n")
				 
    f_js.write("                     }]\n")
    f_js.write("                  },\n")
    f_js.write("               legend: {\n")
    f_js.write("                       display: false\n")
    f_js.write("                       },\n")
    f_js.write("                title: {\n")
    f_js.write("                        display: true,\n")
    f_js.write("                        text: \"%s\",\n"%(titre_histo))
    f_js.write("                        fontSize: 19,\n")
    f_js.write("                        fontColor: \"#2a2d90\"\n")
    f_js.write("                        },\n")
    f_js.write("                 layout: {\n")
    f_js.write("                          padding: {\n")
    f_js.write("                          top: 40,\n")
    f_js.write("                          left: 50,\n")
    f_js.write("                          right: 50,\n")
    f_js.write("                          bottom: 50\n")
    f_js.write("                                    }\n")
    f_js.write("                          },\n")
    f_js.write("                     }\n")
    f_js.write("                });\n")
    f_js.write(" \n")

    
    f_js.close()
    
# Exemple d'appel
# Ecrire_Chartjs_discret("monscript","nom_histo",[4,7,4,1,0,0,1,7,15,11,4,0], "histogramme")
############################################################################################

# Répartition des données continues en plusieurs intervalles

def classes_continues(data,nb_classe):
    # nb_classe : nombre d'intervalles
    import functools
    e0=functools.reduce(lambda x,y: x if x<= y else y , data) # min(data)
    ek=functools.reduce(lambda x,y: x if x>= y else y , data) # max(data)

    Extremites=[e0+(ek-e0)*i/(1.0*nb_classe) for i in range(nb_classe+1)]
    Effectifs=[len([i for i in range(len(data)) if data[i]>= Extremites[k] and data[i]<= Extremites[k+1]]) for k in range(nb_classe)]
    Centres=[round((0.5*(Extremites[i]+Extremites[i+1])),2) for i in range(nb_classe)]

    return Extremites, Effectifs, Centres

##################################################################
# Ecrire de script d'histogramme en formar char.js  (cas des données continues)

def Ecrire_Chartjs_continu(nom_script,nom_histo,data,nb_classe,titre_histo):
    
    Extremites, Effectifs, Centres=classes_continues(data,nb_classe) # à  changer
    
    nom_fich="./static/js/"+str(nom_script)+".js"
    
    f_js = open(nom_fich, "w")
    f_js.write("Chart.pluginService.register({\n")
    f_js.write("beforeDraw: function (chart, easing) {\n")
    f_js.write("                       if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {\n")
    f_js.write("                        var helpers = Chart.helpers;\n")
    f_js.write("			var ctx = chart.chart.ctx;\n")
    f_js.write("			var chartArea = chart.chartArea;\n")

    f_js.write("                        ctx.save();\n")
    f_js.write("			ctx.fillStyle = chart.config.options.chartArea.backgroundColor;\n")
    f_js.write("                        ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);\n")
    f_js.write("ctx.restore();\n")
    f_js.write("}\n")
    f_js.write("}\n")
    f_js.write("});\n")
    f_js.write("const ctx = document.getElementById('{}').getContext('2d'); \n".format(nom_histo))
    f_js.write("Chart.defaults.global.defaultFontFamily = \"Helvetica Neue\"; \n")
    f_js.write("const  %s = new Chart(ctx, { \n"%(nom_histo))
    f_js.write("   type: 'bar', \n")
    f_js.write("     data: {\n")
    f_js.write("         labels: %s, \n"%([str(u) for u in Centres]))
    f_js.write("         datasets: [{ \n")
    f_js.write("         label: \"nombre d'observations\",\n")
    f_js.write("         data: %s,\n"%(Effectifs))
    f_js.write("         backgroundColor:\n")
    f_js.write("         %s,\n"%(RGBA(len(Effectifs))))
    f_js.write("         borderColor: 'rgba(255, 255, 255, 1)',\n")
    f_js.write("         borderWidth: 0,\n")
    f_js.write("         hoverBorderWidth: 2,\n")
    f_js.write("         hoverBorderColor: 'rgba(125, 125, 125, 1)'\n")
    f_js.write("         }]\n")
    f_js.write("       },\n")
    f_js.write("     options: {\n")
    f_js.write("               chartArea: {\n")
    f_js.write("                          backgroundColor: 'rgba(195, 195, 200, 0.25)'\n")
    f_js.write("                          },\n")
    f_js.write("            responsive: true,\n")
    f_js.write("            maintainAspectRatio: false,\n")
    f_js.write("       scales: {\n")
    f_js.write("             y: {\n")
    f_js.write("                 beginAtZero: true\n")
    f_js.write("             },\n")
    f_js.write("             xAxes: [{\n")
    f_js.write("                   categoryPercentage: 1.0, \n")
    f_js.write("                    barPercentage: 1.0,  \n")
    f_js.write("                   ticks: {\n")
    f_js.write("                        autoSkip: false,\n")
    f_js.write("                        maxRotation: 45,\n")
    f_js.write("                        minRotation: 45\n")
    f_js.write("                          },\n")
    ##
    f_js.write("                  scaleLabel: {\n")
    f_js.write("                        display: true,\n")
    f_js.write("                        labelString: \"Valeurs\",\n")
    f_js.write("                        fontFamily: \"Montserrat\",\n")
    f_js.write("                        fontColor: \"black\",\n")
    f_js.write("                        fontSize: 15,\n")
    f_js.write("                             },\n")
    f_js.write("                      }],\n")
    ##
    f_js.write("                     yAxes: [{\n")
    f_js.write("                     	    ticks: {\n")
    f_js.write("                              min: 0,\n")
    #f_js.write("                              max: %s,\n"%(int(max(Effectifs))))
    f_js.write("                            },\n")
    f_js.write("                      scaleLabel: { \n")
    f_js.write("                                display: true, \n")
    f_js.write("                                labelString: \"fr\\u00e9quences\",\n")
    f_js.write("                                fontFamily: \"Montserrat\",\n")
    f_js.write("                                fontColor: \"black\",\n")
    f_js.write("                                fontSize: 15,\n")
    f_js.write("                                 },\n")
				 
    f_js.write("                     }]\n")
    f_js.write("                  },\n")
    f_js.write("               legend: {\n")
    f_js.write("                       display: false\n")
    f_js.write("                       },\n")
    f_js.write("                title: {\n")
    f_js.write("                        display: true,\n")
    f_js.write("                        text: \"%s\",\n"%(titre_histo))
    f_js.write("                        fontSize: 19,\n")
    f_js.write("                        fontColor: \"#2a2d90\"\n")
    f_js.write("                        },\n")
    f_js.write("                 layout: {\n")
    f_js.write("                          padding: {\n")
    f_js.write("                          top: 40,\n")
    f_js.write("                          left: 50,\n")
    f_js.write("                          right: 50,\n")
    f_js.write("                          bottom: 50\n")
    f_js.write("                                    }\n")
    f_js.write("                          },\n")
    f_js.write("                     }\n")
    f_js.write("                });\n")
    f_js.write(" \n")

    
    f_js.close()
    
# Exemple d'appel
# Ecrire_Chartjs_continu(nom_script,nom_histo,data,nb_classe,titre_histo)
###########################################################################

###########################################################################
# simulation des lois usuelles discrètes  et continues

def Bernoulli_va(theta,taille):
    import random
    return [1*(random.random() <= theta) for _ in range(taille)]

#
def Binomiale_va(N_bin,theta,taille):
    import numpy
    return [numpy.random.binomial(N_bin,theta) for _ in range(taille)]

#
def Poisson_va(LLambda,taille):
    import numpy
    return [numpy.random.poisson(LLambda) for _ in range(taille)]

#
def Geo_va(theta,taille):
    import numpy
    return [numpy.random.geometric(theta) for _ in range(taille)]

#
def Unif_Discrete_va(borne_min,borne_max,taille):
    import numpy
    A=min(borne_min,borne_max)
    B=max(borne_min,borne_max)
    return [numpy.random.randint(A,B+1) for _ in range(taille)]

#
def Unif_Continue_va(borne_inf,borne_sup,taille):
    import random
    A=min(borne_inf,borne_sup)
    B=max(borne_inf,borne_sup)
    return [A+(B-A)*random.random() for _ in range(taille)]

#

def Exp_va(LLambda,taille):
    import numpy
    A=-1.0/LLambda
    return [A*numpy.log(numpy.random.rand()) for _ in range(taille)]
#

def Normale_va(mu,sigma2,taille):
    import numpy
    A=numpy.sqrt(sigma2)
    return [numpy.random.normal(mu,A) for _ in range(taille)]

#densite loi weibull 

def Weibull_densite(beta,sigma,c,alpha):
    import sys
    import numpy
    
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

###########################################################################

# Ecrire le script d'un graph en format chart.js (une courbe)


def Ecrire_Chartjs_graph(nom_script,nom_graph,titre_graph,data):
    
    Abscisses , Ordonnees = data
    
    nom_fich="./static/js/"+str(nom_script)+".js"
    
    f_js = open(nom_fich, "w")
    f_js.write("const ctx = document.getElementById('{}').getContext('2d'); \n".format(nom_graph))
    f_js.write("const  %s = new Chart(ctx, { \n"%(nom_graph))
    f_js.write("   type: 'line', \n")
    f_js.write("     data: {\n")
    f_js.write("         labels: %s, \n"%([str(round(u,2)) for u in Abscisses]))
    f_js.write("         datasets: [{ \n")
    f_js.write("         label: \"\",\n")
    f_js.write("         data: %s,\n"%(Ordonnees))
    f_js.write("         borderColor: '#0d6efd',\n")
    f_js.write("         borderWidth: 4,\n")
    f_js.write("         pointRadius: 0,\n")
    f_js.write("         }] \n")
    f_js.write("       },\n")
    f_js.write("     options: {\n")
    f_js.write("                plugins: {\n")
    f_js.write("                    legend: {\n")
    f_js.write("                        display: false\n")
    f_js.write("                    },\n")
    f_js.write("                    title: {\n")
    f_js.write("                        display: true,\n")
    f_js.write("                        text: \"%s\",\n"%(titre_graph))
    f_js.write("                        fontSize: 19,\n")
    f_js.write("                        fontColor: \"#2a2d90\"\n")
    f_js.write("                        }\n")
    f_js.write("                },\n")
    f_js.write("                scales: {\n")
    f_js.write("                    x: {\n")
    f_js.write("                      title: {\n")
    f_js.write("                    display: true,\n")
    f_js.write("                    text: 'x',\n")
    f_js.write("                    font: {\n")
    f_js.write("                        size: 15\n")
    f_js.write("                    }},\n")
    f_js.write("                        ticks: {\n")
    f_js.write("                            maxTicksLimit: 6,\n")
    f_js.write("                         }\n")
    f_js.write("                    }\n")
    f_js.write("                },\n")
    f_js.write("                responsive: true,\n")
    f_js.write("                 tooltips: {\n")
    f_js.write("                          mode: 'index',\n")
    f_js.write("                          intersect: true\n")
    f_js.write("                          },\n")
    f_js.write("                     }\n")
    f_js.write("                });\n")
    f_js.write(" \n")

    
    f_js.close()
    