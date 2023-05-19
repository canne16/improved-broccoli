# Request
`get_changes`

# Answer
`circles n`
    `[...]`
    `fig, n, x, y, vx, vy`
    `...`
`new_edges: [fig, n1, n2], [fig, n1, n2]...`
`del_edges: [fig, n1, n2], [fig, n1, n2]...`

# Request
`get_new`

# Answer
`nodes: [fig, n, x, y, vx, vy], [fig, n, x, y, vx, vy]...`
`edges: [fig, n1, n2], [fig, n1, n2]...`

# Request
`new_node: [fig]`
`new_edge: [fig, n1, n2]`
`del_node: [fig, n]`
`del_edge: [fig, n1, n2]`

# Answer
`ok (n of new node) / err (no such ... / already exists)` Do we need this?

# Request
`beg`
`add i [x, y, r, vx, vy, m] (double)`
`set i [x, y, r, vx, vy, m] (double)`
`end`

# Answer
