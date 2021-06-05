HOL = 'HOL'
MOV = 'MOV'
SUP = 'SUP'
CON = 'CON'
BLD = 'BLD'
DIS = 'DIS'
DEC = 'DEC' #this is for the 'war and peace declarations' variant
DEF = 'DEF' #this is a hack for my submarine / airplane variant idea
NUL = ''
nobody = ''
yes = 1
no = -1
maybe = 0

DEBUG = True
DEBUG_PRINT = False
#add morse syns
syn_list = [
    ['HOL', 'H', 'HOLD', 'HOLDS', 'KILL_CIVILANS'],
    ['MOV', 'M', 'MOVE', 'MOVES', 'TO', '-->', '->', '-'],
    ['SUP', 'S', 'SUPPORT', 'SUPPORTS', '+->'],
    ['CON', 'C', 'CONVOY', 'CONVOYS', '~>', '~~>', '~->'],
    ['BLD', 'B', 'BUILD', 'BUILDS', '$_$'],
    ['DIS', 'D', 'X', 'DISBAND', 'DISBANDS', 'X_X'],
    ['DEF', 'DFN', 'DEFEND', 'DEFENDS','-)','--)'],
    ['WAR', ':<'],
    ['PEACE','PCE','<3'],
    ['Orders','ORDERS','ORDER'],
    ['Retreat', 'RETREAT', 'RETREATS'],
    ['Spring', 'SPRING'],
    ['Fall', 'FALL'],
    ['A', 'Army', 'army', 'a', 'O7', 'o7'],
    ['F', 'Fleet', 'fleet', 'f', '|_7']
]


syn = dict()
for x in range(len(syn_list)):
    for y in syn_list[x]:
        syn[y] = syn_list[x][0]

#new stuff after here
morsetable = dict()
memetable = {'A':'O7', 'F':'|_7', 'U':'?7', HOL:'---', MOV:'-->', SUP:'+->', CON:'~~>', BLD:'$$', DIS:':X', DEC:':O', DEF:'--)'}
notable = dict()

memes = ['O7', '|_7', '---', '-->', '+->', '~~>', '++',':X', '<3', ':<']

