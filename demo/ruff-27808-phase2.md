# PR triage: [astral-sh/ruff#27808](https://github.com/astral-sh/ruff/pull/27808)

**Title:** [ty] Distinguish TypeVarTuple arguments from uninhabited runtime tuples
**Author:** @AlexWaygood  
**Refs:** `main` ← `alex/typevartuple-never-semantics`  
**Commits:** 4 · **Files:** 53 · **Lines:** +1845 / -274

## Verdict

# **BLOCK**

- BLOCK because at least one status check failed.

## Checks

- State: **FAILURE**
- Observed checks: 66
- Failed: `CodSpeed Performance Analysis`

## Risk flags

### `NO_TEST_COVERAGE` — MEDIUM
Changed production files have no obvious neighboring or repository test coverage.
- `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md`
- `crates/ty_python_semantic/resources/mdtest/function/return_type.md`
- `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md`
- `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md`
- `crates/ty_python_semantic/resources/mdtest/subscript/tuple.md`
- `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md`
- `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md`
- `crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md`
- `crates/ty_python_semantic/resources/mdtest/type_properties/is_disjoint_from.md`
- `crates/ty_python_semantic/resources/mdtest/type_properties/is_subtype_of.md`
- `crates/ty_python_semantic/resources/mdtest/type_properties/materialization.md`
- `crates/ty_python_semantic/resources/mdtest/type_properties/tuples_containing_never.md`
- `crates/ty_python_semantic/src/types/call/bind.rs`
- `crates/ty_python_semantic/src/types/call/bind/constructor.rs`
- `crates/ty_python_semantic/src/types/class/static_literal.rs`
- `crates/ty_python_semantic/src/types/equality/enums.rs`
- `crates/ty_python_semantic/src/types/infer/builder/attribute_assignment.rs`
- `crates/ty_python_semantic/src/types/infer/builder/type_form.rs`
- `crates/ty_python_semantic/src/types/infer/builder/typed_dict.rs`
- `crates/ty_python_semantic/src/types/set_theoretic/builder.rs`

### `CHECKS_FAILED` — CRITICAL
One or more required status checks failed.
- `CodSpeed Performance Analysis`


## Blast-radius map

The Phase 1 map is conservative: it identifies changed files, changed symbols, and direct call sites visible in changed hunks. A full repository-wide call graph is a Phase 2 enhancement.

### `crates/ty_python_semantic/resources/mdtest/attributes.md` (modified, +13/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md` (modified, +29/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md` (modified, +13/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/diagnostics/error_context.md` (modified, +30/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`

### `crates/ty_python_semantic/resources/mdtest/function/return_type.md` (modified, +26/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md` (modified, +60/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md` (modified, +322/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md` (modified, +254/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/resources/mdtest/promotion.md` (modified, +53/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/resources/mdtest/subscript/tuple.md` (modified, +23/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/ty_extensions.md` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md` (modified, +4/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md` (modified, +15/-6)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/type_form.md` (modified, +8/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md` (modified, +28/-3)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/type_properties/is_disjoint_from.md` (modified, +99/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/type_properties/is_subtype_of.md` (modified, +19/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/type_properties/materialization.md` (modified, +52/-6)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/type_properties/tuples_containing_never.md` (modified, +48/-17)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/typed_dict.md` (modified, +12/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/resources/mdtest/union_types.md` (modified, +3/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`, `crates/ty_python_semantic/resources/mdtest/diagnostics/special_form_attributes.md`, `crates/ty_python_semantic/resources/mdtest/snapshots/special_form_attribu…_-_Diagnostics_for_inva…_(249d635e74a41c9e).snap`, `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md`

### `crates/ty_python_semantic/src/reachability.rs` (modified, +5/-3)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types.rs` (modified, +88/-10)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/attribute_write.rs` (modified, +2/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/bool.rs` (modified, +4/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/call/bind.rs` (modified, +33/-20)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/call/bind/constructor.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/class.rs` (modified, +15/-5)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/class/static_literal.rs` (modified, +19/-10)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/constraints.rs` (modified, +47/-39)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/cyclic.rs` (modified, +31/-3)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/equality/enums.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/function.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ruff_linter/src/rules/flake8_pytest_style/rules/test_functions.rs`, `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/generics.rs` (modified, +34/-7)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/infer/builder.rs` (modified, +11/-9)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`

