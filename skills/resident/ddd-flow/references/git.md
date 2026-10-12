# Git

Read before project writes or Git mutations, including mechanical edits; reading this reference does not activate DDD.

Worktree use requires still-valid explicit session authorization. A commit or push request does not authorize creating or switching local branches or creating remote branches.

Before first writing to a user-designated non-Git root, initialize Git unless disabled. Never nest repositories; exclude sensitive files, generated outputs and large files before a baseline commit.

After required review and validation pass, locally commit only this task and leave no uncommitted task changes. Preserve unrelated content and staging exactly; a dirty tree need not become clean. Report isolation problems rather than including or discarding unrelated changes. Read-only tasks create no commit. With known concurrent Git activity, coordinate the complete stage/review/commit transaction under [shared checkout coordination](execution.md#shared-checkout-coordination); preserve peer staging and locks, and report an unisolated dependency instead of mixing candidates. Use a conventional commit type with a Simplified Chinese message.

## Commit information

Choose the type from the actual change: `feat` for a new capability, `fix` for a correction, and `docs` for documentation-only changes; use other conventional types when appropriate. A release operation or version increment does not determine the type. Classify version impact separately under the project's version rules.

Write a subject that identifies the concrete change and its result. A reader should understand what was added or corrected without opening the diff. A version may supplement that description; generic subjects such as "release version" or "optimize content" are insufficient. Add a body when the reason, user impact or important limitations need explanation; simple changes do not require a long body.

Before committing, compare the type, subject and any body with the complete staged diff and approved scope. Check that claims match actual changes and evidence, and exclude personal information, private source references, machine paths and credentials. Review generated commit information with the same checks; do not replace it with a fixed release title. These checks grant no commit, push or history-rewriting permission.
