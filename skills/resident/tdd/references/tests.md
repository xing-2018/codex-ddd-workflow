# Good and Bad Tests

## Good Tests

**Behavior-focused**: Exercise the selected subject through its stable contract. The [shared testing policy](../../ddd-implement/references/testing.md) governs subject boundaries, test selection and acceptance at every test level.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Characteristics:

- Tests behavior users/callers care about
- Uses the selected subject's public contract, including a module or function contract
- Survives internal refactors
- Describes WHAT, not HOW
- Covers one coherent behavior, with multiple assertions when needed for its result, state and effects

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

Here, calling `paymentService.process` is an implementation choice, not an approved payment protocol requirement.

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags:

- Replacing implementation inside the selected subject
- Testing private methods
- Asserting on internal call counts/order instead of public behavior
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying private state through a side channel outside the selected contract

An external protocol may make request counts or ordering observable requirements. Assert those at its boundary when the approved contract requires them, not to mirror an internal implementation.

The following example assumes callers are promised user retrieval, not a particular storage schema. A persistence adapter with a storage contract would have a different test boundary.

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**: Expected value restates the implementation, so the test passes by construction.

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```
