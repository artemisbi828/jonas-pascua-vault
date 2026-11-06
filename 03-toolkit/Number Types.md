
```
NUMBER
│
├── INTEGER / WHOLE-VALUE
│   │   No fractional component
│   │
│   ├── Negative Integer      -42
│   ├── Zero                    0
│   └── Positive Integer       42
│
└── FRACTIONAL / NON-INTEGER-CAPABLE
    │
    ├── DECIMAL
    │   │   Fixed/defined decimal precision in data systems
    │   │
    │   ├── Currency           $19.99
    │   ├── Percentage         12.50%
    │   ├── Rate                0.075
    │   ├── Decimal (Generic)   72.25
    │   └── Duration           123.456 seconds
    │
    └── FLOATING-POINT
        │   Approximate numeric representation
        │
        ├── Float
        └── Double
```

# Semantic
```
Numeric
├── Integer
│   ├── Count
│   ├── Identifier
│   ├── Ordinal / Rank
│   └── Generic Integer
│
└── Decimal
    ├── Currency / Monetary
    ├── Percentage
    ├── Rate / Ratio
    ├── Measurement
	└── Generic Decimal
```
# Mathematical
```
NUMBER
└── Complex
    └── Real
        ├── Irrational
        │   ├── π
        │   └── √2
        │
        └── Rational
            ├── Fraction / Decimal
            │   ├── 1/2
            │   └── 12.50
            │
            └── Integer
                ├── Negative Integer
                └── Whole
                    ├── Zero
                    └── Natural / Counting
                        └── 1, 2, 3, ...
```