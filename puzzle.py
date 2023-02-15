class Puzzle:
    def __init__(self,board,weight,goal,path_cost=0,depth=0,actions=None,fvals = None):
        '''
        board -> lst of lst, matrix representation of the puzzle board
        or initial state
        ex. [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]

        goal -> lst of lst, maxtrix representation of the goal state
        pathcost -> int, path cost of current board, if not passed in default to 0
        '''
        self.board = board
        self.ROWS = len(board)
        self.COLS = len(board[0])
        self.weight = weight
        self.goal = goal
        self.path_cost = path_cost
        self.depth = depth
        if actions is None:
            actions = []
        if fvals is None:
            fvals = []
        self.actions = actions
        self.fvals = fvals

        # Error checking
        if self.ROWS != self.COLS:
            raise ValueError("Invalid dimensions of puzzle board")

    def swap(self,x1,y1,x2,y2):
        '''
        given two sets of coordinates,
        returns a copy of the board with swapped positions
        x1,y1,x2,y2 -> int ~ (0-3)
        '''
        new_puz =  [list(row) for row in self.board]
        new_puz[x1][y1],new_puz[x2][y2] = new_puz[x2][y2],new_puz[x1][y1]

        return new_puz

    def getPosition(self,digit,board=None):
        '''
        given a digit and a board,
        returns the position coordinate of the given digit in the board
        digit -> int ~ (0,15)
        board -> lst of lst
        if board not given, use the current board
        if board is given, use the board given (will be goal state to calculate
        manhattan distance)
        '''
        # if a board is not given = current state
        if board==None: 
            board=self.board

        for i in range(self.ROWS):
            for j in range(self.COLS):
                if board[i][j] == digit:
                    return i,j

        raise RuntimeError('Could not find digit in given board')

    def getMoves(self):
        '''
        searches for the position of the empty block (0)
        returns a list of all moves: left, right, up, down
        '''
        moves = []
        r,c = self.getPosition(0)

        # can we move left
        if c > 0:
            new = Puzzle(self.swap(r,c,r,c-1),self.weight, self.goal,self.path_cost+1,self.depth+1, self.actions + ['L'], self.fvals + [self.heuristic()])
            moves.append(('L',new))

        # can we move right
        if c < self.COLS - 1:
            new = Puzzle(self.swap(r,c,r,c+1),self.weight, self.goal,self.path_cost+1,self.depth+1, self.actions + ['R'], self.fvals + [self.heuristic()])
            moves.append(('R',new))

        # can we move up
        if r > 0:
            new = Puzzle(self.swap(r,c,r-1,c),self.weight, self.goal,self.path_cost+1,self.depth+1, self.actions + ['U'], self.fvals + [self.heuristic()])
            moves.append(('U',new))

        # can we move down
        if r < self.ROWS - 1:
            new = Puzzle(self.swap(r,c,r+1,c),self.weight, self.goal,self.path_cost+1,self.depth+1, self.actions + ['D'], self.fvals + [self.heuristic()])
            moves.append(('D',new))

        return moves

    def heuristic(self):
        '''
        returns the heuristic function value from current to goal
        weight -> float W > 1
        '''
        distance = 0

        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.board[i][j] == 0: # the blank spot does not count
                    continue
                r,c = self.getPosition(self.board[i][j],self.goal)
                distance += abs(i-r) + abs(j-c)
        return self.path_cost + self.weight*distance
    
