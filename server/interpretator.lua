dict =
{
  ['+w'] = {"add ", " Y ", -0.002},
  ['-w'] = {"add ", " Y ", 0.002},
  ['+a'] = {"add ", " X ", -0.002},
  ['-a'] = {"add ", " X ", 0.002},
  ['+s'] = {"add ", " Y ", 0.002},
  ['-s'] = {"add ", " Y ", -0.002},
  ['+d'] = {"add ", " X ", 0.002},  
  ['-d'] = {"add ", " X ", -0.002},
  ['+o'] = {"add ", " m ", 10},
  ['-o'] = {"add ", " m ", 0},
  ['+p'] = {"add ", " m ", -10},
  ['-p'] = {"add ", " m ", 0}

}

function translate(index, C)
    return dict[C][1]..math.floor(index)..dict[C][2]..dict[C][3]
end