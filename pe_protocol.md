# Request
`get_changes`

# Answer
`nodes: [fig, n, x, y, vx, vy], [fig, n, x, y, vx, vy]...`
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
`move_abs: [fig, x, y, angle]`
`move_rel: [fig, x, y, angle]`
`add_vel_centre: [fig, vx, vy]`
`set_vel_centre: [fig, vx, vy]`
`set_force_centre: [fig, fx, fy, duration (-1 for infinity)]`
`set_force_node: [fig, n, fx, fy, duration (-1 for infinity)]`
`add_force_centre: [fig, fx, fy, duration (-1 for infinity)]`
`add_force_node: [fig, n, fx, fy, duration (-1 for infinity)]`
