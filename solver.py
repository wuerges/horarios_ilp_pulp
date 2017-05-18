from model import Professor, Course, Slot, Semester, Day, Shift, id_seed

import pulp

cs = [ Course("A", 5), Course("B", 5), Course("C"), Course("D") \
     , Course("E", 5), Course("F", 5), Course("G"), Course("H") ] 

#ps = [ Professor(cs[0:2], "P1"), Professor(cs[2:4], "P2") \
#      , Professor(cs[4:6], "P3"), Professor(cs[6:], "P4") ]

ps = [ Professor(cs[0:4], "P1") \
     , Professor(cs[4:], "P2") ]

slots = [ Slot("M1_seg", 3), Slot("M2_seg", 2), Slot("M1_ter", 3), Slot("M2_ter", 2) \
        , Slot("T1_seg", 3), Slot("T2_seg", 2), Slot("T1_ter", 3), Slot("T2_ter", 2) \
        , Slot("N1_seg", 2), Slot("N2_seg", 2), Slot("N1_ter", 2), Slot("N2_ter", 2) ]

m1s = [slots[0], slots[2]]
m2s = [slots[1], slots[3]]
t1s = [slots[4], slots[6]]
t2s = [slots[5], slots[7]]
n1s = [slots[8], slots[10]]
n2s = [slots[9], slots[11]]

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

#days = [ Day(slots[0:2] + slots[4:6], "Seg.") \
#       , Day(slots[2:4] + slots[6:8], "Ter.") ]

#shifts = [ Shift(slots[0:2], "Mat") \
#         , Shift(slots[2:4], "Mat") \
#         , Shift(slots[4:6], "Not") \
#         , Shift(slots[6:8], "Not") ]

lp_vars = {}
lp_vars_rev = {}

for c in cs:
    for p in ps:
        for s in slots:
            for sem in semesters:
                k = (p, c, s, sem)
                id_n = next(id_seed)
                v = pulp.LpVariable(id_n, lowBound=0, cat=pulp.LpInteger)
                lp_vars[k] = v
                lp_vars_rev[v.name] = k


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
    #for p in professors:
    #    v = pulp.lpSum(lp_vars[(p, c, s, sem)] * s.size \
    #            for s in slots \
    #            for c in p.courses \
    #            for sem in semesters )
    #    prob += v <= sum(c.num_hours for c in p.courses)

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
    #for sem in semesters:
    #    v = pulp.lpSum(lp_vars[(p, c, s, sem)] * s.size \
    #            for s in sem.slots \
    #            for p in ps \
    #            for c in sem.courses)
    #    prob += v <= sum(c.num_hours for c in sem.courses)

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

    def get_slot(s_, sem_):
        for (p,c, s, sem), v in lp_vars.items():
            if sem_ is sem and s is s_ and v.varValue > 0:
                return lp_vars_rev[v.name]


    print("\n\n\n")

    def print_m_(ms, sem):
        for s in ms:
            x = get_slot(s, sem)
            if x: 
                print(x[0].name, x[1].name, end='\t')
            else:
                print("<>", end='\t')
        print()

    for sem in semesters:
        print("\n\n", sem)
        print("7:30", end='\t')
        print_m_(m1s, sem)
        print("9:00", end='\t')
        print_m_(m2s, sem)
        print("13:30", end='\t')
        print_m_(t1s, sem)
        print("16:10", end='\t')
        print_m_(t2s, sem)
        print("19:00", end='\t')
        print_m_(n1s, sem)
        print("21:00", end='\t')
        print_m_(n2s, sem)
    #slots = [ Slot("M1_seg", 3), Slot("M2_seg", 2), Slot("M1_ter", 3), Slot("M2_ter", 2) \
    #        , Slot("T1_seg", 3), Slot("T2_seg", 2), Slot("T1_ter", 3), Slot("T2_ter", 2) \
    #        , Slot("N1_seg", 2), Slot("N2_seg", 2), Slot("N1_ter", 2), Slot("N2_ter", 2) ]

solve(ps, cs, semesters, slots)
