# HFC Geometry Kernel Design Principles

## Coding Standards
- Prefer small, explicit modules with clearly defined responsibilities.
- Use type hints, descriptive names, and predictable interfaces.
- Keep public APIs stable and well documented.
- Avoid hidden state and avoid magic values that are not traced to a formal policy.

## Precision Policy
- The internal unit of length is millimeters.
- All geometric calculations should use robust tolerance handling rather than strict equality.
- Numerical comparisons must be governed by explicit precision rules and a central tolerance strategy.
- Small numerical noise should be tolerated without compromising geometric correctness.

## Documentation Policy
- Every public module, class, and critical function should be documented.
- Documentation should explain intent, assumptions, and constraints, not just syntax.
- Architecture and specification documents must remain aligned with implementation reality.
- Examples and notes should accompany complex geometric behavior.

## Testing Policy
- Core geometry functions must be covered by unit tests.
- Regression tests should protect against precision regressions and behavioral changes.
- Tests should validate real geometric outcomes, not only internal implementation details.
- New features should be introduced with tests before broad adoption.

## Performance Policy
- Performance should be predictable and scalable for real engineering datasets.
- Optimize for correctness and robustness first; optimize later when profiling demonstrates a need.
- Repeated geometric calculations should be structured to avoid unnecessary recomputation.
- The kernel should remain responsive even when handling large meshes or complex reconstruction tasks.
