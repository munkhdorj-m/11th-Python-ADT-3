import ast
import importlib
import inspect
import textwrap

import pytest

import assignment


@pytest.fixture
def s():
    return importlib.reload(assignment)


def calls_in(function):
    tree = ast.parse(textwrap.dedent(inspect.getsource(function)))
    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.append(node.func.id)
            if isinstance(node.func, ast.Attribute):
                names.append("." + node.func.attr)
    return names


def check_no_list_methods(function):
    for name in calls_in(function):
        if name in [".append", ".pop", ".insert", ".remove", ".extend", ".clear"]:
            pytest.fail(
                function.__name__ + "() uses " + name + "(). "
                "Change TopOfStack and use Stack[TopOfStack] instead."
            )


def test1_initial_stack(s):
    assert s.Stack == [-1, -1, -1, -1, -1, -1, -1, -1]
    assert s.TopOfStack == -1


def test1_push(s):
    assert s.Push(15) == True
    assert s.TopOfStack == 0
    assert s.Stack[0] == 15
    assert s.Push(27) == True
    assert s.TopOfStack == 1
    assert s.Stack[1] == 27


def test1_push_when_full(s):
    for x in range(8):
        assert s.Push(x) == True
    assert s.Push(99) == False
    assert s.TopOfStack == 7
    assert s.Stack == [0, 1, 2, 3, 4, 5, 6, 7]


def test1_pop(s):
    s.Push(10)
    s.Push(20)
    s.Push(30)
    assert s.Pop() == 30
    assert s.TopOfStack == 1
    assert s.Pop() == 20
    assert s.Pop() == 10
    assert s.TopOfStack == -1


def test1_pop_when_empty(s):
    assert s.Pop() == -1
    assert s.TopOfStack == -1
    s.Push(5)
    s.Pop()
    assert s.Pop() == -1
    assert s.TopOfStack == -1


def test1_uses_top_of_stack(s):
    check_no_list_methods(s.Push)
    check_no_list_methods(s.Pop)
    for x in range(10):
        s.Push(x)
    assert s.TopOfStack == 7
    for x in range(10):
        s.Pop()
    assert s.TopOfStack == -1
    assert len(s.Stack) == 8


def test2_show_stack(s):
    assert s.ShowStack() == ""
    s.Stack[0] = 10
    s.TopOfStack = 0
    assert s.ShowStack() == "10"
    s.Stack[1] = 20
    s.Stack[2] = 30
    s.TopOfStack = 2
    assert s.ShowStack() == "30 20 10"


def test2_ignores_old_items(s):
    s.Stack[0] = 10
    s.Stack[1] = 20
    s.Stack[2] = 30
    s.Stack[3] = 40
    s.TopOfStack = 1
    assert s.ShowStack() == "20 10"


def test2_keeps_stack(s):
    s.Stack[0] = 5
    s.Stack[1] = 6
    s.TopOfStack = 1
    s.ShowStack()
    s.ShowStack()
    assert s.TopOfStack == 1
    assert s.Stack[0] == 5
    assert s.Stack[1] == 6
    assert s.ShowStack() == "6 5"


@pytest.mark.parametrize("number, expected", [
    [5, "101"],
    [10, "1010"],
    [1, "1"],
    [2, "10"],
    [0, "0"],
    [13, "1101"],
    [128, "10000000"],
    [255, "11111111"],
])
def test3_binary(s, number, expected):
    assert s.DecimalToBinary(number) == expected


def test3_starts_with_empty_stack(s):
    s.Push(7)
    s.Push(8)
    assert s.DecimalToBinary(5) == "101"
    assert s.TopOfStack == -1
    s.Push(1)
    assert s.DecimalToBinary(6) == "110"


def test3_uses_the_stack(s):
    names = calls_in(s.DecimalToBinary)
    for banned in ["bin", "format", ".format"]:
        if banned in names:
            pytest.fail("DecimalToBinary() uses " + banned + "(). Use the stack instead.")
    assert "Push" in names, "DecimalToBinary() must call Push()."
    assert "Pop" in names, "DecimalToBinary() must call Pop()."
    assert s.DecimalToBinary(9) == "1001"


@pytest.mark.parametrize("commands, expected", [
    [["type c", "type a", "type t"], "cat"],
    [["type c", "type a", "type r", "undo", "type t"], "cat"],
    [["type d", "type o", "type g", "undo", "undo", "undo"], ""],
    [["undo", "type h", "type i"], "hi"],
    [["type a", "undo", "undo", "type b"], "b"],
    [[], ""],
])
def test4_editor(s, commands, expected):
    assert s.Editor(commands) == expected


def test4_stack_full(s):
    commands = []
    for letter in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]:
        commands.append("type " + letter)
    assert s.Editor(commands) == "abcdefgh"
    commands.append("undo")
    commands.append("type z")
    assert s.Editor(commands) == "abcdefgz"


def test4_starts_with_empty_stack(s):
    s.Push("x")
    s.Push("y")
    assert s.Editor(["type o", "type k"]) == "ok"
    assert s.Editor(["type h", "type i"]) == "hi"


def test4_uses_the_stack(s):
    names = calls_in(s.Editor)
    assert "Push" in names, "Editor() must call Push()."
    assert "Pop" in names, "Editor() must call Pop()."
    assert s.Editor(["type n", "type o", "type w", "undo"]) == "no"
