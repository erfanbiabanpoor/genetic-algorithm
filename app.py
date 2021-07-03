from typing import Callable
from numpy.random import rand, randint
#تعیین نوع داده(data type)
Person = list[int]
Population = list[Person]
# تابع ساخت افراد
def maxsum(x: Person) -> int:
    return -sum(x)
# تابع عملگر انتخاب
def selection(population: Population, scores: Person, k: int = 3) -> Person:
    # انتخاب اولین شخص به صورت رندوم
    selection_len = randint(len(population))
    for res in randint(0, len(population), k - 1):
        # مقایسه امتیاز شخص انتخاب شده
        if scores[res] < scores[selection_len]:
            selection_len = res
    return population[selection_len]
# تابع عملگر تقاطع دو والد برای تولید دو فرزند جدید
def crossover(p1: Person, p2: Person, crossover_rate: float) -> Population:
    # کروموزوم های فرزندان از والدین کپی می شوند
    c1, c2 = p1.copy(), p2.copy()
    # بررسی برای ترکیب دو والد
    if rand() < crossover_rate:
        pt = randint(1, len(p1) - 2)
        # ترکیب کردن
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]
# تابع جهش
def mutation(bitstring: Person, mutation_rate: float):
    for i in range(len(bitstring)):
        # چک کردن قابلیت جهش
        if rand() < mutation_rate:
            # مکمل کردن بیت های کروموزوم
            bitstring[i] = 1 - bitstring[i]
#تابع الگوریتم ژنتیک
def genetic_algorithm(
    objective: Callable[[Person], int],
    bits_in_candidates: int,
    iterations: int,
    population_size: int,
    crossover_rate: float,
    mutation_rate: float,
):
    # جمعیت اولیه
    population: Population
    population = [
        randint(0, 2, bits_in_candidates).tolist()
        for _ in range(population_size)
    ]
    best: Person
    best, best_eval = population[0], objective(population[0])
    # شمارش نسل ها
    for gen in range(iterations):
        # بررسی همه اشخاص در جمعیت
        scores = [objective(p) for p in population]
        # بررسی و پیدا کردن شخص با ژن بهتر
        for i in range(population_size):
            if scores[i] < best_eval:
                best = population[i]
                best_eval = scores[i]
                print(
                    ">%d, new best f(%s) = %.3f"
                    % (gen, population[i], scores[i])
                )
        # فراخوانی تابع انتخاب
        selected = [
            selection(population, scores) for _ in range(population_size)
        ]
        # ساخت نسل بعدی
        children: Population = list()
        for i in range(0, population_size, 2):
            p1, p2 = selected[i], selected[i + 1]
            # فراخوانی تابع تقاطع و جهش
            for c in crossover(p1, p2, crossover_rate):
                mutation(c, mutation_rate)
                # ذخیره نسل دید در یک لیست
                children.append(c)
        # جایگزینی نسل قبلی با جدید
        population = children
    return [best, best_eval]
#مقدار دهی اولیه
iterations = 100
bits_in_candidates = 40
population_size = 100
crossover_rate = 0.9
mutation_rate = 1.0 / float(bits_in_candidates)
#فراخوانی تابع الگوریتم ژنتیک
best, score = genetic_algorithm(
    maxsum,
    bits_in_candidates,
    iterations,
    population_size,
    crossover_rate,
    mutation_rate,
)
#نمایش بهترین شخص و بهترین امتیاز
print("Done!")
print("f(%s) = %f" % (best, score))