-- 用户自定义区
local kPixelMaxX = 1920 * 2
local kPixelMaxY = 1080
local pixel_in_world_map = {
    ["snow_land"] = {pixel_x = 100, pixel_y = 200},
    ["jian_zhong"] = {pixel_x = 200, pixel_y = 300}
}
-- local pos = pixel_in_world_map["长安城"]
-- OutputLogMessage("长安城坐标: x=%d, y=%d\n", pos.x, pos.y)


-- Enable event reporting for mouse button 1
EnablePrimaryMouseButtonEvents(true)


-- 回点相关的函数
-- 地府回洛阳
-- function hellToLuoYang() 
--     -- 点击孟婆
--     local x = 0
--     local y = 0
--     x, y = pixelToMouseXY()

-- end

function pixelToMouseXY(pixel_x, pixel_y)
    -- 转换公式：
    -- mouse_x = (pixel_x / 屏幕宽度) * 65535
    -- mouse_y = (pixel_y / 屏幕高度) * 65535
    local mouse_x = math.floor((pixel_x / kPixelMaxX) * 65535)
    local mouse_y = math.floor((pixel_y / kPixelMaxY) * 65535)
    OutputLogMessage("mouse_x = %d, mouse_y = %d\n", mouse_x, mouse_y)
    return mouse_x, mouse_y
end

function mouseLeftClicked(pixel_x, pixel_y)
    local x, y = pixelToMouseXY(pixel_x, pixel_y)
    MoveMouseTo(x, y)
    PressAndReleaseMouseButton(1)
end


function Run()
    -- 按下并释放Q键
    OutputLogMessage("Run() is called\n")
    PressAndReleaseKey("q")
    Sleep(math.random(200, 300))  
    -- 按下并释放W键
    PressAndReleaseKey("w")
    -- 添加一个小延迟，避免按键太快
    Sleep(math.random(1000, 1500))
end

-- 主事件处理函数
function OnEvent(event, arg)
    -- 调试日志
    OutputLogMessage("Event: %s, arg: %s\n", event, tostring(arg))
    if (event == "MOUSE_BUTTON_PRESSED" and arg == 5) then
        mouseLeftClicked(800, 400)
        mouseLeftClicked(800, 500)
        mouseLeftClicked(800, 600)
    end
end