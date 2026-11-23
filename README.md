# Python Stack 2

Read the Abstract Data Types lecture (Stack section) before you start.
https://drive.google.com/file/d/1jXGQdSvuUYjGXl-PUuHMUzKWEBGQoARL/view?usp=sharing

**Rules for this assignment**

- The stack is an **array of 8 elements** and a **pointer** called `TopOfStack`.
- Do **not** use `.append()` or `.pop()` inside `Push()` and `Pop()`.
  Change `TopOfStack` yourself and use `Stack[TopOfStack]`. The tests check for this.
- Functions **return** their answer — do not print.
- Every function that changes `Stack` or `TopOfStack` needs this line at the top:
  `global Stack, TopOfStack`


## Exercise 1

**Problem:**

Set up the stack:

- `Stack` → a global array of **8** elements, all set to `-1`
- `TopOfStack` → a global integer, set to `-1`

Then write two functions.

`Push(Item)`

- If the stack is full, return `False`
- Otherwise move `TopOfStack` up by 1, store `Item` there, and return `True`

`Pop()`

- If the stack is empty, return `-1`
- Otherwise return the top item, and move `TopOfStack` down by 1

**Example:**

    Input:
      print(Push(10))
      print(Push(20))
      print(Push(30))
      print(Pop())
      print(TopOfStack)

    Output:
      True
      True
      True
      30
      1

Remember the order from Stack 1: **Push** moves the pointer *then* stores.
**Pop** reads the item *then* moves the pointer.

---

## Exercise 2

**Problem:**

`ShowStack()`

Return every item in the stack as one string, from the **top** down to the
**bottom**, with **one space** between them. Return `""` if the stack is empty.

Do **not** change the stack.

**Example:**

    Input:
      Push(10)
      Push(20)
      Push(30)
      print(ShowStack())
      Pop()
      print(ShowStack())

    Output:
      30 20 10
      20 10

Look at the array after that `Pop()`:

    index:   0    1    2    3   ...
    Stack: [10,  20,  30,  -1, ...]
                  ↑
             TopOfStack = 1

`30` is **still in the array** — `Pop()` only moved the pointer. So
`ShowStack()` must start at `TopOfStack`, not at the end of the array.

*Hint:* `range(TopOfStack, -1, -1)` counts **down** from `TopOfStack` to 0.

---

## Exercise 3

**Problem:**

`DecimalToBinary(Number)`

`Number` is a whole number from `0` to `255`. Use **your stack** to change it
into a binary string.

1. **Empty the stack first** by setting `TopOfStack` to `-1`.
2. If `Number` is `0`, return `"0"`.
3. While `Number` is more than 0:
    - Push the remainder `Number % 2`
    - Divide `Number` by 2 with `//`
4. Pop every digit off the stack, joining them into one string, and return it.

Do **not** use `bin()` or `format()`.

**Example:**

    Input:                      Output:
      DecimalToBinary(5)          "101"
      DecimalToBinary(13)         "1101"
      DecimalToBinary(255)        "11111111"
      DecimalToBinary(0)          "0"

How it works for `13`:

    13 % 2 = 1   Push 1      13 // 2 = 6
     6 % 2 = 0   Push 0       6 // 2 = 3
     3 % 2 = 1   Push 1       3 // 2 = 1
     1 % 2 = 1   Push 1       1 // 2 = 0   stop

    Stack (bottom → top):   1  0  1  1
    Pop them all:           1  1  0  1    →   "1101"

The remainders come out **backwards** — the stack turns them around.

Why is the stack size 8? The biggest number, 255, is `11111111` — exactly 8 digits.

---

## Exercise 4

**Problem:**

`Editor(Commands)`

A tiny text editor with an **undo** button. `Commands` is a list of strings.
Each command is either:

- `"type x"` → type the letter `x` — **push** it onto the stack
- `"undo"` → remove the last letter typed — **pop** it off the stack

Steps:

1. **Empty the stack first** by setting `TopOfStack` to `-1`.
2. Carry out every command in order.
    - `"undo"` on an empty stack does nothing.
    - If the stack is full, the letter is not typed.
3. Return the finished text: the letters from the **bottom** of the stack
   (`Stack[0]`) up to the **top**.

**Example:**

    Input:
      print(Editor(["type c", "type a", "type r", "undo", "type t"]))

    Output:
      cat

Step by step:

    type c    Stack: c
    type a    Stack: c a
    type r    Stack: c a r
    undo      Stack: c a        ← r removed
    type t    Stack: c a t

    Answer: "cat"

More examples:

    Input:                                           Output:
      Editor(["undo", "type h", "type i"])             "hi"
      Editor(["type a", "undo", "undo", "type b"])     "b"
      Editor([])                                       ""

*Hint:* `"type a".split(" ")` gives `["type", "a"]` — the letter is at index 1.

