import pandas as pd


def parse_to_python_array(df, name):
    a = df.to_numpy(na_value=0)
    print(f'{name}=[')
    for i in range(a.shape[0]):
        print('[')
        for j in range(a.shape[1]):
            print(a[i, j], ',')
        print('],')
    print(']')
    pass


df_m = pd.read_excel("SimulationMultiples.xlsx", sheet_name="Multiples M", header=None)
df_f = pd.read_excel("SimulationMultiples.xlsx", sheet_name="Multiple F", header=None)

parse_to_python_array(df_m, "Mat_M")
parse_to_python_array(df_f, "Mat_F")

pass
