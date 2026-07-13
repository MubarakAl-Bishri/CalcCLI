Test Run Timestamp: 2026-07-13 05:51:38

# Calc 3 CLI - Ultimate Vector Operation Test Results

> Automated test run to verify mathematical accuracy, step-by-step logic, single-argument handling, and safety catches.

## 1. Vector & Vector Operations (Standard)

**Command executed:**
`python3 main.py vector-operation "[2,3,4]" add "[4,5,6]"`

**Output:**
```text
╭────────────────────── Vector Operation Result ──────────────────────╮
│ Result of add: 6.0*coord_sys.i + 8.0*coord_sys.j + 10.0*coord_sys.k │
╰─────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" subtract "[1,1,1]"`

**Output:**
```text
╭───────────────────────────────── Vector Operation Result ─────────────────────────────────╮
│ Result of subtract: (x - 1.0)*coord_sys.i + (y - 1.0)*coord_sys.j + (z - 1.0)*coord_sys.k │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[1,0,0]" cross "[0,1,0]"`

**Output:**
```text
╭──── Vector Operation Result ─────╮
│ Result of cross: 1.0*coord_sys.k │
╰──────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" cross "[x,y,z]"`

**Output:**
```text
╭─ Vector Operation Result ─╮
│ Result of cross: 0        │
╰───────────────────────────╯
```

---

## 2. Vector & Vector Operations (Step-by-Step)

**Command executed:**
`python3 main.py vector-operation "[2,3,4]" add "[4,5,6]" --show-steps`

**Output:**
```text
╭─────── Vector Operation (Step-by-Step) ────────╮
│ 1. General Formula (add):                      │
│ ⟨ x₁ + x₂, y₁ + y₂, z₁ + z₂ ⟩                  │
│                                                │
│ 2. Component Substitution:                     │
│ ⟨ 2 + 4, 3 + 5, 4 + 6 ⟩                        │
│                                                │
│ 3. Final Result:                               │
│ 6*coord_sys.i + 8*coord_sys.j + 10*coord_sys.k │
│                                                │
│ 4. No Numerical Value Available                │
│                                                │
╰────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" dot "[1,2,3]" --show-steps`

**Output:**
```text
╭─ Vector Operation (Step-by-Step) ─╮
│ 1. General Formula (dot):         │
│ (x₁ * x₂) + (y₁ * y₂) + (z₁ * z₂) │
│                                   │
│ 2. Component Substitution:        │
│ (x * 1) + (y * 2) + (z * 3)       │
│                                   │
│ 3. Final Result:                  │
│ x + 2*y + 3*z                     │
│                                   │
│ 4. No Numerical Value Available   │
│                                   │
╰───────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[1,0,0]" cross "[0,1,0]" --show-steps`

**Output:**
```text
╭─────────── Vector Operation (Step-by-Step) ───────────╮
│ 1. General Formula (cross):                           │
│ ⟨ (y₁z₂ - z₁y₂), (z₁x₂ - x₁z₂), (x₁y₂ - y₁x₂) ⟩       │
│                                                       │
│ 2. Component Substitution:                            │
│ ⟨ (0 * 0 - 0 * 1), (0 * 0 - 1 * 0), (1 * 1 - 0 * 0) ⟩ │
│                                                       │
│ 3. Final Result:                                      │
│ coord_sys.k                                           │
│                                                       │
│ 4. No Numerical Value Available                       │
│                                                       │
╰───────────────────────────────────────────────────────╯
```

---

## 3. Advanced Vector Operations (Angle & Projection)

**Command executed:**
`python3 main.py vector-operation "[1,0,0]" angle "[0,1,0]"`

**Output:**
```text
╭────── Vector Operation Result ──────╮
│ Result of angle: 1.5707963267948966 │
╰─────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[1,1,0]" angle "[1,0,0]" --show-steps`

**Output:**
```text
╭──────────── Vector Operation (Step-by-Step) ─────────────╮
│ 1. General Formula (angle):                              │
│ cos(θ) = (A · B) / (|A| * |B|)                           │
│                                                          │
│ 2. Component Substitution:                               │
│ cos(θ) = (1) / (sqrt(2) * 1)                             │
│                                                          │
│ 3. Final Result:                                         │
│ pi/4 rad                                                 │
│                                                          │
│ 4. Numerical Value:                                      │
│ 0.7853981633974483                                       │
│                                                          │
│ Note: Angle is in radians. Convert to degrees if needed. │
╰──────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[2,2,0]" projection "[1,0,0]"`

**Output:**
```text
╭─────── Vector Operation Result ───────╮
│ Result of projection: 2.0*coord_sys.i │
╰───────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" projection "[1,1,1]" --show-steps`

**Output:**
```text
╭─────────────────────────────── Vector Operation (Step-by-Step) ───────────────────────────────╮
│ 1. General Formula (projection):                                                              │
│ Projection of A onto B = ((A · B) / |B|²) * B                                                 │
│                                                                                               │
│ 2. Component Substitution:                                                                    │
│ Projection = ((x * 1 + y * 1 + z * 1) / (sqrt(3)²)) * coord_sys.i + coord_sys.j + coord_sys.k │
│                                                                                               │
│ 3. Final Result:                                                                              │
│ (x/3 + y/3 + z/3)*coord_sys.i + (x/3 + y/3 + z/3)*coord_sys.j + (x/3 + y/3 + z/3)*coord_sys.k │
│                                                                                               │
│ 4. No Numerical Value Available                                                               │
│                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## 4. Single Vector Operations (Length & Unit)

**Command executed:**
`python3 main.py vector-operation "[3,4,0]" length`

**Output:**
```text
╭─ Vector Operation Result ─╮
│ Result of length: 5.0     │
╰───────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" length --show-steps`

