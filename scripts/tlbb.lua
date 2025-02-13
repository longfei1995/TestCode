-- 用户自定义区
local kRideHorseKey = "f8"                              -- 上坐骑快捷键
local kOpenGlobalMapKey = "m"                           -- 打开全局地图
local kLocalMapPosition = {x = 161, 148}                -- 银铠雪原161, 148坐标
local kTime = 20                                        -- 洛阳到雪原的时间，unit:s
local kLocalTime = 10                                   -- 到达雪原中央后，到指定坐标的时间，unit:s
-- 坐标定义（基于logitech坐标原点），请勿更改。
local kPosInGlobalMap = {x = 32870, y = 10604}          -- 银铠雪原在世界地图坐标
local kAutoFindButton = {x = 63948, y = 11150}          -- 自动寻路按钮
local kAutoFindLeftDiagBox = {x = 63052, y = 23893}     -- 自动寻路左对话框
local kAutoFindRightDiagBox = {x = 63820, y = 23893}    -- 自动寻路右对话框
local kAutoFindMoveButton = {x = 64793, y = 23893}      -- 移动按钮
local kHellMengPo = {x = 62258, y = 16429}              -- 自动寻路后地府中孟婆文字坐标
local kHellLuoYang = {x = 1664, y = 13562}              -- 点击孟婆后的洛阳坐标
local kMoveMapEnter = {x = 34303, y = 36408}            -- 是否开启跨场景的确认键
local kScreenMid = {x = 32767, 32767}                   -- 屏幕中央
local kAutoFightButton = {x = 65125, y = 6827}          -- 自动战斗按钮
-- Enable event reporting for mouse button 1
EnablePrimaryMouseButtonEvents(true)
-- 添加全局变量
local is_running = false
local last_run_time = 0
local interval = 30 * 60 * 1000  -- 30分钟转换为毫秒

-- 鼠标单击
function moveAndSingleClicked(logi_x, logi_y)
    MoveMouseTo(logi_x, logi_y)
    OutputLogMessage("Mouse is at %d, %d, and single clicked.\n", logi_x, logi_y)
    PressAndReleaseMouseButton(1)
    Sleep(math.random(100, 200))
end

-- 鼠标双击
function moveAndDoubleClicked(logi_x, logi_y)
    MoveMouseTo(logi_x, logi_y)
    OutputLogMessage("Mouse is at %d, %d, and double clicked.\n", logi_x, logi_y)
    PressAndReleaseMouseButton(1)
    Sleep(math.random(20, 50))
    PressAndReleaseMouseButton(1)
    Sleep(math.random(100, 200))
end

-- 输入坐标值
function typeNumber(number)
    local number_string = tostring(number)
    for i = 1, #number_string do
        local digit = number_string:sub(i, i)
        PressAndReleaseKey(digit)
        Sleep(math.random(50, 100))
    end
end

-- 到达当前场景的指定坐标
function goGamePos(game_x, game_y) 
    -- 单击自动寻路 && 等待0.8-1.2s
    moveAndSingleClicked(kAutoFindButton.x, kAutoFindButton.y)
    Sleep(math.random(800, 1200))
    -- 单击左侧框，输入x坐标
    moveAndSingleClicked(kAutoFindLeftDiagBox.x, kAutoFindLeftDiagBox.y)
    typeNumber(game_x)
    -- 单击右侧框，输入Y坐标
    moveAndSingleClicked(kAutoFindRightDiagBox.x, kAutoFindRightDiagBox.y)
    typeNumber(game_y)
    -- 点击移动按钮
    moveAndSingleClicked(kAutoFindMoveButton.x, kAutoFindMoveButton.y)
end

