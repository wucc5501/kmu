import pandas as pd

df=pd.read_excel('107-109general.xls')

#去除欄位名稱後的/xa0
columns=df.columns
columns=[c.strip() for c in columns]
df.columns=columns
print(df.columns)
#107-109所有科目
df1=df[['學年','科目代碼','科目名稱','選必修','通識類別代碼','通識類別','學分']]
df1=df1.drop_duplicates(ignore_index=True)

#print(df1)

#找出符合學年度及科目代碼的課程
def request_courses(year, courseID):
    dfx=df[(df.學年==year) & (df.科目代碼==courseID)]
    dfx=dfx['學年','科目代碼','科目名稱','選必修','通識類別代碼','通識類別','學分','開課序號']
    dfx=dfx.sort_values('開課序號',ignore_index=True)
    return dfx

#找出符合學年度及通識類別代碼的課程代碼
def request_courseID(year, generalType):
    dfx=df1[(df1.學年==year) & (df1.通識類別代碼==generalType)]
    dfx=dfx.sort_values('科目代碼',ignore_index=True)
    dfx.columns=['year','id','name','need','generaltype','generalname','credit']
    return dfx

#找出符合學年度及通識類別代碼的課程代碼及統計開課數及修課人數
def course_sum(year, generalType):
    dfx=df[(df.學年==year) & (df.通識類別代碼==generalType)]
    dfx=dfx.groupby(by=['學年','通識類別代碼','科目代碼']).count()
    #dfx=dfx['學年','科目代碼','科目名稱','選必修','通識類別代碼','通識類別','學分','開課序號']
    print(dfx.columns)
    return dfx
#print(request_courses(107, 'ALASA'))
#print(request_courseID(109, '7'))
'''
#利用迴圈讀取dataframe，第1位加上流水號(序號)
for index, row in request_courseID(109, '7').iterrows():
    print(index+1, row['name'], row['credit'])
'''
print(course_sum(109,'7'))

