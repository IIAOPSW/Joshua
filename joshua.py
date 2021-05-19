#todo: 
#automate / finish unit tests
#handle multiple units getting same order
#board state object

#settings pre-set options
#morse mode / meme mode
#order parsing without the space. Eg A A-B or A A->B
#add multi-coast support

#adjacenct territory representation and rule enforcement.
#season / phase aware adjudication
#add variant rules support
#   ability to specify which units (or non units) can perform a convoy and what types of unit they may convoy
#   ability to specify which units should have the no-self-dislodge rules apply
#   ability to specify which order types are legal in a phase, and the ordering of phases / seasons
#   ability to turn certain support/convoy cutting rules on/off. 
#   ability to specify general unit adjacency graph (eg for more general unit types like aircraft and submarines)
#   ability to give territories the hidden property
DEBUG = True


#let make a basic move adjudicator
HOL = 'HOL'
MOV = 'MOV'
SUP = 'SUP'
CON = 'CON'
BLD = 'BLD'
DIS = 'DIS'
PCE = 'PCE'
WAR = 'WAR'
#convoy paradox settings
#rules for when support at the destination should be canceled
#case 1 is the fleet at the destination supports the convoy itself
#case 2 is the fleet at the destination supports an attack on the convoy

#cancel_rule = 'dislodged' #options are dislodged, support, biggest_force

#dislodged is the usual convoy breaking rule

#support means convoys are canceled in the same way as supports. dislodge not required.

#biggest_force means when a convoy is attacked by an enemy with more support than it is given, the convoy is canceled.
#note: you cant break your own convoys. note: rule applies to supports too when they are attacked from the province they support into


default_unit_types = {'A', 'F'}
default_seasons = ['Spring', 'Fall']
default_non_capturing_units = set()
default_allowed = {'O':{HOL, SUP, MOV, CON}, 'R':{MOV, DIS} ,'B':{BLD, DIS}}
default_disallowed = {
	'F MOV VIA A':('*','Fitzcarraldo Convoy not available'),
	'F MOV VIA F':('*','Portage not legal'),
	'F CON F':('*','Fleet too heavy'),
	'F CON F VIA A':('*','Fleet too heavy for piggyback ride'),
	'F CON F VIA F':('*','Remove men from boat then retry convoy'),
	'F CON A VIA A':('*','Not legal via'),
	'A MOV VIA A':('*','Cannot move through people'),
	'A CON A':('*','Piggyback rides not allowed in the army'),
	'A CON F':('*','Portage not available'),
	'A CON A VIA A':('*','Game is Diplomacy not Leapfrog'),
	'A CON F VIA A':('*','Fitzcarraldo Convoy not legal'),
	'A CON A VIA F':('*','No I will not carry you to the ferry'),
	'A CON F VIA F':('*','Neither unit capable of lifting F'),
	'F CON A':('L','Not permitted on land')
}

default_rules = {
	'convoy_kidnapping':False, 'implicit_convoys':True, 
	'cancel_rule':'dislodged',  'as_if_from_via':True, 'con_order_breaks_sup':False,
	'break_suphol_require_could_dis':False, 'break_suphol_require_no_paradox':False, 
	'break_supmov_require_could_dis':True,  'break_supmov_require_no_paradox':True,
	'bulid_anywhere':False, 'monotonic_builds':True, 'transactional_builds':False,
	'allowed_ords':default_allowed, 'disalllowed':default_disallowed,
	'unit_types':default_unit_types, 'season_order':default_seasons, 
	'non_capturing':default_non_capturing_units
}
#build season also needs settings, but idk what they will be


#to do: add morse code synonyms
syn_list = [
	['HOL', 'H', 'h', 'hol', 'Hol', 'hold', 'Hold', 'HOLD', 'kill_civilians'],
	['MOV', 'M', 'move', 'MOVE', '-->', '->', '-', 'to'],
	['SUP', 'S', 's', 'sup', 'Sup' 'support', 'supports', 'Support', 'Supports', 'SUPPORT', 'SUPPORTS', '+->'],
	['CON', 'C', 'c', 'con', 'Con', 'convoy', 'convoys', 'Convoy', 'Convoys', 'CONVOY', 'CONVOYS', '~>', '~~>'],
	['BLD', 'B', 'b', 'bld', 'Bld', 'build', 'Build', 'BUILD'],
	['DIS', 'D', 'd', 'dis', 'Dis', 'disband', 'Disband', 'DISBAND', 'X_X'],
	['A', 'Army', 'army', 'a', 'O7', 'o7'],
	['F', 'Fleet', 'fleet', 'f', '|_7']
]
wrd_list = [HOL, MOV, SUP, CON, BLD, DIS, 'A', 'F']
syn = dict()
for x in range(len(wrd_list)):
	for y in syn_list[x]:
		syn[y] = wrd_list[x]

