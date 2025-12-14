
# Task 1.3

1) Один файл

Команда:

```bash
poetry run hw-wc test_files/sample1.txt
```

Вывод:

```text
       4      15      73 test_files/sample1.txt
```

2) Несколько файлов

Команда:

```bash
poetry run hw-wc test_files/sample1.txt test_files/sample2.txt
```

Вывод:

```text
       4      15      73 test_files/sample1.txt
      19      40     150 test_files/sample2.txt
      23      55     223 total
```

3) stdin

Команда:

```bash
echo "Hello World                                                                                                                               
Test line" | poetry run hw-wc
```

Вывод:

```text
       2       4      22
```
