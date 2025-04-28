## 0.0.24 *\[2025-04-28\]*

### Improvements

- Do not use `isinstance` check when collecting tests in a module.
     This to avoid custom calling custom `.__class__` descriptors. 

## 0.0.23 *\[2025-03-15\]*

### Improvements

- Test cases and any other wrappers now kept in the order of addition.
- Add "`named`" wrapper.
- Add `WrapperCalling.named`.
- Add `WrapperCallingFrom.named`.
- Add `WrapperCallingFrom.named_first`.
- Add `CallState.name`. 
- Modify `Result.get_modifier_parameters` to `get_final_call_state`, since now we require also the name, so returning
  the whole call state sounds more reasonable.

## 0.0.22 *\[2024-12-28\]*

### Bug fixes

- In reports `Unsatisfied function parameters` section was not rendering as intended.

## 0.0.21 *\[2024-12-23\]*

### Improvements

- Test file & directory name checks are now more specific.
- `TestFileLoadFailure` now stores the exception instead of its message.
    Originally wanted to deallocate the traceback, but representing the exception with deallocated turned out to be
    a longer task than expected. This also means that the default writer now highlights it as intended.
- `AssertionException` rendering moved out to rendering.
- Add missing `AssertionException.__new__`.
- Conditional assertions are not using a meta type to invoke them after constructor instead all uses a top level
    function. This is to make them easier to test with.
- Assertion rendering is now highlighted.
- Add `TestFile.path_parts`. `TestFile.import_route` is now a property.
- Add `TestCase.path_parts`.
- Add `Handle.get_test_documentation_lines`.
     Remove old `.get_test_documentation` which also added a prefix in front of each line.
- Add `highlighter` parameter to `DefaultEventFormatter.__new__`.
- Reorder `ReportFailureRaising`'s and `Result.with_exception`'s parameters.
    In short: from `accept, received, accept`; to `accept, accept, received`.
- Reports are now highlighted.
- Assertion report renderer now displays exceptions raised while invoking their condition.
- `AssertionRaising` now differentiates if it failed due to not receiving exception & receiving a different exception.
- Assertion report rendering now renders the captured different exception inside of a `AssertionRaising`.
- Results are now highlighted.

## 0.0.20 *\[2024-09-11\]*

### Bug fixes

- Fix `mock_globals` did not analyze nested code objects.
  Caused `NameError` when mocking a function with inline generator.

## 0.0.19 *\[2024-08-10\]*

### Improvements

- Improve source root lookup: Correctly handle fallback for project name.
- Improve source root lookup: Add fallback for project scripts.
- Improve source root lookup: Add fallback for git.

## 0.0.18 *\[2024-08-07\]*

### Improvements

- Use `:` to separate file path and test name. From `.`. This allows easier copy pasting.

## 0.0.17 *\[2024-04-02\]*

### Improvements

- Add `TestFile.has_failed_test`.
- Add `RunnerContext.has_failed_test`.
- Add `TestRunner.get_return_code`.
- Add `TestRunner.set_return_code`.
- `TestRunner.run` now returns its return code instead of a boolean.
- `run_tests_in` now returns its return code instead of none.
- `execute_from_parameters` now returns its return code instead of boolean.
- `__main__` now exits with the respective return code.

### Renames, Deprecation & Removals

- Rename `execute_from_terminal` to `execute_from_parameters`.

## 0.0.16 *\[2023-12-31\]*

### Bug fixes

- Fix `AttributeError` in an incorrectly updated frame filter.

## 0.0.15 *\[2023-12-31\]*

### Improvements

- Use new scarletio in dependencies.

## 0.0.14 *\[2023-11-11\]*

### Improvements

- Now its checked whether every dependency is satisfied before importing the framework.

## 0.0.13 *\[2023-10-01\]*

### Improvements

- Remove current working directory from `sys.path` in case, we are executing from inside of a library.
    This caused confused imports.
- Add cli entry point.

## 0.0.12 *\[2023-09-30\]*

### Improvements

- Add new `SourceLoadFailureEvent`.
- The first command line parameter is now auto detected on a smart way.
    It tries to resolve the current library we are at, or we are looking at.
- Imports the tested library before running any tests.
    This means wont all test fail because of a failing import, instead no tests will run.

## 0.0.11 *\[2023-08-27\]*

### Improvements

- Add `mock_globals`.
- Now only `FunctionType` and `WrapperBase` instances can be tests.
- Change `ResultState`'s structure. This is required, so a result can only have 1 state from now on.
- Add new failure type `ReportFailureParameterMismatch`.

## 0.0.10 *\[2023-06-11\]*

### Improvements

- Informal tests now show up with a `I` prefix.

### Bug fixes

- Test wrappers were grouped incorrectly resulting badly generated test cases.
- `WrapperGarbageCollect` was not setting all of its attributes causing `AttributeError`.

## 0.0.9 *\[2023-06-08\]*

### Bug fixes

- Exception occurred when rendering assertions.

## 0.0.8 *\[2023-06-08\]*

### Improvements

- Add `changelog` file.
- `AssertionSubtype` now accepts multiple parameters.
- `AssertionInstance` now accepts multiple parameters.
- `AssertionRaising.__new__` now requires at least `1` exception parameter, so it is harder to mess it up.
- Add `_`.
- `WrapperCall.raising_constructor` now requires at least `1` exception parameter, so it is harder to mess it up.
- `WrapperCall.raising` now requires at least `1` exception parameter, so it is harder to mess it up.
- `WrapperCall` had `raising_accept_subtypes` parameters. They should have been called `accept_subtypes`.
- Add `where` parameter to `WrapperCall.raising_constructor`.
- Add `where` parameter to `WrapperCall.raising`.
- Add `where` parameter to `AssertionRaising.__new__`.
- `Result` instances now completely replace `ResultGroup`. They also inherit every functionality from them.
- Add `Result.is_conflicted`.
- Add `Result.is_last`.
- Wrappers with contexts now return a context instance instead of a generator. This should reduce wrapper complexity.
- Add `ContextCalling`.
- Add `ContextBase`.
- Add `ContextGarbageCollect`.
- Add `ReportBase.is_failure`.
- Add `ReportBase.is_informal`.
- Add `ReportBase.iter_reports`.
- Add `ReportBase.get_failure_report`.
- Add `ReportBase.get_output_report`.
- Add `Result.with_output`.
- Output is now more colorful.
- Add `RunnerContext.iter_informal_results`.
- Add `TestFile.iter_informal_results`.
- Add `Result.is_informal`.
- Add `CaptureOutputContextManager`.
- Add `call_from`.
- Add `WrapperCallingFrom`.

### Bug fixes

- If a test had `parameters` they were not always rendering.

### Renames, Deprecation & Removals

- Deprecate `revert`.
- Rename `revert` values to `reverse`.
- Remove `ResultGroup`.
- Remove `ReportBase.get_report_message`.
- Remove `WrapperConflict.get_report_message`.
- Remove `Result.iter_report_messages`.
