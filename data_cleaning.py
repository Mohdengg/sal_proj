# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:40:53 2021

@author: Katpadi
"""


import pandas as pd
df = pd.read_csv("glassdoor_jobs.csv")

#Salary Estimate


df = df[df['Salary Estimate'] !='-1']

salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kd = salary.apply(lambda x:x.replace('K','').replace('$',''))

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'Employer Provided' in x.lower() else 0)

min_hr = minus_kd.apply(lambda x:x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary']  = min_hr.apply(lambda x: int(x.split('-')[0]))

print(df['min_salary'].dtype)

df['max_salary']  = min_hr.apply(lambda x: int(x.split('-')[1]))

df['avg_salary'] = (df.min_salary + df.max_salary)/2

# Company Name Text

df['company_txt'] = df.apply(lambda x:x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3],axis=1)

# state Field

df['job_state'] = df['Location'].apply(lambda x:x.split(',')[1])
print(df['job_state'].value_counts())

df['same_state'] = df.apply(lambda x:1 if x.Location== x.Headquarters else 0,axis=1)

#age of Company

df['age'] = df.Founded.apply(lambda x:x if x <1 else 2021-x)

# Parsing of Job Description Python..etc

df['Job Description'][0]

#python
df['python'] = df['Job Description'].apply(lambda x:1 if 'python' in x.lower() else 0)

#r-studio
df['R_yn'] = df['Job Description'].apply(lambda x:1 if 'r studio' or 'r-studio' in x.lower() else 0)
df['R_yn'].value_counts()

#spark
df['spark']= df['Job Description'].apply(lambda x:1 if 'spark' in x.lower() else 0)
df['spark'].value_counts()

#aws
df['aws']= df['Job Description'].apply(lambda x:1 if 'aws' in x.lower() else 0)
df['aws'].value_counts()

#excel
df['excel']= df['Job Description'].apply(lambda x:1 if 'excel' in x.lower() else 0)
df['excel'].value_counts()

df.columns
df_out = df.drop(['Unnamed: 0'],axis=1)

df_out.to_csv("salary_data_cleaned.csv",index=False)