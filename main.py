import numpy as np
import pandas as pd

p4_vals = [12, 10, 8, 6]   # порядок как ты просил
x2_vals = np.arange(1, 8, 1)

for p4 in p4_vals:

    rows = []

    for x2 in x2_vals:

        A = x2 - 400*x2**2/(20+x2)**2
        B = -p4 + 400*p4*x2/(20+x2)**2
        C = -p4

        roots = np.roots([A, B, C])

        for y in roots:
            if np.isreal(y):
                p5 = y.real - 1
                if p5 > 0:
                    rows.append([p4, x2, p5])

    df = pd.DataFrame(rows, columns=["p4", "x2", "p5"])
    df = df.round(3)
    df.index = np.arange(1, len(df) + 1)

    print("\nТаблица для p4 =", p4)
    print(df)