def parse(ordl, player = nobody, unit_types = ['_','*','A','F'], seasons = ['Spring', 'Fall'], phases = ['Orders', 'Retreat', 'Build'], year = 1901, inner = 'self', fres=[], fict=False):
    if len(ordl) == 0: return []
    if len(fres) == 0: fres.append((order_set(seasons[0],phases[0],year), state(seasons[0],phases[0],year)))
    if type(ordl) == str:
        #first do some data sanitization
        sp = ' / '
        for m in range(len(ordl)): 
            if ordl[m] not in '.-/ ': sp = ' '
        ords = ordl.split('\n')
        if len(ords) > 1:
            for i in range(len(ords)):
                if len(ords[i]) > 0 and sp not in ords[i]: player = ords[i]
                else: parse(ords[i], player, unit_types, seasons, phases, year, inner, fres, fict)
            return fres
        newordstr = ''
        if sp == ' / ': #we are in morse mode
            ords = ordl.split(' ') #split into letters
            ordl = ''
            for i in ords:
                pass #lookup morse here
        for i in range(len(ordl)-1):
            if not (ordl[i] == ' ' and ordl[i+1]  in '( '): newordstr += ordl[i]
            if ordl[i] not in ' ~+-' and ordl[i+1] in '~+-': newordstr += ' '
            if ordl[i+1] not in ' ->' and ordl[i] in '->': newordstr += ' '
        newordstr += ordl[-1]
        ordl = newordstr.split(sp)
    #figure out if we have the start of a new ord set, process it here
    w = lookup(ordl[0])
    w2 = w.strip('):').split('(')
    w2[0] = lookup(w2[0])
    if w2[0] in seasons or w2[0] in phases: #or is numeric
        s,p,y = seasons[0], phases[0], year
        ordl = w2 + ordl[1:]
        for i in range(len(ordl)):
            ii = ordl[i].strip('):').split('(')
            for j in ii:
                w = lookup(j)
                if w in seasons: s = w
                elif w in phases: p = w
                elif True: y = int(w) #elif numeric
        if len(fres[0][0]) == 0: fres.pop()
        fres.append((order_set(s,p,y), state(s,p,y)))
        return fres
    #now process lines which represent individual orders
    if w == DEC:
        return #do declarations here!
    if w in ('LAND', 'CONVOY'): return parse(ordl[1:]+['OR'], player, unit_types, seasons, phases, year, inner, fres, True) + [w]
    if w == 'VIA': return parse(ordl[1:]+['OR'], player, unit_types, seasons, phases, year, inner, fres, True)
    if w in (BLD, DIS): ordl = ordl[1:] + [w]
    if lookup(ordl[0]) not in unit_types: ordl = [unit_types[0]] + ordl
    if len(ordl) < 3: ordl += [NUL]
    ut, terr, ot = lookup(ordl[0]), fres[-1][1].get_t(ordl[1],autofill=True), lookup(ordl[2])
    ut = unit(player, ut)
    ordl = ordl[3:]
    if ot == 'OR': return [order(nobody, ut, terr, CON, inner, inner.dest)] + parse(ordl, nobody, unit_types, seasons, phases, year, inner, fres, True)
    if ot not in (HOL, MOV, SUP, CON, BLD, DIS, DEF, DEC, 'VIA', 'OR'):
        ordl = [ot] + ordl
        ot = MOV
    if ot in (SUP, CON):
        inner = parse(ordl, nobody, unit_types, seasons, phases, year, 'self', fres, True)
        via = inner.via
        inner.via = []
        res = order(player, ut, terr, ot, inner, inner.dest, *via)
        if not fict: 
            terr.add_u(ut)
            ut.add_o(res)
            fres[-1][0].add_o(res)
        return res
    if len(ordl) == 0: ordl = [terr.name] + ordl
    dest = fres[-1][1].get_t(ordl[0],autofill = True)
    ordl = ordl[1:]
    res = order(player, ut, terr, ot, 'self', dest)
    via = parse(ordl, nobody, unit_types, seasons, phases, year, res, fres, True)
    res.via = via
    if not fict: 
        terr.add_u(ut)
        ut.add_o(res)
        fres[-1][0].add_o(res)
    return res


