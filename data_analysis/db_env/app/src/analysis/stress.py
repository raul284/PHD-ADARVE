import pandas as pd

EXPERIMENT_USER_DATA_PATH = "../data/users/"
EXPERIMENT_USER_RESULT_PATH = "../results/users/"
REVERSE_INDEX = [4, 5, 6, 7, 9, 10, 13]

MAX_VALUE = 14 * 4

# Calcula el estres de todos los usuarios que aparezcan en la 
def calculate_stress():

    # Lee el archivo con la informacion del cuestionario PSS
    df_stress = pd.read_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('stress.csv'))
    df_results = pd.read_csv(EXPERIMENT_USER_RESULT_PATH + "{0}".format('results.csv'))

    # Calcula el estres del usuario y lo almacena en un dict
    results = {}
    for row_index, row in df_stress.iterrows():
        values = [df_stress.iloc[row_index, col_index] for col_index in range(1, len(df_stress.columns))]
        for index in REVERSE_INDEX:
            values[index - 1] = reverse_value(values[index - 1])
        results[row['id']] = round((sum(values) * 100 ) / MAX_VALUE, 2)


    if 'stress' not in df_results.columns:
        df_results["stress"] = [0.0] * len(df_results)

    for key in results:
        for row_index, row in df_results.iterrows():
            if row['id'] == key:
                df_results.at[row_index, 'stress'] = results[key]

    df_results.to_csv(EXPERIMENT_USER_RESULT_PATH + "{0}".format('results.csv'), index=False)

def reverse_value(val):
    if val == 0: return 4
    elif val == 1: return 3
    elif val == 2: return 2
    elif val == 3: return 1
    elif val == 4: return 0