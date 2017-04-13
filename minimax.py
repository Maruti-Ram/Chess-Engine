import collections
import copy
import chess
import heuristicY
import heuristicX
from treelib import Node, Tree
heuristicValues = {}
depthList = []
def miniMaxTree(board,currentPlayer):
    tree = Tree()
    Level0List   = [board]
    tree.create_node('currentBoard','currentBoard',data=board)
    index = 0
    depthList = []
    def addPossMovesByList(listOfBoards,nodeName,parentNodeName,nodeType):
        index = 0
        i2    = 0
        newGenBrd = []
        newdepth = []
        for b in listOfBoards:
            for move in b.legal_moves:
                currentMove = chess.Move.from_uci(move.uci())
                brd = copy.deepcopy(b)
                brd.push(currentMove)
                if brd.is_castling(currentMove):
                    continue
                newGenBrd.append(brd)
                # check if it's root of tree
                if (parentNodeName == "currentBoard"):
                    boardName = parentNodeName
                else:
                    boardName = parentNodeName+'_'+str(index);
                val = -100000
                if (nodeType == "MIN"):
                    val = 1000000
                elif(nodeType == "MAX"):
                    val = -1000000
                elif(nodeType =="LEAF"):
                    if (currentPlayer == "Y"):
                    	val = heuristicY.h(brd)
                    else:
                    	val = heuristicX.h(brd)
                heuristicValues[boardName] = val
                tree.create_node(nodeName+'_'+str(i2),nodeName+'_'+str(i2),parent=boardName,data=brd)
                i2 = i2+1
                newdepth.append(boardName)
            index = index+1
        depthList.append(newdepth)
        return newGenBrd
    heuristicValues["currentBoard"] = -100000
    brdList = addPossMovesByList(Level0List,"LevelOne","currentBoard","MIN")
    brdList = addPossMovesByList(brdList,"LevelTwo","LevelOne","MAX")
    brdList = addPossMovesByList(brdList,"LevelThree","LevelTwo","LEAF")
    
    for node in depthList[1]:
        children = tree.children(node)
        for child in children:
            cid = child.identifier
            if heuristicValues[cid] > heuristicValues[node]:
                heuristicValues[node] = heuristicValues[cid]
    for node in depthList[0]:
        children = tree.children(node)
        for child in children:
            cid = child.identifier
            if heuristicValues[cid] < heuristicValues[node]:
                heuristicValues[node] = heuristicValues[cid]      
    child = tree.children("currentBoard")
    # set first one as default
    bestChoice = child[0].identifier
    for node in child:
        cid = node.identifier
        if heuristicValues[cid] > heuristicValues[bestChoice]:
            heuristicValues["currentBoard"] = heuristicValues[cid]
            bestChoice = node.identifier
    tree.root = bestChoice

    return tree  
