
from src.latex_table import generate_latex_table


def main():
    data = [
        ['Column 1', 'Column 2'],
        ['Row 1 Data 1', 'Row 1 Data 2'],
        ['Row 2 Data 1', 'Row 2 Data 2']
    ]
    
    latex = generate_latex_table(data, with_document=True)
    
    path = 'artifacts/task_2_1.tex'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print(f"Artifact saved to {path}")


if __name__ == '__main__':
    main()

