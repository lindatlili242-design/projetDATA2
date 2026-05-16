import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare data
df = pd.read_csv('AI_Impact_Student_Life_2026.csv')

df.drop_duplicates(inplace=True)

df['GPA_Improvement'] = df['GPA_Post_AI'] - df['GPA_Baseline']

def gpa_status(diff):
    if diff > 0:    return 'Improved'
    elif diff == 0: return 'Same'
    else:           return 'Decreased'

df['GPA_Change'] = df['GPA_Improvement'].apply(gpa_status)

def age_group(age):
    if age <= 20:   return 'Junior'
    elif age <= 22: return 'Mid'
    else:           return 'Senior'

df['AgeGroup'] = df['Age'].apply(age_group)

# ── Title 
st.title("🤖 AI Impact on Student Life Dashboard")
st.write("Total students:", len(df))

# ── Sidebar filters 
st.sidebar.title("Filters")

major_options = ["All"] + list(df["Major"].unique())
selected_major = st.sidebar.selectbox("Major", major_options)

tool_options = ["All"] + list(df["Primary_AI_Tool"].unique())
selected_tool = st.sidebar.selectbox("AI Tool", tool_options)

age_options = ["All"] + list(df["AgeGroup"].unique())
selected_age = st.sidebar.selectbox("Age Group", age_options)

ethics_options = ["All"] + list(df["AI_Ethics_Concern"].unique())
selected_ethics = st.sidebar.selectbox("Ethics Concern", ethics_options)

# Apply filters
if selected_major  != "All": df = df[df["Major"]            == selected_major]
if selected_tool   != "All": df = df[df["Primary_AI_Tool"]  == selected_tool]
if selected_age    != "All": df = df[df["AgeGroup"]         == selected_age]
if selected_ethics != "All": df = df[df["AI_Ethics_Concern"]== selected_ethics]

st.write("Showing:", len(df), "students")

# ── Key Numbers 
st.header("📊 Key Numbers")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students",     len(df))
col2.metric("Avg GPA Before AI",  round(df["GPA_Baseline"].mean(), 2))
col3.metric("Avg GPA After AI",   round(df["GPA_Post_AI"].mean(), 2))
col4.metric("Avg Time Saved",     str(round(df["Time_Saved_Hours_Weekly"].mean(), 1)) + "h/week")

# ── Statistical Summary 
st.header("📋 Statistical Summary")
st.dataframe(df[["Age", "GPA_Baseline", "GPA_Post_AI", "GPA_Improvement",
                  "Time_Saved_Hours_Weekly", "Career_Confidence_Score"]].describe().round(2))

# ── GroupBy Tables 
st.header("🎓 GPA Improvement by Major")
st.dataframe(df.groupby("Major")["GPA_Improvement"].mean().round(3).sort_values(ascending=False))

st.header("⏰ Time Saved by AI Tool")
st.dataframe(df.groupby("Primary_AI_Tool")["Time_Saved_Hours_Weekly"].mean().round(1).sort_values(ascending=False))

st.header("📚 Stats by Major")
st.dataframe(df.groupby("Major").agg(
    AvgGPA_Before  = ("GPA_Baseline", "mean"),
    AvgGPA_After   = ("GPA_Post_AI", "mean"),
    AvgTimeSaved   = ("Time_Saved_Hours_Weekly", "mean"),
    AvgCareerScore = ("Career_Confidence_Score", "mean"),
    TotalStudents  = ("Student_ID", "count")
).round(2))

# ── Charts 
st.header("📈 Charts")

# Chart 1: Most used AI tool
st.subheader("Most Used AI Tool")
tool_counts = df["Primary_AI_Tool"].value_counts()
fig1, ax1 = plt.subplots()
ax1.bar(tool_counts.index, tool_counts.values, color="steelblue")
ax1.set_xlabel("AI Tool")
ax1.set_ylabel("Number of Students")
plt.xticks(rotation=15)
st.pyplot(fig1)

# Chart 2: Main usage case
st.subheader("What do Students use AI for?")
usage_counts = df["Main_Usage_Case"].value_counts()
fig2, ax2 = plt.subplots()
ax2.bar(usage_counts.index, usage_counts.values, color="orange")
ax2.set_xlabel("Usage Case")
ax2.set_ylabel("Number of Students")
plt.xticks(rotation=15)
st.pyplot(fig2)

# Chart 3: GPA before vs after by Major
st.subheader("GPA Before vs After AI by Major")
gpa_major = df.groupby("Major")[["GPA_Baseline", "GPA_Post_AI"]].mean().round(2)
fig3, ax3 = plt.subplots(figsize=(8, 4))
gpa_major.plot(kind="bar", ax=ax3, color=["red", "green"])
ax3.set_xlabel("Major")
ax3.set_ylabel("GPA")
plt.xticks(rotation=15)
st.pyplot(fig3)

# Chart 4: GPA change status
st.subheader("Did AI Improve GPA?")
change_counts = df["GPA_Change"].value_counts()
fig4, ax4 = plt.subplots()
ax4.pie(change_counts.values, labels=change_counts.index, autopct="%1.1f%%",
        colors=["green", "orange", "red"])
st.pyplot(fig4)

# Chart 5: Ethics concern distribution
st.subheader("AI Ethics Concern Level")
ethics_counts = df["AI_Ethics_Concern"].value_counts()
fig5, ax5 = plt.subplots()
ax5.bar(ethics_counts.index, ethics_counts.values, color=["red", "orange", "green"])
ax5.set_xlabel("Ethics Concern")
ax5.set_ylabel("Number of Students")
st.pyplot(fig5)

# Chart 6: Career confidence by Major
st.subheader("Career Confidence Score by Major")
career_major = df.groupby("Major")["Career_Confidence_Score"].mean().round(2).sort_values()
fig6, ax6 = plt.subplots(figsize=(8, 4))
career_major.plot(kind="barh", ax=ax6, color="purple")
ax6.set_xlabel("Avg Career Confidence Score")
st.pyplot(fig6)

# ── Business Insight ───────────────────────────────────────
st.header("💡 Business Insights")

st.subheader("🏆 Best AI tool for GPA improvement")
best_tool = df.groupby("Primary_AI_Tool")["GPA_Improvement"].mean().sort_values(ascending=False)
st.dataframe(best_tool.round(3))
st.write("Best tool:", best_tool.idxmax())

st.subheader("⚠️ Students with decreased GPA after AI")
decreased = df[df["GPA_Change"] == "Decreased"][["Student_ID", "Major", "Primary_AI_Tool",
                                                   "GPA_Baseline", "GPA_Post_AI"]]
st.write(len(decreased), "students had lower GPA after using AI")
st.dataframe(decreased.head(10))

# ── Full Dataset ───────────────────────────────────────────
st.header("🔍 Full Dataset")
st.dataframe(df)
