dict =
{
  ['w'] = {"ADD ", " y ", 50},
  ['a'] = {"ADD ", " x ", -50},
  ['s'] = {"ADD ", " y ", -50},
  ['d'] = {"ADD ", " x ", 50},
  ['o'] = {"ADD ", " m ", 10},
  ['p'] = {"ADD ", " m ", -10}

}

function translate(index, com)
    C = com:sub(2)
    sign = ''
    if com:sub(1,1) == '-' then
        sign = '-'
    end
    return dict[C][1]..math.floor(index)..dict[C][2]..sign..dict[C][3]
end