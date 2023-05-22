dict =
{
  ['+w'] = {"set ", " Y ", -0.001},
  ['-w'] = {"set ", " Y ", 0},
  ['+a'] = {"set ", " X ", -0.001},
  ['-a'] = {"set ", " X ", 0},
  ['+s'] = {"set ", " Y ", 0.001},
  ['-s'] = {"set ", " Y ", 0},
  ['+d'] = {"set ", " X ", 0.001},  
  ['-d'] = {"set ", " X ", 0},
  ['+o'] = {"add ", " m ", 10},
  ['-o'] = {"add ", " m ", 0},
  ['+p'] = {"add ", " m ", -10},
  ['-p'] = {"add ", " m ", 0}

}

function translate(index, C)
    return dict[C][1]..math.floor(index)..dict[C][2]..dict[C][3]
end