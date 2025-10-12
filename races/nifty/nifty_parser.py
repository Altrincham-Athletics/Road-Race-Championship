import sys
import numpy as np

input_path = sys.argv[1]
output_path = sys.argv[2]
club_col = int(sys.argv[3])

all_data = np.loadtxt(input_path, delimiter=',', dtype=str, skiprows=1)

first_name_col = 3
last_name_col = 4
time_col = 5

with open(output_path, 'wt') as f:
    for row in all_data[1:,:]:
        if len(row) < club_col + 1:
            continue
        if row[club_col].lower().startswith('altrincham') and row[time_col]:
            name = f'{row[first_name_col]} {row[last_name_col]}'
            
            #Deal with custom overrides
            if name == 'Andy Pickford':
                name = 'Andrew Pickford'
            if name == 'Rich Hill':
                name = 'Richard Hill'
            elif name == 'Kieran McGlade':
                continue

            print(f'{name}, {row[time_col]}')
            print(f'{name}, {row[time_col]}', file=f)
