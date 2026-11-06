```table-of-contents
```

# 1:M Decomposes
de-polymerizes into monomers

```

decomposes into -- entity decomposition
enumerates into
  explodes into
  **expands across** dimension x
  fans out into
  branches into
  decomposes into
  splices into
  normalizes into (splitting repeating groups into a separate table) -- spli
  row expansion

grain elevation | grain shift
```

## Employee to EmployeeC9 
> “We take a base identifier and expand it into multiple context-specific identities”
> Employee → explodes into Employee-System logins
> Employee expands across system dimension
> Employee materializes at the employee-system grain
> Introduces cardinality expansion from 1 → M

> **EmployeeLogin** represents a one-to-many expansion of Employee, materializing each system-specific credential at the employee-system grain. Each row uniquely identifies a login context per employee and system.

| Term                                 | When to Use                           | Why it Fits                                                      |
| ------------------------------------ | ------------------------------------- | ---------------------------------------------------------------- |
| **Normalize / Normalization**        | Classic relational modeling           | You’re splitting repeating groups (logins) into a separate table |
| **Child Table (1:M relationship)**   | Structural description                | Employee → EmployeeLogin is canonical parent-child               |
| **Row Expansion**                    | Data-shaping / transformation context | You “explode” 1 employee into multiple login rows                |
| **Grain Elevation (or Grain Shift)** | Analytics / modeling vocabulary       | You’re moving from _employee grain_ → _employee-system grain_    |
| **Entity Decomposition**             | Design-level explanation              | Breaking one conceptual entity into multiple related ones        |
| **One-to-Many Projection**           | Query/model view framing              | You’re projecting employee into multiple system-specific records |

# Rolls Up (1:M)
polymerizes (monomers → polymers)

```
rollup / rollsup
coalesces into
aggregates
normalizes into a single entity
collapes into
```

# Bijection (1:1)
allows forward AND backward deterministically. no ambiguities allowed.

- 1:1 mapping only (not 1:M, M:M, M:1)
- injective (1:1) = no dups
- surjective (onto) = no orphans → map to "Unknown"


A **bijection** is a function between two sets that pairs every element in the domain to exactly one element in the codomain, and vice versa (one-to-one correspondence). It is both injective (no two elements map to the same target) and surjective (no target is left unmapped). Bijections define equivalent set cardinalities, allow for inverse functions, and indicate identical set sizes for finite cases set inclusion, set exclusion, and surjectivity (no element left unmapped)

# Bridge (M:M)
M:M 