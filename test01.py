import pandas as pd

#讀取資料
def read_data(filename):

    df=pd.read_excel(filename)

    #去除欄位名稱後的/xa0
    columns=df.columns
    columns=[c.strip() for c in columns]
    df.columns=columns
    print(df.columns)
    #挑選欄位
    dfx=df[['學年','學期','科目名稱','開課序號','是否開課','科目代碼','選必修','通識類別代碼','通識類別','選課人數','節次起','節次迄','核心能力.1','學習成效權重','學分']]
    #更換欄位名稱
    dfx.columns=['學年','學期','科目名稱','開課序號','是否開課','科目代碼','選必修','通識類別代碼','通識類別','選課人數','節次起','節次迄','核心能力','學習成效權重','學分']
    #篩選已開課
    dfx=dfx[dfx.是否開課=='Y']
    return dfx

#得所有科目代號，並求出科目代號的開課數量及修課總人數
def all_courseID(df):
    
    dfx=df[['學年','學期','科目代碼','開課序號','科目名稱','選必修','通識類別代碼','通識類別','學分','選課人數']]
    dfx=dfx.drop_duplicates(subset=['學年','學期','開課序號'])
    #dfx=dfx.sort_values(['學年','科目代碼'],ignore_index=True)

    dfx['開課數量']=dfx.groupby(by=['學年','科目代碼'], sort=False)['科目代碼'].transform('count')
    dfx['選課總人數']=dfx.groupby(by=['學年','科目代碼'], sort=False)['選課人數'].transform('sum')
    
    dfx=dfx.drop_duplicates(subset=['學年','科目代碼'])

    return dfx
#print(df1)
#求出所有課程及相關核心能力
def all_courses(df):
    dfx=df[['學年','學期','科目代碼','開課序號','科目名稱','選必修','通識類別代碼','通識類別','學分','選課人數','核心能力','學習成效權重']]
    dfy=pd.pivot_table(dfx, index=['學年','學期','開課序號','科目名稱','通識類別','學分'], columns='核心能力', values='學習成效權重', aggfunc='sum', fill_value=0)
    return dfy

#找出符合學年度及科目代碼的所有課程
def request_courses(df, year, courseID):
    df['科目代碼']=df['科目代碼'].str.strip()
    dfx=df[(df.學年==year) & (df.科目代碼==courseID)]
    #dfx=dfx['學年','學期','科目代碼','科目名稱','選必修','通識類別代碼','通識類別','學分','開課序號']
    dfx=dfx.drop_duplicates(subset=['學年','學期','開課序號'])
    dfx=dfx.sort_values(['學期','開課序號'])
    return dfx

#找出符合學年度及通識類別代碼的課程代碼
def request_courseID(df, year, generalType):
    dfx=df[(df.學年==year) & (df.通識類別代碼==generalType)]
    dfx=dfx.sort_values('科目代碼')
    #dfx.columns=['year','sem','id','name','need','generaltype','generalname','credit','courseid']
    return dfx

#找出符合學年度及通識類別代碼的課程代碼及統計開課數及修課人數
def course_sum(df, year, generalType):
    dfx=df[(df.學年==year) & (df.通識類別代碼==generalType)]
    dfc=[]
    dfc=dfx.groupby(by=['學年','通識類別代碼','科目代碼']).count()
    dfs=dfx.groupby(by=['學年','通識類別代碼','科目代碼']).sum()
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

#依學年度及核心能力為群組求加權學習成效
def core(df):
    dfx=df[['學年','科目名稱','開課序號','科目代碼','選必修','核心能力.1','學習成效權重','學分','通識類別代碼']]
    dfx['核心分數']=dfx['學習成效權重']*0.01*dfx['學分']
    dfx=dfx.groupby(by=['學年','核心能力.1']).sum()
    
    return dfx

def corebyYear(df, year):
    dfx=df.loc[year,:]
    coreValues=[]
    for row in dfx.itertuples():
        coreValues.append(round(row.total,2))
    return coreValues

#依學年度及核心能力為index，核心能力為columns，求加權學習成效樞紐分析表  
def core_pivot(df):
    dfx=df[['學年','科目名稱','開課序號','科目代碼','選必修','核心能力','學習成效權重','學分','通識類別代碼']]
    dfx['核心分數']=dfx['學習成效權重']*0.01*dfx['學分']
    dfx=pd.pivot_table(dfx, values='核心分數', index=['學年','核心能力'], columns='通識類別代碼', aggfunc='sum', fill_value=0)
    dfx['total']=dfx.sum(axis=1, skipna=True)
    dfx['year_core']=dfx.index
    dfx['year'],dfx['core']=dfx['year_core'].str
        
    return dfx

def addno(df):
    dfx=df
    dfx['no']=[c+1 for c in range(df.shape[0])]

    return dfx

if __name__=='__main__':
    df=read_data('107-109general.xls')
    print(df)

    df1=all_courseID(df)
    print(df1)

    df2=request_courses(df,109,'ACHI')
    print(df2)

    df3=core_pivot(df)
    print(df3)

    df4=request_courseID(df1, 109, '7')
    print(df4)

    df5=corebyYear(df3,109)
    print(df5)

    df6=all_courses(df)
    print(df6)