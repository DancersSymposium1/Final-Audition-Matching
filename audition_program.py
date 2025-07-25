# Modification of Gale-Shapley algorithm to match dancers into pieces based on mutual preferences

# Run: python audition_program.py <choreo-rankings.csv> <dancer-rankings.csv> <sign-in.csv>
# Ensure there's a directory "piece_assignments" to put assignments in

# TO-DO: Clean up style (documentation, inputs/return types, variable names (camelCase))
# TO-DO: Add README with file formats (+ trouble-shooting: make sure no commas in .csv files)

import argparse

printOUT_PATH = 'piece_assignments/'
parser = argparse.ArgumentParser()
parser.add_argument('choreographer_prefs') #path to the choreographers' rankings file (.csv)
parser.add_argument('dancer_prefs') #path to the dancers' rankings file (.csv)
parser.add_argument('sign_in') #path to sign in sheet (.csv)
args = parser.parse_args()

# Piece rankings: list of tuples (piece ID, dancer's ranking), sorted by dancer's ranking
# Pieces: set of pieces dancer is in with capacity num_pieces
class Dancer(object):
	def __init__(self, first_name, last_name, audition_number, num_pieces, piece_rankings, email, phone):

		self.first_name = first_name
		self.last_name = last_name
		self.audition_number = audition_number
		self.num_pieces = num_pieces
		self.piece_rankings = piece_rankings
		self.email = email
		self.phone = phone
		self.pieces = {}

	def __repr__(self):
		return f"{self.audition_number} ; {self.first_name} {self.last_name} ; {self.email}"

# Dancer rankings: dict of choreorapher's dancer preferences, key: dancer ID, val: 
# choreographer's dancer preference (rank)
# Dancers: set of dancers currently in piece
# Alternates: set of dancers who may later join the piece 
class Piece(object):
	def __init__(self, piece_id, choreographer_name, 
				 capacity, dancer_rankings):

		self.piece_id = piece_id
		self.choreographer_name = choreographer_name
		self.capacity = capacity
		self.dancer_rankings = dancer_rankings
		self.dancers = {}
		self.alternates = {}

	def __repr__(self):
		return str(self.choreographer_name) + ": " + str(self.piece_id)

#turns CSV into map of pieces (key: piece id (1,2,...), val: Piece object)
def csvToPieces(choreographerPrefFile):
	choreoPrefs = open(choreographerPrefFile, 'r')
	choreoPrefsHeaders = ['id', 'name', 'total']
	pieceMap = {}

	for i, line in enumerate(choreoPrefs):
		if i == 0: continue

		column = line.strip().split(',')
		piece_id = (column[choreoPrefsHeaders.index('id')])
		name = column[choreoPrefsHeaders.index('name')]
		total = int(column[choreoPrefsHeaders.index('total')])

	
		preferences = column[len(choreoPrefsHeaders):]
		rankings = {} #rank is 0 if definite, >1 if alternate
		for rank, audition_num in enumerate(preferences):
			if audition_num == '':
				break
			if rank < total:
				rankings[int(audition_num)] = 0
			else:
				rankings[int(audition_num)] = rank - total +1
		pieceMap[piece_id]  = Piece(piece_id, name, total, rankings)

	choreoPrefs.close()

	return pieceMap

