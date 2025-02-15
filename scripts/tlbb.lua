-- 说明
-- 1. 适用范围：罗技G502测试通过
-- 2. 使用方法：
--      2.1 以管理员身份运行罗技G HUB
--      2.2 按下罗技鼠标G5键即可启动脚本
--      2.3 使用过程中切勿将windows锁屏、挂后台、开向日葵（会挤占按键）
-- 3. 其他说明：
--      3.1 仅供交流学习，切勿用于其他用途，切勿随意传播，尊重他人劳动成果
--      3.2 除用户定义区外的内容，勿随意更改，免得脚本报错
--      3.3 lua脚本没有opencv等库，无法做到事件触发，而是定时触发，所以有点呆。好处在于
--          较为稳定（模拟鼠标和键盘的操作，较难检测）
--      3.4 如果封号了，后果自负
-- 用户自定义区
local kRideHorseKey = "f8"                              -- 上坐骑快捷键
local kOpenGlobalMapKey = "m"                           -- 打开全局地图
-- local kLocalMapPosition = {x = 89, y = 66}              -- 银铠雪原局部坐标
local kLocalMapPosition = {x = 172, y = 185}            -- 银铠雪原9孔
local kScreenResolution = {x = 2560, y = 1440}          -- 屏幕分辨率
local kTime = 60 * 3.5                                  -- 洛阳到雪原的时间，unit:s
-- local kTime = 1                                      -- 洛阳到雪原的时间，unit:s
local kTime2 = 40                                       -- 雪原地图入口到指定坐标（上述的kLocalMapPosition）的时间
-- 坐标定义（基于logitech坐标原点），请勿更改。
local kPosInGlobalMap = {x = 33381, y = 11605}          -- 银铠雪原在世界地图坐标
local kPosLiaoXi = {x = 23833, y = 48969}
local kAutoFindButton = {x = 63948, y = 11150}          -- 自动寻路按钮
local kAutoFindLeftDiagBox = {x = 63052, y = 23893}     -- 自动寻路左对话框
local kAutoFindRightDiagBox = {x = 63820, y = 23893}    -- 自动寻路右对话框
local kAutoFindMoveButton = {x = 64793, y = 23893}      -- 移动按钮
local kHellMengPo = {x = 27289, y = 14700}              -- 地府中孟婆坐标
local kHellLuoYang = {x = 1664, y = 13562}              -- 点击孟婆后的洛阳坐标
local kMoveMapEnter = {x = 34303, y = 36408}            -- 是否开启跨场景的确认键
local kAutoFightButton = {x = 65125, y = 6827}          -- 自动战斗按钮

-- Enable event reporting for mouse button 1
EnablePrimaryMouseButtonEvents(true)

-- 鼠标单击
function moveAndSingleClicked(logi_x, logi_y)
    MoveMouseTo(logi_x, logi_y)
    OutputLogMessage("Mouse is at %d, %d, and single clicked.\n", logi_x, logi_y)
    PressMouseButton(1)
    Sleep(100)
    ReleaseMouseButton(1)
end

-- 鼠标双击
function moveAndDoubleClicked(logi_x, logi_y)
    MoveMouseTo(logi_x, logi_y)
    OutputLogMessage("Mouse is at %d, %d, and double clicked.\n", logi_x, logi_y)
    PressMouseButton(1)
    Sleep(100)
    ReleaseMouseButton(1)
    Sleep(50)
    PressMouseButton(1)
    Sleep(100)
    ReleaseMouseButton(1)
end

function pressKey(key)
    PressKey(key)
    Sleep(math.random(100, 200))
    ReleaseKey(key)
end

-- 屏幕分辨率转成罗技坐标
function screenResolutionToLogi(pixel_x, pixel_y)
    -- 使用 math.floor 取整
    local x = math.floor(pixel_x / kScreenResolution.x * 65535)
    local y = math.floor(pixel_y / kScreenResolution.y * 65535)
    -- 确保坐标在有效范围内
    x = math.min(math.max(x, 0), 65535)
    y = math.min(math.max(y, 0), 65535)
    return x, y
end

-- 天龙坐标转成屏幕分辨率坐标
function gameCoordToScreenResolution(game_x, game_y)
    OutputLogMessage("gameCoordToScreenResolution 输入坐标: %d, %d\n", game_x, game_y)
    
    -- 确保输入的游戏坐标在有效范围内
    if game_x < 0 or game_x > 255 or game_y < 0 or game_y > 255 then
        OutputLogMessage("错误：游戏坐标超出范围(0-255)\n")
        return nil, nil
    end
    
    -- 转换为像素坐标
    local x = math.floor(game_x / 255 * 1024 + 696)
    local y = math.floor(game_y / 255 * 1024 + 208)
    
    OutputLogMessage("gameCoordToScreenResolution 输出像素坐标: %d, %d\n", x, y)
    return x, y
end

-- 输入坐标值
function typeNumber(number)
    local number_string = tostring(number)
    for i = 1, #number_string do
        local digit = number_string:sub(i, i)
        pressKey(digit)
        Sleep(math.random(50, 100))
    end
end

