w0 = 0
a0 = 0
s0 = 0
d0 = 0
w1 = 0
a1 = 0
s1 = 0
d1 = 0


function set_pos()
  return "begin\n"..
  "add_circle 60 10 100 540 0 0\n"..
  "add_circle 60 10 1820 540 0 0\n"..
  "add_circle 30 1 960 540 10 5\n"..
  "add_section 0 0 0 1080\n"..
  "add_section 0 0 1920 0\n"..
  "add_section 1920 1080 0 1080\n"..
  "add_section 1920 1080 1920 0\n"..
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
  res = "max 0 x 400\n"..
  "min 1 x 1520"
  dv = "0.5"

  if s0 == 1 then
    res = res.."add 0 vy "..dv.."\n"..
    "max 0 v 10"
  end
  if w0 == 1 then
    res = res.."add 0 vy -"..dv.."\n"..
    "max 0 v 10"
  end
  if a0 == 1 then
    res = res.."add 0 vx -"..dv.."\n"..
    "max 0 v 10"
  end
  if d0 == 1 then
    res = res.."add 0 vx "..dv.."\n"..
    "max 0 v 10"
  end
  if s1 == 1 then
    res = res.."add 1 vy "..dv.."\n"..
    "max 1 v 10"
  end
  if w1 == 1 then
    res = res.."add 1 vy -"..dv.."\n"..
    "max 1 v 10"
  end
  if a1 == 1 then
    res = res.."add 1 vx -"..dv.."\n"..
    "max 1 v 10"
  end
  if d1 == 1 then
    res = res.."add 1 vx "..dv.."\n"..
    "max 1 v 10"
  end

  return res
end