from modules.initializer import Initializer
from modules.transition_matrix import TransitionMatrix
from modules.config import Config
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm


FOLDER = './inputs'

df1 = pd.read_csv(f"{FOLDER}/merged.csv", delimiter=',')
df = df1.sample(frac=1).reset_index(drop=True)

df_test = df.tail(1000)
df = df.iloc[4*round(len(df)/8):5*round(len(df)/8)]
df.to_csv("df_4.csv")

df['Formula'] = df['Formula'].str.replace('-', '1') + '1'
df_test['Formula'] = df_test['Formula'].str.replace('-', '1') + '1'

def process_formula(value):
    formula = value.replace('-', '1')
    config = Config(formula)
    initializer = Initializer(config)
    atoms = initializer.distribute(end=1000, step=200)
    matrix = TransitionMatrix(atoms, config).data
    return matrix

x_train = []
total = len(df_test['Formula'])

def update(*a):
    pbar.update()

with tqdm(total=total) as pbar:

    # Define the number of processes
    num_processes = 8

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(tqdm(executor.map(process_formula, df_test['Formula']), total=total))
        update(pbar)

    x_train.extend(results)


x_train = np.array(x_train)

np.save(f'{FOLDER}/x_train_test_1000.npy', x_train)
df_test.to_csv("./df_test.csv")

# Assuming data2 is already loaded as a pandas DataFrame
def process_formula(value, k=0):
    if k == 0:
        formula = value.replace('-', '1')
    else:
        formula = value
    config = Config(formula)
    initializer = Initializer(config)
    atoms = initializer.distribute(end=1000, step=200)
    matrix = TransitionMatrix(atoms, config).data
    return matrix

def process_row(row):
    index, i = row
    if index % 500 == 0:
        print(index)
    system = i[1]
    decomp = eval(i[10])
    decomp2 = eval(i[11])
    
    # Process system
    system_matrix = process_formula(system)
    string_elements = map(str, system_matrix.flatten())
    resulting_string = ', '.join(string_elements)
    
    # Process decomp
    decomp_sum_matrix = np.zeros((40,40))
    for j in decomp:
        decomp_matrix = process_formula(j, k=1)
        decomp_sum_matrix += decomp_matrix
    string_elements2 = map(str, decomp_sum_matrix.flatten())
    resulting_string2 = ', '.join(string_elements2)
    
    # Process decomp2
    decomp2_sum_matrix = np.zeros((40,40))
    for m in decomp2:
        decomp2_matrix = process_formula(m, k=1)
        decomp2_sum_matrix += decomp2_matrix
    string_elements3 = map(str, decomp2_sum_matrix.flatten())
    resulting_string3 = ', '.join(string_elements3)
    
    return resulting_string, resulting_string2, resulting_string3
total = len(data2)

with tqdm(total=total) as pbar:
    with ProcessPoolExecutor(max_workers=8) as executor:
        results = list(tqdm(executor.map(process_row, data2.iterrows()), total=total))
        for res in results:
            resulting_string, resulting_string2, resulting_string3 = res
            
            # Write results to files
            with open('system_text.txt', 'a') as file:
                file.write(resulting_string + "\n")
            with open('decomp_text.txt', 'a') as file:
                file.write(resulting_string2 + "\n")
            with open('decomp2_text.txt', 'a') as file:
                file.write(resulting_string3 + "\n")
            pbar.update(1)

