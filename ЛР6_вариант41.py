"""ЛР №6. Модуль itertools. Вариант 41"""
from itertools import product, permutations, combinations, cycle, islice

# ---------- Задание 1: product ----------
alpha, n = "АЛГОРИТ", 6
X, Y = "И", "Т"
codes = ("".join(c) for c in product(sorted(alpha), repeat=n))
ok = [c for c in codes
      if c.count(X) <= 1 and c[-1] != X
      and X + Y not in c and Y + X not in c]
print("Задание 1")
print("Количество:", len(ok))
print("Первые 5:", ok[:5])

# ---------- Задание 2: permutations ----------
word = "МИМИНО"
vowels = set("АЕЁИОУЫЭЮЯ")
uniq = set(permutations(word))
good = sorted("".join(p) for p in uniq
              if not any(a in vowels and b in vowels for a, b in zip(p, p[1:])))
print("\nЗадание 2")
print("Всего различных слов:", len(uniq))
print("Подходящих:", len(good))
print(good)

# ---------- Задание 3: combinations ----------
data = [4, 6, 13, 20, 26, 32, 39]
res = [c for c in combinations(data, 3) if sum(c) <= 45]
print("\nЗадание 3")
print(len(res), res)
print([(c, sum(c)) for c in res])

# ---------- Задание 4 (тип «б»): cycle + islice ----------
digits, K = (3, 6, 9, 2), 48
first = list(islice(cycle(digits), K))
print("\nЗадание 4")
print("Сумма:", sum(first), "Среднее:", sum(first)/K)
