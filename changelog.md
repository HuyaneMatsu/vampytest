## 0.0.8

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

#### Renames, Deprecation & Removals

- Deprecate `revert`.
- Rename `revert` values to `reverse`.
