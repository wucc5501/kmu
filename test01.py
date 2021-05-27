import pandas as pd

def read_data(filename):

    df=pd.read_excel(filename)

    #去除欄位名稱後的/xa0
    columns=df.columns
    columns=[c.strip() for c in columns]
    df.columns=columns
    #print(df.columns)

    return df

#107-109所有科目
def all_courseID(df):
    
    dfx=df[['學年','科目代碼','科目名稱','選必修','通識類別代碼','通識類別','學分']]
    dfx=dfx.drop_duplicates(ignore_index=True)
    return dfx
#print(df1)

#找出符合學年度及科目代碼的課程
def request_courses(df, year, courseID):
    dfx=df[(df.學年==year) & (df.科目代碼==courseID)]
    dfx=dfx['學年','科目代碼','科目名稱','選必修','通識類別代碼','通識類別','學分','開課序號']
    dfx=dfx.sort_values('開課序號',ignore_index=True)
    return dfx

#找出符合學年度及通識類別代碼的課程代碼
def request_courseID(df, year, generalType):
    dfx=df[(df.學年==year) & (df.通識類別代碼==generalType)]
    dfx=dfx.sort_values('科目代碼',ignore_index=True)
    dfx.columns=['year','id','name','need','generaltype','generalname','credit']
    return dfx

#找出符合學年度及通識類別代碼的課程代碼及統計開課數及修課人數
def course_sum(df, year, generalType):
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

#找出符合學年度及通識類別代碼的課程代碼及統計開課數及修課人數
def core(df):
    dfx=df[['學年','科目名稱','開課序號','科目代碼','選必修','核心能力.1','學習成效權重','學分']]
    dfx['核心分數']=dfx['學習成效權重']*0.01*dfx['學分']
    dfx=dfx.groupby(by=['學年','核心能力.1']).sum()
    
    return dfx

if __name__=='__main__':
    df=read_data('107-109general.xls')

    df1=all_courseID(df)
    print(df1)
    '''
    print(course_sum(109,'7'))


    df2=df[['核心能力.1', '核心能力說明']]
    df2=df2.drop_duplicates()
    df2=df2.sort_values('核心能力.1')
    print(df2)

    print(core(df).loc[107,:])
    '''