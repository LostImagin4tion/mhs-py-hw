
# Task 1.1

1) Простое чтение из файла

Команда:

```bash
poetry run hw-nl test_files/sample1.txt
```

Вывод:

```text
     1  Hello, World!
     2  This is a test file.
     3  Line 3 here.
     4
     5  Line 5 after empty line.
```

2) Чтение из stdin

Команда:

```bash
poetry run hw-nl
```

Вывод:

```text
hello
     1  hello
world
     2  world
nice
     3  nice
```

3) Чтение из pipe

Команда:

```bash
echo "Line 1
Line 2
Line 3" | poetry run hw-nl
```

Вывод:

```text
     1  Line 1
     2  Line 2
     3  Line 3
```
