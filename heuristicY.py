import chess 
######################################################################
# Strategy :
# --------------------------------------------------------------------
# The board value starts at 500. We want to MAXIMIZE the points and 
# that would determine our next move. We start at 500 instead of 0
# (like we did in the heuristic x) because we don't want to move too 
# much. The idea is to delay the game since we only have two pieces.
# So as long as nothing is wrong, we are fine. We are not trying to
# attack. (But we may find ourselves doing so at times)
# 
# -------------------
# In Check?
# -------------------
# A lot of points (200) are taken off if our current board is in check.
# -------------------
# Positions
# -------------------
# The closer we are to Player X's rows, the more points we take off. 
# We take more points off for our King getting closer to them.
# We want to discourage both our Knight and King to move any closer to
# Player X. We also encourage the column to be more towards our left
# so we take points off the more they get close to the right (with
# also taking more points off from the King). The reason is because
# Player X starts in positions more towards the right so we would like
# to kind of stay in the left corner to delay the game as much as 
# possible!
# ------------------
# Attacking
# ------------------
# We check for those attacking us. The more player are in attack
# mode towards our king, the more points taken off. The same goes
# for knight, except that we don't take as many points off for the
# knight since it's not as important as the king.
#
# In conclusion, We add a lot of points to real key moves (such as 
# killing their pieces and being in attack mode) and discourage
# our king to move forward while encouraging the Knight and Rook to
# move forward towards the other play.
######################################################################
def h(board):
	return f(board)+g(board)
def g(board):
	# number of moves. Half will be other player's moves
	return len(board.move_stack)/2
def f(board):
	# Everything starts at 500(being the best move)
	value = 500
	####################################
	# IN CHECK?
	###################################
	if(board.is_check()): 
		value = value-100
		#print("in check, -100"+str(value))
	#####################################
	# K I N G
	####################################
	# Is king still there?
	kingLocation = board.pieces(chess.KING,False)
	if(len(kingLocation) == 0):
		value = value - 500
    else:
		# There will only be one piece
		for s in kingLocation:
			kingLocation = s

		# king ATTACKERS :(
		attackers = board.attackers(True,kingLocation)
		#print(str(len(attackers))+" number of king attackers!")
		#print("Location: "+str(kingLocation))

		# One attacker
		if(len(attackers) == 1):
			value = value-60
		# Two attackers
		elif(len(attackers) == 2):
			value = value-80
		# at least Three attackers
		elif(len(attackers)>0):
			value = value-100
		# Now, let's deal with location. We need to stall
		# So further away from the player, the better. Also,
		# The sides are better.
		# COLUMN
		kingLocation = chess.SQUARE_NAMES[kingLocation]
		currentCol =  kingLocation[0:1]
	 
		if (currentCol == "d"):
			value = value-30			
			#print("king: column c, -2"+str(value))
		elif(currentCol == "e"):
			value = value-40
			#print("king: column d, -6"+str(value))
		elif(currentCol == "f"):
			value = value-60
		elif(currentCol == "g"):
			value = value-80
			#print("king: column e, -2"+str(value))
		# ROW
		row = kingLocation[1:2]
		row = int(row)	
		if (row is 6 or row is 7):
			value = value-200
		elif(row is 5):
			value = value-250
		elif(row is 4):
			value = value-225
		elif (row is 3):
			value = value-250
	#####################################
	# K N I G H T
	####################################
	# Is king still there?
	knightLocation = board.pieces(chess.KNIGHT,False)
	# -50 if knight no longer there
	if(len(knightLocation) == 0):
		value = value - 150
		#print("Knight gone, -50"+str(value))
	else:
		# There will only be one piece
		for a in knightLocation:
			knightLocation = a

		# KNIGHT ATTACKERS :(
		attackers = board.attackers(True,knightLocation)
		# One attacker
		if(len(attackers) == 1):
			value = value-8
			#print("Knight: one attacker, -8"+str(value))
		# Two attackers
		elif(len(attackers) == 2):
			value = value-18
			#print("Knight: two attackers, -18"+str(value))
		# at least Three attackers
		elif(len(attackers)>0):
			value = value-25
			#print("Knight: three attackers, -25"+str(value))
		# Now, let's deal with location. We need to stall
		# So further away from the player, the better. Also,
		# The sides are better.		
		knightLocation = chess.SQUARE_NAMES[knightLocation]
		# COLUMN
		currentCol =  knightLocation[0:1]
		if (currentCol == "d"):
			value = value-30			
			#print("king: column c, -2"+str(value))
		elif(currentCol == "e"):
			value = value-40
			#print("king: column d, -6"+str(value))
		elif(currentCol == "f"):
			value = value-60
		elif(currentCol == "g"):
			value = value-80
		# ROW
		row = knightLocation[1:2]
		row = int(row)
		if(row == 7):
			value = value-15 
		elif(row == 6):
			value = value-50
		elif(row == 5):
			value = value-100
		elif(row == 4):
			value = value-125
		elif (row == 3):
			value = value-150
	return value
	
