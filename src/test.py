test_cases = """ID,Category,Function,TestType,Precondition,Input,Action,ExpectedOutput,Description,Remark
FOLD_001,foldMirrors,等价类划分,/,park_data.plan_enable=false,调用foldMirrors,park_data.mirror_fold_req=false,测试规划未启用时不应折叠后视镜,/
FOLD_002,foldMirrors,边界值分析,/,park_data.veh_curr_pos距离goal_pos > kVehCenterToFront,调用foldMirrors,park_data.mirror_fold_req=false,测试车辆不在车位内时不应折叠后视镜,/
FOLD_003,foldMirrors,等价类划分,/,park_data.slot_type != SlotType::kOblique,调用foldMirrors,park_data.mirror_fold_req=false,测试非斜列车位时不应折叠后视镜,/
FOLD_004,foldMirrors,边界值分析,/,mirror_dist >= kMirrorDist,调用foldMirrors,park_data.mirror_fold_req=false,测试障碍物距离大于阈值时不应折叠后视镜,/
FOLD_005,foldMirrors,场景组合,/,1. plan_enable=true 2. 车辆在车位内 3. slot_type=kOblique 4. mirror_dist < kMirrorDist 5. p14_od < kSlotObsDist,调用foldMirrors,park_data.mirror_fold_req=true,测试满足所有折叠条件时应折叠后视镜,/
FOLD_006,foldMirrors,场景组合,/,1. plan_enable=true 2. 车辆在车位内 3. slot_type=kOblique 4. mirror_dist < kMirrorDist 5. p15_od < kSlotObsDist,调用foldMirrors,park_data.mirror_fold_req=true,测试另一侧满足所有折叠条件时应折叠后视镜,/
FOLD_007,foldMirrors,状态保持,/,park_data.mirror_fold_req=true,调用foldMirrors,park_data.mirror_fold_req保持为true,测试已经请求折叠时应保持折叠状态,/
FOLD_008,foldMirrors,边界值分析,/,err_lat_curr接近但未超过kVehWid 0.5f,调用foldMirrors,根据其他条件判断是否折叠,测试车辆横向位置在边界值附近的行为,/
FOLD_009,foldMirrors,错误推测,/,park_data数据不完整或异常,调用foldMirrors,不应崩溃且mirror_fold_req保持false,测试异常输入的健壮性,/
FOLD_010,foldMirrors,组合场景,/,多个条件同时在边界值附近,调用foldMirrors,根据具体组合正确判断是否折叠,测试多个条件同时在临界状态时的行为,/"""

# 将测试用例写入CSV文件
with open('test_cases.csv', 'w', encoding='utf-8') as f:
    f.write(test_cases)
