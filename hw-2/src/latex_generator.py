from typing import Any, List, Optional


def escape_latex_char(char: str) -> str:
    special_chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    return special_chars.get(char, char)


def escape_latex_string(text: str) -> str:
    return ''.join(map(escape_latex_char, str(text)))


def format_cell(cell: Any) -> str:
    return escape_latex_string(cell)


def format_row(row: List[Any]) -> str:
    return ' & '.join(map(format_cell, row)) + r' \\'


def create_column_spec(num_columns: int) -> str:
    return '|' + '|'.join(['c'] * num_columns) + '|'


def wrap_in_tabular(column_spec: str, rows_content: str) -> str:
    return f"\\begin{{tabular}}{{{column_spec}}}\n\\hline\n{rows_content}\n\\hline\n\\end{{tabular}}"


def wrap_in_table(tabular_content: str, caption: Optional[str] = None, label: Optional[str] = None) -> str:
    parts = ["\\begin{table}[h!]", "\\centering"]
    
    if caption:
        parts.append(f"\\caption{{{escape_latex_string(caption)}}}")
    
    if label:
        parts.append(f"\\label{{tab:{label}}}")
    
    parts.append(tabular_content)
    parts.append("\\end{table}")
    
    return '\n'.join(parts)


def generate_latex_table(
    data: List[List[Any]],
    with_document: bool = False,
    caption: Optional[str] = None,
    label: Optional[str] = None
) -> str:
    if not data or not data[0]:
        return ""
    
    num_columns = len(data[0])    
    column_spec = create_column_spec(num_columns)
    
    rows_content = '\n'.join(map(format_row, data))
    
    tabular = wrap_in_tabular(column_spec, rows_content)
    
    if caption or label:
        table_content = wrap_in_table(tabular, caption, label)
    else:
        table_content = tabular
    
    if with_document:
        return wrap_in_document(table_content)
    
    return table_content


def wrap_in_document(content: str) -> str:
    return f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{graphicx}}

\\begin{{document}}

{content}

\\end{{document}}"""


def generate_latex_image(
    image_path: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    width: Optional[str] = None,
    height: Optional[str] = None,
    scale: Optional[float] = None,
    center: bool = True
) -> str:
    options: List[str] = []
    if width:
        options.append(f'width={width}')
    if height:
        options.append(f'height={height}')
    if scale is not None:
        options.append(f'scale={scale}')
    
    options_str = f'[{",".join(options)}]' if options else ''
    
    includegraphics = f'\\includegraphics{options_str}{{{image_path}}}'
    
    if center:
        includegraphics = f'\\centering\n{includegraphics}'
    
    if not caption and not label:
        return includegraphics
    
    parts = ['\\begin{figure}[h!]']
    parts.append(includegraphics)
    
    if caption:
        parts.append(f'\\caption{{{escape_latex_string(caption)}}}')
    
    if label:
        parts.append(f'\\label{{fig:{label}}}')
    
    parts.append('\\end{figure}')
    
    return '\n'.join(parts)

