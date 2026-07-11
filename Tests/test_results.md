Test Run Timestamp: 2026-07-12 02:04:41

# Calc 3 CLI - Vector Operation Test Results

> Automated test run to verify mathematical accuracy and safety catches.

## 1. Vector & Vector Operations (Constants & Algebraic)

**Command executed:**
`python3 main.py vector-operation "[2,3,4]" "[4,5,6]" "add"`

**Output:**
```text
╭──────────── Vector Operation Result ────────────╮
│ Result of add operation: 6*N.i + 8*N.j + 10*N.k │
╰─────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" "[1,1,1]" "subtract"`

**Output:**
```text
╭─────────────────────── Vector Operation Result ───────────────────────╮
│ Result of subtract operation: (x - 1)*N.i + (y - 1)*N.j + (z - 1)*N.k │
╰───────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" "[1,2,3]" "dot"`

**Output:**
```text
╭─────── Vector Operation Result ────────╮
│ Result of dot operation: x + 2*y + 3*z │
╰────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[1,0,0]" "[0,1,0]" "cross"`

**Output:**
```text
╭─── Vector Operation Result ────╮
│ Result of cross operation: N.k │
╰────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" "[x,y,z]" "cross"`

**Output:**
```text
╭── Vector Operation Result ───╮
│ Result of cross operation: 0 │
╰──────────────────────────────╯
```

---

## 2. Vector & Scalar Operations (Scaling)

**Command executed:**
`python3 main.py vector-operation "[3,-2,1]" "x*y*z" "multiply"`

**Output:**
```text
╭─────────────────────── Vector Operation Result ────────────────────────╮
│ Result of multiply operation: 3*x*y*z*N.i + (-2*x*y*z)*N.j + x*y*z*N.k │
╰────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[2,4,6]" "2" "divide"`

**Output:**
```text
╭──────────── Vector Operation Result ────────────╮
│ Result of divide operation: N.i + 2*N.j + 3*N.k │
╰─────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x**2, y**2, z**2]" "1/x" "multiply"`

**Output:**
```text
╭─────────────────── Vector Operation Result ───────────────────╮
│ Result of multiply operation: x*N.i + y**2/x*N.j + z**2/x*N.k │
╰───────────────────────────────────────────────────────────────╯
```

---

## 3. Pure Scalar Operations

**Command executed:**
`python3 main.py vector-operation "x**2" "2*x" "add"`

**Output:**
```text
╭────── Vector Operation Result ──────╮
│ Result of add operation: x**2 + 2*x │
╰─────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "x+1" "x-1" "multiply"`

**Output:**
```text
╭─────────── Vector Operation Result ───────────╮
│ Result of multiply operation: (x - 1)*(x + 1) │
╰───────────────────────────────────────────────╯
```

---

## 4. The Safety Catch Tests (Expecting Errors)

**Command executed:**
`python3 main.py vector-operation "[2,3,4]" "5" "add"`

**Output:**
```text
╭─────────────────────────────── Error ────────────────────────────────╮
│ Error performing vector operation: 5 cannot be interpreted correctly │
╰──────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "x" "[1,2,3]" "subtract"`

**Output:**
```text
╭─────────────────────────────── Error ────────────────────────────────╮
│ Error performing vector operation: x cannot be interpreted correctly │
╰──────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "[x,y,z]" "x" "dot"`

**Output:**
```text
╭─────────────────────────────────────────────────── Error ───────────────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: The dot product is only defined between two vectors. │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

**Command executed:**
`python3 main.py vector-operation "5" "[1,2,3]" "cross"`

**Output:**
```text
╭──────────────────────────────────────────────────── Error ────────────────────────────────────────────────────╮
│ Error performing vector operation: Mathematical Error: The cross product is only defined between two vectors. │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

---

