import chess

######################################################################
# Strategy :
# --------------------------------------------------------------------
# The board value starts at 0. We choose that which MAXIMIZES the 
# benefit of the move. 
# For every piece that we still have, we will add points depending on
# how valuable we consider each piece. Think of it like money!
# King: 200
# Knight: 100
# Rook: 150
# -------------------
# In Check?
# -------------------
# A lot of points (200) are taken off if our current board is in check.
# -------------------
# KING PLACE
# -------------------
# The closer the king moves to the other player, the more dangerous
# so we take points off the closer he gets to the other side. So
# second row is -50 then -100 for 3rd row then -200 for 4th row and so 
# on
# -------------------
# KNIGHT PLACE
# -------------------
# We ENCOURAGE the Knight to move forward towards the other player. 
# The more the Knight is closer to OUR side, the more points we take 
# off.
# -------------------
# ROOK
# -------------------
# Similar to Knight's strategy with the difference that we are more
# willing to take points off of Knight because we could risk him more
# since he's the least important piece.
# -------------------
# Pieces Killed
# -------------------
# We add points when we see the move killed their piece. It is +500
# if it kills their king (cause we really wanna do that). And if we 
# kill their knight, that's +400! 
# ------------------
# Attacking
# ------------------
# The more attackers we have towards our opponent's pieces, the more 
# points. So +100 if there is one attacker, +200 for two attackers,
# +300 for three attackers.
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
	value = 0
	###################################
	# Current pieces
	###################################
	king = board.pieces(chess.KING,True)
	knight = board.pieces(chess.KNIGHT,True)
	rook = board.pieces(chess.ROOK,True)
    # Check if king exists
	if len(king)>0:
		value = value+200
		for s in king:
			kingLocation = s
		kingLocation = chess.SQUARE_NAMES[kingLocation]
		# we want king to stay!
		currentRow =  kingLocation[1:2]
		currentRow = int(currentRow)
		if(currentRow == 7):
			value = value-50
		elif(currentRow == 6):
			value = value-100
		elif(currentRow == 5):
			value = value-200
		elif(currentRow == 4):
			value = value-250
		elif(currentRow == 3):
			value = value-280
		elif(currentRow == 2):
			value = value-290
		elif(currentRow == 1):
			value = value-300
    # Check if knight exists
	if len(knight)>0:
		value = value+100
		for s in knight:
			knightLocation = s

		# we need knight to move! towards player!
		knightLocation = chess.SQUARE_NAMES[knightLocation]
		currentRow =  knightLocation[1:2]
		currentRow = int(currentRow)
		if(currentRow == 1):
			value = value-350
		elif(currentRow == 2):
			value = value-200
		elif(currentRow == 3):
			value = value-50
    # Check if rook exists
	if len(rook)>0:
		value = value+150
		for s in rook:
			rookLocation = s
	
		# we need rook to move towards player! but not
		# as much as the knight!
		rookLocation = chess.SQUARE_NAMES[rookLocation]
		currentRow =  rookLocation[1:2]
		currentRow = int(currentRow)
		if(currentRow == 1):
			value = value-150
		elif(currentRow == 2):
			value = value-100
		elif(currentRow == 3):
			value = value-50
        elif(currentRow == 4):
			value = value-20
	###################################
	# Pieces killed
	###################################
	opponentKing = board.pieces(chess.KING,False)
	if len(opponentKing) == 0:
		value = value+500
	else:	
		for s in opponentKing:
			oppKingLocation = s 
			# Number of pieces we are attacking 
			# king
			attacking = board.attackers(True,oppKingLocation)
			if (len(attacking) == 1):
				value = value+100
			elif (len(attacking) == 2):
				value = value+200
			elif (len(attacking) == 3):
				value = value+300
	opponentKnight = board.pieces(chess.KNIGHT,False)

	if len(opponentKnight) == 0:
		value = value+400
	else:
		for s in opponentKnight:
			oppKnightLocation = s
			# knight
			attacking = board.attackers(True,oppKnightLocation)
			if (len(attacking) == 1):
				value = value+100
			elif (len(attacking) == 2):
				value = value+200
			elif (len(attacking) == 3):
				value = value+300
	####################################
	# IN CHECK?
	###################################
	if(board.is_checkmate()): 
		value = value-200 # cost of losing a king 
	
	# check if in check 
	if (board.is_check()):
		value - 200 # cost of losing a king

	return value
