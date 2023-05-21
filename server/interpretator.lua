dict =
{
  ['+w'] = {"ADD ", " Y ", -0.1},
  ['-w'] = {"ADD ", " Y ", 0},
  ['+a'] = {"ADD ", " X ", -0.1},
  ['-a'] = {"ADD ", " X ", 0},
  ['+s'] = {"ADD ", " Y ", 0.1},
  ['-s'] = {"ADD ", " Y ", 0},
  ['+d'] = {"ADD ", " X ", 0.1},  
  ['-d'] = {"ADD ", " X ", 0},
  ['+o'] = {"ADD ", " m ", 10},
  ['-o'] = {"ADD ", " m ", 0},
  ['+p'] = {"ADD ", " m ", -10},
  ['-p'] = {"ADD ", " m ", 0}

}

function translate(index, C)
    return dict[C][1]..math.floor(index)..dict[C][2]..dict[C][3]
end