**Output:**
```text
╭─ Vector Operation (Step-by-Step) ─╮
│ 1. General Formula (length):      │
│ √(x² + y² + z²)                   │
│                                   │
│ 2. Component Substitution:        │
│ √((x)² + (y)² + (z)²)             │
│                                   │
│ 3. Final Result:                  │
│ sqrt(x**2 + y**2 + z**2)          │
│                                   │
│ 4. No Numerical Value Available   │
│                                   │
╰───────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[3,4,0]" unit`

**Output:**
```text
╭───────────── Vector Operation Result ─────────────╮
│ Result of unit: 0.6*coord_sys.i + 0.8*coord_sys.j │
╰───────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" unit --show-steps`

**Output:**
```text
╭─────────────────────────────────────────────── Vector Operation (Step-by-Step) ────────────────────────────────────────────────╮
│ 1. General Formula (unit):                                                                                                     │
│ Unit Vector = A / |A|                                                                                                          │
│                                                                                                                                │
│ 2. Component Substitution:                                                                                                     │
│ Unit Vector = x*coord_sys.i + y*coord_sys.j + z*coord_sys.k / sqrt(x**2 + y**2 + z**2)                                         │
│                                                                                                                                │
│ 3. Final Result:                                                                                                               │
│ (x/sqrt(x**2 + y**2 + z**2))*coord_sys.i + (y/sqrt(x**2 + y**2 + z**2))*coord_sys.j + (z/sqrt(x**2 + y**2 + z**2))*coord_sys.k │
│                                                                                                                                │
│ 4. No Numerical Value Available                                                                                                │
│                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

## 5. Vector & Scalar Operations (Scaling)

**Command executed:**
`python3 main.py vector-operation "[3,-2,1]" multiply "x*y*z"`

**Output:**
```text
╭──────────────────────────────── Vector Operation Result ─────────────────────────────────╮
│ Result of multiply: 3.0*x*y*z*coord_sys.i + (-2.0*x*y*z)*coord_sys.j + x*y*z*coord_sys.k │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[2,4,6]" divide "2"`

**Output:**
```text
╭─────────────────────── Vector Operation Result ───────────────────────╮
│ Result of divide: 1.0*coord_sys.i + 2.0*coord_sys.j + 3.0*coord_sys.k │
╰───────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x**2, y**2, z**2]" multiply "1/x" --show-steps`

**Output:**
```text
╭────────────────────────── Vector Operation Result ──────────────────────────╮
│ Result of multiply: x*coord_sys.i + y**2/x*coord_sys.j + z**2/x*coord_sys.k │
╰─────────────────────────────────────────────────────────────────────────────╯
```

---

## 6. Pure Scalar Operations

**Command executed:**
`python3 main.py vector-operation "x**2" add "2*x"`

**Output:**
```text
╭── Vector Operation Result ──╮
│ Result of add: x**2 + 2.0*x │
╰─────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "x+1" multiply "x-1" --show-steps`

**Output:**
```text
╭──────── Vector Operation Result ────────╮
│ Result of multiply: (x - 1.0)*(x + 1.0) │
╰─────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "10" divide "2"`

**Output:**
```text
╭─ Vector Operation Result ─╮
│ Result of divide: 5.0     │
╰───────────────────────────╯
```

---

## 7. Safety Catches & Mathematical Errors

**Command executed:**
`python3 main.py vector-operation "[2,3,4]" add "5"`

**Output:**
```text
╭─────────────────────────────── Error ────────────────────────────────╮
│ Error performing vector operation: 5 cannot be interpreted correctly │
╰──────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "x" subtract "[1,2,3]"`

**Output:**
```text
╭─────────────────────────────── Error ────────────────────────────────╮
│ Error performing vector operation: x cannot be interpreted correctly │
╰──────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" dot "x"`

**Output:**
```text
╭─────────────────────────────────────────────────── Error ───────────────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: The dot product is only defined between two vectors. │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "5" cross "[1,2,3]"`

**Output:**
```text
╭──────────────────────────────────────────────────── Error ────────────────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: The cross product is only defined between two vectors. │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "5" length`

**Output:**
```text
╭─────────────────────────────────────────── Error ───────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: Length is only defined for a vector. │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "x" unit`

**Output:**
```text
╭───────────────────────────────────────────── Error ──────────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: Unit vector is only defined for a vector. │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[0,0,0]" unit`

**Output:**
```text
╭────────────────────────────────────────────────── Error ──────────────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: Unit vector is only defined for a non-zero vector. │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[1,2,3]" projection "[0,0,0]"`

**Output:**
```text
╭────────────────────────────────────────── Error ──────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: Cannot project onto a zero vector. │
╰───────────────────────────────────────────────────────────────────────────────────────────╯
```

---

