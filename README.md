# Traffic System

## Grid Shape (m, n)

The grid is structured as follows:

- `m` represents the number of columns (indexed by `j`)
- `n` represents the number of rows (indexed by `i`)

## Matrix Representation

Here is a visual representation of the matrix:

|       | **j = 0** | **j = 1** | **...** | **j = m-1** |
|-------|:---------:|:---------:|:-------:|:-----------:|
| **i = 0** | (0, 0)   | (0, 1)   | ...     | (0, m-1)     |
| **i = 1** | (1, 0)   | (1, 1)   | ...     | (1, m-1)     |
| **...**   | ...      | ...      | ...     | ...          |
| **i = n-1** | (n-1, 0) | (n-1, 1) | ...     | (n-1, m-1)   |

- Each cell `(i, j)` in the table corresponds to the grid coordinates.
- The top-left corner of the grid is `(0, 0)`, and the bottom-right corner is `(n-1, m-1)`.
