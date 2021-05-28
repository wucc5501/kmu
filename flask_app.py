
import pandas as pd
import flask
from test01 import read_data, all_courseID, request_courses, request_courseID, all_courseID, core

#ctype=set(df['通識類別'])
#ctype=[c.replace(u'\xa0', u'') for c in ctype]  #去除\xa0

df=read_data('107-109general.xls')

df1=all_courseID(df)

dfcore=core(df)

#courses={}




'''
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
'''
app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("chart.html")

@app.route("/core")
def core():
    return flask.render_template("chartcore.html")

@app.route('/list', methods=['GET'])
def listByYearType():
    year=flask.request.args.get('year')
    gtype=flask.request.args.get('gtype')
    dfx=request_courseID(df1, int(year), gtype)
    #print(dfx)
    html='chart'+str(year)+'.html'
    return flask.render_template(html, courses=dfx.to_dict('records'))
    #return dfx.to_dict()

@app.route('/<string:year>', methods=['GET'])
def listByYear(year):
    html='chart'+year+'.html'
    return flask.render_template(html)
    
@app.route("/coremap")
def k():
    year=flask.request.args.get('year')
    return flask.render_template("chartcore.html", corevalues=dfcore.loc[year,'7'])

app.run(debug=True)