-- 到达全局地图坐标
function goGlobalMapPos(time, local_time)
    OutputLogMessage("开始执行 goGlobalMapPos\n")
    -- 上坐骑，需要读条，等待一下
    PressAndReleaseKey(kRideHorseKey)
    OutputLogMessage("上坐骑完成\n")
    Sleep(math.random(1500, 1700))
    
    -- 打开世界地图
    PressAndReleaseKey(kOpenGlobalMapKey)
    OutputLogMessage("打开世界地图完成\n")
    Sleep(math.random(200, 300))
    
    -- 选择对应的地图,点击屏幕中央
    moveAndSingleClicked(kPosInGlobalMap.x, kPosInGlobalMap.y)
    OutputLogMessage("选择目标地图完成\n")
    Sleep(math.random(1500, 1700))
    moveAndSingleClicked(kScreenMid.x, kScreenMid.y)
    Sleep(math.random(200, 300))
    
    -- 处理自动寻路确定弹窗
    moveAndSingleClicked(kMoveMapEnter.x, kMoveMapEnter.y)
    OutputLogMessage("确认跨场景寻路完成，等待 %d 秒到达目的地\n", time + 2)
    -- 休眠标定的时间
    Sleep(math.random((time + 2) * 1000, (time + 3) * 1000))
    
    -- 到达局部场景地图了，寻路到指定坐标
    OutputLogMessage("开始在当前场景寻路到指定坐标\n")
    goGamePos(kLocalMapPosition.x, kLocalMapPosition.y)
    OutputLogMessage("等待 %d 秒到达指定坐标\n", local_time + 2)
    Sleep(math.random((local_time + 2) * 1000, (local_time + 3) * 1000))
    
    -- 下坐骑，需要读条，等待一下
    PressAndReleaseKey(kRideHorseKey)
    OutputLogMessage("下坐骑完成\n")
    Sleep(math.random(1500, 1700))
    
    -- 点击自动战斗
    moveAndSingleClicked(kAutoFightButton.x, kAutoFightButton.y)
    OutputLogMessage("开启自动战斗完成\n")
end

-- 出地府去洛阳
function escapeHellToLuoYang()
    OutputLogMessage("开始执行 escapeHellToLuoYang\n")
    
    -- 单击自动寻路 && 等待0.5 - 1s
    moveAndSingleClicked(kAutoFindButton.x, kAutoFindButton.y)
    OutputLogMessage("点击自动寻路完成\n")
    Sleep(math.random(500, 1000))
    
    -- 单击孟婆 && 单击移动
    moveAndDoubleClicked(kHellMengPo.x, kHellMengPo.y)
    OutputLogMessage("点击孟婆完成\n")
    moveAndSingleClicked(kAutoFindMoveButton.x, kAutoFindMoveButton.y)
    OutputLogMessage("点击移动按钮完成\n")
    
    -- 等待左侧对话框弹出 && 点击洛阳
    Sleep(math.random(5000, 6000))
    moveAndDoubleClicked(kHellLuoYang.x, kHellLuoYang.y)
    OutputLogMessage("点击洛阳完成\n")
end


-- 主事件处理函数（修改部分）
function OnEvent(event, arg)
    -- 只处理鼠标按钮事件
    if event == "MOUSE_BUTTON_PRESSED" then
        OutputLogMessage("Event: %s, arg: %d\n", event, arg)
        
        -- 只在按下按钮5时切换运行状态
        if arg == 5 then
            is_running = not is_running
            OutputLogMessage("Script is_running = %s\n", tostring(is_running))
            -- 如果启动，记录时间
            if is_running then
                last_run_time = GetRunningTime()
                -- 立即执行第一次任务
                OutputLogMessage("开始新一轮循环\n")
                escapeHellToLuoYang()
                goGlobalMapPos(kTime, kLocalTime)
            end
        -- 只在脚本运行状态下检查时间间隔
        elseif is_running then
            local current_time = GetRunningTime()
            if current_time - last_run_time >= interval then
                OutputLogMessage("开始新一轮循环\n")
                escapeHellToLuoYang()
                goGlobalMapPos(kTime, kLocalTime)
                last_run_time = current_time
            end
        end
    end
end