# Army                O7 
# Fleet              |_7
# Hold               ---
# Move               -->
# Support            +->
# Convoy             ~~>
# Build (army)       ^_^
# Build (fleet)      ^|_7^
# Resolved           :-)
# Canceled           :-(
# Dislodged (army)   \o/
# Dislodged (fleet)  ~\o/~
# Disbanded (army)   X_X
# Disbanded (fleet)  ~~~
# Illegal            O_o

def is_morse(x):
	morse_set = {'.', '-', '/', ' '}
	for i in range(len(x)):
		if x[i] not in morse_set: return False
	return True

class board_territory:
	#needs to know:
	# name
	# type (land, sea)
	# adjacency list
	# coast names
	# is center?
	# initial owner
	# initial build
	# internal x anchor positions (for drawing on map)
	# internal y anchor positions (for drawing on map)
	pass


class board:
	#a collection of territories
	#needs to know:
	# territories (lookup by name)
	# map graphic
	#must be able to:
	# color everything in and display itself given territory colors
	# return initial units
	# load the initial territories and adjacency from a text file
	pass



class board_state:
	#needs to know:
	# year
	# season
	# phase
	# board_state_territories (lookup by name)
	# is blind?
	
	#must be able to:
	# build the next state from an adjudicated list of orders
	# count up the supply centers for each player
	pass

class unit:
	def __init__(t, player, unit_type, coast_pos = None):
		t.player = player
		t.unit_type = unit_type
		t.coast_pos = coast_pos

null_unit = unit('', '')
bounce = unit('','B')

class board_state_territory:
	#needs to know:
	# territory name
	# occupying unit
	# dislodged unit
	# dislodged from territory name
	# is a center?
	# initial owner
	# current owner
	def __init__(t, name, occupant = null_unit, dislodged = null_unit):
		t.name = name
		t.occu = occupant
		t.dis = dislodged
		#blahblahblah


class order:
	def __init__(t, player, unit_type='', territory='', ord_type='', destination='', helped='', *via):
		#def __init__(t, player, ord_str): #split this into a parser, switch back to a normal init
		t.morse_mode = False
		if unit_type not in syn:
			if unit_type == '': ord_str = player
			else: ord_str = unit_type
			t.morse_mode = is_morse(ord_str)
			if t.morse_mode: 
				pass #translate from morse
			temp = ord_str.split(' via ')
			via = []
			if len(temp) > 1: via = temp[1].split(' or ')
			temp = temp[0].split(' ')
			m = len(temp)-1
			destination = ''
			helped = ''
			unit_type = temp[0]
			territory = temp[min(m,1)]
			#implicit hold order goes here
			ord_type = temp[min(m,2)]
			if ord_type not in syn:
				destination = ord_type
				ord_type = MOV
			elif ord_type == MOV:
				destination = temp[min(m,3)]
			elif ord_type != HOL:
				helped = temp[min(m,3)]
				destination = temp[min(m,4)]
				if syn.get(destination, '') == MOV:
					destination = temp[min(m,5)]
				elif syn.get(destination, '') == HOL:
					destination = temp[min(m,3)]
		t.player = player
		t.terr = territory
		t.unit = syn.get(unit_type, unit_type)
		t.ord_type = syn.get(ord_type, ord_type)
		t.dest = destination
		t.helped = helped
		t.via = via
		t.cause = 'no matching unit'
		t.status = 'tentative' #(other possible values are dislodged, canceled and resolved)
		t.presolved = False
		t.done = False
		
	def clear(t):
		t.cause = ''
		t.status = 'tentative'
		t.presolved = False
		t.done = False
	
	def next_terr(t, curr = True):
		if (t.status not in ('tentative', 'resolved') and curr) or t.ord_type != MOV: return t.terr
		return t.dest
	
	def curr_ord(t):
		if t.status in ('tentative', 'resolved'): return t.ord_type
		return HOL
	
	def update_status(t, status, *cause):
		if status in ('resolved', 'dislodged'): t.done = True
		if t.status == 'canceled' and status == 'resolved': return
		elif t.status == 'dislodged': return
		elif status != t.status: t.cause = ''
		t.status = status
		if len(t.cause) > 0: t.cause += ', '
		for c in range(len(cause)):
			#if cause[c] == null_order: t.cause += 'no matching unit, '
			if cause[c] != t and (DEBUG or type(cause[c]) != int): 
				t.cause += str(cause[c])
				t.cause += ', '
		t.cause = t.cause.strip(', ') #remove erroneous comma here
	
	def __str__(t): 
		res = t.unit + ' ' + t.terr + ' ' + t.ord_type
		if t.ord_type != HOL:
			if t.ord_type != MOV:
				res += ' ' + t.helped + ' '
				if t.helped == t.dest: res += HOL
				else: res += MOV
			if t.ord_type != HOL: res += ' ' + t.dest
		if len(t.via) > 0:
			res += ' via ' + t.via[0]
			for v in range(1,len(t.via)):
				res += ' or ' + t.via[v]
		return res
	
	def report(t):
		res = str(t) + ' : '
		if t.status == 'canceled' and t.ord_type == MOV: res += 'bounced'
		else: res += t.status
		if t.status != 'resolved': res += ' by'
		res += ' ' + t.cause
		return res

