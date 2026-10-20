# Git

Read before project writes or Git mutations, including mechanical edits; reading this reference does not activate DDD.

Worktree use requires still-valid explicit session authorization. A commit or push request does not authorize creating or switching local branches or creating remote branches.

Before first writing version-controlled deliverables to a user-designated non-Git root, initialize Git unless disabled. Never nest repositories; exclude sensitive files, generated outputs and large files before a baseline commit.

For version-controlled deliverables, after required review and validation pass, locally commit only this task and leave no uncommitted task changes. Preserve unrelated content and staging exactly; a dirty tree need not become clean. Report isolation problems rather than including or discarding unrelated changes. Read-only tasks create no commit. With known concurrent Git activity, coordinate the complete stage/review/commit transaction under [shared checkout coordination](execution.md#shared-checkout-coordination); preserve peer staging and locks, and report an unisolated dependency instead of mixing candidates. Use a conventional commit type with a Simplified Chinese message.

## Runtime-only tasks

For tasks confined to runtime data, caches or processes with no version-controlled deliverable, do not initialize Git, create tracked workflow records or make a commit merely to satisfy the workflow. Keep necessary authorized evidence in the project's designated Git-ignored location. Explicit user or project requirements to archive or commit take precedence. This exception grants no operation permission; source, formal-documentation and configuration changes retain their existing delivery rules.

## Integrate existing work

For an authorized PR integration or main synchronization, fix the source revision, target baseline and existing working/staged content before applying changes. Use the existing implementation path when approved behavior and execution authority are recoverable; an integration request does not replace missing design approval. Resolve equivalent wiring within scope, and return only material behavior, data or interface conflicts to design. Preserve necessary dependencies and unrelated work; a local-first instruction is not permission to discard the incoming change or use `ours` for every conflict.

Distinguish local integration, remote publication, another host's source synchronization, database migration, service restart and actual UI/data operations. Recover each requested action's authorization and project prerequisites from existing authority, using the current record or conversation rather than a new matrix or tracker. A dirty shared directory blocks the affected write or synchronization; it blocks another action only through an identified project dependency. Preserve required cross-host gates and obtain a real exception before deferring them. Reuse a valid scoped deferral; do not invent authority to contact or take over another task.

Identify project-required checks before creating integration commits. Run checks that can inspect the fixed candidate before changing the destination or creating commits, including applicable whitespace, inventory, link, version and proposed-message checks; run only authorized checks and retain mandatory checks that require actual integration. Use isolated copies only for a concrete conflict or validation need in an authorized location, without creating branches or worktrees merely for the method. Recheck source and destination drift before applying; source updates invalidate only affected evidence, while required final integration and publication checks remain.

## Match content identity to the claim

Compare a Git source candidate by paths, file modes and blob identity under the project's actual attributes and clean conversions. A checkout or archive may contain converted line endings; a raw-byte mismatch alone does not prove source drift. Explain a mismatch using the actual Git rules, not arbitrary whitespace normalization, and retain unexplained differences. This comparison does not permit rewriting the working content.

Preserving existing user changes may require their original bytes and staged content; checking delivered artifact bytes uses their actual inventory and hashes. Neither is replaced by canonical source equivalence. Behavior, formal source acceptance and installation keep their own evidence contracts; a matching tree does not establish them.

## Commit organization

When existing worktree or staged changes touch the task, assess the boundary before substantive edits. Compare HEAD, recoverable task-start working content and current content to distinguish this task's changes, necessary dependencies and unrelated work; preserve existing staging separately. Reuse available evidence and report unknown provenance rather than inventing it. Complete safe isolation and repository-authorized commits within the approved scope without asking the user to select files. If a necessary dependency is outside that scope or cannot be isolated safely, identify the smallest uncovered content, why it is needed and the blocked action, and obtain any missing authorization before expanding the candidate; never silently include pre-existing work or treat overlap alone as task completion.

One task may require several commits. Before staging, group changes by a concrete purpose that can be reviewed, validated and reverted coherently. Keep a correction or capability with its necessary callers, tests, documentation and version changes. Separate independently useful design updates, tooling, workflow changes and cleanup; a shared task, directory or delivery deadline alone does not justify combining them. Do not split by file count, directory or a fixed number of commits. Keep dependencies valid in the proposed sequence; tightly coupled changes may belong in one commit.

Do not introduce unrelated formatting cleanup. Necessary non-semantic whitespace or final-newline corrections in affected content belong with the related implementation or integration commit and should be completed before creating it; they are not independently useful cleanup. If discovered after committing, preserve history and establish whether a required check actually blocks delivery. Do not automatically amend, rebase or append a cosmetic-only commit. If a mandatory gate can only be satisfied by a separate correction or history repair, present that minimum exception and obtain the applicable decision before proceeding; never mix unrelated changes merely to avoid a separate commit.

For each proposed commit, identify its purpose, file or hunk scope, necessary dependencies, applicable validation and intended message. Use the existing conversation or task record, not a new mandatory tracker. Shared files may require hunk separation; protect unrelated content and staging. If isolation is impossible, report the dependency instead of broadening the candidate or discarding changes.

Before each commit, inspect the complete staged diff and compare it with that boundary, approved scope and message. Correct unjustified mixing or inaccurate descriptions within existing authorization before committing; technical checks and a recorded PASS do not replace this semantic review. When reviewing a handoff or push, inspect each commit in the exact candidate range rather than only its combined final tree. Reuse still-valid review and validation for unchanged content, and recheck the affected evidence when the staged candidate changes.

Repeated titles across directories in a repository browser and a large file count are not failures by themselves. Judge the commit's purpose and dependencies as a whole; README-only paths do not make a commit containing a necessary code correction documentation-only. Quality findings do not authorize rewriting published history. Separate a future-process correction from any explicitly requested history repair; the latter needs its own approval and recovery plan.

## Commit information

Before creating any commit, recover the project's allowed types, language and required message checks from its instructions and existing checker. Apply those rules to the proposed message before freezing it; generic syntax acceptance is not project compliance. When the project checker only accepts existing commits, inspect its applicable rules before creation and run its still-required range check afterward. Do not change the checker, install hooks or invent a second policy to make a message pass.

Choose the type from the actual change within those project rules: `feat` for a new capability, `fix` for a correction, and `docs` for documentation-only changes; use other permitted conventional types when appropriate. A release operation or version increment does not determine the type. Classify version impact separately under the project's version rules.

Write a subject that identifies the concrete change and its result. A reader should understand what was added or corrected without opening the diff. A version may supplement that description; generic subjects such as "release version" or "optimize content" are insufficient. Add a body when the reason, user impact or important limitations need explanation; simple changes do not require a long body.

Before committing, compare the type, subject and any body with the complete staged diff and approved scope. Check that claims match actual changes and evidence, and exclude personal information, private source references, machine paths and credentials. Review generated commit information with the same checks; do not replace it with a fixed release title. These checks grant no commit, push or history-rewriting permission.

## Freeze and verify delivery

For an ordinary commit, freeze the actual reviewed message and staged content before committing. Use [git_delivery.py](../scripts/git_delivery.py) from this Skill with the project's authorized Python and task-artifact directory. `freeze` copies the message as UTF-8/LF with a final newline and binds its bytes, repository, HEAD and complete staged entries; it rejects unmerged entries and an existing output directory. Review the resulting `message.txt` for Simplified Chinese, accuracy, scope and sensitive information. Commit from that same file with `git commit --cleanup=verbatim -F <freeze-dir>/message.txt`; do not regenerate an inline `-m` after the check. A receipt records input identity, not approval.

After committing, run `verify-commit` against that receipt and the actual commit. It checks the exact raw message, expected parent and full committed entries against the frozen values. A changed message, staged content, parent or checker invalidates the corresponding evidence: stop dependent delivery, inspect the cause and obtain only the missing authorization; do not automatically amend or rewrite history. Preserve the failed attempt. Passing source, version, link or whitespace checks does not establish commit-message compliance.

Before an authorized push, observe the real target branch tip, fix the candidate HEAD and inspect **every** commit in that exact range with `check-range`, together with the existing semantic diff/message review. The target must still match the observed state and the actual candidate must match the checked HEAD; drift requires a new range check and may require a new decision. An intermediate invalid subject fails the range even when the final subject is valid. This check performs no push and grants no publication authority.

```text
python -B <ddd-flow>/scripts/git_delivery.py freeze --repo <root> --message <reviewed-message-file> --output <new-task-directory>
python -B <ddd-flow>/scripts/git_delivery.py verify-commit --repo <root> --receipt <freeze-dir>/receipt.json --commit <actual-commit>
python -B <ddd-flow>/scripts/git_delivery.py check-range --repo <root> --base <observed-target-commit> --head <fixed-candidate>
```

The script checks conventional subject syntax and rejects summaries without Chinese characters; Chinese text only in the scope does not satisfy it. It cannot certify Simplified Chinese usage, semantic quality, truthful claims, safe content or approval. It does not install hooks, change configuration, create commits, access the network or push. Its verification command covers ordinary one-parent commits in an existing repository. For initial/merge/amend operations, an explicit different language contract or an unavailable helper, retain equivalent exact-message, parent/content and whole-range evidence under the effective rules; do not narrow supported workflows or bypass the checks merely by omitting the tool. Store receipts only in authorized task locations, without adding a mandatory project tracker.
