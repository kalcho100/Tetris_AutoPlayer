from board import Direction, Rotation, Block
from random import Random


class Player:

    def agg_height(self, sandbox):
        height = 0
        for x in range(sandbox.width):
            for y in range(sandbox.height):
                if (x, y) in sandbox.cells:
                    height = height + 24 - y
                    break
        return height

    def cleared_lines(self, sandbox, oldscore):
        newScore = sandbox.score
        diff = newScore - oldscore

        if 100 < diff < 130:
            return 1
        elif 400 < diff < 450:
            return 2
        elif 800 < diff < 850:
            return 3
        elif 1600 < diff < 1650:
            return 4
        else:
            return 0

    def holes(self, sandbox):
        hole = 0
        arr = []
        for t in range(10):
            for x in range(sandbox.width):
                for y in range(sandbox.height):
                    if (x, y) not in sandbox.cells and ((x, y - 1) in sandbox.cells or (x, y - 1) in arr):
                        hole += 1
                        arr.append((x, y))
        hole = hole // 10
        return hole

    def bumpiness(self, sandbox):
        arr = [0 for i in range(sandbox.width)]
        bump = 0
        for x in range(sandbox.width):
            max_y = 24
            for y in range(sandbox.height):
                if (x, y) in sandbox.cells:
                    if y < max_y:
                        max_y = y
            arr[x] = max_y
        for t in range(sandbox.width - 1):
            bump = bump + abs(arr[t + 1] - arr[t])
        return bump

    def score(self, sandbox, oldscore):
        height_param = -0.510066
        comply_param = 0.760666
        holes_param = -0.35663
        bump_param = -0.184483
        height = self.agg_height(sandbox)
        comply = self.cleared_lines(sandbox, oldscore)
        holes = self.holes(sandbox)
        bump = self.bumpiness(sandbox)
        score = height_param * height + comply_param * comply + holes_param * holes + bump_param * bump
        return score

    def get_best_route(self, board):
        max_score = -1000000000
        best_move = 0
        best_rotate = 0
        oldscore = board.score
        left = 0
        clockwise = 1
        arr = [0 for i in range(4)]
        for pos in range(board.width):
            for i in range(4):
                landed = False
                sandbox = board.clone()
                for rot in range(i):
                    if sandbox.rotate(Rotation.Clockwise):
                        landed = True
                        score = self.score(sandbox, oldscore)
                        if score > max_score:
                            max_score = score
                            left = 1
                            clockwise = 1
                            best_rotate = i
                            best_move = 0
                        break
                if not landed:
                    current = sandbox.falling
                    mini = min(x for (x, y) in current.cells)
                    maxi = max(x for (x, y) in current.cells)
                    minis = mini
                    maxis = maxi
                    k = 0
                    while minis > pos:
                        k = k + 1
                        if sandbox.move(Direction.Left):
                            landed = True
                            score = self.score(sandbox, oldscore)
                            if score > max_score:
                                max_score = score
                                left = 1
                                clockwise = 1
                                best_rotate = i
                                best_move = k
                            break
                        minis = min(x for (x, y) in sandbox.falling.cells)
                    while maxis < pos:
                        k = k + 1
                        if sandbox.move(Direction.Right):
                            landed = True
                            score = self.score(sandbox, oldscore)
                            if score > max_score:
                                max_score = score
                                left = 0
                                clockwise = 1
                                best_rotate = i
                                best_move = k
                            break
                        maxis = max(x for (x, y) in sandbox.falling.cells)
                    if not landed:
                        minis = min(x for (x, y) in sandbox.falling.cells)
                        maxis = max(x for (x, y) in sandbox.falling.cells)
                        sandbox.move(Direction.Drop)
                        score = self.score(sandbox, oldscore)
                        if score > max_score:
                            max_score = score
                            clockwise = 1
                            best_rotate = i
                            if minis < mini:
                                left = 1
                                best_move = mini - minis
                            elif maxis > maxi:
                                left = 0
                                best_move = maxis - maxi
                            else:
                                left = 1
                                best_move = 0
                landed = False
                sandbox = board.clone()
                for rot in range(i):
                    if sandbox.rotate(Rotation.Anticlockwise):
                        landed = True
                        score = self.score(sandbox, oldscore)
                        if score > max_score:
                            max_score = score
                            left = 1
                            clockwise = 0
                            best_rotate = i
                            best_move = 0
                        break
                if not landed:
                    current = sandbox.falling
                    mini = min(x for (x, y) in current.cells)
                    maxi = max(x for (x, y) in current.cells)
                    minis = mini
                    maxis = maxi
                    k = 0
                    while minis > pos:
                        k = k + 1
                        if sandbox.move(Direction.Left):
                            landed = True
                            score = self.score(sandbox, oldscore)
                            if score > max_score:
                                max_score = score
                                left = 1
                                clockwise = 0
                                best_rotate = i
                                best_move = k
                            break
                        minis = min(x for (x, y) in sandbox.falling.cells)
                    while maxis < pos:
                        k = k + 1
                        if sandbox.move(Direction.Right):
                            landed = True
                            score = self.score(sandbox, oldscore)
                            if score > max_score:
                                max_score = score
                                left = 0
                                clockwise = 0
                                best_rotate = i
                                best_move = k
                            break
                        maxis = max(x for (x, y) in sandbox.falling.cells)
                    if not landed:
                        minis = min(x for (x, y) in sandbox.falling.cells)
                        maxis = max(x for (x, y) in sandbox.falling.cells)
                        sandbox.move(Direction.Drop)
                        score = self.score(sandbox, oldscore)
                        if score > max_score:
                            max_score = score
                            clockwise = 0
                            best_rotate = i
                            if minis < mini:
                                left = 1
                                best_move = mini - minis
                            elif maxis > maxi:
                                left = 0
                                best_move = maxis - maxi
                            else:
                                left = 1
                                best_move = 0
        arr[0] = clockwise
        arr[1] = best_rotate
        arr[2] = left
        arr[3] = best_move
        return arr

    def choose_action(self, board):
        k = self.get_best_route(board)
        if k[0] == 1:
            for t in range(k[1]):
                yield Rotation.Clockwise
        else:
            for t in range(k[1]):
                yield Rotation.Anticlockwise
        if k[2] == 1:
            for t in range(k[3]):
                yield Direction.Left
        else:
            for t in range(k[3]):
                yield Direction.Right
        yield Direction.Drop


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
        ])


SelectedPlayer = Player
