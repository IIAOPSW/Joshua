from joshua import *

#parser tests
print(order('player_1', 'F A HOL'))
print(order('player_1', 'F A H'))
print(order('player_1', 'F A'))
print(order('player_1', '|_7 A HOLD'))
print(order('player_1', 'O7 A kill_civilians'))
print()
print(order('player_1', 'A A MOV B'))
print(order('player_1', 'A D E'))
print(order('player_1', 'A A MOVE B'))
print(order('player_1', 'A A to B'))
print(order('player_1', 'A A - B'))
print(order('player_1', 'A A -> B'))
print(order('player_1', 'O7 A -> B'))
print(order('player_1', 'O7 A-B'))
print(order('player_1', 'A A->B'))
print()
print(order('player_1', 'A A SUP B'))
print(order('player_1', 'A A SUP B -> C'))
print(order('player_1', 'A A S B'))
print(order('player_1', 'A A S B->C'))
print(order('player_1', 'O7 A +-> B -> C'))
print(order('player_1', 'A A SUP B C'))
print()


#rulebook tests

print('stupid tests (most of these adjudicate right for the wrong reason)\n')
print('malformed move\n')
adjudicate([
    order('player_1', 'A A MOV A')
])

print('malformed move via convoy\n')
adjudicate([
    order('player_1', 'A A MOV A via B'),
    order('player_1', 'F B CON A MOV A')
])

print('mismatched stupid convoy\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV A')
])

print('mismatched stupider convoy\n')
adjudicate([
    order('player_1', 'A A MOV B via B'),
    order('player_1', 'F B CON A MOV A')
])

print('abuse of via\n')
adjudicate([
    order('player_1', 'A A SUP B via C'),
    order('player_1', 'F C CON A SUP B')
])

print('impossible support move')
adjudicate([
    order('player_1', 'A A SUP A MOV B')
])

print('impossible support hold')
adjudicate([
    order('player_1', 'A A SUP A HOL A')
])

print('suicidial support')
adjudicate([
    order('player_1', 'A A SUP B MOV A'),
    order('player_2', 'A B MOV A')
])

print('suicidial convoy')
adjudicate([
    order('player_1', 'A A MOV B via B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'F B CON A MOV B')
])

#special tests
print('special tests\n')
print('unopposed chain of moves\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_1', 'A C MOV D')
])

print('traffic jam\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_1', 'A C MOV D'),
    order('player_2', 'A D HOL')
])

print('traffic jam with no self dislodge\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_1', 'A C MOV D'),
    order('player_2', 'A D HOL'),
    order('player_1', 'A E SUP B MOV C')
])

print('traffic jam with no self dislodge adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_1', 'A C MOV D'),
    order('player_2', 'A D HOL'),
    order('player_2', 'A E SUP B MOV C')
])

print('traffic jam with no self dislodge adversarial support case 2\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_2', 'A C MOV D'),
    order('player_2', 'A D HOL'),
    order('player_2', 'A E SUP B MOV C')
])

print('non-traffic jam because dislodge\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_2', 'A C MOV D'),
    order('player_2', 'A D HOL'),
    order('player_1', 'A E SUP B MOV C')
])

print('non-traffic jam because dislodge, erroneous support hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_2', 'A C MOV D'),
    order('player_2', 'A D HOL'),
    order('player_2', 'A E SUP C HOL'),
    order('player_1', 'A F SUP B MOV C')
])


print('rotation\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_1', 'A C MOV A')
])

print('rotation with traffic jam\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_1', 'A C MOV A'),
    order('player_2', 'A D MOV A')
])

print('convoy paradox type 1\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_2', 'F C SUP B HOL'),
    order('player_3', 'F D MOV B'),
    order('player_3', 'F E SUP D MOV B')
])

print('convoy paradox type 1 dislodging\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_1', 'A D SUP A MOV C'),
    order('player_2', 'F C SUP B HOL'),
    order('player_3', 'F E MOV B'),
    order('player_3', 'F F SUP E MOV B')
])

print('convoy paradox type 2\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_2', 'F D MOV B'),
    order('player_2', 'F C SUP D MOV B')
])

print('convoy paradox type 2 dislodging\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_1', 'F D SUP A MOV C'),
    order('player_2', 'F E MOV B'),
    order('player_2', 'F C SUP E MOV B')
])

print('convoy paradox type 3\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_2', 'F D MOV B'),
    order('player_2', 'F C SUP D MOV B'),
    order('player_3', 'F E MOV B'),
    order('player_3', 'F F SUP E MOV B')
])

print('convoy paradox type 3 dislodging\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_2', 'F D MOV B'),
    order('player_2', 'F C SUP D MOV B'),
    order('player_3', 'F E MOV B'),
    order('player_3', 'F F SUP E MOV B'),
    order('player_1', 'A F SUP A MOV C')
])

