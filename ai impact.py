# Modification de test pour GitHub - projet data science
import pandas as pd 
df = pd.read_csv('C:/Users/LENOVO/Desktop/projetDATA2/AI_Impact_Student_Life_2026.csv')
#data exploration
print(df.head(5))
df.info()
print(df.columns)
print(df.shape)
print(df.isnull())
print(df.isnull().sum())
df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(df.describe())
#data cleaning

# See how many unknowns in each column
print((df == 'unknown').sum())
# remplacer 'unknown' par NaN
df.replace('unknown', pd.NA, inplace=True)

# supprimer les valeurs nulles
df.dropna(inplace=True)

# supprimer les doublons
df.drop_duplicates(inplace=True)
# GPA improvement after using AI
df['GPA_Improvement'] = df['GPA_Post_AI'] - df['GPA_Baseline']

# Did GPA improve?
def gpa_status(diff):
    if diff > 0:   return 'Improved'
    elif diff == 0: return 'Same'
    else:           return 'Decreased'

df['GPA_Change'] = df['GPA_Improvement'].apply(gpa_status)

# Age group
def age_group(age):
    if age <= 20:  return 'Junior'
    elif age <= 22: return 'Mid'
    else:           return 'Senior'

df['AgeGroup'] = df['Age'].apply(age_group)
print(df.groupby('Major')['GPA_Improvement'].mean().sort_values(ascending=False))
print(df['Primary_AI_Tool'].value_counts())
print(df.groupby('Primary_AI_Tool')['Time_Saved_Hours_Weekly'].mean().sort_values(ascending=False))
print(df['Main_Usage_Case'].value_counts())
print(df.groupby('Major').agg(
    AvgGPA_Before    = ('GPA_Baseline', 'mean'),
    AvgGPA_After     = ('GPA_Post_AI', 'mean'),
    AvgTimeSaved     = ('Time_Saved_Hours_Weekly', 'mean'),
    AvgCareerScore   = ('Career_Confidence_Score', 'mean'),
    TotalStudents    = ('Student_ID', 'count')
).round(2))
print(df.groupby('Primary_AI_Tool')['Task_Frequency_Daily'].mean().sort_values(ascending=False))
