
#def meme_status(t, reverse=False, noterr = False):
		#resolved with caveat at the post-resolution stage
		# ¯\_(ツ)_/¯ ++> :/ --> <-- U7 X  #resolved (but supported unit was bounced by U7 X)
		# ¯\_(ツ)_/¯ ~~> :/ --> <-- U7 X  #resolved (but convoyed unit was bounced by U7 X)
		# ¯\_(ツ)_/¯ ++> \o/ <-- ;) X     #resolved (but supported army was dislodged by U7 X)
		# ¯\_(ツ)_/¯ ~~> \o/ <-- ;) X     #resolved (but convoyed army was dislodged by U7 X)
		# ¯\_(ツ)_/¯ ++> ~\o/~ <-- ;) X   #resolved (but supported fleet was dislodged by U7 X)
		# ¯\_(ツ)_/¯ ~~> ~\o/~ <-- ;) X   #resolved (but convoyed fleet was dislodged by unit X)
		# ¯\_(ツ)_/¯ ++> RIP <-- ;) X     #resolved (but supported army was disbanded by U7 X)
		# ¯\_(ツ)_/¯ ~~> RIP <-- ;) X     #resolved (but convoyed army was disbanded by U7 X)
		# ¯\_(ツ)_/¯ ++> SOS <-- ;) X     #resolved (but supported fleet was disbanded by U7 X)
		# ¯\_(ツ)_/¯ ~~> SOS <-- ;) X     #resolved (but convoyed fleet was disbanded by U7 X)

		#disbanded at the post-resolution stage
		# RIP <-- ;) X                   #disbanded (army)
		# SOS <-- ;) X                   #disbanded (fleet)

		#canceled / dislodged / resolved at the resolution stage
		# :( --> <-- ;) X                #bounced against move X (and move X resolved)
		# :( --> <-- :/ X                #bounced against move X (and move X bounced something else)
		# :/ --> <-- :/ X                #bounced against move X (and caused X to bounce)
		# :( --> O7 X                    #bounced against non-moving army X (accomplishing nothing)
		# :( --> |_7 X                   #bounced against non-moving fleet X (accomplishing nothing)
		# :3 --> O7 X                    #bounced against non-moving army X (no self dislodge/cancel rule applied)
		# :3 --> |_7 X                   #bounced against non-moving fleet X (no self dislodge/cancel rule applied)
		# :/ --> :( X                    #bounced against non-moving X (and caused X to be canceled)
		# :( <-- :/ X                    #canceled (but not dislodged) by X
		# \o/ <-- ;) X                   #dislodged by X (army)
		#~\o/~ <-- ;) X                  #dislodged by X (fleet)
		# ;) -->                         #resolved move
		# :)                             #resolved (non-move)
		
		#canceled at the path stage
		# :( <~~ :( <-- :/ X             #canceled by convoying |_7 canceled by unit X
		# :( <~~ \o/ <-- ;) X            #canceled by convoying army dislodged by unit X
		# :( <~~ ~\o/~ <-- ;) X          #canceled by convoying fleet dislodged by unit X

		#canceled at the matching stage
		# :? <~~ |_7 X -->               #move canceled by |_7 X did not have matching convoy order (army)
		# :? <~~ ?_? X -->               #move canceled by no such |_7 for convoy (army)

		# :? ++> O7 X                    #support canceled by O7 X did not have matching orders
		# :? ++> |_7 X                   #support canceled by |_7 X did not have matching orders
		# :? ++> O?                      #support canceled by no such army to support
		# :? ++> |_?                     #support canceled by no such fleet to support
		# :? ++> U?                      #support canceled by no such unit to support

		# :? ~~> O7 X                    #convoy canceled by O7 X did not match convoy given
		# :? ~~> |_7 X                   #convoy canceled by |_7 X did not match convoy given
		# :? ~~> O? X 	                 #convoy canceled by no such army at X
		# :? ~~> |_? X 	                 #convoy canceled by no such fleet at X
		# :? ~~> U? X                    #convoy canceled by no such unit at X

		#canceled at the legal stage
		# O? -->						 #invalid army
		# |_? -->                        #invalid fleet
		# O7 -?->                        #illegal move order(army)
		# |_7 -?->                       #illegal move order (fleet)
		# O7 --> ?                       #illegal move destination (army)
		# |_7 --> ?                      #illegal move destination (fleet)

		# O? ++>                         #invalid army
		# |_? ++>                        #invalid fleet
		# O7 +?+>                        #illegal support order (army)
		# |_7 +?+>                       #illegal support order (fleet)
		# O7 ++> ?                       #illegal support destination (army)
		# |_7 ++> ?                      #illegal support destination (fleet)

		# O? ~~>                         #invalid army
		# |_? ~~>                        #invalid fleet
		# O7 ~?~>                        #illegal convoy order (army)
		# |_7 ~?~>                       #illegal convoy order (fleet)
		# O7 ~~> ?                       #illegal convoy destination (army)
		# |_7 ~~> ?                      #illegal convoy destination (fleet)

		#unresolved
		# O7                             #unresolved (army)
		#|_7                             #unresolved (fleet)

#		o=['valid', 'legal', 'match', 'path', 't2h', 'h2h', 'disl', 'disb', 'res']
#		a=['?_?', '0_o', '¯\\_(ツ)_/¯', ':(', ':(', ':(',  '\\o/', 'RIP',   ';)']
#		f=['?_?', '0_o', '¯\\_(ツ)_/¯', ':(', ':(', ':(', '~\\o/~','SOS',   ':3']
#		m=[False, False, False, True, True, False, True] #should move arrows be drawn? 


#PCE:'<3', WAR:':<'
#idea, order object can double as template to define what type of orders are illegal. 
#EG 'A * CON * * MOV *' means 'army anywhere cannot convoy move anywhere'
# 'F <coast> CON * * MOV *' means 'fleet on territory with property <coast> cannot convoy move anywhere
# '* * CON * * SUP *' means 'nothing may convoy support'
