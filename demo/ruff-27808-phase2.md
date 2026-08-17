# PR triage: [astral-sh/ruff#27808](https://github.com/astral-sh/ruff/pull/27808)

**Title:** [ty] Distinguish TypeVarTuple arguments from uninhabited runtime tuples
**Author:** @AlexWaygood  
**Refs:** `main` ← `alex/typevartuple-never-semantics`  
**Commits:** 1 · **Files:** 49 · **Lines:** +1675 / -254

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

### `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md` (modified, +60/-0)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md` (modified, +322/-2)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md` (modified, +224/-2)
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

### `crates/ty_python_semantic/src/types.rs` (modified, +60/-18)
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

### `crates/ty_python_semantic/src/types/call/bind.rs` (modified, +34/-20)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/call/bind/constructor.rs` (modified, +1/-1)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: none detected

### `crates/ty_python_semantic/src/types/constraints.rs` (modified, +44/-36)
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

### `crates/ty_python_semantic/src/types/instance.rs` (modified, +40/-4)
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

### `crates/ty_python_semantic/src/types/relation.rs` (modified, +79/-7)
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

### `crates/ty_python_semantic/src/types/tuple.rs` (modified, +91/-17)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/type_alias.rs` (modified, +47/-6)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`

### `crates/ty_python_semantic/src/types/typed_dict.rs` (modified, +33/-15)
- Touched symbols: none detected
- Direct callers: none detected in changed hunks
- Related tests: `crates/ty_python_semantic/src/types/infer/tests.rs`, `crates/ty_python_semantic/src/types/special_form.rs`, `crates/ty_python_semantic/src/types/tests.rs`, `crates/ty_python_semantic/src/types/tests.rs`


## Literate diff — generated explanation

> Generated by `gpt-5-mini` from bounded, redacted context. This prose cannot change the deterministic verdict.
> Redactions applied before the model call: 0

### Background

This PR changes how the type system distinguishes between two uses of tuple-shaped type lists: (a) a runtime tuple type (a product of runtime values), and (b) a variadic type-argument sequence (a TypeVarTuple / argument pack). The motivation is that a runtime tuple containing a required Never element is uninhabited and should behave like Never (and be disjoint from every type), while a TypeVarTuple specialization may legitimately include Never as a type argument and should preserve its argument shape.

### Intent in plain language

Introduce an explicit role distinction for tuple specifications so identical element sequences can have different semantics depending on whether they describe a runtime tuple value or a variadic type-argument pack. Preserve full variadic argument shape (including Never elements and their positions and fixed lengths) for TypeVarTuple-related operations while treating runtime tuples with required Never elements as uninhabited (equivalent to Never). Update the repository's specification tests and documentation to reflect the new semantics.

### Narrative

#### 1. Why this change was proposed

Previously, the implementation preserved Never elements inside variadic specializations in a way that blurred the difference between an argument pack containing Never and a runtime tuple that has a required Never element. The PR asserts the need to treat those two meanings differently: a runtime tuple with a required Never element has no inhabitants and should be equivalent to Never, whereas a TypeVarTuple argument sequence like Container[int, Never] is a valid specialization and must keep the Never argument and its position.
- Files: `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md`, `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md`
- Evidence: From type_compendium/tuple.md: static_assert(is_equivalent_to(tuple[Never], Never)); From type_compendium/never.md: static_assert(is_equivalent_to(tuple[int, Never], Never))

```text
static_assert(is_equivalent_to(tuple[int, Never], Never))
```

#### 2. Representation change: tuple role separation

The PR introduces a conceptual representation change: tuple specifications carry an explicit role (interned TupleRole) that marks whether they describe a runtime tuple or a TypeVarTuple argument pack. Interning the role means the same element sequence can be represented twice with distinct meanings, preventing the runtime semantics of an impossible tuple from erasing the shape of a variadic argument pack.
- Files: `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md`
- Evidence: From generics/pep695/typevartuple.md: reveal_type(first)  # revealed: Container[int, Never]; From generics/legacy/typevartuple.md: reveal_type(Factory(1, value))  # revealed: Factory[int, Never]

```text
class Container[*Ts]: ...  # argument packs preserve Never
```

#### 3. Marking and propagation at variadic boundaries

Argument packs are marked when variadic generic arguments or TypeVarTuple constraints are constructed. Once marked, the pack's full shape (fixed prefix/suffix, element positions including Never, and length information) is preserved through inference, constructor specialization, callable signatures, and relation checking. The test and doc updates show examples for constructor inference and binding (functools.partial) that keep Never in place rather than dropping or collapsing it to bottom semantics in the variadic argument context.
- Files: `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md`
- Evidence: From generics/pep695/typevartuple.md: reveal_type(Factory(1, value))  # revealed: Factory[Literal[1], Never]; From generics/legacy/typevartuple.md: reveal_type(Factory(1, value))  # revealed: Factory[int, Never]; From call/functools_partial.md: reveal_type(partial(f, value))  # revealed: partial[(first: tuple[Never], second: int) -> None]

