"""ЛР №6. Модуль itertools. Вариант 16"""
from itertools import (product, permutations, combinations,
                       count, accumulate, islice)
from operator import mul

# ---------- Задание 1: product ----------
alpha, n = "ТИМОФЕЙ", 4
X, Y = "Й", "О"
codes = ("".join(c) for c in product(sorted(alpha), repeat=n))  # лексикографический порядок
ok = [c for c in codes
      if c.count(X) <= 1            # Й не более одного раза
      and c[-1] != X                # Й не на последнем месте
      and X + Y not in c            # Й и О не рядом
      and Y + X not in c]
print("Задание 1")
print("Количество:", len(ok))
print("Первые 5:", ok[:5])

# ---------- Задание 2: permutations ----------
word = "НАГАН"
vowels = set("АЕЁИОУЫЭЮЯ")
uniq = set(permutations(word))      # уникальные перестановки
good = sorted("".join(p) for p in uniq
              if not any(a in vowels and b in vowels for a, b in zip(p, p[1:])))
print("\nЗадание 2")
print("Всего различных слов:", len(uniq))
print("Подходящих:", len(good))
print(good)

# ---------- Задание 3: combinations ----------
data = [1, 8, 13, 18, 24, 30, 37]
res = [c for c in combinations(data, 3) if sum(c) <= 40]
print("\nЗадание 3")
print(len(res), res)

# ---------- Задание 4 (тип «а»): accumulate + islice ----------
def seq():
    return (4*i*i + i - 2 for i in count(0))     # a_i = 4i^2 + i - 2
terms = list(islice(seq(), 10))
prod = list(islice(accumulate(seq(), mul), 10))[-1]
print("\nЗадание 4")
print("Первые 10 членов:", terms)
print("Произведение:", prod)
