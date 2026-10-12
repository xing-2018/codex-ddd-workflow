# Logic Prototype

Choose the smallest runnable experiment that answers the question. Use an existing command, REPL or short script for machine-checkable logic; use a single self-contained HTML file (a **shareable demo**) only when human interaction is needed. Use this when the question is about **business logic, state transitions, or data shape**: the kind of thing that looks reasonable on paper but only feels wrong once you push it through real cases.

Because it's one file with nothing to install, you can hand it to a non-developer and let them feel the model for themselves. So it speaks their language, not the code's.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where someone wants to **press buttons and watch state change**.

If the question is "what should this look like," use [UI design](ui-design.md) without treating prototype evidence as approval.

## Interactive demo process

Apply the following only when interactive judgment is necessary; a script or REPL result does not need a UI, portable module or walkthrough tabs.

### 1. State the question

Before writing code, write down what state model and what question you're prototyping. A logic prototype that answers the wrong question is pure waste.

### 2. Isolate the logic in a portable module

Put the actual logic in a small pure module that could be lifted out later. The page around it is throwaway. Pick the shape that fits the question: pure reducer, explicit state machine, pure functions over a plain data type, or a module with a small method surface when ongoing internal state is real.

Keep it pure: no DOM or button handlers inside the model. The page calls the model; nothing flows the other direction.

### 3. Build the shareable HTML file

One file, plain HTML/CSS/JS: no framework, bundler, or server. Write it for a non-developer using domain language.

Show the question, relevant state as readable labelled fields, and controls for the actions needed to answer it. Add guided replay from a known state only when a difficult sequence needs it; choose buttons, presets or tabs to fit that sequence.

Choose scenarios that include the happy path, a tricky edge case, and an action that should be illegal when relevant.

### 4. Hand it over

Open or share the file. The useful feedback is when the user says the model permits or prevents something they did not expect. Those reactions answer the design question.

### 5. Capture the answer

Once the prototype answers the question, return observations, limitations and decision impact to the main workflow. Record the decision in its authority owner only when the decision and persistence are authorized; a semantic design change still needs approval. The HTML shell remains evidence, and product implementation continues under its existing approved contract and implementation authorization.

## Anti-patterns

- Use direct assertions when useful; do not build a separate test suite for disposable evidence.
- **Don't wire it to the real database** unless persistence is the question.
- **Don't generalise.** No future-use abstractions.
- **Don't blur the logic and page together.**
- **Don't reach for a framework, bundler, or server** for a one-file logic demo.
- **Don't ship the HTML shell into production.**
