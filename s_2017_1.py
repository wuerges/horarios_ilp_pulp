from model import Professor, Course, Slot, Semester, dias

cs = [ Course("A", 5), Course("B", 5), Course("C"), Course("D") \
     , Course("E", 5), Course("F", 5), Course("G"), Course("H") ] 

#ps = [ Professor(cs[0:2], "P1"), Professor(cs[2:4], "P2") \
#      , Professor(cs[4:6], "P3"), Professor(cs[6:], "P4") ]

ps = [ Professor(cs[0:4], "P1") \
     , Professor(cs[4:], "P2") ]


m1s = [Slot("M1_%s" % d, 3) for d in dias]
m2s = [Slot("M2_%s" % d, 2) for d in dias]
t1s = [Slot("T1_%s" % d, 3) for d in dias]
t2s = [Slot("T2_%s" % d, 2) for d in dias]
n1s = [Slot("N1_%s" % d, 2) for d in dias]
n2s = [Slot("N2_%s" % d, 2) for d in dias]


slots = m1s + m2s + t1s + t2s + n1s + n2s

matutino1 =  Semester(slots[0:4], "Mat1")
matutino1.add_course(cs[0])
matutino1.add_course(cs[1])

noturno2  =  Semester(slots[4:8], "Not2")
noturno2.add_course(cs[2])
noturno2.add_course(cs[3])

matutino3 =  Semester(slots[0:4], "Mat3")
matutino3.add_course(cs[4])
matutino3.add_course(cs[5])

noturno4  =  Semester(slots[4:8], "Not4")
noturno4.add_course(cs[6])
noturno4.add_course(cs[7])

semesters = [ matutino1, noturno2, matutino3, noturno4 ]


proibidos = [ (slots[0], slots[5]), (slots[2],slots[7]) \
            , (slots[5], slots[2]) ]