class rulebook:
    #this needs to contain:
    #the disruption rules (aka the equations of Diplomacy)
    #the disallowed templates (the orders that are not allowed)
    #maybe some other shit. idk. 

    #disruption rules need to be applied in the following order
    #canceled from outside destination (towards next_terr), canceled from destination (towards current terr) ,
    #then, if canceled, the dislodged rule applies from anywhere
    #canceled from destination only applies when destination points back (head to head case)
    #there is more than one head-to-head case. 

    # A --> B -->
    # A <-> B
    # A --> <-- B

    #When is B canceled from the outside (A --> B)
    #           |  A move    | A move via  | A convoy | A sup mov  | A sup hol |
    #B move     |  never     | never       | never    | never      |  never    |
    #B move via |  never     | never       | never    | never      |  never    |
    #B convoy   | any* > all | any* > all  |          |            |  never    |
    #B sup mov  | any* > 0   | any* > 0    |          | never      |  never    |
    #B sup hol  | any* > 0   | any* > 0    |          | never      |  never    |
    
    #When is B canceled at the destination (A <-- B )
    #           |  A move    | A move via  | A convoy | A sup mov  | A sup hol |
    #B move     |            |             |  A >= B  |  A >= B    | A >= B    |
    #B move via |            |             |          |  A >= B    | A >= B    |
    #B convoy   |  never     |   never     |          |            |           |
    #B sup mov  |  never     |   never     |  never   |  never     | never     |
    #B sup hol  |  never     |   never     |  never   |  never     | never     |

    #When is B canceled by directly opposed tail to head order (A <--> B)     |
    #           |  A move   | A move via | A convoy | A sup mov  | A sup hol  |
    #B move     |  A >= B   |  A >= B    |  A >= B  |  A >= B    |  A >= B    |
    #B move via |  A >= B   |  A >= B    |  A >= B  |  A >= B    | any* > [B] |
    #B convoy   |  A* > all | any* > all |  never   | any* > [B] | any* > [B] |
    #B sup mov  |  A* > all | any* > all |  never   |   never    |   never    |
    #B sup hol  |  A > 0    | any* > all |  never   |   never    |   never    |

    #When is B canceled by a looping rule  |-->A-->B--|
    #           |  A move    | A move via  | A convoy | A sup mov  | A sup hol |
    #B move     |  never     |             |          |            |           |
    #B move via |            |             |          |            |           |
    #B convoy   |            |             |          |            |           |
    #B sup mov  |            |             |          |            |           |
    #B sup hol  |            |             |          |            |           |

    #When is B dislodged given it is already canceled A --> B
    #           | A move     | A move via
    #B move     | any* > all |
    #B move via |            |
    #B convoy   | any* > all |
    #B sup mov  | any* > all |
    #B sup hol  | any* > all |
    #B hold     | any* > all |


    #possible rules: never, any, >=, >, >=all, >all, always 
    #* means the opposing orders must not depend on support from (or be of) the same nation as B (AKA the self dislodge rules) 
    #[X] means all the units in the conflict at X with the same nationality of X. 
    

    #some settings to eventually incorporate 
    #default_rules = {
    #   'convoy_kidnapping':False, 'implicit_convoys':True, 'friendly_passthrough':False,
    #   'cancel_rule':'dislodged',  'as_if_from_via':True, 'con_order_breaks_sup':False,
    #   'break_suphol_require_could_dis':False, 'break_suphol_require_no_paradox':False, 
    #   'break_supmov_require_could_dis':True,  'break_supmov_require_no_paradox':True,
    #   'bulid_anywhere':False, 'monotonic_builds':True, 'transactional_builds':False
    #}

    def __init__(t):

        t.sp = [
            "Spring", ["order", "retreat"],
            "Fall", ["order", "retreat", "build" ]
        ]

        t.outside_rule = {
            MOV:'>=', CON:'>all*', SUP:'any*', HOL:'any*'
        }
        t.tugowar_rule = {
            MOV:{MOV:'>=', CON:'', SUP:'none', HOL:'none'},
            CON:{MOV:'', CON:'', SUP:'', HOL:''},
            SUP:{MOV:'', CON:'', SUP:'', HOL:''},
            HOL:{MOV:'any*', CON:'never', SUP:'never', HOL:'never'}
        }
        t.dis_rule = {MOV:'1*', CON:'N*', SUP:'N*', HOL:'N*'}
        
        x = parse('''MATCHING_SUPPORTS UNRESOLVED 1901
helper
* A SUP * B MOV C
* A SUP * B MOV C
* A SUP * B HOL
* A SUP * B HOL
* A SUP * B HOL
* A SUP * B HOL
* A SUP * B HOL

helped
* B MOV C
* B MOV C via F D
* B SUP * D MOV E
* B SUP * D HOL
* B HOL
F B CON A C MOV D
F B CON A C MOV E via F D

MATCHING_SUPPORTS CANCELED 1901
helper
* A SUP * B HOL
* A SUP * B HOL
* A SUP * B HOL
* A SUP * B HOL
* A SUP * B HOL

helped
* B SUP * D MOV E
* B SUP * D HOL
* B HOL
F B CON A C MOV D
F B CON A C MOV E via F D

MATCHING_CONVOYS UNRESOLVED 1901
helper
F A CON A B MOV C
F A CON A B MOV C

helped
* B MOV C
* B MOV C via F D

MATCHING_VIA UNRESOLVED 1901
helped
A A MOV D via F B
A A MOV D via F B
F B CON A A MOV D via F C

helper
F B CON A A MOV D
F B CON A A MOV D via F C
F C CON A A MOV D

''', fres = [], seasons=['MATCHING_SUPPORTS', 'MATCHING_CONVOYS', 'MATCHING_VIA'], phases=['UNRESOLVED', 'CANCELED'])

        t.sup_rules = (x[0][0].ords['helped'], x[0][0].ords['helper'])

    def sup_min_max(t, ord_, ignore = ''):
        return 0, 1 #temp

    def has_more_sup(t, any_A = [] , all_B = [], or_equal = False, ignore = ''):
        maxmin = 0
        maxmax = 0
        best = None
        for x in any_A + all_B:
            a, b = t.sup_min_max(x, ignore)
            maxmin = max(a, maxmin)
            if b > a and b > maxmax:
                best = x
                maxmax = b
        newAB = [[],[]]
        oldAB = [any_A, all_B]
        for i in range(2):
            for x in oldAB[i]:
                a, b = t.sup_min_max(x, ignore)
                if b >= maxmin: newAB[i].append(x)

        if len(newAB[0])*len(newAB[1]) == 0:
            if or_equal: return len(newAB[0]) >= len(newAB[1])
            return len(newAB[0]) > len(newAB[1])
        elif best is None: return or_equal
        #resolve a support for  best
        #return t.has_more_sup(newAB[0], newAB[1], or_equal, ignore)


    def resolve_t2h(t, ord1, ord2):
        pass

    def resolve_h2h(t,ord_, conf):
        pass

    def resolve_upto_convoy(t, ord_):
        pass

    def resolve_upto_cancel(t, ord_):
        #first, check convoys
        #then, check dest (or via) to terr (tail to head case)
        #then, check head to head (aka from outside) canceling rule
        #last, check hdest to terr (also a head to head case)
        pass

    def ez_res(t, ord_):
        pass

    def resolve(t, ord_):
        pass

    def adjudicate(t, ords, state = None, adj = None):
        #first, check *valid* against the known state
        #    fill in any missing hold orders while here
        #then, check *legal* against the adjacency
        #    if implicit convoys allowed, fill in the missing via info while here
        #then, check *legal* against the template book
        #now we can fill in all the relations (ords.prep_ords)
        #then, check *matching* against the matching rule

        #that concludes the pre adjudication steps

        pass
    
