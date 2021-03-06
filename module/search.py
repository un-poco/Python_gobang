
# vector = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8个方向的单位向量
dx = [1, 1, 0, -1, -1, -1, 0, 1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]  # （dx,dy）是8个方向向量


def live4(state, pos, key):
    counter = 0
    for u in range(4):  # 4个方向，每个方向最多1个活4
        flag = True
        sumk = 1
        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        if sumk == 4:
            counter += 1

    return counter


def chong4(state, pos, key):
    counter = 0
    for u in range(8):  # 8个方向，每方最多1个
        flag = True
        sumk = 0
        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                break
            if flag or key == state[cur]:
                if key != state[cur]:
                    if flag and state[cur] != 0:
                        sumk -= 10
                    flag = False
                sumk += 1
            else:
                break

        if (cur < 0).any() or (cur > 14).any():
            continue

        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                break
            if key != state[cur]:
                break
            sumk += 1

        if sumk == 4:
            counter += 1

    return counter


def live3(state, pos, key):
    counter = 0

    for u in range(4):  # 三连的活三
        sumk = 1
        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        i += 1
        cur = pos + [i * dx[u], i * dy[u]]
        if (cur < 0).any() or (cur > 14).any():
            continue
        if state[cur] != 0:
            continue

        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        i += 1
        cur = pos + [-i * dx[u], -i * dy[u]]
        if (cur < 0).any() or (cur > 14).any():
            continue
        if state[cur] != 0:
            continue

        if sumk == 3:
            counter += 1

    for u in range(8):  # 非三连的活三
        sumk = 0
        flag = True

        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                break
            if flag or key == state[cur]:
                if key != state[cur]:
                    if flag and state[cur] != 0:
                        sumk -= 10
                    flag = False
                sumk += 1
            else:
                break
        if (cur < 0).any() or (cur > 14).any():
            continue
        i -= 1
        cur = pos + [i * dx[u], i * dy[u]]
        if state[cur] == 0:
            continue

        # sumk sub
        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        if sumk == 3:
            counter += 1

    return counter


def mian3(state, pos, key):
    counter = 0
    for u in range(8):
        sumk = 0
        flag = True
        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                break
            if flag or key == state[cur]:
                if key != state[cur]:
                    if flag and state[cur] != 0:
                        sumk -= 10
                    flag = False
                sumk += 1
            else:
                break
        if (cur < 0).any() or (cur > 14).any():
            continue

        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                break
            if key != state[cur]:
                break
            sumk += 1

        if sumk == 3:
            counter += 1
    return counter - live3(state, pos)


def live2(state, pos, key):
    counter = 0

    for u in range(4):  # 二连的活二
        sumk = 0
        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        i += 1
        cur = pos + [i * dx[u], i * dy[u]]
        if (cur < 0).any() or (cur > 14).any():
            continue
        if state[cur] != 0:
            continue
        i += 1
        cur = pos + [i * dx[u], i * dy[u]]
        if (cur < 0).any() or (cur > 14).any():
            continue
        if state[cur] != 0:
            continue

        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        i += 1
        cur = pos + [-i * dx[u], -i * dy[u]]
        if (cur < 0).any() or (cur > 14).any():
            continue
        if state[cur] != 0:
            continue
        i += 1
        cur = pos + [-i * dx[u], -i * dy[u]]
        if (cur < 0).any() or (cur > 14).any():
            continue
        if state[cur] != 0:
            continue

        if sumk == 2:
            counter += 1

    for u in range(8):  # 非二连的活二
        sumk = 0
        flag = True

        for i in range(1, 6):
            cur = pos + [i * dx[u], i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                break
            if flag or key == state[cur]:
                if key != state[cur]:
                    if flag and state[cur] != 0:
                        sumk -= 10
                    flag = False
                sumk += 1
            else:
                break
        if (cur < 0).any() or (cur > 14).any():
            continue
        i -= 1
        cur = pos + [i * dx[u], i * dy[u]]
        if state[cur] == 0:
            continue

        for i in range(1, 6):
            cur = pos + [-i * dx[u], -i * dy[u]]
            if (cur < 0).any() or (cur > 14).any():
                flag = False
                break
            if key != state[cur]:
                if state[cur] != 0:
                    flag = False
                break
            sumk += 1
        if not flag:
            continue

        i += 1
        cur = pos + [-i * dx[u], -i * dy[u]]
        if state[cur] == 0:
            continue

        if sumk == 2:
            counter += 1
    return counter