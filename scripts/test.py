def calXY(x: float, y: float):
    logi_x = x / 2560 * 65535
    logi_y = y / 1440 * 65535
    print(f"logi_x = {logi_x:.0f}, logi_y = {logi_y:.0f}")

calXY(248, 474)
calXY(248, 494)
calXY(248, 514)
calXY(248, 534)