```text
reveal_type(Factory(1, value))  # revealed: Factory[int, Never]
```

#### 4. Runtime tuple semantics tightened (tuples containing Never become Never)

Documentation and test expectations were updated to mark runtime tuples that contain a required Never element as equivalent to Never and therefore disjoint from every type (including themselves). This affects is_equivalent_to, is_disjoint_from, and assignability assertions, and indexing behavior for homogeneous portions that are uninhabited.
- Files: `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md`, `crates/ty_python_semantic/resources/mdtest/type_properties/is_disjoint_from.md`, `crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md`, `crates/ty_python_semantic/resources/mdtest/subscript/tuple.md`
- Evidence: From type_compendium/never.md: static_assert(is_equivalent_to(tuple[int, Never], Never)); From is_disjoint_from.md: static_assert(is_equivalent_to(tuple[Never], Never)) and static_assert(is_disjoint_from(tuple[Never], tuple[Never])); From is_assignable_to.md: static_assert(is_assignable_to(Any, tuple[Never])); From subscript/tuple.md: reveal_type(empty)  # revealed: tuple[()]  and empty[0]  # error: [index-out-of-bounds]

```text
static_assert(is_equivalent_to(tuple[Never], Never))
```

#### 5. Special-case: homogeneous variable-length tuples remain inhabited by the empty tuple

The PR keeps a distinction for homogeneous variable-length tuples: tuple[Never, ...] is still inhabited by the empty tuple, so it is not equivalent to Never. The test updates explicitly preserve this earlier exception while tightening semantics for fixed-length tuples that include a required Never element.
- Files: `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md`, `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md`
- Evidence: From type_compendium/never.md: static_assert(not is_equivalent_to(tuple[Never, ...], Never)); From type_compendium/tuple.md: static_assert(is_equivalent_to(tuple[Never], Never)) and adjacent examples showing homogeneous portions collapsing to empty sequences

```text
static_assert(not is_equivalent_to(tuple[Never, ...], Never))
```

#### 6. Tests and documentation updated across many spec files

A large set of mdtest resource files were edited to reflect the new semantics: examples, static asserts, diagnostic snapshots, and reveal_type expectations were updated to show tuples with required Never elements collapsing to Never, while TypeVarTuple-specializations preserve Never elements. Many of these changes are pedagogical/test fixtures that codify the new expected behavior.
- Files: `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md`, `crates/ty_python_semantic/resources/mdtest/type_compendium/tuple.md`, `crates/ty_python_semantic/resources/mdtest/type_compendium/never.md`, `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md`, `crates/ty_python_semantic/resources/mdtest/subscript/tuple.md`, `crates/ty_python_semantic/resources/mdtest/type_properties/is_assignable_to.md`, `crates/ty_python_semantic/resources/mdtest/type_properties/is_disjoint_from.md`
- Evidence: From call/functools_partial.md: reveal_type(partial(f, value))  # revealed: partial[(first: tuple[Never], second: int) -> None]; From generics/pep695/typevartuple.md: reveal_type(Factory(1, value))  # revealed: Factory[Literal[1], Never]; From type_compendium/tuple.md: static_assert(is_equivalent_to(tuple[int, *tuple[tuple[Never], ...], str], tuple[int, str]))

```text
reveal_type(partial(f, value))  # revealed: partial[(first: tuple[Never], second: int) -> None]
```

### Review questions

