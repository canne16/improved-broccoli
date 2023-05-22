dict =
{
  ['+s'] = {"ADD ", " Y ", 0.1},
}

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
      return "add 0 vy 1"
    end
    if C == "+w" then
      return "add 0 vy -1"
    end
    if C == "+a" then
      return "add 0 vx -1"
    end
    if C == "+d" then
      return "add 0 vx 1"
    end
  end
  if index == 1 then
    if C == "+s" then
      return "add 1 vy 1"
    end
    if C == "+w" then
      return "add 1 vy -1"
    end
    if C == "+a" then
      return "add 1 vx -1"
    end
    if C == "+d" then
      return "add 1 vx 1"
    end
  end
end

function tick()
  return "max 0 x 400\n"..
  "min 1 x 1520"
end