### `crates/ty_python_semantic/src/types/infer/builder/attribute_assignment.rs` (modified, +11/-7)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/infer/builder/type_form.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/infer/builder/typed_dict.rs` (modified, +1/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/infer/comparisons.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`

### `crates/ty_python_semantic/src/types/instance.rs` (modified, +32/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/match_pattern.rs` (modified, +6/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/narrow.rs` (modified, +27/-20)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/property_tests.rs` (modified, +4/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/protocol_class.rs` (modified, +13/-7)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/relation.rs` (modified, +120/-16)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/set_theoretic.rs` (modified, +24/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/set_theoretic/builder.rs` (modified, +4/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/signatures.rs` (modified, +7/-4)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/tests.rs` (modified, +2/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/tuple.rs` (modified, +106/-17)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/type_alias.rs` (modified, +48/-6)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/typed_dict.rs` (modified, +33/-15)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/typevar.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`


## Literate diff — generated explanation

> Generated by `gpt-5-mini` from bounded, redacted context. This prose cannot change the deterministic verdict.
> Redactions applied before the model call: 0

### Background

This PR addresses a semantic mismatch introduced earlier: tuple type annotations that contain a required Never element look similar to TypeVarTuple argument sequences that contain Never, but they mean different things at runtime. The author introduces an explicit role for tuple specifications so the type system can keep a full variadic argument sequence for generic specializations while still treating runtime tuples that require a Never element as uninhabited (i.e., equivalent to Never). The branch is alex/typevartuple-never-semantics against main, 4 commits, 53 changed files, and the repository check suite shows a blocking status because at least one check (CodSpeed Performance Analysis) failed.

### Intent in plain language

Make the type system distinguish two uses of tuple-like specifications: (1) runtime tuple types (product types) whose elements determine inhabitance (a mandatory Never element makes the tuple uninhabited), and (2) TypeVarTuple / variadic generic argument sequences where Never is a legitimate type argument that must be preserved in the argument sequence. Preserve the full shape of variadic argument sequences through inference and relation checking while keeping runtime tuple semantics correctly simplified to Never when appropriate.

### Narrative

#### 1. Introduce a distinct role for tuple specifications

The central design change is to record a TupleRole (interned) on TupleType representations so the same element sequence can be treated either as a runtime tuple type or as a TypeVarTuple/argument pack. The documentation and examples were updated to show that unpacking or specializing generics preserves explicit Never elements in TypeVarTuple specializations, while runtime tuple types containing a required Never element simplify to Never for inhabitance reasoning.
- Files: `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md`
- Evidence: crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md; crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md

```text
def check(first: Container[*tuple[int, Never]], ...) -> None:
    reveal_type(first)  # revealed: Container[int, Never]
```

#### 2. Expose the behavioral difference in many doc-tests (mdtest)

A large number of mdtest files were edited to capture the new semantics: runtime tuples that include a required Never are now asserted equivalent to Never, while homogenous variable-length tuples (tuple[Never, ...]) remain inhabited by the empty tuple. These edits show where behavior changed (equivalence and indexing examples) and how callers should expect simplifications for runtime tuple types containing Never.
- Files: `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md`, `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md`, `crates/ty_python_semantic/resources/mdtest/subscript/tuple.md`
- Evidence: crates/ty_python_semantic/resources/mdtest/type_compendium/never.md; crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md; crates/ty_python_semantic/resources/mdtest/subscript/tuple.md

```text
static_assert(is_equivalent_to(tuple[int, Never], Never))
static_assert(not is_equivalent_to(tuple[Never, ...], Never))
```

#### 3. Preserve Never elements in variadic generic inference and defaults

Multiple examples were added demonstrating that constructor inference, default type arguments, and unpacking retain the exact position and presence of Never elements inside a variadic specialization. These examples document expected revealed types like Factory[int, Never] or WithNeverDefault[int, Never] so tooling and type-checker behavior keep the full argument sequence for generics.
- Files: `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md`
- Evidence: crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md; crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md; crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md

```text
reveal_type(Factory(1, value))  # revealed: Factory[Literal[1], Never]
reveal_type(WithNeverDefault())  # revealed: WithNeverDefault[int, Never]
```