print('convoy non-paradox type 3\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_2', 'F D MOV B'),
    order('player_2', 'F C SUP D MOV B'),
    order('player_1', 'F E MOV B'),
    order('player_1', 'F F SUP E MOV B')
])

print('convoy non-paradox type 3 dislodging\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C'),
    order('player_2', 'F D MOV B'),
    order('player_2', 'F C SUP D MOV B'),
    order('player_1', 'F E MOV B'),
    order('player_1', 'F F SUP E MOV B'),
    order('player_1', 'A F SUP A MOV C')
])


#manually constructed tests
print('x vs y over empty\n\n')
print('1 vs 0\n')
adjudicate([
    order('player_1', 'A A MOV B')
])

print('2 vs 0\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C')
])

print('2 vs 0, 1 adversarial sup\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_2', 'A B SUP A MOV C')
])

print('3 vs 0\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B SUP A MOV D'),
    order('player_1', 'A C SUP A MOV D')
])

print('3 vs 0, 1 adversarial sup \n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B SUP A MOV D'),
    order('player_2', 'A C SUP A MOV D')
])

print('3 vs 0, 2 adversarial sup \n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_2', 'A B SUP A MOV D'),
    order('player_2', 'A C SUP A MOV D')
])

print('1 vs 1\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A C MOV B')
])

print('1 vs 1, self bounce\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A C MOV B')
])

print('2 vs 1\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_2', 'A D MOV C')
])

print('2 vs 1, broken support\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_2', 'A D MOV C'),
    order('player_2', 'A E MOV B')
])

print('2 vs 1, 1 adversarial sup\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_2', 'A B SUP A MOV C'),
    order('player_1', 'A D MOV C')
])

print('2 vs 1, contradictory goals\n')
adjudicate([
    order('player_2', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_1', 'A D MOV C')
])

print('2 vs 1, 1 self non-bounce\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_1', 'A D MOV C')
])

print('2 vs 1, 1 self non-bounce broken support\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_1', 'A D MOV C'),
    order('player_2', 'A E MOV B')
])

print('2 vs 2\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_2', 'A D MOV C'),
    order('player_2', 'A E SUP D MOV C'),
])

print('2 vs 2 with 1 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_2', 'A B SUP A MOV C'),
    order('player_2', 'A D MOV C'),
    order('player_2', 'A E SUP D MOV C'),
])

print('2 vs 2 with 2 self bounce and 2 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_2', 'A B SUP A MOV C'),
    order('player_1', 'A D MOV C'),
    order('player_2', 'A E SUP D MOV C'),
])

print('2 vs 2 with 2 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_2', 'A B SUP A MOV C'),
    order('player_2', 'A D MOV C'),
    order('player_1', 'A E SUP D MOV C'),
])

print('2 vs 2 with self bounce and contradictory goals\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'A B SUP A MOV C'),
    order('player_1', 'A D MOV C'),
    order('player_1', 'A E SUP D MOV C'),
])

print('3 vs 1\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B SUP A MOV D'),
    order('player_1', 'A C SUP A MOV D'),
    order('player_2', 'A E MOV D')
])

print('3 vs 1, 1 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B SUP A MOV D'),
    order('player_2', 'A C SUP A MOV D'),
    order('player_2', 'A E MOV D')
])

print('3 vs 1, 2 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_2', 'A B SUP A MOV D'),
    order('player_2', 'A C SUP A MOV D'),
    order('player_2', 'A E MOV D')
])

print('3 vs 2\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B SUP A MOV D'),
    order('player_1', 'A C SUP A MOV D'),
    order('player_2', 'A E MOV D'),
    order('player_2', 'A F SUP E MOV D')
])

print('3 vs 3\n')

print('1 vs 1 vs 1\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_2', 'A B MOV D'),
    order('player_3', 'A C MOV D')
])

print('1 vs 1 vs 1 with 1 self bounce\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B MOV D'),
    order('player_2', 'A C MOV D')
])

print('1 vs 1 vs 1 triple self bounce\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_1', 'A B MOV D'),
    order('player_1', 'A C MOV D')
])

print('2 vs 1 vs 1\n')
adjudicate([
    order('player_1', 'A A MOV E'),
    order('player_1', 'A B SUP A MOV E'),
    order('player_2', 'A C MOV E'),
    order('player_3', 'A D MOV E')
])

print('2 vs 1 vs 1 with 1 self bounce\n')
adjudicate([
    order('player_1', 'A A MOV E'),
    order('player_1', 'A B SUP A MOV E'),
    order('player_2', 'A C MOV E'),
    order('player_2', 'A D MOV E')
])

