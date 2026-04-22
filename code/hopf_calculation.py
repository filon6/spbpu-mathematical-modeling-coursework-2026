import numpy as np
import pandas as pd


def stationary_check(x1, x2, p2, p4, p5):
    E = np.exp(20 * x2 / (20 + x2))

    f1 = -x1 + p2 * (1 - x1) * E
    f2 = -(1 + p5) * x2 + p2 * p4 * (1 - x1) * E

    return abs(f1) < 1e-3 and abs(f2) < 1e-3


def hopf_check(a11, a12, a21, a22):
    J = np.array([
        [a11, a12],
        [a21, a22]
    ])

    eigenvalues = np.linalg.eigvals(J)

    l1 = eigenvalues[0]
    l2 = eigenvalues[1]

    complex_pair = np.iscomplex(l1) and np.iscomplex(l2)
    real_zero = abs(l1.real) < 1e-3 and abs(l2.real) < 1e-3

    if complex_pair and real_zero:
        return "Подходит"
    else:
        return "НЕ подходит"


def print_all(df, p4):
    df_all = df.copy()
    df_all.index = np.arange(1, len(df_all) + 1)

    print(f"Полная таблица для p4 = {p4}")

    print(df_all.to_csv(sep="\t", index=True))


p4_vals = [12, 10, 8, 6]
x2_vals = np.arange(1, 8, 0.1)


for p4 in p4_vals:
    rows = []
    for x2 in x2_vals:
        A = x2 - 400 * x2**2 / (20 + x2)**2
        B = -p4 + 400 * p4 * x2 / (20 + x2)**2
        C = -p4

        roots = np.roots([A, B, C])

        for y in roots:
            if np.isreal(y):
                p5 = y.real - 1
                if p5 > 0:
                    denominator = p4 - (1 + p5) * x2

                    if abs(denominator) < 1e-6:
                        continue

                    x1 = (1 + p5) * x2 / p4
                    p2E = (1 + p5) * x2 / denominator

                    E = np.exp(20 * x2 / (20 + x2))
                    p2 = p2E / E

                    if not stationary_check(x1, x2, p2, p4, p5):
                        continue

                    a11 = -p4 / denominator
                    a12 = 400 * (1 + p5) * x2 / (p4 * (20 + x2)**2)
                    a21 = -p4 * (1 + p5) * x2 / denominator
                    a22 = -(1 + p5) + 400 * (1 + p5) * x2 / (20 + x2)**2

                    result = hopf_check(a11, a12, a21, a22)

                    rows.append([
                        p4,
                        x2,
                        x1,
                        p2,
                        p5,
                        result
                    ])

    df = pd.DataFrame(
        rows,
        columns=["p4", "x2", "x1", "p2", "p5", "Result"]
    ).round(4)

    print_all(df, p4)