def lookup(wrd, tab = notable):
    wrd = wrd.upper()
    wrd = syn.get(wrd, wrd)
    wrd = tab.get(wrd, wrd)
    return wrd

def streq(s1,s2):
    if s1 == '*' or s2 == '*': return True
    if lookup(s1) == lookup(s2): return True
    return False

def debugstr(s, iden):
    if DEBUG_PRINT: return iden+'<'+s+'>'
    return s
    
null_terr = NUL #these will be redefined later lol
null_order = NUL
null_unit = NUL
null_oset = NUL

class unit:
    def __init__(t, player, unit_type):
        t.player = player
        t.ut = unit_type
        t.dis_from = null_terr
        t.ord = null_order
        t.conflicting = []

    def __str__(t):
        res = ''
        if t.dis_from != null_terr: res += '~'
        res += t.ut
        return debugstr(res,'unit')

    def __and__(t,o):
        return streq(t.ut,o.ut) #streq(t.player, o.player)
        
    def summary(t, pov = '*', mememode = False, morsemode = False):
        table = notable
        if mememode: table = memetable
        if morsemode: table = morsetable
        if streq(pov, t.player): return lookup(t.ut, table)
        return ''

    def add_o(t, ord_, replace = False): 
        if not streq(ord_.player,t.player) or not streq(ord_.ut.ut, t.ut):
            return
        if replace or t.ord == null_order: 
            t.ord = ord_
            return
        t.conflicting.append(ord_)
        cause = t.conflicting+[t.ord]
        ord_.update_status('legal', False, *cause)
        if len(t.conflicting) == 1:
            t.ord.update_status('legal', False, ord_)
            t.conflicting.append(t.ord)
            t.ord = order(t.player, t, t.ord.terr, HOL, 'self', t.ord.terr)
        
    def get_o(t, to = '*', autofill = False): return t.ord

    def add_u(t, to = '*', replace = False):
        pass #hmm. this feels like the bottom of some recursion I never finished
    
    def get_u(t, to = '*', autofill = False):
        if to[0] == '~': to = to[1:]
        if streq(to, t.ut): return t
        return null_unit
    
    def clear(t):
        t.conflicting.clear()
        t.ord = null_order
        t.dis_from = t

