# C++ and MFC

Read only for relevant code. Inspect the existing compiler, language standard, runtime, SDK, build target and ownership conventions; preserve delivery compatibility rather than choosing the newest standard.

For newly authorized work with a capable toolchain, C++20 is the current mature baseline. Verify actual compiler and standard-library support before using facilities; C++23/26 are not default validation targets. Existing project standards and SDK constraints still govern migration decisions.

Use RAII for owned resources, preferring value semantics, const and the rule of zero where they fit. State ownership and lifetime of references, pointers and handles. Raw pointers can be non-owning observers; do not mechanically replace them with smart pointers or take ownership of framework-managed objects. Match numeric ranges, precision and narrowing conversions to domain and SDK contracts.

For concurrent work, identify the state owner, lock scope, cancellation and exit protocol. Avoid long I/O, unknown callbacks or waits on a thread that calls back while holding a lock. Lock-free code is not an automatic performance improvement. Preserve needed numerical and concurrency evidence.

std::span is a non-owning view, not a resource owner. Its backing storage must outlive every asynchronous use. std::jthread helps own join/cancellation, but it does not extend captured references' lifetime or interrupt work that ignores its stop token. Establish storage ownership and shutdown ordering explicitly.

## MFC branch

Keep .sln/.vcxproj, message maps, destruction rules and device SDK contracts. Respect thread affinity and framework handle maps. Send worker results to the correct UI thread through the project's established message/update mechanism; do not share framework objects as unrestricted cross-thread state. Preserve acquisition, storage, UI, cancellation and resource lifetimes.

Reuse the existing build, formatting and static analysis. Do not migrate to CMake, adopt C++20 across all targets or enable unsupported library facilities as a side effect of modernization. Real hardware operations still need their explicit authorization.