- Where in the source tree is the new TupleRole type defined and interned? (I can't locate the core implementation diff from the provided mdtest-only contexts.)
- Do unit tests (beyond mdtest resource examples) exercise the new role separation in inference and relation-checking code paths (e.g., in crates/ty_python_semantic/src/types/...)?
- The repository's performance check 'CodSpeed Performance Analysis' failed — do the implementation changes introduce measurable allocation or interning overhead that needs addressing?
- Are there any interactions with recursive alias normalization, ParamSpec, or Self that were not covered by the edited mdtests and might still break? (Several mdtest files added examples for recursive/growing aliases, but I cannot confirm code-level coverage.)
- Has the distinction between argument-pack roles and runtime tuples been propagated to all places that materialize or simplify tuple types (materialization, canonicalization, serialization, equality tests)?

### Uncertainties

- The provided changed-file contexts are primarily documentation/mdtest updates. The authoritative deterministic facts describe an implementation change (an interned TupleRole and marking at variadic boundaries), but I cannot see the actual source diffs for the core type system changes (no concrete files like 'src/types/tuple.rs' were shown in the provided context).
- I cannot confirm the exact filenames or code locations where TupleRole or its interning were added, nor the API by which a tuple spec is marked as an argument pack. The PR body describes the change, but the code-level edits that implement interning and propagation are not included in the supplied diffs.
- The 'NO_TEST_COVERAGE' risk flag lists production files (e.g., crates/ty_python_semantic/src/types/...) that were changed but there are no obvious unit tests shown in the supplied contexts to cover those production changes.
- The failing status check 'CodSpeed Performance Analysis' is listed as a blocker (BLOCK). The provided context does not include profiling output or details explaining which change triggered the regression.
- I cannot verify whether additional edge cases (e.g., interaction with backward-compatibility for older TypeVarTuple backports, or with third-party tooling) were considered beyond the updated mdtests.

## Changed-file inventory

| File | Status | Additions | Deletions | Symbols |
| --- | --- | ---: | ---: | --- |
| `crates/ty_python_semantic/resources/mdtest/attributes.md` | modified | 13 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/call/functools_partial.md` | modified | 29 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/comparison/instances/membership_test.md` | modified | 13 | 1 | — |
| `crates/ty_python_semantic/resources/mdtest/diagnostics/error_context.md` | modified | 30 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/generics/legacy/typevartuple.md` | modified | 60 | 0 | — |
| `crates/ty_python_semantic/resources/mdtest/generics/pep695/typevartuple.md` | modified | 322 | 2 | — |
| `crates/ty_python_semantic/resources/mdtest/pep695_type_aliases.md` | modified | 224 | 2 | — |
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
| `crates/ty_python_semantic/src/types.rs` | modified | 60 | 18 | — |
| `crates/ty_python_semantic/src/types/attribute_write.rs` | modified | 2 | 2 | — |
| `crates/ty_python_semantic/src/types/bool.rs` | modified | 4 | 1 | — |
| `crates/ty_python_semantic/src/types/call/bind.rs` | modified | 34 | 20 | — |
| `crates/ty_python_semantic/src/types/call/bind/constructor.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/constraints.rs` | modified | 44 | 36 | — |
| `crates/ty_python_semantic/src/types/cyclic.rs` | modified | 31 | 3 | — |
| `crates/ty_python_semantic/src/types/equality/enums.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/function.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/generics.rs` | modified | 34 | 7 | — |
| `crates/ty_python_semantic/src/types/infer/builder.rs` | modified | 11 | 9 | — |
| `crates/ty_python_semantic/src/types/infer/builder/attribute_assignment.rs` | modified | 11 | 7 | — |
| `crates/ty_python_semantic/src/types/infer/builder/type_form.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/infer/builder/typed_dict.rs` | modified | 1 | 0 | — |
| `crates/ty_python_semantic/src/types/infer/comparisons.rs` | modified | 1 | 1 | — |
| `crates/ty_python_semantic/src/types/instance.rs` | modified | 40 | 4 | — |
| `crates/ty_python_semantic/src/types/match_pattern.rs` | modified | 6 | 4 | — |
| `crates/ty_python_semantic/src/types/narrow.rs` | modified | 27 | 20 | — |
| `crates/ty_python_semantic/src/types/property_tests.rs` | modified | 4 | 4 | — |
| `crates/ty_python_semantic/src/types/protocol_class.rs` | modified | 13 | 7 | — |
| `crates/ty_python_semantic/src/types/relation.rs` | modified | 79 | 7 | — |
| `crates/ty_python_semantic/src/types/set_theoretic.rs` | modified | 24 | 2 | — |
| `crates/ty_python_semantic/src/types/set_theoretic/builder.rs` | modified | 4 | 4 | — |
| `crates/ty_python_semantic/src/types/signatures.rs` | modified | 7 | 4 | — |
| `crates/ty_python_semantic/src/types/tests.rs` | modified | 2 | 2 | — |
| `crates/ty_python_semantic/src/types/tuple.rs` | modified | 91 | 17 | — |
| `crates/ty_python_semantic/src/types/type_alias.rs` | modified | 47 | 6 | — |
| `crates/ty_python_semantic/src/types/typed_dict.rs` | modified | 33 | 15 | — |

## Deterministic policy

- `BLOCK`: failed checks or authentication/secrets/security-sensitive changes.
- `QUARANTINE`: database changes, dependency changes, missing obvious test coverage, or unavailable/pending checks.
- `SHIP`: no rules fired and observed checks passed.

_Generated by diffly-cli. Deterministic triage is authoritative; any literate-diff prose is optional generated explanation._
