## 0.0.17 *\[2024-04-02\]*

#### Improvements

- Add `TestFile.has_failed_test`.
- Add `RunnerContext.has_failed_test`.
- Add `TestRunner.get_return_code`.
- Add `TestRunner.set_return_code`.
- `TestRunner.run` now returns its return code instead of a boolean.
- `run_tests_in` now returns its return code instead of none.
- `execute_from_parameters` now returns its return code instead of boolean.
- `__main__` now exits with the respective return code.

#### Renames, Deprecation & Removals

- Rename `execute_from_terminal` to `execute_from_parameters`.

## 0.0.16 *\[2023-12-31\]*

#### Bug fixes

- Fix `AttributeError` in an incorrectly updated frame filter.

## 0.0.15 *\[2023-12-31\]*

#### Improvements

- Use new scarletio in dependencies.

## 0.0.14 *\[2023-11-11\]*

#### Improvements

- Now its checked whether every dependency is satisfied before importing the framework.

## 0.0.13 *\[2023-10-01\]*

#### Improvements

- Remove current working directory from `sys.path` in case, we are executing from inside of a library.
    This caused confused imports.
- Add cli entry point.

## 0.0.12 *\[2023-09-30\]*

#### Improvements

- Add new `SourceLoadFailureEvent`.
- The first command line parameter is now auto detected on a smart way.
    It tries to resolve the current library we are at, or we are looking at.
- Imports the tested library before running any tests.
    This means wont all test fail because of a failing import, instead no tests will run.

## 0.0.11 *\[2023-08-27\]*

#### Improvements

- Add `mock_globals`.
- Now only `FunctionType` and `WrapperBase` instances can be tests.
- Change `ResultState`'s structure. This is required, so a result can only have 1 state from now on.
- Add new failure type `ReportFailureParameterMismatch`.

## 0.0.10 *\[2023-06-11\]*

#### Improvements

- Informal tests now show up with a `I` prefix.

#### Bug fixes

- Test wrappers were grouped incorrectly resulting badly generated test cases.
- `WrapperGarbageCollect` was not setting all of its attributes causing `AttributeError`.

## 0.0.9 *\[2023-06-08\]*

#### Bug fixes

- Exception occurred when rendering assertions.

## 0.0.8 *\[2023-06-08\]*

#### Improvements

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

#### Bug fixes

- If a test had `parameters` they were not always rendering.

#### Renames, Deprecation & Removals

- Deprecate `revert`.
- Rename `revert` values to `reverse`.
- Remove `ResultGroup`.
- Remove `ReportBase.get_report_message`.
- Remove `WrapperConflict.get_report_message`.
- Remove `Result.iter_report_messages`.
