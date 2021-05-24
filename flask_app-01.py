
import pandas as pd
import flask

def read_data():
    df=pd.read_excel("/home/wucc/mysite/109-2-996.xlsx")

    df=df[['開課序號','科目代碼','科目名稱','選必修別','學分','通識類別']]

    df1=df[['科目代碼','科目名稱','選必修別','學分','通識類別']]
    df1=df1.drop_duplicates()
    df1.sort_values(['通識類別','科目代碼'])
    df1.columns=['id','name','need','credit','type']

    return df1

#ctype=set(df['通識類別'])
#ctype=[c.replace(u'\xa0', u'') for c in ctype]  #去除\xa0

df1=read_data()

dfh=df1[df1['type']=='審美\xa0']
dfa=df1[(df1['type'] =='基礎\xa0') | (df1['type'] =='進階\xa0') ]  #基礎
dfb=df1[df1['type']=='體育\xa0']
dfk=df1[df1['type']=='不分領域\xa0']
dff=df1[df1['type']=='思考\xa0']
dfc=df1[df1['type']=='體驗課程\xa0']
dfe=df1[df1['type']=='全球\xa0']
dfj=df1[df1['type']=='跨域融通\xa0']
dfi=df1[df1['type']=='環境科學\xa0']
dfg=df1[df1['type']=='經典\xa0']
dfd=df1[df1['type']=='公民\xa0']


dfa=dfa.to_dict('records')
dfb=dfb.to_dict('records')
dfc=dfc.to_dict('records')
dfd=dfd.to_dict('records')
dfe=dfe.to_dict('records')
dff=dff.to_dict('records')
dfg=dfg.to_dict('records')
dfh=dfh.to_dict('records')
dfi=dfi.to_dict('records')
dfj=dfj.to_dict('records')
dfk=dfk.to_dict('records')

def addno(d):
    n=1
    for dx in d:
        dx['no']=n
        n+=1

    return d

dfa=addno(dfa)
dfb=addno(dfb)
dfc=addno(dfc)
dfd=addno(dfd)
dfe=addno(dfe)
dff=addno(dff)
dfg=addno(dfg)
dfh=addno(dfh)
dfi=addno(dfi)
dfj=addno(dfj)
dfk=addno(dfk)

app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("chart.html")

@app.route("/a")
def a():
    return flask.render_template("charta.html", courses=dfa)

@app.route("/b")
def b():
    return flask.render_template("charta.html", courses=dfb)

@app.route("/c")
def c():
    return flask.render_template("charta.html", courses=dfc)

@app.route("/d")
def d():
    return flask.render_template("charta.html", courses=dfd)

@app.route("/e")
def e():
    return flask.render_template("charta.html", courses=dfe)

@app.route("/f")
def f():
    return flask.render_template("charta.html", courses=dff)

@app.route("/g")
def g():
    return flask.render_template("charta.html", courses=dfg)

@app.route("/h")
def h():
    return flask.render_template("charta.html", courses=dfh)

@app.route("/i")
def i():
    return flask.render_template("charta.html", courses=dfi)

@app.route("/j")
def j():
    return flask.render_template("charta.html", courses=dfj)

@app.route("/k")
def k():
    return flask.render_template("charta.html", courses=dfk)