print('2 vs 1 vs 1 with contradictory goal\n')
adjudicate([
    order('player_1', 'A A MOV E'),
    order('player_1', 'A B SUP A MOV E'),
    order('player_1', 'A C MOV E'),
    order('player_2', 'A D MOV E')
])

print('2 vs 1 vs 1 with 1 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV E'),
    order('player_2', 'A B SUP A MOV E'),
    order('player_2', 'A C MOV E'),
    order('player_3', 'A D MOV E')
])

print('2 vs 1 vs 1 with 1 self bounce and 1 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV E'),
    order('player_2', 'A B SUP A MOV E'),
    order('player_1', 'A C MOV E'),
    order('player_2', 'A D MOV E')
])

print('2 vs 1 vs 1 with 1 self bounce and 1 adversarial support\n')
adjudicate([
    order('player_1', 'A A MOV E'),
    order('player_2', 'A B SUP A MOV E'),
    order('player_2', 'A C MOV E'),
    order('player_2', 'A D MOV E')
])

print('2 vs 2 vs 1\n')

print('3 vs 2 vs 1\n')

print('3 vs 2 vs 2\n')



print('x vs y adjacent\n\n')

print('move vs move adjacent\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A B MOV A')
])

print('move vs move adjacent with support\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A B MOV A'),
    order('player_2', 'A C SUP B MOV A')
])

print('move vs move adjacent with convoys\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A B MOV A'),
    order('player_2', 'F C CON B MOV A')
])



print('x vs y over occupied non-moving\n\n')

print('supported move vs supported move over hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B HOL'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'A D MOV B'),
    order('player_2', 'A E SUP D MOV B')   
])


print('x vs y over occupied moving\n\n')

print('breaking support with dislodging\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_2', 'A C SUP D MOV B'),
    order('player_2', 'A D MOV B'),
    order('player_1', 'A E SUP B MOV C')
])

print('protecting support with self attack\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A B MOV C'),
    order('player_2', 'A C SUP D MOV B'),
    order('player_2', 'A D MOV B'),
    order('player_1', 'A E SUP B MOV C'),
    order('player_2', 'A F MOV C'),
    order('player_2', 'A G SUP F MOV C')
])


print('convoy chain tests\n\n')

print('unopposed move via convoy\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'F B CON A MOV C')
])

print('unopposed move via convoy chain\n')
adjudicate([
    order('player_1', 'A A MOV D via B'),
    order('player_1', 'F B CON A MOV D via C'),
    order('player_1', 'F C CON A MOV D')
])

print('unopposed move via double convoy\n')
adjudicate([
    order('player_1', 'A A MOV D via B or C'),
    order('player_1', 'F B CON A MOV D'),
    order('player_1', 'F C CON A MOV D')
])

#unopposed move via double convoy chain

print('unopposed move via missing convoy\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
])

print('unopposed move via mismatched convoy chain\n')
adjudicate([
    order('player_1', 'A A MOV D via B'),
    order('player_1', 'F B CON A MOV E via C'),
    order('player_1', 'F C CON A MOV D')
])

print('unopposed move via missing convoy chain\n')
adjudicate([
    order('player_1', 'A A MOV D via B'),
    order('player_1', 'F B CON A MOV D via C'),
])

print('unopposed move via double convoy with 1 missing\n')
adjudicate([
    order('player_1', 'A A MOV D via B or C'),
    order('player_1', 'F B CON A MOV D'),
    order('player_2', 'F C MOV B')
])

print('Attempted convoy of a fleet\n')
adjudicate([
    order('player_1', 'F A MOV C via B'),
    order('player_1', 'F B CON A MOV C')
])

print('attempted convoy by an army\n')
adjudicate([
    order('player_1', 'A A MOV C via B'),
    order('player_1', 'A B CON A MOV C')
])

print('via convoy\n')
adjudicate([
    order('player_1', 'A A MOV C via convoy'),
    order('player_1', 'F B CON A MOV C')
])

print('implicit convoy\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_1', 'F B CON A MOV C')
])

print('convoy kidnap\n')
adjudicate([
    order('player_1', 'A A MOV C'),
    order('player_2', 'F B CON A MOV C')
])

print('via convoy un-kidnap\n')
adjudicate([
    order('player_1', 'A A MOV C via convoy'),
    order('player_1', 'F B CON A MOV C')
])

print('unopposed support to hold\n')
adjudicate([
    order('player_1', 'A A HOL'),
    order('player_1', 'A B SUP A HOL')
])

print('broken support to move\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'A D MOV C')
])

print('broken support to hold\n')
adjudicate([
    order('player_1', 'A A HOL'),
    order('player_1', 'A B SUP A HOL'),
    order('player_2', 'A C MOV B')
])

print('non-matching support to move\n')
adjudicate([
    order('player_1', 'A A MOV D'),
    order('player_2', 'A C SUP A MOV B')
])

