from model import Professor, Course, Slot, Semester, Day, Shift

import pulp

cs = [ Course("A", 5), Course("B", 5), Course("C"), Course("D") \
     , Course("E", 5), Course("F", 5), Course("G"), Course("H") ] 

#ps = [ Professor(cs[0:2], "P1"), Professor(cs[2:4], "P2") \
#      , Professor(cs[4:6], "P3"), Professor(cs[6:], "P4") ]

ps = [ Professor(cs[0:4], "P1") \
     , Professor(cs[4:], "P2") ]

slots = [ Slot("M1_seg", 3), Slot("M2_seg", 2), Slot("M1_ter", 3), Slot("M2_ter", 2) \
        , Slot("N1_seg", 2), Slot("N2_seg", 2), Slot("N1_ter", 2), Slot("N2_ter", 2) ]

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


proibidos = [ (slots[0], slots[5]), (slots[1],slots[6]) \
            , (slots[5], slots[1]) ]

#days = [ Day(slots[0:2] + slots[4:6], "Seg.") \
#       , Day(slots[2:4] + slots[6:8], "Ter.") ]

#shifts = [ Shift(slots[0:2], "Mat") \
#         , Shift(slots[2:4], "Mat") \
#         , Shift(slots[4:6], "Not") \
#         , Shift(slots[6:8], "Not") ]

lp_vars = {}

for c in cs:
    for p in ps:
        for s in slots:
            for sem in semesters:
                k = (p, c, s, sem)
                lp_vars[k] = \
                        pulp.LpVariable(str(k), lowBound=0, cat=pulp.LpInteger)


def solve(professors, courses, semesters, slots):
    prob = pulp.LpProblem("Semester Problem", pulp.LpMaximize)

    prob += pulp.lpSum(v for k,v in lp_vars.items())

    #print(lp_vars.keys())

    # Maximum one class for slot
    for s in slots:
        for sem in semesters:
            v = pulp.lpSum(lp_vars[(p, c, s, sem)] \
                    for p in professors \
                    for c in courses)
            prob += v <= 1 #s.size

    #for sem in semesters:
    #    for s in sem.slots:
    #        v = pulp.lpSum(lp_vars[(p, c, s, sem)] \
    #                for p in professors \
    #                for c in courses)
    #        prob += v <= 1 #s.size

    # Each professor must only give his classes
    for p in professors:
        v = pulp.lpSum(lp_vars[(p, c, s, sem)] * s.size \
                for s in slots \
                for c in p.courses \
                for sem in semesters )
        prob += v <= sum(c.num_hours for c in p.courses)

    # Each proessor must not give other professor's classes
    for p in professors:
        v = pulp.lpSum(lp_vars[(p, c, s, sem)] \
                for s in slots \
                for c in courses if not c in p.courses \
                for sem in semesters )
        prob += v == 0

    # Each course must be complete
    for c in cs:
        v = pulp.lpSum(lp_vars[(p, c, s, sem)] * s.size \
                for s in slots \
                for p in ps \
                for sem in semesters )
        prob += v <= c.num_hours

    # Each semester must have all its courses filled
    for sem in semesters:
        v = pulp.lpSum(lp_vars[(p, c, s, sem)] * s.size \
                for s in sem.slots \
                for p in ps \
                for c in sem.courses)
        prob += v <= sum(c.num_hours for c in sem.courses)

    # Each semester must only have its courses
    for sem in semesters:
        v = pulp.lpSum(lp_vars[(p, c, s, sem)] \
                for s in slots \
                for p in ps \
                for c in cs if not c in sem.courses)
        prob += v == 0

    # Each semester must only have its slots
    for sem in semesters:
        v = pulp.lpSum(lp_vars[(p, c, s, sem)] \
                for s in slots if not s in sem.slots \
                for p in ps \
                for c in cs)
        prob += v == 0


    for p in professors:
        print(p, proibidos)
        for (a, b) in proibidos:
            va = pulp.lpSum(lp_vars[(p, c, a, sem)] \
                    for c in p.courses \
                    for sem in semesters )
            vb = pulp.lpSum(lp_vars[(p, c, b, sem)] \
                    for c in p.courses \
                    for sem in semesters )
            prob += va + vb <= 1

    #for p in professors:
    #    prob += pulp.lpSum([s.size * prof_slot[(p, c, s)] for c in p.courses for s in slots]) == p.total_time()


    # maximum one professor per slot of time
    #for p in professors:
    #    prob += pulp.lpSum([prof_slot[(p,st)] for sh in shifts for st in sh.slots]) <= 1.1


    #print(professors)
    #print(courses)
    #print(semesters)
    #print(days)
    #print(shifts)
    #print(slots)
    for sem in semesters:
        print(sem)
        for c in sem.courses:
            print("  ", c)
        for s in sem.slots:
            print("  ", s)
    prob.writeLP("problem.lp")
    prob.solve()
    print("Status:", pulp.LpStatus[prob.status])
    for v in prob.variables(): 
        if v.varValue and v.varValue > 0:
            print(v.name, "=", v.varValue)



solve(ps, cs, semesters, slots)
