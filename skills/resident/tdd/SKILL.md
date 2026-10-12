---
name: tdd
description: Use TDD when the user requests TDD, test-first or testing-first work (including 测试优先 or 先写测试), or when non-trivial behavior has an independent failing expectation at a stable public interface. Skip mechanical edits and routine post-implementation verification.
---

# Test-Driven Development

TDD is a test-first development method: establish a failing behavior expectation, implement enough to pass it, then refactor within the approved design. It is not routine post-implementation verification or test-suite cleanup. Read [testing and test maintenance](../ddd-implement/references/testing.md) for shared test boundaries, selection, execution and acceptance rules; this Skill owns only the test-first method and its supporting guidance.

If work has already started green, or a narrow verification test is only confirming a mechanical/configuration edit, do not retroactively turn the task into TDD. Use the repository's ordinary validation path instead.

Read relevant `CONTEXT.md` or ADR clauses when domain vocabulary or approved behavior is unresolved; reuse valid context already available so test names and interfaces match the project's language.

## What a good test is

Tests verify behavior through the selected subject's stable public contract. A behavior-preserving internal refactor should leave them valid. A good test reads like a specification.

See [references/tests.md](references/tests.md) for examples and [references/mocking.md](references/mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the selected subject's public contract where behavior is observed without reaching into its implementation. The subject may be an internal domain module or pure function; it need not be the product's outermost API.

Identify the public seam before writing a durable test. Reuse seams established by approved design or repository testing practice without asking the user to approve each test entry point. Select equivalent existing public interfaces autonomously; changing a public contract, adding a dependency or redesigning architecture to create a seam returns to the applicable design or authorization gate. Focus on critical paths and complex logic instead of internal detail.

When the interface shape or seam placement is itself in question, read [ddd-design architecture](../ddd-design/references/architecture.md).

## Anti-patterns

- **Implementation-coupled**: replaces implementation inside the selected subject, tests private methods, or verifies through a side channel outside its contract. The tell: a behavior-preserving refactor breaks the test.
- **Tautological**: the assertion recomputes the expected value the same way the code does. Expected values need an independent source of truth: a known literal, worked example, or approved requirement.
- **Horizontal slicing**: writing all tests first and all implementation later. Work in vertical slices instead: one test → one minimal implementation → repeat.

## Rules of the loop

- **Red before green.** Reuse or adapt an existing test when it can express the missing behavior; otherwise add the smallest justified case. Before implementation, confirm the test reaches and fails the intended behavior expectation, rather than failing in setup or infrastructure; then write only enough code to pass it.
- **One slice at a time.** One behavior expectation and minimal implementation per cycle. A cycle does not require a new permanent test or file.
- **Do not anticipate future tests.** Add behavior only when the approved requirement and current red test demand it.
- **Keep refactoring bounded by the current design.** Structural cleanup must serve the approved change rather than becoming speculative redesign.
