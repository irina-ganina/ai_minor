import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# Считываем датасет
df = pd.read_csv('train.csv')

# Визуализируем распределение (Survived, Pclass, Age, Sex, Parch)
fig, ax = plt.subplots()
counts_surv = df['Survived'].value_counts()
ax.bar(counts_surv.index, counts_surv.values)
ax.set_title('Распределение Survived')
ax.set_xlabel('0 - не выжил, 1 - выжил')
ax.set_ylabel('Количество')
plt.show()

fig, ax = plt.subplots()
counts_pclass = df['Pclass'].value_counts()
ax.bar(counts_pclass.index, counts_pclass.values)
ax.set_title('Распределение Pclass')
ax.set_xlabel('Класс билета')
ax.set_ylabel('Количество')
plt.show()

fig, ax = plt.subplots()
ax.hist(df['Age'].dropna(), bins=20)
ax.set_title('Распределение Age')
ax.set_xlabel('Возраст')
ax.set_ylabel('Количество')
plt.show()

fig, ax = plt.subplots()
counts_sex = df['Sex'].value_counts()
ax.bar(counts_sex.index, counts_sex.values)
ax.set_title('Распределение Sex')
ax.set_xlabel('Пол')
ax.set_ylabel('Количество')
plt.show()

fig, ax = plt.subplots()
counts_parch = df['Parch'].value_counts()
ax.bar(counts_parch.index, counts_parch.values)
ax.set_title('Распределение Parch')
ax.set_xlabel('Количество родителей/детей на борту')
ax.set_ylabel('Количество')
plt.show()

# Построим график типа boxplot для столбца Age
plt.figure(figsize=(8, 6))
sns.boxplot(x='Age', data=df)
plt.title('Boxplot of Age')
plt.xlabel('Age')
plt.show()

# Проанализировать boxplot
#Основная масса возрастов (от первого до третьего квартиля) находится в диапазоне примерно от 20 до 38 лет.
#Медиана, обозначенная горизонтальной линией в ящике, составляет около 27–28 лет.
#Мы также наблюдаем выбросы как в сторону более молодого возраста (ближе к 0), так и в сторону пожилых людей (возраст около 70–80 лет).
#Это указывает на то, что большинство пассажиров находятся в возрасте примерно от 20 до 40 лет, однако среди них есть и значительно более молодые, и значительно более пожилые пассажиры.

# Построим график типа pie chart для переменных Survived и Pclass
survived_counts = df['Survived'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(survived_counts, labels=survived_counts.index, autopct='%1.1f%%')
plt.title('Survival Rate')
plt.show()

pclass_counts = df['Pclass'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(pclass_counts, labels=pclass_counts.index, autopct='%1.1f%%')
plt.title('Passenger Class Distribution')
plt.show()

# Построим график типа pairplot для всех числовых переменных
sns.pairplot(df.select_dtypes(include=['float64', 'int64']))
plt.show()
# Построим интерактивный sunburst plot с помощью plotly
df['Gender'] = df['Sex'].map({'male': 'Male', 'female': 'Female'})
sunburst_data = df.groupby(['Pclass', 'Gender']).size().reset_index(name='Count')
fig = px.sunburst(sunburst_data, path=['Pclass', 'Gender'], values='Count', title='Passenger Distribution by Class and Gender')
fig.show()

