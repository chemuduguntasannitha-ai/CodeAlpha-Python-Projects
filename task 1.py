import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv"
df = pd.read_csv(DATA_URL)

print("Dataset shape:", df.shape)
print(df.head())
df.info()

os.makedirs("outputs", exist_ok=True)

# Clean data
df['age'] = df['age'].fillna(df['age'].median())
df = df.drop(columns=['deck'])
df['embarked'] = df['embarked'].fillna(df['embarked'].mode()[0])
df['embark_town'] = df['embark_town'].fillna(df['embark_town'].mode()[0])
df = df.dropna()

# Stats
survival_rate = df['survived'].mean() * 100
survival_by_class = df.groupby('pclass')['survived'].mean() * 100
survival_by_sex = df.groupby('sex')['survived'].mean() * 100
print(f"Overall survival rate: {survival_rate:.2f}%")
print(survival_by_class)
print(survival_by_sex)

sns.set_style("whitegrid")

plt.figure(figsize=(8, 5))
sns.histplot(df['age'], bins=30, kde=True, color="steelblue")
plt.title("Age Distribution of Passengers")
plt.savefig("outputs/age_distribution.png", bbox_inches="tight")
plt.close()

plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="pclass", hue="survived", palette="Set2")
plt.title("Survival Count by Passenger Class")
plt.legend(title="Survived", labels=["No", "Yes"])
plt.savefig("outputs/survival_by_class.png", bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
sns.barplot(data=df, x="sex", y="survived", hue="sex", palette="Set1", legend=False)
plt.title("Survival Rate by Sex")
plt.savefig("outputs/survival_by_sex.png", bbox_inches="tight")
plt.close()

plt.figure(figsize=(7, 5))
sns.boxplot(data=df, x="pclass", y="fare", hue="pclass", palette="coolwarm", legend=False)
plt.title("Fare Distribution by Passenger Class")
plt.savefig("outputs/fare_by_class.png", bbox_inches="tight")
plt.close()

plt.figure(figsize=(8, 6))
numeric_df = df.select_dtypes(include=['int64', 'float64'])
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.savefig("outputs/correlation_heatmap.png", bbox_inches="tight")
plt.close()

print("All charts saved in 'outputs' folder.")
