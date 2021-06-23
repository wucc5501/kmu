import pandas as pd

#通識類別
GeneralType={'0':'非通識', '6': '進階', '7':'基礎', '8':'公民', '9':'全球', 'a':'經典', 'b':'思考', 'c':'審美', 
                'g':'環境科學', 'i':'跨域融通', 'j':'體驗課程', 'l':'體育','m':'部分領域'}
#新通識類別
NewGeneralType={'0':'非通識', '1':'國文', '2':'英文', '3':'程式','8':'公民', '9':'全球', 'a':'經典', 'b':'思考', 'c':'審美', 
                'g':'環境科學', 'i':'跨域融通', 'j':'體驗課程', 'l':'體育','m':'部分領域', 's':'服務學習', '5':'通識'}

CoreType={'A': '基礎力', 'B': '人文力', 'C': '關懷力', 'D': '思辨力', 'E':'學習力', 'F':'國際力'}

#轉換新類別
def transfer01(row):
    
    if row['通識類別代碼']=='7':
        if '英' in row['科目名稱']:
            return ('2', '英文')
        elif '國文' in row['科目名稱']:
            return ('1', '國文')
        else:
            return ('3', '程式')
    elif row['通識類別代碼']=='6':
         return ('2', '英文')
    else:
       
        return (row['通識類別代碼'], row['通識類別'])

#計算新核心分數=核心分數*新學分，體育課2學分，其他0學分以2學分計 
def transfer02(row):
    
    if row['學分']==0:
        credit=2
    else:
        credit=row['學分']
           
    return (row['A']*credit, row['B']*credit, row['C']*credit, row['D']*credit, row['E']*credit, row['F']*credit)

def transfer03(row):
    if row['科目名稱']=='服務學習':
        return ('s', '服務學習')
    if row['通識類別代碼']=='7':
        if '英' in row['科目名稱']:
            return ('2', '英文')
        elif '國文' in row['科目名稱']:
            return ('1', '國文')
        else:
            return ('3', '程式')
    elif row['通識類別代碼']=='6':
         return ('2', '英文')
    elif row['通識類別代碼'] in '89abcgi':
        return ('5', '通識')
    else:
       
        return (row['通識類別代碼'], row['通識類別'])   
        

#讀取課程資料，回饋已開課清單
def read_courses(filename):

    df=pd.read_excel(filename)

    #去除欄位名稱後的/xa0
    columns=df.columns
    columns=[c.strip() for c in columns]
    df.columns=columns
    print(df.columns)
    #挑選欄位
    dfx=df[['學年','學期','科目名稱','開課序號','是否開課','科目代碼','選必修','通識類別代碼','通識類別','選課人數','節次起','節次迄','核心能力.1','能力指標','學習成效權重','學分']]
    #更換欄位名稱
    dfx.columns=['學年','學期','科目名稱','開課序號','是否開課','科目代碼','選必修','通識類別代碼','通識類別','選課人數','節次起','節次迄','核心能力','能力指標','學習成效權重','學分']
    #篩選已開課
    dfx=dfx[dfx.是否開課=='Y']
    
    return dfx

def read_courses_evaluation(filename):
    df=pd.read_excel(filename)

    return df

#加上通識新類別資料
def addNewType(df):
    #df['通識類別新代碼']=df.apply(lambda row: transfer01(row), axis=1)
    df['通識類別代碼1']=df.apply(lambda row: transfer01(row)[0], axis=1)
    df['通識類別1']=df.apply(lambda row: transfer01(row)[1], axis=1)
    df['AA']=df.apply(lambda row: transfer02(row)[0], axis=1)
    df['BB']=df.apply(lambda row: transfer02(row)[1], axis=1)
    df['CC']=df.apply(lambda row: transfer02(row)[2], axis=1)
    df['DD']=df.apply(lambda row: transfer02(row)[3], axis=1)
    df['EE']=df.apply(lambda row: transfer02(row)[4], axis=1)
    df['FF']=df.apply(lambda row: transfer02(row)[5], axis=1)
    df['通識類別代碼2']=df.apply(lambda row: transfer03(row)[0], axis=1)
    df['通識類別2']=df.apply(lambda row: transfer03(row)[1], axis=1)
    return df

#得所有科目代號，並求出科目代號的開課數量及修課總人數
def all_courseID(df):
    
    dfx=df[['學年','學期','科目代碼','開課序號','科目名稱','選必修','通識類別代碼','通識類別','學分','選課人數']]
    dfx=dfx.drop_duplicates(subset=['學年','學期','開課序號'])
    #dfx=dfx.sort_values(['學年','科目代碼'],ignore_index=True)

    dfx['開課數量']=dfx.groupby(by=['學年','科目代碼'], sort=False)['科目代碼'].transform('count')
    dfx['選課總人數']=dfx.groupby(by=['學年','科目代碼'], sort=False)['選課人數'].transform('sum')
    
    dfx=dfx.drop_duplicates(subset=['學年','科目代碼'])

    #dfx=dfx.set_index(['學年','科目代碼'])
    return dfx


#求出所有課程及相關核心能力
def all_courses(df):
    dfx=df[['學年','學期','科目代碼','開課序號','科目名稱','選必修','通識類別代碼','通識類別','學分','選課人數','核心能力','能力指標','學習成效權重']]
    #dfx=dfx.drop_duplicates(subset=['學年','學期','開課序號','能力指標'])
    dfy=pd.pivot_table(dfx, index=['學年','學期','開課序號','科目名稱','通識類別','學分', '通識類別代碼'], columns='核心能力', values='學習成效權重', aggfunc='sum', fill_value=0)
    
    dfy.reset_index(inplace=True)

    #dfy=dfy.set_index(['學年','學期','開課序號'])
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

def df_tolist(df):
    dflist=[]

#def addCourseEvaluation(df, dfce):
#def addNewTypebyID(df1, df2):

def core_sum_by_gtype(df):
    dfx=addNewType(df)
    dfx=dfx[dfx.通識類別代碼2.isin(['1','2','3','s','5','l'])]
    dfx=dfx.groupby(['通識類別代碼2', '通識類別2'])['AA','BB','CC','DD','EE','FF'].sum()
    dfx.reset_index(inplace=True)
    
    
    #print(dfx)
    return dfx


if __name__=='__main__':
    df=read_courses('107-109general_0611.xls')
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

    df1x=all_courses(df)
    #所有課程核心能力加上新分類
    df6=addNewType(df1x)
    df6x=core_sum_by_gtype(df6)
    #print('ok')
    print(df6x.values)
    df6.to_excel('allcourses.xlsx', index=False)
        
    #課程評量
    dfce=read_courses_evaluation('107-109course.xlsx')
    print(dfce)

    #所有課程核心能力加上新分類再加上課程評量
    #df7=addCourseEvaluation(df6, dfce)
    #print(df7)


    #df8=addNewTypebyID(dfce, df6)
    df8=pd.merge(df6,dfce, left_on=['學年','學期','開課序號'], right_on=['學年','學期','開課序號'], how='left' )
    #df8=pd.merge(dfce,df6, left_on=['學年','學期','開課序號'], right_on=['學年','學期','開課序號'], how='left' )
    df8.rename(columns=CoreType, inplace=True)
    print(df8.columns)
    df8.to_excel('test01.xlsx', index=False)
    