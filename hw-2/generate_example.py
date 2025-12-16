
from src.latex_generator import generate_latex_table, generate_latex_image


def main():
    data = [
        ['Column 1', 'Column 2'],
        ['Row 1 Data 1', 'Row 1 Data 2'],
        ['Row 2 Data 1', 'Row 2 Data 2']
    ]
    
    table = generate_latex_table(data)
    image = generate_latex_image('includes/test-picture.png', 
                                  caption='Test Picture', 
                                  width='0.5\\textwidth')
    
    latex = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{graphicx}}

\\begin{{document}}

\\section{{Table Example}}

{table}

\\section{{Image Example}}

{image}

\\end{{document}}"""
    
    path = 'artifacts/task_2_2.tex'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print(f"Artifact saved to {path}")


if __name__ == '__main__':
    main()

