# Project and stack adaptation

Read only for an unresolved architecture choice involving project shape, runtime or process boundaries. Inspect the nearest rules, subproject declarations and locks, supported interpreter/compiler, startup, checks and adjacent code. Distinguish allowed ranges, resolved locks, observed environments and approved targets. Reuse discoverable facts; public interfaces, stack or delivery changes still require approval.

Keep domain responsibilities, state owners, failures and lifetimes clear. Project size does not impose a layer count. Use ordinary functions and existing APIs unless present consumers, variation or isolation justify more structure.

| Project shape | Starting point and reason to expand |
| --- | --- |
| Python tool or numerical script | One entry and clear functions; split for independent reuse, change or lifecycle, not a universal src layout |
| Distributed Python package | Consumers and installation/import isolation can justify src/package; verify real import/install behavior when authorized |
| Small FastAPI service | Entry, routes, models and necessary dependencies; simple operations may use the existing ORM session directly |
| Complex FastAPI business | Organize by business capability; shared workflows, transactions and external failure may justify services/data access, without mandatory Service/Repository/DTO/Interface for each feature |
| React/TS application | Cohesive feature pages, components, data access and needed hooks; lift shared components/state only for actual consumers |
| Electron | Preserve main/preload/renderer and explicit IPC capabilities; shared static types do not replace runtime boundary validation |
| Embedded or old solver script | Preserve host API/interpreter; isolate independent computation and add adapters only for current replacement, compatibility or verification needs |
| C++/MFC acquisition | Retain engineering/SDK organization, separating acquisition, storage, UI, cancellation and resources according to actual thread and object ownership |

Personal preferences such as Python, FastAPI, React, Chinese comments, direct IDE launch or development ports apply only to corresponding new projects or projects that adopted them. Do not rewrite an existing project to fit a global template.

For new work without an established target, prefer a mature maintained release over the newest major: Python 3.11+, modern browser JavaScript or a supported Node LTS, TypeScript 5.9.x, React 19.2.x where needed, and C++20 with confirmed toolchain support are current validation baselines. Verify dependencies and deployment constraints; existing locks take precedence. Record the selected version and its reason, and verify capabilities actually used rather than creating an exhaustive historical-version matrix. Do not migrate established projects or enable experimental features solely to match the baseline.

Use [architecture](architecture.md) and [deepening](architecture-deepening.md) for actual boundary decisions. A simple HTTP call need not acquire an interface; one external solver may need isolation; independent numerical modules need not merge; two semantically different implementations need not share a port. Verification reuses the approved project's checks and the shared [testing policy](../../ddd-implement/references/testing.md), without authorizing new tool chains or product frameworks.
