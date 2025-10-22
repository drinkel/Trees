# 🧪 Research on Merkle Tree Properties

This project is dedicated to the experimental analysis of the efficiency of three types of Merkle trees. The implementation is done in **Python**.

## 🔍 Goal

- Implement:
  - ✅ Binary Merkle Tree (BMT)
  - ✅ Sparse Merkle Tree (SMT)
  - ✅ Indexed Merkle Tree (IMT)
- Insert `2^16 = 65,536` random elements into each tree
- Perform benchmarks for:
  - Adding a new element
  - Generating a Membership Proof (MP)
  - Verifying an MP
  - Measuring MP size
  - Generating an Exclusion Proof (EP)
  - Verifying an EP
  - Measuring EP size

---

## 🌳 Algorithm Descriptions

### 1. Binary Merkle Tree (BMT)

A binary tree where each internal node is a hash of the concatenation of its children's hashes. It is a balanced tree with a height of `log₂(n)`.

**Features:**
- Membership proof — a path of `log₂(n)` hashes  
- Adding a new element: full rebuild or incremental insertion (for dynamic BMT)

---

### 2. Sparse Merkle Tree (SMT)

A tree with a fixed depth (e.g., 256), where each possible key position has a unique place in the tree. It is used in scenarios with long keys or when only a small number of elements occupy a large key space.

**Features:**
- Efficient inclusion/exclusion proofs of equal length  
- Uninitialized nodes share the same value (zero hash)

---

### 3. Indexed Merkle Tree (IMT)

A binary Merkle tree where each element has an index, ensuring a deterministic tree structure and allowing fast index-based access.

**Features:**
- Efficient addressing  
- Support for positional proofs

---

## 🧠 Function Pseudocode

The pseudocode uses simplified structures to illustrate the logic.