class territory:
    def __init__(t, name, terr_type = '*', center = False, hidden = False):
        name = name.split('(')
        t.name = name[0]
        t.terr_type = terr_type
        t.center = center
        t.hidden = hidden
        t.owner = ''
        t.init_owner = ''
        t.occu = null_unit
        t.disl = null_unit
        t.coasts = dict()
        t.perse = order('','_',t,NUL,'self','')
        t.conflicting = []
        if len(name)>1: t.add_c(name[1].strip(')'))

    def __str__(t):
        res = ''
        if t.owner == 'rule':
            res = 'in a'
            if t.name[0] in '<[(' and t.name[-1] in ')]>': res += t.name.strip('<[]>')
            if '*' in t.name:
                res += 'ny '
            if '!' in t.name: res += 'n occupied '
            if '-' in t.name: res += 'hidden '
            if '.' in t.name: res += 'supply center '
            elif len(res)>2: res += 'territory'
            else: res += t.name
        else:
            if t.hidden: res += '-'
            if t.center: res += '*'
            res += t.name
        if len(t.coasts)>0:
            res += '('
            for c in t.coasts: res += c + ','
            res = res[:-1]
            res += ')'
        return debugstr(res, 'territory')

    def __and__(t, o):
        if streq(t.name, o.name) and streq(t.terr_type, o.terr_type):
            return t.occu & o.occu
        return False

    def summary(t, pov = '*', table = notable):
        if not streq(pov, t.owner): return ''
        return lookup(t.name, table)

    def add_c(t, c, replace = False):
        if c in '_~*': return
        if not replace:
            pass #do some checks to see if this is the conflicting case
        if c not in t.coasts:
            t.coasts[c] = territory(c, t.terr_type, t.center, t.hidden)

    def get_c(t, c, autofill = False):
        if c == '*': return t
        if str(c) in t.coasts: return t.coasts[str(c)]
        if autofill:
            pass
        return null_terr
    
    def add_u(t, u, to = '*', replace = False):
        if not replace:
            pass #do some checks to see if this is the conflicting case
        to2 = to[0]
        if to2 not in '_~*': to2 = '*'
        coast = to.strip('_~*')
        if len(coast) > 0:
            t.add_c(coast, replace)
            t.coasts[coast].add_u(u, to2 , replace)
            u = t.coasts[coast]
        if to2 == '~': t.disl = u
        elif to2 == '_': pass
        else: t.occu = u
    
    def get_u(t, to = '*', autofill = False):
        if to[0] == '~': u = t.disl.get_u(to)
        elif to[0] == '_': u = t.perse.ut.get_u(to)
        elif to == '*': u = t.occu.get_u(to)
        elif len(to) > 0: u = t.get_c(to.strip('*')).get_u(to)
        if u == null_unit and autofill:
            u = unit('*', to)
            t.add_u(u)
        return u
        

    def add_o(t, o, to='*', replace = False):
        u = t.get_u(to, replace)
        if u != null_unit: u.add(o)

    def get_o(t, to = '*', autofill = False):
        u = t.get_u(to)
        if u == null_unit: return t.perse
        return u.get_o()


class declaration:
    def __init__(t, player, dec_type = 'WAR', targplayer = '*'):
        t.player = player
        t.dec_type = dec_type
        t.targplayer = targplayer

    def __str__(t): 
        return debugstr(t.player +' declares '+t.dec_type+' with '+t.targplayer+'!','declaration')
        
    def summary(t, pov = '*', table = notable):
        # <3                    peace declared
        # :<                    war declared
        return t.player+' '+'declares'+lookup(t.dec_type, table)+' '+'with'+' '+t.targplayer+'!'

