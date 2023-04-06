# Initial request
method: get
request: "initial"

answer:
{
    watching_keys: ["w", "a", "s", "d", "lmb", "rmb", "m_pos"],
    figure_number: (int) // Number of connected figure
}

# Get position
method: get
request: "get_pos"

answer:
{
    circles: [{x: (float), y: (float), r: (float)}, ...],
    polygons:
    [
        {
            nodes: [{x: (float), y: (float), vx: (float), vy: (float)}, ...],
            edges: [{n1: (int), n2: (int)}, ...]
        },
        ...
    ]
}

# Update_position
method: get
request: "update_pos"

answer:
{
    circles: [{dx: (float), dy: (float), dr: (float)}, ...],
    polygons:
    [
        {
            nodes: [{dx: (float), dy: (float), vx: (float), vy: (float)}, ...],
            new_edges: [{n1: (int), n2: (int)}, ...],
            del_edges: [{n1: (int), n2: (int)}, ...],
            direction: (float) // In radiand I think
        },
        ...
    ]
}

# Send_btns
method: post

request:
{
    keys: [
        {
            key: "A",
            duration: (float) // if less than delta \approx 0.3s, else -1
        },
        ...
    ]
    mouse: 
    {
        delta_x: (float),
        delta_y: (float)
    }
}