#### 4. Update related diagnostics and higher-level behaviors

The change ripples into diagnostics and inference behaviors: examples were added to show how invariance, promotion, and partial() binding behave when uninhabited tuple parameters or variadic arguments are present. These edits document how the invariant/variance and callable construction logic should treat argument packs that contain Never.
- Files: `crates/ty_python_semantic/resources/mdtest/diagnostics/error_context.md`, `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md`, `crates/ty_python_semantic/resources/mdtest/promotion.md`
- Evidence: crates/ty_python_semantic/resources/mdtest/diagnostics/error_context.md; crates/ty_python_semantic/resources/mdtest/call/functools_partial.md; crates/ty_python_semantic/resources/mdtest/promotion.md

```text
def f(first: tuple[Never], second: int) -> None: ...
reveal_type(partial(f, value))  # revealed: partial[(first: tuple[Never], second: int) -> None]
```

#### 5. Concrete adjustments to equivalence/assignability examples

Tests and static_assert samples were changed to reflect the new normalization: e.g., tuple[int, Never] is now asserted equivalent to Never, and assignability examples treat tuple[Never] as the bottom type in places where prior semantics kept its shape. These are direct behavioral assertions that callers and internal relations must follow.
- Files: `crates/ty_python_semantic/resources/mdtest/ty_extensions.md`, `crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md`
- Evidence: crates/ty_python_semantic/resources/mdtest/ty_extensions.md; crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md

```text
static_assert(is_equivalent_to(tuple[int, Never], Never))
static_assert(is_assignable_to(Any, tuple[Never]))
```

### Review questions

- Where in the core type-representation code (crates/ty_python_semantic/src/...) is the new TupleRole type defined and interned, and are all consumers of tuple equality/identity updated to consider role? (core implementation diffs are not present in the supplied context.)
- The PR updates many mdtest files (documentation-style tests). Are there unit or integration tests (non-mdtest) exercising the new TupleRole logic and relation-checking code paths? The risk flags list 'NO_TEST_COVERAGE' for a number of production files — were tests added to cover the changed logic in inference and relation builder modules?
- CodSpeed Performance Analysis failed (blocking). Did the interning of roles or any new bookkeeping add measurable overhead in hot code paths (e.g., type equality, caching)? Can we see profiling or benchmark diffs that explain the CodSpeed failure?
- Does the new role affect caching keys for interned tuple types and any global caches used by type relation or materialization logic? Are cache invalidations or comparisons updated accordingly?
- Are callers that expect a tuple annotation to remain a concrete structural type (e.g., user-defined tuple subclasses) still handled correctly where a runtime tuple simplifies to Never? The mdtests show many assertions, but I want to confirm semantic edges like subclass reasoning are considered.

### Uncertainties

- The supplied changed-file context is predominantly mdtest documentation edits; the PR message describes a core implementation change (an interned TupleRole), but the actual source-code diffs implementing TupleRole (likely under crates/ty_python_semantic/src/...) are not shown in the provided context. I cannot verify code-level changes, call sites, or whether all equality/relational consumers were updated.
- The CodSpeed Performance Analysis check failed (the verdict is BLOCK). The context does not include the performance report details, so I cannot determine which code paths regressed or whether the failure is due to test coverage, measurement noise, or a real performance regression introduced by interning or new logic.
- The 'NO_TEST_COVERAGE' risk flag lists many files that were changed but lack obvious neighboring tests. From the provided context I cannot tell whether new unit/integration tests were added outside the mdtest resources, or whether the mdtests suffice as coverage for the changed behavior.
- I cannot confirm whether any public API surface or downstream consumers (other crates) rely on tuple identity semantics that might be subtly affected by introducing a TupleRole; the changes shown are just the mdtests and documentation examples.

## Changed-file inventory