print('non-matching support to hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A C SUP A')
])

print('move vs move in empty\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A C MOV B')
])

print('unopposed hold\n')
adjudicate([
    order('player_1', 'A A HOL')
])

print('move vs hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A B HOL')
])

print('supported move vs hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'A B HOL')
])

print('move vs supported hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A B HOL'),
    order('player_2', 'A D SUP B HOL')
])

print('supported move vs supported hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'A B HOL'),
    order('player_2', 'A D SUP B HOL')
])

print('supported move vs supported hold same player\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'A B HOL'),
    order('player_1', 'A D SUP B HOL')
])

print('dislodging move attempted support break\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_2', 'A B MOV C')
])


print('supported self-dislodge move vs hold\n')
adjudicate([
    order('player_1', 'A A MOV B'),
    order('player_2', 'A C SUP A MOV B'),
    order('player_1', 'A B HOL')
])

print('self-dislodging support for move vs hold\n')
adjudicate([
    order('player_2', 'A A MOV B'),
    order('player_1', 'A C SUP A MOV B'),
    order('player_1', 'A B HOL')
])


[
    order('Eng', 'F north_atlantic'),
    order('Eng', 'F north_sea'),
    order('Eng', 'F *london'),
    order('Eng', 'F *liverpool')
]


eng1 = [
    [
        order('Eng', 'F north_sea SUP *london HOL'),
        order('Eng', 'F *london HOL')
    ],
    [
        order('Eng', 'F north_sea MOV english_channel'),
        order('Eng', 'F *london SUP north_sea MOV english_channel'),
    ],
    [
        order('Eng', 'F north_sea MOV *edinburgh'),
        order('Eng', 'F *london HOL')
    ],
]


eng2 = [
    [
        order('Eng', 'F north_atlantic SUP *liverpool HOL'),
        order('Eng', 'F *liverpool HOL')
    ],
    [
        order('Eng', 'F north_atlantic SUP *liverpool MOV irish_sea'),
        order('Eng', 'F *liverpool MOV irish_sea')
    ],
    [
        order('Eng', 'F north_atlantic MOV irish_sea'),
        order('Eng', 'F *liverpool sup north_atlantic MOV irish_sea')
    ]
]
eng3 = [
    [
        order('Eng', 'A picardy MOV *brest')
    ],
    [
        order('Eng', 'A picardy MOV *paris')
    ],
    [
        order('Eng', 'A picardy MOV *belgium')
    ]
]

fr1 = [
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *london'),
        order('Fra', 'A yorkshire SUP english_channel MOV *london')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *london'),
        order('Fra', 'A yorkshire MOV *edinburgh')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *brest'),
        order('Fra', 'A yorkshire MOV *edinburgh')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *belgium'),
        order('Fra', 'A yorkshire MOV *edinburgh')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *brest'),
        order('Fra', 'A yorkshire SUP irish_sea MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *belgium'),
        order('Fra', 'A yorkshire SUP irish_sea MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *london'),
        order('Fra', 'A yorkshire SUP irish_sea MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV north_sea'),
        order('Fra', 'A yorkshire SUP irish_sea MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV *brest'),
        order('Fra', 'A yorkshire SUP irish_sea MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea MOV *liverpool'),
        order('Fra', 'F english_channel MOV belgium'),
        order('Fra', 'A yorkshire SUP irish_sea MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea SUP yorkshire MOV *liverpool'),
        order('Fra', 'F english_channel MOV *london'),
        order('Fra', 'A yorkshire MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea SUP yorkshire MOV *liverpool'),
        order('Fra', 'F english_channel MOV north_sea'),
        order('Fra', 'A yorkshire MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea SUP yorkshire MOV *liverpool'),
        order('Fra', 'F english_channel MOV *brest'),
        order('Fra', 'A yorkshire MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea SUP yorkshire MOV *liverpool'),
        order('Fra', 'F english_channel MOV *belgium'),
        order('Fra', 'A yorkshire MOV *liverpool')
    ],
    [
        order('Fra', 'F irish_sea SUP english_channel HOL'),
        order('Fra', 'F english_channel SUP yorkshire MOV *london'),
        order('Fra', 'A yorkshire MOV *london')
    ]
]

fr2 = [
    [
        order('Fra', 'A burgundy MOV *belgium')
    ],
    [
        order('Fra', 'A burgundy MOV *paris')
    ]
]

en = []
for x in eng1:
    for y in eng2:
        for z in eng3:
            en.append(x+y+z)
            
fr = []

for x in fr1:
    for y in fr2:
        fr.append(x+y)
        
for i in en:
    for j in fr:
        adjudicate(i+j)

def number_of_players(n):
    if n != 0: return
    #run all the unit tests here

print("A strange game, the only winning move is to negotiate.")