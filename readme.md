# Python to C++ Parser

The goal of this project is to parse Python script and translate it to C++

Since Python is an indented language, the project makes use of a symbol `<IN>` to indicate an indent. The **program does not interpret regular indents.**

The program also ignores all whitespace. Since the indents are denoted by `<IN>` the ignore of whitespace does not inhibit the script.

The program accepts one command line argument. This argument is the name of the file that contains Python code with indents represented by `<IN>`.

To run the script, run:

`python parser.py file_name`

If there is no file provided, the program runs with a sample prepopulted sameple input to the parser.

Here, I have described the purpose of each test_file:

-   `arithmetic.txt` performs several arithmetic operations. The parser is able to perform addition, subtraction, multiplication, division between constants, and other variables. Currently the parser can only parse arithmetic between two variables. Another important note is that the parser can only be initialized. By this, I mean that the parser cannot perform `a = 1 + 2`. The parser can perform initializations to variables such as `a = 0`. This is because python dynamically parses and assigns data. My parses looks at the data type and creates an assignment based on that. The parser can only assign `int` and `string`.

Indentation

The following indentation examples contain very simple if cases. This is to isolate the problem and focus just on interesting indentation cases.

-   `indent.txt` containts basic indentation of one level indents. Note that the

-   `indent2.txt` contains more advanced nested indents. In particular, there is a 3 level nested indentation following a line at a level 0 indentation. The parser is able to recogonize the level 0 indentation immediatly after a level 3 and close the brackets appropriately.

-   `indent3.txt` contains a much more advanced indentation test. It increases the indentation level, contains 2 if statements at the same indentation level, followed by an indentation decrease.

loops

-   `simple_while.txt` contains a basic while loop. Since the code relies on structure from indents, I have not shown an extensive test to reduce redundancy.

-   `advanced_while.txt` performs an incremental addition

-   `sum_square` sums the square [0,100]