class order:
    def __init__(t, player, unit_type = null_unit, terr = null_terr, ord_type = NUL, helped = 'self', dest = null_terr, *via):
        t.player = player
        t.tab = notable
        #autoparse here
        t.ut = unit_type
        t.terr = terr
        t.ord_type = ord_type
        if helped == 'self': t.helped = t
        else: t.helped = helped
        t.hdest = dest
        t.hterr = t.helped.terr
        if t.ord_type != MOV: t.dest = terr
        else: t.dest = dest
        t.via = via
        t.info = dict()
        t.clear_results()
        t.clear_relations()

    def occu(t): return t.tab.get(str(t.ut), str(t.ut))+t.tab.get(' ', ' ')+t.home()

    def home(t): return str(t.terr)

    def facing(t): return str(t.hdest)
    
    def __str__(t):
        s = t.tab.get(' ', ' ')
        ut = t.tab.get(str(t.ut), str(t.ut))
        ot = t.tab.get(t.ord_type, t.ord_type)
        hot = t.tab.get(t.helped.ord_type, t.helped.ord_type)
        res = t.occu()
        if t.ord_type != '':
            if t.ord_type != MOV: res += s+ot
            if t.ord_type in (SUP, CON): res += s+t.helped.occu()
            if t.ord_type not in (HOL, DIS, BLD): res += s+hot+s+t.facing()
        w = s+t.tab.get('via','via')+s
        w2 = s+t.tab.get('or','or')+s
        for v in t.via:
            res += w + v.occu()
            w = w2
        return debugstr(res,'order')

    def summary(t, pov = '*', mememode = False, morsemode = False): #not done
        if mememode: t.tab = memetable
        if morsemode: t.tab = morsetable
        res = str(t)
        if t.status != 'tentative':
            res += ': '+t.status
            # ['legal', 'match', 'path', 't2h', 'h2h', 'disl']
        return res

    def __and__(t, temp): #not done
        if not temp.ut & t.ut: return False
        if not temp.terr & t.terr: return False
        if not streq(t.ord_type, temp.ord_type): return False
        if t.ord_type in (SUP, CON) and not (temp.helped & t.helped): return False
        if not temp.hdest and t.hdest: return False
        #last, check the via's. This will be tedious.
        return True

    def clear_results(t):
        #1 for not canceled , -1 for canceled, 0 for unknown
        #for x in ['legal', 'match', 'path', 't2h', 'h2h', 'disl']: t.info[x] = 0
        t.checked = {'valid':False, 'legal':False, 'match':False, 'path':False, 't2h':False, 'h2h':False,'final':False}
        t.stage = ''
        t.face = ':/'
        t.status = 'tentative'

    def update_status(t, status, stage, face ='', code=0, *cause):
        t.checked[stage]=True    
        #if stage != t.stage: t.cause.clear()
        print(t, stage, status, code, face)
        t.dislodged = t.dislodged or (stage == 'final' and not status)
        t.canceled = t.canceled or t.dislodged or not status
        if t.dislodged and t.status != 'dislodged':
            t.status = 'dislodged'
            t.cause.clear()
            t.stage = stage
            t.face = face
        if t.canceled and t.status not in ('dislodged', 'canceled'):
            t.status = 'canceled'
            t.cause.clear()
            t.stage = stage
            t.face = face
        for x in t.checked: status = status and t.checked[x]
        if status:
            t.resolved = True
            t.status = 'resolved'
            t.stage = stage
            t.face = face
        t.cause += cause
        t.codes += [code]
        

    def quick_res(t):
        if t.ord_type != CON and len(t.via) == 0:
            t.update_status(True, 'path', ':)', 546)
        if t.ord_type not in (SUP, CON) and len(t.via) == 0:
            t.update_status(True, 'match', ':)', 548)
        if len(t.to_dest) == 0:
            t.update_status(True, 'h2h', ':)', 548)
        if t.at_hdest.dest != t.terr:
            t.update_status(True, 't2h', ':)', 548)
        
    def clear_relations(t):
        t.at_hdest = t
        t.at_hterr = t
        t.to_dest = set()
        t.to_terr = set()
        t.cons = set()
        t.sups = set()
        t.cause = []
        t.codes = []
        t.canceled = False
        t.resolved = False
        t.dislodged = False
        t.inprog = False

    def fill_relations(t):
        t.at_hdest = t.hdest.get_o()
        t.at_hterr = t.hterr.get_o()
        if t.ord_type in (MOV, DEF):
            t.at_hdest.add_o(t)
            t.to_dest = t.at_hdest.to_terr
        if t.ord_type == SUP: t.at_hterr.add_o(t)
        for i in t.via: t.add_o(i.terr.get_o())

    def add_o(t,o):
        if o == null_order: return
        if o.ord_type == CON: t.cons.add(o)
        if o.ord_type == SUP: t.sups.add(o)
        if o.terr == t.hterr: t.at_hterr = o
        if o.terr == t.hdest: t.at_hdest = o
        else:
            if o.dest == t.dest: t.to_dest.add(o)
            if o.dest == t.terr: t.to_terr.add(o)

    def remove_o(t,o):
        if o in t.cons: t.cons.remove(o)
        if o in t.sups: t.sups.remove(o)
        if o in t.to_terr: t.to_terr.remove(o)
        if o in t.to_dest: t.to_dest.remove(o)
        if o & t.at_hterr: t.at_hterr = null_order
        if o & t.at_hdest: t.at_hdest = null_order

    def copy_names(t, o):
        t.terr.name = o.terr.name
        t.dest.name = o.dest.name
        if t.helped != t: t.helped.copy_names(o)
        for i in range(min(len(o.via), len(t.via))):
            t.via[i].copy_names(o.via[i])
        
    def check_valid(t):
        u = t.terr.get_u()
        f = t.ut.summary('*', mememode = True)
        if u == null_unit:
            v=f[:-2]+'?'
            t.update_status(False,'valid',v, 415, t.at_hterr)
        if u.ord != t:
            t.update_status(False, 'legal', f, 416, u.conflicting)

    def check_legal(t, law):
        if t & law:
            f = t.ut.summary('*', mememode = True)
            t.update_status(False, 'legal', f, 417, law)
            t.at_hterr.remove_o(t)

    def check_map(t, adj):
        pass
    
    def check_matching_ord(t, inner, outter, ord_type = SUP):
        if t.ord_type != ord_type: return
        for i in range(len(outter)):
            outter.copy_names(t)
            inner.copy_names(t.at_hterr)
            if t & outter: 
                t.update_status(True, 'match', ':)', code=620)
                return
        t.update_status(False, 'match', ':(', 622, t.at_hterr)

    def check_matching_via(t, inner, outter):
        pass
    

