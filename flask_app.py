
import pandas as pd
import flask
from test01 import addNewType, core_sum_by_gtype, all_courses, read_courses, all_courseID, request_courses, request_courseID, all_courseID, core, addno, corebyYear, request_courses,core_pivot, all_courses
import html

#已開課
df=read_courses('107-109general.xls')
#df=read_courses('/home/kmu/mysite/107-109general.xls')  #pythonanywhere

#所有課程代號
dfcourse=all_courseID(df)

#所有開課含核心能力
courses=all_courses(df)
newcourses=addNewType(courses)
newcourseslist=core_sum_by_gtype(newcourses).values
newcore=[]
t1=t2=t3=t4=t5=t6=0
factor={'1':4, '2':8, '3':2, '5':15, 'l':8, 's':1}
for c in newcourseslist:
    total=sum(c[2:])
    cname=c[1]
    c1=round(c[2]/total,1)
    c2=round(c[3]/total,1)
    c3=round(c[4]/total,1)
    c4=round(c[5]/total,1)
    c5=round(c[6]/total,1)
    c6=1-c1-c2-c3-c4-c5
    clist=[cname, c1, c2, c3, c4, c5, c6]
    newcore.append(c)
    
    t1+=c[2]*factor[c[0]]
    t2+=c[3]*factor[c[0]]
    t3+=c[4]*factor[c[0]]
    t4+=c[5]*factor[c[0]]
    t5+=c[6]*factor[c[0]]
    t6+=c[6]*factor[c[0]]

tt=t1+t2+t3+t4+t5+t6
p1=round(t1/tt*100,1)
p2=round(t2/tt*100,1)
p3=round(t3/tt*100,1)
p4=round(t4/tt*100,1)
p5=round(t5/tt*100,1)
p6=100-p1-p2-p3-p4-p5
#
student_expect_core= [p1, p2, p3, p4, p5, p6]



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
def coremap3year():
    return flask.render_template("chartcore3years.html", values=[corebyYear(dfcore, 107),corebyYear(dfcore, 108),corebyYear(dfcore, 109)])

@app.route("/coreexpect")
def coremapexpect():

    return flask.render_template("chartcoreexpect.html", values=student_expect_core)
    
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