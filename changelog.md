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
