
import pandas as pd
import flask
from test01 import all_courses, read_data, all_courseID, request_courses, request_courseID, all_courseID, core, addno, corebyYear, request_courses,core_pivot, all_courses
import html

#已開課
df=read_data('107-109general.xls')
#df=read_data('/home/kmu/mysite/107-109general.xls')  #pythonanywhere

#所有課程代號
dfcourse=all_courseID(df)

#所有開課含核心能力
courses=all_courses(df)

#按年度及核心能力統計核心能力的總和
dfcore=core_pivot(df)
#dfcore=core(df)

app = flask.Flask(__name__)

@app.route("/")
def home():
    return flask.render_template("chart.html")

#核心能力
@app.route("/coretest")
def coretest():
    return flask.render_template("coretest.html", courses=courses.values.tolist())

#查詢年度通識類別的科目
@app.route('/list', methods=['GET'])
def listByYearType():
    year=flask.request.args.get('year')
    gtype=flask.request.args.get('gtype')
    dfx=request_courseID(dfcourse, int(year), gtype)
    dfx=addno(dfx)
    html='chart'+str(year)+'.html'
    return flask.render_template(html, courses=dfx.to_dict('records'))
    #return dfx.to_dict()

#顯示年度課程架構圖
@app.route('/<string:year>', methods=['GET'])
def listByYear(year):
    html='chart'+year+'.html'
    return flask.render_template(html)

#顯示年度核心統計圖    
@app.route("/coremap")
def coremap():
    year=int(flask.request.args.get('year'))
    #return flask.render_template("chartcore.html", corevalues=dfcore.loc[year,'7'])
    return flask.render_template("chartcore.html", corevalues=corebyYear(dfcore, year), year=year)
    #return corebyYear(dfcore, year)

#顯示3年度核心統計圖    
@app.route("/coremap3year")
def coremap():
    return flask.render_template("chartcore3year.html", corevalues=[corebyYear(dfcore, 107),corebyYear(dfcore, 108),corebyYear(dfcore, 109)])
    
#顯示年度科目代碼的課程    
@app.route("/courselist", methods=['GET'])
def courselist():
    year=flask.request.args.get('year')
    courseID=flask.request.args.get('courseid')
    dfx=request_courses(df, int(year), courseID)
    dfx=addno(dfx)
    return flask.render_template("courselist.html", courses=dfx.to_dict('records'))


#課程大綱查詢網址
#https://wac.kmu.edu.tw/tea/teaaca/team2002c.php?SYEAR=109&SEM=2&SEQNO=9961237
#核心能力查詢
#https://wac.kmu.edu.tw/aca/acamap/acara407.php?cond=109,2,9961237
app.run(debug=True)