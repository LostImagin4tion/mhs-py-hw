
# Task 1.2

1) Один файл

Команда:

```bash
poetry run hw-tail test_files/sample2.txt
```

Вывод:

```text
Line 11
Line 12
Line 13
Line 14
Line 15
Line 16
Line 17
Line 18
```

2) Несколько файлов

Команда:

```bash
poetry run hw-tail test_files/sample1.txt test_files/sample2.txt
```

Вывод:

```text
==> test_files/sample1.txt <==
Hello, World!
This is a test file.
Line 3 here.

Line 5 after empty line.
==> test_files/sample2.txt <==
Line 11
Line 12
Line 13
Line 14
Line 15
Line 16
Line 17
Line 18
Line 19
Line 20
```

3) stdin

Команда:

```bash
seq 1 25 | poetry run hw-tail
```

Вывод:

```text
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
```