#turns CSV into map of dancers (key: audition num, val: Dancer object)
def csvToDancers(dancerPrefsFile, signInFile):
	dancerInfo = open(signInFile, 'r',encoding='utf-8')
	dancerInfoHeaders = ['time', 'audition_number', 
				'first_name', 'last_name', 'class','email', 
				'num_semesters', 'phone']
	contactMap = {}

	for i,line in enumerate(dancerInfo):
		if i == 0: continue

		column = line.strip().split(',')
		audition_number = int(column[dancerInfoHeaders.index('audition_number')])
		email = column[dancerInfoHeaders.index('email')]
		phone = column[dancerInfoHeaders.index('phone')]
		# pronouns = column[dancerInfoHeaders.index('pronouns')]
		contactMap[audition_number] = (email, phone)

	dancerInfo.close()

	dancerRankings = open(dancerPrefsFile, 'r',encoding='utf-8')
	dancerRankingsHeaders = ['time', 'email', 'audition_number', 'first_name', 'last_name', 
							'num_pieces']
	dancerMap = {}

	for i,line in enumerate(dancerRankings):
		if i == 0: continue

		column = line.strip().split(',')
		print("column",column)
		first_name = column[dancerRankingsHeaders.index('first_name')]
		last_name = column[dancerRankingsHeaders.index('last_name')]
		audition_number = int(column[dancerRankingsHeaders.index('audition_number')])
		num_pieces = int(column[dancerRankingsHeaders.index('num_pieces')]) 

		piece_prefs = column[len(dancerRankingsHeaders):]
		# print("preferences:",piece_prefs)
		piece_rankings = [(piece, ranking) 
			for ranking, piece in enumerate(piece_prefs) if piece != ""]
		# print("piece rankings: ",piece_rankings)
		# piece_rankings = sorted(ranking_tuples, key=lambda tup: tup[1])
		# print("sorted rankings: ",piece_rankings)
		# piece_rankings = [(dance_name, ranking) 
		# 	for (dance_name, ranking) in sorted_rankings]

		(email, phone) = contactMap.get(audition_number, ('no email', 'no phone'))

		dancerMap[audition_number] = Dancer(first_name, last_name, 
									audition_number, num_pieces, 
									piece_rankings, email, phone)
	dancerRankings.close()

	return dancerMap

#checks if certain piece ranked a certain dancer
def checkIfPieceRankedDancer(piece, dancer):
	dancer_id = dancer.audition_number
	rankings = piece.dancer_rankings
	if dancer_id in rankings:
		return True
	return False

# return dancer's least fave piece (worstID, worstRank)
# note: (piece, rank) = (x, int)
def findWorstPiece(dancer):
	worstRank = 0
	worstID = None

	for rank, piece in enumerate(dancer.piece_rankings):
		# print("rank and piece: ",rank,piece)
		# print("\n\n",piece,dancer.pieces, piece[0] in dancer.pieces,"\n\n")
		if piece[0] in dancer.pieces and rank > worstRank:
			# print("getting here ever????")
			worstID, worstRank = piece, rank
	
	return (worstID, worstRank)

# check if a dancer wants to add this piece to their pieces 
# return: (False, None, None) if we can't add (dancer rejects proposal)
# (True, rank, None): rank = rank of added piece or None if dancer wasn't removed from a piece
# (True, rank, removedPiece): rank = rank of added piece, 
# and removedPiece = piece ID of the piece dancer left
def checkCanAddDancerToPiece(piece, dancer):
	# possible piece: (piece, rank)
	# gets rank of current piece in dancer's rankings
	# if(piece.piece_id=="E - Caroline"):
	# 	print(piece,dancer)
	# if(piece.piece_id=="F - Nina & Lily"):
	# 	print(piece,dancer)
	pieceRank = 1000
	actual_piece = piece.piece_id

	# print("actual piece format:",actual_piece)
	# print(dancer.piece_rankings)

	for possiblePiece in dancer.piece_rankings:
		# print("possiblePiece",possiblePiece)
		if possiblePiece[0] == actual_piece:
			pieceRank = possiblePiece[1]
			break

	if pieceRank == 1000:
		return (False, None, None)

	# check if dancer has room to add
	if len(dancer.pieces) < dancer.num_pieces:
		return (True, pieceRank, None)

	# dancer is at max number of pieces, checks if they want to drop a piece
	else:
		# print("entering else statement")
		(worstID, worstRank) = findWorstPiece(dancer)
		# print("worst rank: ",worstRank)
		if worstRank > pieceRank:
			# curr piece is higher priority, dancer wants to drop their worst piece
			return (True, pieceRank, worstID)

	# dancer doesn't want to add piece (rank not high enough)
	return (False, None, None)

# gets next dancer for piece to propose to
def findDancer(piece):
	dancers = []
	for key in piece.dancer_rankings:
		dancers.append((key,piece.dancer_rankings[key]))
	sortedDancers = sorted(dancers, key = lambda x:x[1])

	if sortedDancers == []:
		return None

	dancer_id = sortedDancers[0][0]

	return dancer_id

