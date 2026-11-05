**Elemental "Measure"** -- single-concept, additive, countable
**Composite** -- mix of elementals
**Atomic** -- normalized structure or storage grain or source fidelity. not relevant to measures. avoid b/c it is semantically overloaded (lots of overlapping yet ontologically different)


# Primitive
**Primitive** -- raw, source-captured (bronze) value with no applied business logic, derivation, or transformation (or slice)

Anti-Patterns -- misuse *primitive*

* “important”
* “core”
* “frequently used”

That is **incorrect**.

- “all numerators are primitive” ❌
- “all denominators are primitive” ❌

### Examples of Primitives
```
Layer              | Primitive Type        | Example
------------------|-----------------------|---------------------------
Storage           | Data primitive        | integer, string
Entity modeling   | Ontological primitive | Customer, Contract
Metrics           | Measure primitive     | NetContractAmount (raw)
Logic             | Operator primitive    | CASE, =, AND
```