| File | Status | Additions | Deletions | Symbols |
| --- | --- | ---: | ---: | --- |
| `crates/ty_python_semantic/resources/mdtest/attributes.md` | modified | 13 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md` | modified | 29 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md` | modified | 13 | 1 | — |
| `crates/ty_python_semantic/resources/mdtest/diagnostics/error_context.md` | modified | 30 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/function/return_type.md` | modified | 26 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md` | modified | 60 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md` | modified | 322 | 2 | — |
| `crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md` | modified | 254 | 2 | — |
| `crates/ty_python_semantic/resources/mdtest/promotion.md` | modified | 53 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/subscript/tuple.md` | modified | 23 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/ty_extensions.md` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md` | modified | 4 | 5 | — |
| `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md` | modified | 15 | 6 | — |
| `crates/ty_python_semantic/resources/mdtest/type_form.md` | modified | 8 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md` | modified | 28 | 3 | — |
| `crates/ty_python_semantic/resources/mdtest/type_properties/is_disjoint_from.md` | modified | 99 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/type_properties/is_subtype_of.md` | modified | 19 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/type_properties/materialization.md` | modified | 52 | 6 | — |
| `crates/ty_python_semantic/resources/mdtest/type_properties/tuples_containing_never.md` | modified | 48 | 17 | — |
| `crates/ty_python_semantic/resources/mdtest/typed_dict.md` | modified | 12 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/union_types.md` | modified | 3 | 4 | — |
| `crates/ty_python_semantic/src/reachability.rs` | modified | 5 | 3 | — |
| `crates/ty_python_semantic/src/types.rs` | modified | 88 | 10 | — |
| `crates/ty_python_semantic/src/types/attribute_write.rs` | modified | 2 | 2 | — |
| `crates/ty_python_semantic/src/types/bool.rs` | modified | 4 | 1 | — |
| `crates/ty_python_semantic/src/types/call/bind.rs` | modified | 33 | 20 | — |
| `crates/ty_python_semantic/src/types/call/bind/constructor.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/class.rs` | modified | 15 | 5 | — |
| `crates/ty_python_semantic/src/types/class/static_literal.rs` | modified | 19 | 10 | — |
| `crates/ty_python_semantic/src/types/constraints.rs` | modified | 47 | 39 | — |
| `crates/ty_python_semantic/src/types/cyclic.rs` | modified | 31 | 3 | — |
| `crates/ty_python_semantic/src/types/equality/enums.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/function.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/generics.rs` | modified | 34 | 7 | — |
| `crates/ty_python_semantic/src/types/infer/builder.rs` | modified | 11 | 9 | — |
| `crates/ty_python_semantic/src/types/infer/builder/attribute_assignment.rs` | modified | 11 | 7 | — |
| `crates/ty_python_semantic/src/types/infer/builder/type_form.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/infer/builder/typed_dict.rs` | modified | 1 | 0 | — |
| `crates/ty_python_semantic/src/types/infer/comparisons.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/instance.rs` | modified | 32 | 4 | — |
| `crates/ty_python_semantic/src/types/match_pattern.rs` | modified | 6 | 4 | — |
| `crates/ty_python_semantic/src/types/narrow.rs` | modified | 27 | 20 | — |
| `crates/ty_python_semantic/src/types/property_tests.rs` | modified | 4 | 4 | — |
| `crates/ty_python_semantic/src/types/protocol_class.rs` | modified | 13 | 7 | — |
| `crates/ty_python_semantic/src/types/relation.rs` | modified | 120 | 16 | — |
| `crates/ty_python_semantic/src/types/set_theoretic.rs` | modified | 24 | 2 | — |
| `crates/ty_python_semantic/src/types/set_theoretic/builder.rs` | modified | 4 | 4 | — |
| `crates/ty_python_semantic/src/types/signatures.rs` | modified | 7 | 4 | — |
| `crates/ty_python_semantic/src/types/tests.rs` | modified | 2 | 2 | — |
| `crates/ty_python_semantic/src/types/tuple.rs` | modified | 106 | 17 | — |
| `crates/ty_python_semantic/src/types/type_alias.rs` | modified | 48 | 6 | — |
| `crates/ty_python_semantic/src/types/typed_dict.rs` | modified | 33 | 15 | — |
| `crates/ty_python_semantic/src/types/typevar.rs` | modified | 1 | 1 | — |

## Deterministic policy

- `BLOCK`: failed checks or authentication/secrets/security-sensitive changes.
- `QUARANTINE`: database changes, dependency changes, missing obvious test coverage, or unavailable/pending checks.
- `SHIP`: no rules fired and observed checks passed.

_Generated by diffly-cli. Deterministic triage is authoritative; any literate-diff prose is optional generated explanation._
