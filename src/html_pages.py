from pathlib import Path

def html_table_col(value, file):
    print(f'    <td>{value}</td>', file=file)

def html_table_row(values:list, file):
    print('<tr>', file=file)
    for value in values:
        html_table_col(value, file=file)
    print('</tr>', file=file)

def html_start_table(headers:list, file, caption:str=''):
    print('<table id="sortableTable">', file=file)
    if caption:
        print(f'<caption>{caption}</caption>', file=file)
    print('<tr>', file=file)
    for i_h,header in enumerate(headers):
        print(f'    <th onclick="sortTable({i_h})">{header}</th>', file=file)
    print('</tr>', file=file)
    print('<tbody id="tableBody">', file=file)

def html_end_table(file):
    print('</tbody>', file=file)
    print('</table>', file=file)

def html_list(items:list, file):
    print('<ul>', file=file)
    for item in items:
        print(f'    <li>{item}</li>', file=file)
    print('</ul>', file=file)

def html_h(header:str, level:int, file):
    print(f'<h{level}>{header}</h{level}>', file=file)

def html_p(text:str, file):
    print(f'<p>{text}</p>', file=file)

def html_link(show_str:str, link:Path)->str:
    web_link = link.as_posix().replace('docs/', '')
    if web_link.startswith('https:/'):
        web_link = web_link.replace('https:/', 'https://')
    return f'<a href="{web_link}">{show_str}</a>'

def html_header(title:str, css, file_id):
    print('<!DOCTYPE html>', file=file_id)
    print('<html lang="en">', file=file_id)
    print('<head>', file=file_id)
    print('  <meta charset="utf-8">', file=file_id)
    print('  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">', file=file_id)
    print(f'  <title>{title}</title>', file=file_id)
    print(f'  <link rel="stylesheet" type="text/css" href="{css}">', file=file_id)
    print('</head>', file=file_id)
    print('', file=file_id)
    print('<body>', file=file_id)
    print('', file=file_id)

def html_footer(file_id, script):
    print('', file=file_id)
    print(f'  <script src="{script}"></script>', file=file_id)
    print('</body>', file=file_id)
    print('</html>', file=file_id)