# check if all pieced filled or, if unfilled, then all dancers in that piece were proposed to
def checkAllProposed(pieces):
	for pieceID in pieces:
		piece = pieces[pieceID]
		if len(piece.dancers) < piece.capacity:
			# piece unfilled
			if len(piece.dancer_rankings) != 0:
				# unfilled piece didn't finish proposing
				return False

	# all pieces filled + unfilled pieces proposed to all

	return True

# outputs pieces to .txt files
def writePieces(pieces):
	for pieceID in pieces:
		piece = pieces[pieceID]
		pieceFile = open(printOUT_PATH + '%s - %s.txt' % (piece.piece_id, 
							piece.choreographer_name.replace('/', '_')), 'w')
		pieceFile.write('********************\n')
		pieceFile.write('%s (%s) \n' % (piece.choreographer_name, piece.piece_id))

		pieceFile.write('********************\n')
		dancers = []
		for dancerID in piece.dancers:
			dancers.append(dancerID)
		sortedDancers = sorted(dancers)
		for dancerID in sortedDancers:
			dancerStr = piece.dancers[dancerID]
			pieceFile.write(str(dancerStr) + '\n')

		pieceFile.close()
	return

# writes list of dancers who were successfully assigned into piece(s) to .csv file
def makeAssigned(pieces):
	assignedFile = open(printOUT_PATH + "assigned.csv", 'w')
	for pieceID in pieces:
		piece = pieces[pieceID]
		assignedFile.write(str(piece) + '\n')
		dancers = []
		for dancerID in piece.dancers:
			dancers.append(dancerID)
		sortedDancers = sorted(dancers)
		for dancerID in sortedDancers:
			dancerStr = piece.dancers[dancerID]
			assignedFile.write(str(dancerStr) + '\n')

	assignedFile.close()
	return

# outputs list of dancers not assigned to a piece to .csv file
def makeUnassigned(dancers):
	unassignedFile = open(printOUT_PATH + 'unassigned.csv', 'w')
	for dancerID in dancers:
		dancer = dancers[dancerID]
		if len(dancer.pieces) == 0:
			unassignedFile.write(f"{dancer.audition_number}, {dancer.first_name} {dancer.last_name}, {dancer.email}, {dancer.phone}\n")

	unassignedFile.close()
	return

def main():
	pieces = csvToPieces(args.choreographer_prefs)
	dancers = csvToDancers(args.dancer_prefs, args.sign_in)

	while (not checkAllProposed(pieces)):
		for pieceID in pieces:
			# print("pieceID: ",pieceID)
			piece = pieces[pieceID]
			# print("piece: ",piece)
			# piece = pieceID
			while len(piece.dancers) < piece.capacity and len(piece.dancer_rankings) != 0:
				# propose to dancer
				dancerID = findDancer(piece)
				
				if dancerID != None:

					#print dancerID
					if dancerID not in dancers:
						print(f"Erorr: dancer ID {dancerID} is invalid.")
						piece.dancer_rankings.pop(dancerID)
						continue
					dancer = dancers[dancerID]

					# check if dancer accepts proposal
					(res, pieceRank, removedID) = checkCanAddDancerToPiece(piece, dancer)

					if res:
						# dancer can be added to current piece
						# add dancer to accepted piece
						piece.dancers[dancerID] = dancer

						if removedID == None:
							# dancer isn't leaving a piece, add piece to dancer's list
							dancer.pieces[piece.piece_id] = pieceRank

						else:
							# dancer leaving removedID piece
							# print("pieces=",pieces)
							# print("removedID=",removedID)
							leavingPiece = pieces[removedID[0]]

							# remove rejected piece from dancer's list
							dancer.pieces.pop(removedID[0])

							# add accepted piece to dancer's list
							dancer.pieces[piece.piece_id] = pieceRank

							# remove dancer from rejected piece
							leavingPiece.dancers.pop(dancerID)

					# remove curr dancer from proposal list
					piece.dancer_rankings.pop(dancerID)

	# print(dancers[225].pieces)
	file = open("dancers.csv","w")
	for dancer in dancers:
		file.write(str(dancer))
		file.write(",")
		pieces = [str(d) for d in dancers[dancer].pieces]
		for p in pieces:
			file.write(p[0])
			file.write("/")
		file.write("\n")

	writePieces(pieces)
	makeAssigned(pieces)
	makeUnassigned(dancers)

main()