from puzzle import Puzzle
from socket import inet_pton
import argparse

def listify(lst):
    '''
    turns the states into list of lists
    returnlst = list of lists (2D matrix for the 4x4 puzzle)
    '''
    returnlst = []
    for item in lst:
        nums = [int(x) for x in item.split()]
        returnlst.append(nums)
    return returnlst

def printlst(lst, f):
    '''
    formatting the list to print out each item in the list
    '''
    for item in lst:
        for enter in item:
            f.write(str(enter))
            f.write(" ")
        f.write('\n')
    f.write('\n')

def result(lst, w):
    acts = ""
    for item in lst[2]:
        acts += str(item) + " "
    hvals = ""
    for item in lst[3]:
        hvals += str(item) + " "
    return "{w}\n{d}\n{N}\n{actions}\n{hvals}".format(w = w,d=lst[0],N=lst[1],actions=acts,hvals=hvals)

def solve(puzzle,weight):
    '''
    uses the a* algorithm to solve the puzzle
    weight -> float W > 1
    :returns:res -> lst
    res[0] = d, level of shallowest goal
    res[1] = N, total number of nodes generated not includig root
    res[2] = action list
    res[3] = heuristic values list
    '''
    res = [0]*4 # list of results
    d = 0
    N = 0


    frontier = [puzzle]
    visited = []
    while frontier:
        
        min_index = 0
        for i in range(len(frontier)):
            if frontier[min_index].heuristic() > frontier[i].heuristic():
                min_index = i

        curr=frontier[min_index]
        frontier.pop(min_index)
        # perform checks
        if curr.board == curr.goal:
            d = curr.depth
            break
        if curr.board in visited: # do not allow repeated states
            continue

        for move in curr.getMoves():
            if move[1].board in visited:
                continue
            N+=1
            frontier.append(move[1])
            visited.append(curr.board)
    res[0] = d
    res[1] = N
    res[2] = curr.actions
    res[3] = curr.fvals

    return res

def main():
    '''
    takes input file and outputs the result using argparse
    infile = list of lines from input file
    w = w-value
    start = initial state
    goal = goal state
    puz = Puzzle class
    res = solver for puzzle, given w-value
    '''
    parser = argparse.ArgumentParser(description='15 Puzzle solver')
    parser.add_argument('--infile',type=argparse.FileType('r'),help='input file')
    parser.add_argument('--outfile',type=argparse.FileType('w'),help='output file')
    args = parser.parse_args()
    #Reads the lines from the input file
    infile = args.infile.readlines()
    #Initialize output file
    outfile = args.outfile
    #Strips all whitespace
    infile = [k.rstrip() for k in infile]
    for item in infile:
        if not item:
            infile.remove(item)

    #Obtains input data from infile
    w = float(infile[0])
    start = listify(infile[1:5])
    goal = listify(infile[5:9])

    #Prints the initial & goal state

    #Create the puzzle with the initial & goal states
    puz = Puzzle(start,w,goal)

    #Input the puzzle and the w-value into the solver function
    res = solve(puz,w)

    #Prints the output 
    printlst(start, outfile)
    printlst(goal, outfile)
    outfile.writelines(result(res, w))



main()