null_order = order("","")


class order_set:
	def __init__(t, orders):
		t.default = {HOL:[], MOV:[], SUP:[], CON:[]}
		t.rule_set = dict()
		if type(orders) == str:
			temp = orders.split('\n')
			orders = []
			player = ''
			for x in temp:
				if x[-1] == ':': player = x.strip(':')
				elif len(x) > 0: orders.append(order(player,x))
		t.lookup_by_dest = dict()
		t.lookup_by_terr = dict()
		t.lookup_by_help = dict()
		t.lookup_by_player = dict()
		for x in orders:
			if x.dest not in t.lookup_by_dest: t.lookup_by_dest[x.dest] = {HOL:[], MOV:[], SUP:[], CON:[]}
			if x.helped not in t.lookup_by_help: t.lookup_by_help[x.helped] = {HOL:[], MOV:[], SUP:[], CON:[]}
			if x.player not in t.lookup_by_player: t.lookup_by_player[x.player] = []
			if x.dest != '': t.lookup_by_dest[x.dest][x.ord_type].append(x)
			if x.helped != '': t.lookup_by_help[x.helped][x.ord_type].append(x)
			t.lookup_by_terr[x.terr] = x #aww shit, what if same territory is given two orders (some or all of which are illegal?)
			t.lookup_by_player[x.player].append(x)

	def by_dest(t, dest, ord_type=None): return t.lookup_by_dest.get(dest, t.default).get(ord_type, [])
		
	def by_helped(t, helped, ord_type=None): return t.lookup_by_help.get(helped, t.default).get(ord_type, [])
		
	def by_terr(t, terr): return t.lookup_by_terr.get(terr, null_order)

	def by_player(t, terr): return t.lookup_by_player.get(player, [])

	def rule(t, rule): return t.rule_set.get(rule, default_rules[rule])

	def add_ord(t, ord_, overwrite = True):
		pass

	def remove_ord(t, terr):
		pass

	def copy(t):
		pass

	def __add__(t, o):
		pass

	def __iter__(t):
		for x in t.lookup_by_terr:
			yield t.lookup_by_terr[x]
	
	def __str__(t):
		res = ''
		for x in t.lookup_by_player: 
			res += x+':\n'
			for y in t.lookup_by_player[x]:
				res += y.report() + '\n'
			res += '\n'
		return res

	def occupying(t, terr):
		pass

	def dislodged(t, terr):
		pass

	def owns(t, terr):
		pass

	def autofill_convoys(oset, ord_):
		if not oset.rule('implicit_convoys'): return
		shouldfill = 'convoy' in ord_.via
		helps = oset.by_helped(ord_.terr, CON)
		badterr = []
		for x in helps:
			shouldfill = shouldfill or (x.player == ord_.player) or oset.rule('convoy_kidnapping')
			badterr += x.via
		if not shouldfill: return
		goodterr = []
		for x in helps:
			if x.terr not in badterr: goodterr.append(x.terr)
		ord_.via = goodterr
	
	def check_legal(oset, ord_, state = None, adj = None):
		if adj is not None:
			pass #check if valid adjacent move. check if allowed retreat
		if state is not None:
			pass #check if unit exists and belongs to player. check if move valid this season
		#make sure armies aren't attacking convoying fleets. that aint kosher
		if ord_.ord_type == CON and ord_.unit == 'A': ord_.update_status('canceled', 'Fitzcarraldo convoys not allowed.')
		elif ord_.ord_type == MOV and len(ord_.via) > 0 and ord_.unit == 'F': ord_.update_status('canceled', 'Fleet piggybacking not allowed.')

	def check_matching(oset, ord_):
		if ord_.ord_type not in [CON, SUP]: return True
		u = oset.by_terr(ord_.helped) #['terr'].get(ord_.helped, null_order)
		if ord_.dest != u.next_terr(False):
			ord_.update_status('canceled', u, 348)
			return False
		return True
	
	def support_level_n(oset, ord_, n, ignore_player = ''):
		s = 0
		unres_sup = []
		sups = oset.by_helped(ord_.terr, SUP) #['thrd'].get(ord_.terr, default)[SUP]
		for x in sups:
			if x.player != ignore_player or x.helped == x.dest: #don't ignore support holds
				if x.status == 'resolved': s += 1
				elif x.status == 'tentative': unres_sup.append(x)
		m = len(unres_sup)
		while n > s and s + m >= n and m > 0:
			m -= 1
			x = unres_sup.pop()
			oset.resolve_support(x)
			if x.status == 'resolved': s += 1
		return s >= n

	def most_supported(oset, ords, ignore_player = '', known_min = 0):
		newords = []
		for x in ords:
			if oset.support_level_n(x, known_min, ignore_player) and x != null_order: newords.append(x)
		if len(newords) < 2:
			oldords = []
			for x in ords: 
				if x not in newords: oldords.append(x)
			return newords, oldords
		return oset.most_supported(newords, ignore_player, known_min+1)


	def presolve_support(oset, ord_):
		if ord_.done or ord_.presolved or ord_.ord_type != SUP: return
		oset.check_matching(ord_)
		ord_.presolved = True
		breakers = oset.by_dest(ord_.terr, MOV) #.get(ord_.terr, default)[MOV]
		last = oset.by_terr(ord_.dest)
		if last.ord_type == CON: last = oset.by_terr(last.helped)
		can_res = True
		for x in breakers:
			if x != last: oset.presolve_move(x)
			can_res = can_res and len(oset.by_helped(x.terr)) == 0 #['thrd'].get(x.terr, default)[SUP]
		oset.presolve_move(last)
		if ord_.status == 'tentative': ord_.update_status('resolved', 392)
		elif can_res: ord_.done = True

	def presolve_move(oset, ord_):
		oset.presolve_support(oset.by_terr(ord_.next_terr()))
		if ord_.done or ord_.presolved or ord_.ord_type != MOV: return
		oset.autofill_convoys(ord_)
		ord_.presolved = True
		if len(ord_.via) > 0: oset.presolve_convoy(ord_)
		if ord_.status == 'canceled': return #the convoy failed, this is now a hold order
		if len(oset.by_dest(ord_.next_terr(), MOV)) == 0 and oset.by_terr(ord_.next_terr()) == null_order: # not in oset['terr']:
			ord_.update_status('resolved', 404)
			return #if the end is empty, resolve now
		occu = oset.by_terr(ord_.next_terr())#['terr'].get(ord_.next_terr(),null_order)
		if occu.status == 'canceled': return
		if occu.ord_type == SUP and occu.player != ord_.player:
			targ = oset.by_terr(occu.dest)
			if targ == ord_ and (len(ord_.via)==0 or not oset.rule('as_if_from_via')): #apply rule 'as if from via' here
				oset.resolve_hold(occu)
				return
			if targ.ord_type == CON and targ.helped == ord_.terr:
				oset.resolve_hold(occu)
				return
			occu.update_status('canceled', ord_, 411)

	def paradox_police(oset, con, sup):
		m = oset.by_terr(con.helped)
		if sup.status in ('canceled', 'dislodged') or sup.ord_type != SUP or sup.player == m.player: return
		if sup.dest != con.terr: 
			sup.update_status('canceled',  m, 418)
			return
		if sup.dest == sup.helped:
			req_no_par = oset.rule('break_suphol_require_no_paradox')
			req_dis = oset.rule('break_suphol_require_could_dis')
			if oset.rule('con_order_breaks_sup'): 
				sup.update_status('canceled',  m, 426)
				req_no_parq = True
			#check this rule here
		else:
			req_no_par = oset.rule('break_supmov_require_no_paradox')
			req_dis = oset.rule('break_supmov_require_could_dis')
		if req_dis:
			w,c = oset.most_supported(oset.by_dest(sup.terr,MOV)+[sup])
			if len(w) == 0 or sup in w: 
				m.update_status('canceled', sup, 436)
				return
			w,c = oset.most_supported(w + [sup], sup.player)
			if len(w) == 0 or sup in w: 
				m.update_status('canceled', sup, 440)
				return
		if req_no_par:
			og = sup.status
			sup.status = 'resolved' #temp so we can sort of resolve it
			w0,c0 = oset.most_supported(oset.by_dest(con.terr, MOV)+[con])
			w1,c1 = oset.most_supported(w0+[con], con.player)
			sup.status = 'canceled'
			w2,c2 = oset.most_supported(oset.by_dest(con.terr, MOV)+[con])
			w3,c3 = oset.most_supported(w2+[con], con.player)
			sup.status = og
			withsup = len(w0) == 0 or w0[0].player == con.player
			nosup = len(w2) == 0 or w2[0].player == con.player
			if withsup and not nosup:
				withsup = len(w1) == 0 or w1[0].player == con.player
				nosup = len(w3) == 0 or w3[0].player == con.player	
				if withsup and not nosup: 
					m.update_status('canceled', sup, 'paradox rule', 456)
					return
		sup.update_status('canceled',  m, 440)


	def presolve_convoy(oset, ord_, prev = []):
		h = ord_.terr
		if len(ord_.via) == 0: 
			if ord_.ord_type == MOV: return
			#ord_.presolved = True
			targ = oset.by_terr(ord_.dest) #['terr'].get(ord_.dest, null_order)
			oset.paradox_police(ord_, targ)
		if ord_.ord_type == CON:
			h = ord_.helped
			oset.resolve_hold(ord_)
			if not oset.check_matching(ord_): return
			if len(ord_.via) == 0: return
		if ord_.status in ('dislodged', 'canceled'): return
		cause = []
		unres_con = []
		notdone = True
		for x in ord_.via:
			c = oset.by_terr(x) #['terr'].get(x, null_order)
			if c not in prev and c.ord_type == CON and c.helped == h and c.dest == ord_.dest and c.unit == 'F':
				if c.status == 'resolved':
					#ord_.presolved = True
					cause = []
					notdone = False
					if ord_.ord_type == CON: return
				elif c.status == 'tentative': unres_con.append(c)
				elif notdone: cause += [c]
		for c in unres_con:
			if c not in prev and c.ord_type == CON and c.helped == h and c.dest == ord_.dest and c.unit == 'F':
				oset.presolve_convoy(c, prev + [ord_])
				if c.status == 'resolved':
					#ord_.presolved = True
					cause = []
					notdone = False
					if ord_.ord_type == CON: return
				elif notdone: cause += [c]
		if notdone:
			#print(ord_.report())
			ord_.status = 'canceled'
			if len(cause) == 0: ord_.cause = 'no matching convoys 503'
			else:
				for c in cause:
					if c.status == 'dislodged': ord_.cause += c.terr + ' dislodged 506, '
					else: ord_.cause += c.cause +' 507, '

	def resolve_empty(oset, terr, res_winner = True):
		conf0 = oset.by_dest(terr,MOV) #['dest'].get(terr, default)[MOV]
		conf = []
		for x in conf0:
			oset.presolve_move(x)
			if x.next_terr() == terr: conf.append(x)
		best, cause = oset.most_supported(conf)
		for x in conf: 
			if x not in best: x.update_status('canceled', *(best+cause+[491]))
		if len(best)>0 and res_winner:
			best[0].update_status('resolved', 493)
		return best

	def resolve_hold(oset, ord_):
		winner = oset.resolve_empty(ord_.terr, False)
		if len(winner) > 0:
			if winner[0].player == ord_.player: winner[0].update_status('canceled', ord_, 499)
			else:
				if ord_.ord_type != MOV: winner += [ord_]
				winner2, c = oset.most_supported(winner, ord_.player, 1)
				if len(winner2) > 0:
					if ord_ in winner2:
						winner[0].update_status('canceled', ord_, 505)
					else:
						winner[0].update_status('resolved',507)
						ord_.update_status('dislodged', winner[0],508)
				elif ord_ != winner[0]:
					winner[0].update_status('canceled', ord_,510)
					if winner[0].ord_type == MOV: 
						oset.presolve_move(winner[0])
						oset.resolve_hold(winner[0])
		if ord_.status == 'tentative': ord_.update_status('resolved', 514)
		ord_.done = True

	def resolve_support(oset, ord_):
		oset.presolve_support(ord_)
		if not ord_.done: oset.resolve_hold(ord_)
			
	def resolve_convoy(oset, ord_):
		mov = oset.by_terr(ord_.helped) #['terr'].get(ord_.helped, null_order)
		if mov.ord_type != MOV: ord_.update_status('canceled', mov, 523)
		else: oset.presolve_move(mov)
		if ord_.status == 'tentative': ord_.update_status('canceled', mov.cause, 525)
		#resolve_hold(oset, ord_)

	def resolve_move(oset, ord_, orig = ''):
		if ord_.done: return
		if ord_.ord_type != MOV: 
			oset.resolve(ord_)
			return
		oset.presolve_move(ord_)
		if oset.by_terr(ord_.next_terr()) == null_order:
			oset.resolve_empty(ord_.dest)
			return
		occu = oset.by_terr(ord_.next_terr()) #['terr'][ord_.next_terr()]
		oset.presolve_move(occu)
		if occu.next_terr() == occu.terr:
			oset.resolve_hold(occu)
			#if ord_.status == 'tentative': resolve_hold(oset, ord_)
			return
		
		#print(ord_.next_terr(), occu.terr, occu.next_terr(), occu.terr,  len(occu.via) + len(ord_.via))
		if ord_.next_terr() == occu.terr and occu.next_terr() == ord_.terr and len(occu.via) + len(ord_.via) == 0:
			tugowar = [ord_, occu]
			best, cause = oset.most_supported(tugowar)
			for x in tugowar:
				if x not in best:
					x.update_status('canceled', *cause,550)
			if ord_.status == 'canceled': oset.resolve_hold(ord_)
			else: oset.resolve_move(occu)
			return 
		
		canquit = occu.status == 'resolved' or occu.terr == orig
		best = oset.resolve_empty(ord_.next_terr(), canquit)
		if ord_ not in best:
			oset.resolve_hold(ord_)
			return
		if canquit:
			ord_.done = True
			return
		if len(orig) == 0: orig = ord_.terr
		oset.resolve_move(occu, orig)
		if occu.status == 'resolved': 
			ord_.update_status('resolved', 566)
			return
		oset.resolve_hold(occu)
		if ord_.status != 'resolved':
			#ord_.update_status('canceled', ('traffic jam', occu))
			oset.resolve_hold(ord_)
		ord_.done = True

	def resolve(oset, ord_):
		if ord_.done: return
		elif ord_.ord_type == MOV: oset.resolve_move(ord_)
		elif ord_.ord_type == SUP: oset.resolve_support(ord_)
		elif ord_.ord_type == CON: oset.resolve_convoy(ord_)
		elif ord_.ord_type == HOL: oset.resolve_hold(ord_)

	def post_resolve(oset, ord_, adj = None):
		if ord_.ord_type not in (SUP, CON) or ord_.status != 'resolved': return
		h = oset.by_terr(ord_.helped)
		if h.status == 'resolved': return
		verb = ' supported '
		if ord_.ord_type == CON: verb = ' convoyed '
		ord_.cause += ' (but'+verb+'unit '+h.unit+' '+ord_.helped+' '+h.status+' by '+h.cause+')'

def adjudicate(orders, phase = 'order', season = 'S', year = 1, state = None, adj = None, **rule_set):
	if type(orders) in (str, list):
		orders = order_set(orders)
	orders.rule_set = rule_set
	for x in orders:
		x.clear()
		orders.check_legal(x, state, adj)
	for x in orders:
		orders.resolve(x)
	for x in orders:
		orders.post_resolve(x)
		#finally check if any dislodges are forced to disband
		#put caveats on supports/convoys for broken orders
		#do whatever cleanup
		pass
	print(orders)
	#the creation of a new game state object goes here


#what's needed here is a basic order generator. Then the adjudicator coupled with some game_state
#metric can tell us the payoff of each strat, and that's basically the matrix oracle that we need