import pandas as pd
from collections import defaultdict

# Шаг 1: Считываем датасет
df = pd.read_csv('train.csv')

# Шаг 2: Выводим основную информацию о датасете
print("Основная информация о датасете:")
print(df.info())
print("\nЧисло пропусков:")
print(df.isnull().sum())
print("\nСтатистические показатели (describe):")
print(df.describe(include='all'))

# Шаг 3: Процент выживаемости у каждого класса
survival_rate = df.groupby('Pclass')['Survived'].mean() * 100
print("\nПроцент выживаемости у каждого класса:")
print(survival_rate)

# Шаг 4: Самое популярное мужское и женское имя
def extract_first_name(full_name: str) -> str:
    """
    Выделяем "первое" реальное имя:
    - Для некоторых женщин в скобках указано настоящее имя (например, (Florence ...)).
    - Для мужчин и остальных случаев пытаемся взять имя после титула (Mr., Miss. и т.п.).
    """
    start_idx = full_name.find("(")
    end_idx = full_name.find(")")
    if start_idx != -1 and end_idx != -1:
        in_parentheses = full_name[start_idx + 1 : end_idx].strip()
        return in_parentheses.split()[0]
    else:
        part_after_comma = full_name.split(",")[1].strip()
        parts = part_after_comma.split(".")
        if len(parts) > 1:
            name_part = parts[1].strip()
            first_word = name_part.split()[0] if name_part else ""
            return first_word
        else:
            return part_after_comma

# Создаём столбец с "FirstName"
df["FirstName"] = df["Name"].apply(extract_first_name)

# Самое популярное мужское имя
male_names = df[df["Sex"] == "male"]["FirstName"].value_counts()
most_popular_male = male_names.idxmax() if not male_names.empty else "Нет данных"

# Самое популярное женское имя
female_names = df[df["Sex"] == "female"]["FirstName"].value_counts()
most_popular_female = female_names.idxmax() if not female_names.empty else "Нет данных"

print(f"Самое популярное мужское имя: {most_popular_male}")
print(f"Самое популярное женское имя: {most_popular_female}")

# Шаг 5: Самое популярное мужское и женское имя по классам

grouped = df.groupby(["Pclass", "Sex"])["FirstName"].value_counts()
grouped_df = grouped.reset_index(name="Count")
# В каждой группе (Pclass, Sex) находим FirstName с макс. 'Count'
popular_names_by_class_sex = grouped_df.groupby(["Pclass", "Sex"]).apply(
    lambda g: g.loc[g["Count"].idxmax(), "FirstName"]
)

for (pclass, sex), name in popular_names_by_class_sex.items():
    print(f"Класс {pclass}, Пол {sex}: самое популярное имя — {name}")

# Шаг 6: Пассажиры старше 44 лет
print("\nПассажиры старше 44 лет:")
print(df[df['Age'] > 44])

# Шаг 7: Пассажиры младше 44 лет и мужского пола
print("\nПассажиры младше 44 лет и мужского пола:")
print(df[(df['Age'] < 44) & (df['Sex'] == 'male')])

# Шаг 8: количества n-местных кабин (в которых было 2, 3, 4, ... человека)
# Чтобы посчитать, сколько пассажиров проживало в одной и той же каюте,
# учитываем, что у некоторых пассажиров несколько кают, записанных через пробел (например, 'C23 C25 C27').
# Пропущенные Cabin (NaN) не учитываем.
cabin_occupants = defaultdict(int)

for idx, row in df.dropna(subset=["Cabin"]).iterrows():
    cabins = row["Cabin"].split()
    for c in cabins:
        cabin_occupants[c] += 1

# Получили словарь: cabin_code -> кол-во человек
# Теперь сгруппируем по (кол-во человек), чтобы узнать сколько таких кабин
cabin_counts = defaultdict(int)
for _, count in cabin_occupants.items():
    cabin_counts[count] += 1

for n_people in sorted(cabin_counts.keys()):
    print(f"{n_people}-местных кают: {cabin_counts[n_people]}")
