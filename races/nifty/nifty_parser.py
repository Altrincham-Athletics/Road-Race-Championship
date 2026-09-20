import sys

input_path = sys.argv[1]
output_path = sys.argv[2]
if len(sys.argv) > 3:
    encoding = sys.argv[3]
else:
    encoding = 'UTF-8'

all_data = []
lines = []
with open(input_path, 'rt', encoding=encoding) as f:
    for line in f:
        try:
            lines.append(line.rstrip())
        except Exception:
            pass

headers = lines[1].split(',')
for line in lines[2:]:
    all_data.append(line.split(','))
num_cols = len(headers)

time_col = -1
first_name_col = -1
last_name_col = -1
club_col = -1

for col_num,col in enumerate(headers):
    col_name = col.lower().strip()
    if col_name == 'chip time':
        time_col = col_num
    elif col_name == 'name':
        first_name_col = col_num
    elif col_name == 'first name':
        first_name_col = col_num
    elif col_name == 'last name':
        last_name_col = col_num
    elif col_name == 'club':
        club_col = col_num

print('Headers: ', headers)
print(club_col)
print(time_col)
print(first_name_col)
print(last_name_col)

with open(output_path, 'wt') as f:
    for row in all_data:
        if len(row) != num_cols:
            continue
        if row[club_col].lower().startswith('altrincham') and row[time_col]:
            if last_name_col < 0:
                name = row[first_name_col]
            else:
                name = f'{row[first_name_col]} {row[last_name_col]}'
            
            #Deal with custom overrides
            if name == 'Andy Pickford':
                name = 'Andrew Pickford'
            if name == 'Richard Hill':
                name = 'Richard Hill'
            elif name == 'Kieran McGlade':
                continue

            print(f'{name}, {row[time_col]}')
            print(f'{name}, {row[time_col]}', file=f)
