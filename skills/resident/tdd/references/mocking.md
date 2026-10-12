# When to Mock

Choose the subject and dependency boundary under the [shared testing policy](../../ddd-implement/references/testing.md). Typical dependencies that may need a substitute include:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Exercise the selected subject's implementation through its public contract; substitute dependencies across that boundary without replacing the behavior being tested. An internal module can be the subject, so the boundary need not be the whole application.

Ownership does not determine the boundary: your own remote service or database can still need a test adapter. Prefer a real test dependency when practical; preserve the substituted contract and required real integration coverage. Do not redesign approved architecture solely to make mocking easier.

## Designing for Mockability

When boundary design is within approved scope, the following patterns can help; they do not require changing existing interfaces solely for a test:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. Prefer SDK-style interfaces over generic fetchers**

Create specific functions for each external operation instead of one generic function with conditional logic:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

The SDK approach means:
- Each mock returns one specific shape
- No conditional logic in test setup
- Easier to see which endpoints a test exercises
- Type safety per endpoint