class state:
    def __init__(t, season, phase, year):
        t.terrs = dict()
        t.units = dict()
        t.decs = dict()
        t.sc = dict()
        t.prev_ords = null_oset
        t.ref_board = t
        t.season, t.phase, t.year = season, phase, year

    def add_t(t, terr, coast = '*', replace = False):
        if replace:
            pass #do some checking
        t.terrs[str(terr)] = terr
        terr.add_c(coast)

    def get_t(t, terr_name, coast = '*', autofill = False):
        if '(' in terr_name:
            x = terr_name.strip(')').split('(')
            return t.get_t(x[0],x[1], autofill)
        if terr_name in t.terrs: return t.terrs[terr_name].get_c(coast)
        #condition for non-blind case goes here
        if autofill:
            t.terrs[terr_name] = territory(terr_name)
            t.terrs[terr_name].add_c(coast)
            return t.terrs[terr_name]
        return null_terr

    def add_u(t, u, terr, coast = '*', replace = False):
        t.get_t(terr, coast).add_u(u, coast, replace)

    def get_u(t, terr, coast = '*'):
        t.get_t(terr, coast).get_u(u, coast)

    def add_d(t, d):
        pass

    def get_d(t, pl):
        pass

    def __len__(t): 
        return len(t.terrs)

    def __str__(t):
        return debugstr(t.summary(), 'state')

    def summary(t, pov = '*', mememode = False, morsemode = False):
        res = ''
        res += t.season+' '+t.phase+' '+str(t.year)+'\n\n'
        for x in t.terrs: res += str(t.terrs[x].get_u())+' '+str(t.terrs[x])+'\n'
        return res


