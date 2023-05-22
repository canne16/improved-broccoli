w0 = 0
a0 = 0
s0 = 0
d0 = 0
w1 = 0
a1 = 0
s1 = 0
d1 = 0

width = 800
height = 400

function set_pos()
  return "begin\n"..
  "set_collision_c_s 2 0\n"..
  "add_circle 30 15 "..tostring(100 - width / 2).." 0 0 0\n"..
  "add_circle 30 15 "..tostring(width / 2 - 100).." 0 0 0\n"..
  "add_circle 10 1 0 0 0 0\n"..
  "add_section 0 "..tostring(0+height / 2).." 0 "..tostring(0-height / 2).."\n"..
  "add_section "..tostring(0+width / 2).." "..tostring(0+height / 2).." "..tostring(0+width / 2).." "..tostring(0-height / 2).."\n"..
  "add_section "..tostring(0+width / 2).." "..tostring(0+height / 2).." "..tostring(0-width / 2).." "..tostring(0+height / 2).."\n"..
  "add_section "..tostring(0-width / 2).." "..tostring(0-height / 2).." "..tostring(0+width / 2).." "..tostring(0-height / 2).."\n"..
  "add_section "..tostring(0-width / 2).." "..tostring(0-height / 2).." "..tostring(0-width / 2).." "..tostring(0+height / 2).."\n"..
  "set_collision_c_s 2 0\n"..
  "end"
end

function translate(index, C)
  if index == 0 then
    if C == "+s" then
      s0 = 1
    end
    if C == "+w" then
      w0 = 1
    end
    if C == "+a" then
      a0 = 1
    end
    if C == "+d" then
      d0 = 1
    end
    if C == "-s" then
      s0 = 0
    end
    if C == "-w" then
      w0 = 0
    end
    if C == "-a" then
      a0 = 0
    end
    if C == "-d" then
      d0 = 0
    end
  end
  if index == 1 then
    if C == "+s" then
      s1 = 1
    end
    if C == "+w" then
      w1 = 1
    end
    if C == "+a" then
      a1 = 1
    end
    if C == "+d" then
      d1 = 1
    end
    if C == "-s" then
      s1 = 0
    end
    if C == "-w" then
      w1 = 0
    end
    if C == "-a" then
      a1 = 0
    end
    if C == "-d" then
      d1 = 0
    end
  end
end

function tick()
  res = "add 0 v -0.01\n"..
        "add 1 v -0.01\n"..
        "add 2 v -0.01\n"
  --res = ""
  dv = "0.05"

  if s0 == 1 then
    res = res..
    "add 0 vy "..dv.."\n"..
    "max 0 v 30\n"
  end
  if w0 == 1 then
    res = res.."add 0 vy -"..dv.."\n"..
    "max 0 v 30\n"
  end
  if a0 == 1 then
    res = res.."add 0 vx -"..dv.."\n"..
    "max 0 v 30\n"
  end
  if d0 == 1 then
    res = res.."add 0 vx "..dv.."\n"..
    "max 0 v 30\n"
  end
  if s1 == 1 then
    res = res.."add 1 vy "..dv.."\n"..
    "max 1 v 30\n"
  end
  if w1 == 1 then
    res = res.."add 1 vy -"..dv.."\n"..
    "max 1 v 30\n"
  end
  if a1 == 1 then
    res = res.."add 1 vx -"..dv.."\n"..
    "max 1 v 30\n"
  end
  if d1 == 1 then
    res = res.."add 1 vx "..dv.."\n"..
    "max 1 v 30\n"
  end

  return res
end