-- 到达当前场景的指定坐标
function goGamePos(game_x, game_y) 
    OutputLogMessage("\n=== goGamePos开始执行 ===\n")
    
    -- 检查输入参数
    if not game_x or not game_y then
        OutputLogMessage("错误：无效的输入坐标\n")
        return false
    end
    
    -- 转换坐标
    local pixel_x, pixel_y = gameCoordToScreenResolution(game_x, game_y)
    if not pixel_x or not pixel_y then
        OutputLogMessage("错误：坐标转换失败\n")
        return false
    end
    
    local logi_x, logi_y = screenResolutionToLogi(pixel_x, pixel_y)
    
    -- 打印所有坐标信息
    OutputLogMessage("游戏坐标: %d, %d\n", game_x, game_y)
    OutputLogMessage("像素坐标: %d, %d\n", pixel_x, pixel_y)
    OutputLogMessage("罗技坐标: %d, %d\n", logi_x, logi_y)
    
    -- 检查罗技坐标是否有效
    if logi_x < 0 or logi_x > 65535 or logi_y < 0 or logi_y > 65535 then
        OutputLogMessage("错误：罗技坐标超出有效范围(0-65535)\n")
        return false
    end
    
    -- 等待地图加载
    pressKey("tab")
    OutputLogMessage("等待地图加载...\n")
    Sleep(1000)
    
    -- 执行点击
    OutputLogMessage("准备点击坐标...\n")
    moveAndSingleClicked(logi_x, logi_y)
    OutputLogMessage("点击完成\n")
    
    -- 等待操作完成
    Sleep(2000)
    pressKey("tab")
    
    OutputLogMessage("=== goGamePos执行完成 ===\n\n")
    return true
end

-- 到达全局地图坐标
function goGlobalMapPos(time)
    OutputLogMessage("开始执行 goGlobalMapPos\n")
    pressKey("escape")  
    Sleep(500)
    pressKey("escape")

    -- 上坐骑，需要读条，等待一下
    pressKey(kRideHorseKey)
    OutputLogMessage("上坐骑完成\n")
    Sleep(math.random(5000, 5500))
    
    -- 打开世界地图
    pressKey(kOpenGlobalMapKey)
    OutputLogMessage("打开世界地图完成\n")
    Sleep(math.random(1000, 1500))
    
    -- 选择对应的地图
    moveAndSingleClicked(kPosInGlobalMap.x, kPosInGlobalMap.y)
    OutputLogMessage("选择目标地图完成\n")
    Sleep(math.random(1500, 1700))
    
    
    -- 点击辽西
    moveAndSingleClicked(kPosLiaoXi.x, kPosLiaoXi.y)
    Sleep(math.random(1500, 1700))
    
    -- 处理自动寻路确定弹窗
    moveAndSingleClicked(kMoveMapEnter.x, kMoveMapEnter.y)
    OutputLogMessage("确认跨场景寻路完成，等待 %d 秒到达目的地\n", time)

    -- 点击TAB，关闭地图
    pressKey("tab")

    -- 洛阳跑去雪原的时间
    Sleep(time * 1000)
    
    -- 点击对应的局部坐标地图
    goGamePos(kLocalMapPosition.x, kLocalMapPosition.y)
    
    OutputLogMessage("开始局部跑图，需要 %d 秒\n", kTime2)
    -- 局部地图跑图时间
    Sleep(kTime2 * 1000)  
    
    -- 下坐骑，需要读条，等待一下
    pressKey(kRideHorseKey)
    OutputLogMessage("下坐骑完成\n")
    Sleep(math.random(1000, 1500))

    -- 开始打怪
    moveAndSingleClicked(kAutoFightButton.x, kAutoFightButton.y)
end

-- 出地府去洛阳
function escapeHellToLuoYang()
    OutputLogMessage("开始执行 escapeHellToLuoYang\n")
    -- pressKey("escape")
    -- Sleep(500)
    -- pressKey("escape")

    -- 单击孟婆
    moveAndSingleClicked(kHellMengPo.x, kHellMengPo.y)
    OutputLogMessage("单击孟婆完成\n")
    
    -- 等待左侧对话框弹出 && 点击洛阳
    Sleep(5000)
    moveAndDoubleClicked(kHellLuoYang.x, kHellLuoYang.y)
    OutputLogMessage("点击洛阳完成\n")
    Sleep(5000)
end

function main_loop()
    OutputLogMessage("开始新一轮循环\n")
    escapeHellToLuoYang()
    goGlobalMapPos(kTime)
end


-- 主事件处理函数（修改部分）
function OnEvent(event, arg)
    if event == "MOUSE_BUTTON_PRESSED" and arg == 5 then
        OutputLogMessage("\n=== 脚本已启动 ===\n")
        
        while true do
            OutputLogMessage("\n当前时间: %s\n", GetDate())
            OutputLogMessage("开始执行主循环\n")
            main_loop()
            
            -- 每次循环重新生成随机等待时间
            local wait_time = math.random(40, 50)
            OutputLogMessage("主循环执行完成，等待 %d 分钟后重新执行\n", wait_time)
            
            -- 每分钟显示一次时间
            for i = 1, wait_time do
                Sleep(60 * 1000)  -- 等待1分钟
                OutputLogMessage("当前时间: %s，还需等待 %d 分钟\n", 
                    GetDate(), wait_time - i)
            end
        end
    end
end