class order_set:
    def __init__(t, season, phase, year):
        t.ords = dict()
        t.decs = dict()
        t.cnt = 0
        t.prev_state = null_state
        t.next_state = null_state
        t.season, t.phase, t.year = season, phase, year

    def add_o(t, ord_, replace = False):
        if ord_.player not in t.ords: t.ords[ord_.player] = []
        if ord_.player not in t.decs: t.decs[ord_.player] = []
        if type(ord_) == declaration: t.decs.append(ord_)
        else: t.ords[ord_.player].append(ord_)
        t.cnt += 1

    def add_d(t, dec, replace = False):
        pass

    def prep_ords(t):
        for p in t.ords:
            for o in t.ords[p]:
                o.fill_relations()

    def copy(t):
        pass

    def __len__(t): return t.cnt

    def __str__(t): 
        return debugstr(t.summary(), 'order_set')

    def summary(t, pov = '*', mememode = False, morsemode = False):
        res = t.season+' '+t.phase+' '+str(t.year)+'\n'
        for p in t.ords:
            res += p+':\n'
            for d in t.decs[p]: res += d.summary(pov, mememode, morsemode)+'\n'
            for o in t.ords[p]: res += o.summary(pov, mememode, morsemode)+'\n'
            res += '\n'
        return res


null_unit = unit('',' ')
bounce = unit('','bounce')
null_terr = territory('', '')
null_unit.dis_from = null_terr
null_dec = declaration('',NUL,'')
null_order = order('','')
null_unit.ord = null_order
null_state = state('','',0)
null_oset = order_set('','',0)
null_state.prev_ords = null_oset
default_rules = rulebook()

# #order(player, ord_type, terr = '', hterr = '', dest = '', *via)
# print(parse('France', '|_7 POR -> SPA'))
# print(parse('France', 'F NTH SUP F POR -> SPA'))
# print(parse('France','NTH SUP F POR -> SPA'))
# print(parse('France','F NTH SUP F POR -> SPA via F MAO or ENG'))
# #print(parse('France','SPA'), 'U')
# print(parse('France', 'F SPA'))
# print(parse('France', 'F SPA(SC)'))
# print(parse('France', 'BLD F SPA'))
# print(parse('France', 'F SPA DIS'))
# print(parse('France', 'F SPA POR'))
# print(parse('France', '|_7 POR -> SPA via |_7 MAO'))
# print(parse('France', 'declare war Germany'))
# #print(parse('France', '* * SUP F * -> * via _'),'*')
# #process(parse('F POR', HOL))

s1 = '''
Spring 1901 (Order):
Russia
F STP(SC) - BOT
A MOS - SEV

France
F PAR - BUR

Fall 1901 (Orders)
Russia
F BOT - SWE
'''

s2 ='''Spring Orders 1901
FRANCE
A PAR TO BUR
A BEL SUP A PAR TO BUR
F MAR TO GOL

GERMANY
A KIE TO SWE VIA F BAL
F BAL CON A KIE TO SWE
A MUN TO BUR'''

OS19 = parse(s2).pop()

#print(' ')
#s1901, s1902 = parse(s)
#print(s1901[0].summary())
#print(s1901[1])


#print(x[0].bydest['territory<MOS>'][HOL][0].hdest)


#todo: 
#automate / finish unit tests
#handle multiple units getting same order
#board state object

#settings pre-set options
#morse mode / meme mode
#add multi-coast support

#adjacenct territory representation and rule enforcement.
#season / phase aware adjudication
#add variant rules support
#   ability to specify which units (or non units) can perform a convoy and what types of unit they may convoy
#   ability to specify which order types are legal in a phase, and the ordering of phases / seasons
#   ability to specify which units should have the no-self-dislodge rules apply
#   ability to turn certain support/convoy cutting rules on/off. 
#   ability to specify general unit adjacency graph (eg for more general unit types like aircraft and submarines)
#   ability to give territories the hidden property
