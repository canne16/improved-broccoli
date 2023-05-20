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
  ['+o'] = {"SET ", " m ", 10},
  ['-o'] = {"SET ", " m ", 10},
  ['+p'] = {"SET ", " m ", -10},
  ['-p'] = {"SET ", " m ", -10}

}

function translate(index, C)
    return dict[C][1]..math.floor(index)..dict[C][2]..dict[C][3]
end