<h1 align="center">
    Vampytest
</h1>


<div align="center">
  <a>
    <img src="https://img.shields.io/badge/stability-alpha-orange.svg?style=flat-square" alt="Stability" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/python-3.6 -- 3.11-blue?style=flat-square" alt="Python version" />
  </a>
  <a>
    <img src="https://img.shields.io/badge/PyPy-Supported-gre?style=flat-square" alt="PyPy" />
  </a>
  <a href="https://pypi.org/project/vampytest/">
    <img src="https://img.shields.io/badge/package-PyPi-blue.svg?style=flat-square" alt="PyPi" />
  </a>
</div>

Vampytest is a testing framework that allows, but is not limited to, writing relative import based tests.

---

## Table of contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Writing tests](#writing-tests)
- [Running tests](#running-tests)
- [Return codes](#running-tests)
- [Features](#features)
  - [Assertions](#assertions)
    - [Equality assertions](#equality-assertions)
    - [Boolean assertions](#boolean-assertions)
    - [Container assertions](#container-assertions)
    - [Identity assertions](#identity-assertions)
    - [Exception assertions](#exception-assertions)
    - [Type assertions](#type-assertions)
    - [Reversed assertions](#reversed-assertions)
  - [Parameterized tests](#parameterized-tests)
  - [Returning and raising tests](#returning-and-raising-tests)
  - [Skipping tests](#skipping-tests)
  - [Reversing test results](#reversing-test-results)
  - [Garbage collection](#garbage-collection)
  - [Capturing output](#capturing-output)
- [Advanced features](#advanced-features)
  - [Testing environments](#testing-environments)

---

## Introduction

Here are several advantages why you would want to use a relative import supporting testing framework such as vampytest:

- **Simplicity and ease of use**

    Relative import based tests simplifies the process of writing and executing tests.
    Relative imports provide a straightforward and intuitive way to import and utilize testing functionalities without
    the need for complex configuration or setup.
    Developers can quickly get started with writing tests and running them, making the testing process more accessible
    and efficient.

- **Seamless integration with codebase**

    By using relative imports the testing framework seamlessly integrates with the codebase being tested.
    It allows the developers to import and test modules or components in a manner that reflects the same import
    structure used in the actual code. This integration enhances readability and maintainability.

- **Encourages modular and isolated testing**

    Relative import based testing promotes modular and isolated testing practices.
    It's encouraging the testing of individual units in isolation.
    This isolation makes it easier to pinpoint issues, debug problems, and maintain the codebase.
    It also supports the principles of unit testing, where individual units of code are tested independently for their
    expected behavior.

- **Enhanced collaboration and teamwork**

    Relative import based testing facilitate collaboration among team members.
    By utilizing the same import structure as the codebase, it allows multiple developers to work on tests concurrently
    without conflicts. It makes coordinating testing efforts easier within a team.

- **Easy test refactoring**

    When refactoring or restructuring the codebase, relative import based testing can make it easier to refactor tests
    as well.
    Since the test code closely follows the structure of the codebase, the required changes in test imports are often
    straightforward, resulting in less effort and potential errors during refactoring.

- **Ease of migration and adoption**

    If a codebase already follows a relative import structure, using a testing framework that supports them too
    simplifies the adoption and integration of testing practices.
    Developers can directly use relative imports in their test code, resulting in a smoother transition to the
    testing framework.

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Installation

To install vampytest, you can use pip. Open your terminal and run the following command:

```sh
python3 -m pip install vampytest
```

Once installed you are ready to run your tests with vampytest.

### Writing tests

1. Create a directory for your test suite in your project.
    The directory should be called `tests` or have `test_` or `tests_` prefix.
2. Create a new python file. The file should have `test_` prefix for example: `test_example.py`.
3. In the file import the necessary libraries including `vampytest`.
4. Write test functions within the file. Each test function should start with the prefix `test_`.

```py3
import vampytest


def test_addition():
    vampytest.assert_eq(2 + 2, 4)

def test_subtraction():
    vampytest.assert_eq(5 - 3, 2)
```

To check whether the actual behavior matches the expected behavior use `assert_...` functionalities such as `assert_eq`.
Using python builtin options such as `assert` works as well, but the report will not be as detailed.

### Running tests

To run the tests, navigate to the directory where your project is located using the terminal.
Then enter the following command:

```sh
vampytest
```

If the project has a setup file, it will detect which are your project's directories and import its files beforehand.
If you do not have a file like that, you might want to navigate into your project or pass the target path where the
tests should be loaded from:

```sh
vampytest *directory*
```

By navigating into a specific directory it is possible to limit the test lookup only to the directories / files under
it.
The same can be achieved by passing the path to the location.

```sh
vampytest *directory/sub_directory/etc*
```

> Note: To test vampytest itself `vampytest` command wont work. Use `python3 -m vampytest` instead.

### Return codes

By reading the return code of the vampytest call it is possible to determine how the testing went without actually
reading the output.


| Return code   | Description                                           |
|---------------|-------------------------------------------------------|
| 0             | Tests passed                                          |
| 1             | Internal error occurred                               |
| 2             | Any test failed                                       |
| 4             | Test runner stopped (from inside)                     |
| 5             | Test runner interrupted (from outside presumably)     |
| 7             | Could not identify from where the tests should run    |


<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

# Features

### Assertions

Vampytest provides a rich set of assertion methods to validate expected behavior and outcomes.
These assertions include checking for equality, inequality, truthiness, exceptions, containment, and more.

**Here is a list of available assertions:**

| Name              | Aliases                                                  |
|-------------------|----------------------------------------------------------|
| `assert_eq`       | `assert_equals`                                          |
| `assert_false`    | `assert_not`                                             |
| `assert_in`       | `assert_contains`                                        |
| `assert_instance` | N / A                                                    |
| `assert_is`       | `assert_id`, `assert_identical`                          |
| `assert_is_not`   | `assert_not_id`, `assert_not_identical`, `assert_not_is` |
| `assert_ne`       | `assert_not_eq`, `assert_not_equals`                     |
| `assert_not_in`   | `assert_not_contains`                                    |
| `assert_raises`   | N / A                                                    |
| `assert_subtype`  | N / A                                                    |
| `assert_true`     | `assert_`                                                |


**Here are them in examples:**

##### Equality assertions

```py3
# Asserts a == b
vampytest.assert_eq(a, b)

# Asserts c != d
vampytest.assert_ne(c, d)
```

##### Boolean assertions

```py3
# Asserts bool(e)
vampytest.assert_true(e)

# Asserts not bool(f)
vampytest.assert_false(f)
```

##### Container assertions

```py3
# Asserts g in h
vampytest.assert_in(g, h)

# Asserts i not in j
vampytest.assert_not_in(i, j)
```

##### Identity assertions

```py3
# Asserts k is l
vampytest.assert_is(k, l)

# Asserts m is not n
vampytest.assert_is_not(m, n)
```

##### Exception assertions

```py3
# Asserts that the code inside the context manager raises the defined exception
with vampytest.assert_raises(ValueError):
    raise ValueError

# Asserts that the code inside the context manager raises an equal exception as the defined one.
with vampytest.assert_raises(ValueError('aya')):
    raise ValueError('aya')

# Also asserts whether the given condition is satisfied
with vampytest.assert_raises(ValueError, where = lambda e: 'aya' in repr(e)):
    raise ValueError('ayaya')
```

##### Type assertions

```py3
# Asserts isinstance(o, str)
vampytest.assert_instance(o, str)

# Asserts q is None or isinstance(q, str)
vampytest.assert_instance(q, str, nullable = True)

# Asserts type(r) is str
vampytest.assert_instance(r, str, accept_subtypes = False)

# Asserts isinstance(s, type) and issubclass(s, str)
vampytest.assert_subtype(s, str)

# Asserts t is None or isinstance(t, type) and issubclass(t, str)
vampytest.assert_subtype(t, str, nullable = True)
```

##### Reversed assertions

```py3
# Assert not u == v
vampytest.assert_eq(u, v, reverse = True)

# Asserts not isinstance(w, str)
vampytest.assert_instance(w, str, reverse = True)
```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Parameterized tests

Vampytest allows you to write parameterized tests that run the same test function with different sets of inputs.
This allows for more comprehensive testing with fewer lines of code.

```py3
import vampytest


@vampytest.call_with(2, 2)
@vampytest.call_with(3, 3)
def test_values_equal(value_0, value_1):
    vampytest.assert_eq(value_0, value_1)
```

Multiple inputs can also be parameterised with one decorator.
This can be useful when the input is more complex, and you might want to define a generator for it.

```py3
import vampytest
 
 
def input_generator():
    a = object()
    yield a, a
    
    b = 'apple'
    yield b ,b
    
    c = int
    yield c, c


@vampytest.call_from(input_generator())
def test_values_identical(value_0, value_1):
    vampytest.assert_is(value_0, value_1)

```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Returning and raising tests

With vampytest, it is possible to assert the output of tests.
This assertion can be done using the `returning` and `raising` decorators.

```py3
import vampytest


@vampytest.returning(True)
def test_values_equal():
    return 2 == 2


@vampytest.raising(ValueError)
def test_convert_to_int():
    return int('apple')
```

These decorators pair-up well with parameterised tests.

```py3
import vampytest


@vampytest.returning(True)
@vampytest.call_with(2, 2)
@vampytest.call_with(3, 3)
def test_values_equal(value_0, value_1):
    return value_0 == value_1


@vampytest.raising(ValueError)
@vampytest.call_with('apple')
@vampytest.call_with('peach')
def test_convert_to_int(fruit):
    return int(fruit)
```

It is also possible to define the expected output for each set of input.

```py3
import vampytest


@vampytest.call_with('apple').raising(ValueError)
@vampytest.call_with('peach').raising(ValueError)
@vampytest.call_with('12').returning(12)
def test_convert_to_int(fruit):
    return int(fruit)
```

For cases when the returned value could be easily calculated from the input parameters the `returning_transformed`
option might be the solution.

```py3
import operator
import vampytest


@vampytest.call_with(2, 1).returning_transformed(operator.add)
@vampytest.call_with(3, 1).returning_transformed(operator.add)
@vampytest.call_with(4, 3).returning(0)
def test_sum_if_lt_5(value_0, value_1):
    output = value_0 + value_1
    if output >= 5:
        output = 0
    
    return output
```

When using `call_from`, aside from the already mentioned `raising`, `returning`, `returning_transformed` options,
we'll also have `returning_last` and `raising_last` as available.
As their name implies they take the last input parameter and expect it to be either raised or returned.

```py3
import vampytest


@vampytest.call_from(['apple', 'peach']).raising(ValueError)
@vampytest.call_from(['12', '12']).returning(12)
@vampytest.call_from(['6', '42']).returning_transformed(int)
def test_convert_to_int(fruit):
    return int(fruit)


def input_and_return_generator():
    yield {'a': 'b'}, 'a', 'b'
    yield {'b': 'c'}, 'b', 'c'


def input_and_exception_generator():
    yield None, None, TypeError
    yield {}, 'a', KeyError
    yield {}, {}, TypeError


@vampytest.call_from(input_and_return_generator()).returning_last()
@vampytest.call_from(input_and_exception_generator()).raising_last()
def test_get_item_fails(container, key):
    return container[key]
```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Skipping tests

Vampytest provides decorators to skip or mark tests as skipped in certain conditions.

```py3
import vampytest


class MyType:
    def a():
        return 1


@vampytest.skip()
def test_repr():
    instance = MyType()
    vampytest.assert_instance(repr(instance), str)


@vampytest.skip_if(not hasattr(MyType, 'b'))
def test_repr():
    instance = MyType()
    vampytest.assert_eq(instance.b(), 2)
```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Reversing test results

If you have a test where you expect the assertions to fail they can be marked with the `reverse` decorator.
These tests will show up as passing when the tests' assertions fail. On the other hand they will show up as failing
if the assertions pass.

```py
import vampytest


@vampytest.reverse()
def test_addition():
    vampytest.assert_eq(9 + 10, 21)
```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Garbage collection

By default, garbage collection is not explicitly called between each test case since it could easily increase the
time required to run the tests by 10000% on large projects. By using `with_gc` it is possible to explicitly call
garbage collection before or after a test.

```py3
import vampytest


@vampytest.with_gc(after = True, before = True)
def test_addition():
    vampytest.assert_eq(2 + 2, 4)
```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

### Capturing output

Capturing `stdout` and `stderr` in tests is useful in scenarios where you need to verify the content, format, or
structure of the output generated by your code.
This technique allows you to intercept and store the output that would normally be printed to the console during the
execution of your code, enabling you to inspect and assert against it in your tests.

```py3
import vampytest


def test_print():
    capture = vampytest.capture_output()
    with capture:
        print('apple')
    
    vampytest.assert_eq(capture.get_value(), 'apple\n')
```

Vampytest is capturing the `stdout` and `stderr` by default. If a test fails the captured output will show
up in its report. If the test passes its captured output will only show up if all tests passed. This is to help the
developer focus on the failing tests firsts. This feature can be useful to help debug failing tests and to catch
*warnings* and forgotten *print* calls.

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>

---

# Advanced features

### Testing environments

Vampytest supports tests to be run in a specific environment to ensure that the code behaves correctly and consistently.

Environments can be set to be used on a specific scope using the `set_global_environment`, `set_directory_environment`
`set_file_environment` functions. They can also be set to apply to just a specific test using the `in_environment`
decorator.

```py3
from vampytest import DefaultEnvironment, ResultState, in_environment, returning
from vampytest.core.environment.constants import ENVIRONMENT_TYPE_GENERATOR


# We create an environment that unpacks generators into a list
class GenerativeReturnTestEnvironment(DefaultEnvironment):
    __slots__ = ()
    
    # Define that this environment is only applicable for generators and will propagate the tests' results like that
    identifier = ENVIRONMENT_TYPE_GENERATOR
    
    # Run is called to run the test with the given parameters and we except it to return a `ResultState`
    def run(self, test, positional_parameters, keyword_parameters):
        try:
            returned_value = [*test(*positional_parameters, **keyword_parameters)]
        except BaseException as raised_exception:
            return ResultState().with_raise(raised_exception)
        
        return ResultState().with_return(returned_value)
    
    # Shutdown is called when we do not need this environment anymore. Can be useful when using global environments.
    def shutdown(self):
        pass


@in_environment(GenerativeReturnTestEnvironment())
@returning([1, 2])
def test_generator_in_environment():
    yield 1
    yield 2
```

Vampytest only defines 2 environments by default: `default` and `scarletio coroutine`.

- `default` environment applies to normal non-generator non-coroutine tests.
- `scarletio coroutine` environment applies to coroutine tests.
    Vampytest assumes that every coroutine test is meant to run on a scarletio event loop.

> For generators and coroutine generators there is no environment defined by default.

Scarletio based projects might use the same event loop for their whole lifecycle. To use their event loop in
the tests use a global environment for it:

```py3
import sys

if 'vampytest' in sys.modules:
    from vampytest import ScarletioCoroutineEnvironment, assert_is, set_global_environment
    
    # import event loop
    from somewhere import EVENT_LOOP
    
    set_global_environment(ScarletioCoroutineEnvironment(event_loop = EVENT_LOOP))
```

Test whether the event loops indeed match:

```py3
import vampytest
from scarletio import get_event_loop

# import event loop
from somewhere import EVENT_LOOP


# Test whether we are indeed on the correct event loop
async def test_event_loop_same():
    vampytest.assert_is(EVENT_LOOP, get_event_loop())
```

<div align="right">[ <a href="#table-of-contents">↑ Back to top ↑</a> ]</div>
