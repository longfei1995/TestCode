local TOGGLE_BUTTON = 5
local isEnable = false

-- Run函数
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
    
    -- 只处理鼠标按键事件
    if event == "MOUSE_BUTTON_PRESSED" then
        -- 如果是G5键被按下
        if arg == TOGGLE_BUTTON then
            -- 切换运行状态
            isEnable = not isEnable
            
            if isEnable then
                OutputLogMessage("脚本已【开启】- 开始循环按QW\n")
                SetMKeyState(1, "kb")
            else
                OutputLogMessage("脚本已【停止】\n")
                SetMKeyState(0, "kb")
            end
        end
    end
    
    -- 当收到M键事件且脚本启用时，继续执行Run
    if event == "M_PRESSED" then
        if "M_PRESSED" == 1 then
            Run()
        elseif "M_PRESSED" == 2 then
            OutputLogMessage("脚本已【停止】\n")
        end
    end

end