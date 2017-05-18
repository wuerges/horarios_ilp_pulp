from model import Professor, Course, Slot, Semester, Day, Shift

import pulp

cs = [ Course("A"), Course("B"), Course("C"), Course("D"), Course("E"), Course("F"), Course("G"), Course("H") ]
ps = [ Professor(cs[0:2], "P1"), Professor(cs[2:5], "P2"), Professor(cs[5:], "P3") ]


slots = [ Slot("M1_seg", 3), Slot("M2_seg", 2), Slot("M1_ter", 3), Slot("M2_ter", 2) \
        , Slot("N1_seg", 2), Slot("N2_seg", 2), Slot("N1_ter", 2), Slot("N2_ter", 2) ]

matutino =  Semester(slots[0:4], "Mat")
noturno  =  Semester(slots[4:8], "Not")

semesters = [ matutino, noturno ]


days = [ Day(slots[0:2] + slots[4:6], "Seg.") \
       , Day(slots[2:4] + slots[6:8], "Ter.") ]

shifts = [ Shift(slots[0:2], "Mat") \
         , Shift(slots[2:4], "Mat") \
         , Shift(slots[4:6], "Not") \
         , Shift(slots[6:8], "Not") ]

prof_slot = {}

for c in cs:
    for p in ps:
        for s in slots:
            prof_slot[(p, c, s)] = \
                    pulp.LpVariable(p.name + "_" + c.name + "_ " + s.name, 0, 1, pulp.LpInteger)


def solve(professors, courses, semesters, days, shifts, slots):

    prob = pulp.LpProblem("Semester Problem", pulp.LpMaximize)
    prob += pulp.lpSum([v for (k,v) in prof_slot.items()])

    #print(prof_slot.keys())

    #for s in slots:
    #    prob += pulp.lpSum([prof_slot[(p, c, s)] for p in professors for c in courses]) <= 1

    
    #for p in professors:
    #    for c in p.courses:
    #        v = pulp.lpSum([s.size * prof_slot[(p, c, s)] for s in slots])
    #        prob += v <= (c.num_hours + 0.1)
    #        prob += v >= (c.num_hours - 0.1)


    #for p in professors:
    #    prob += pulp.lpSum([s.size * prof_slot[(p, c, s)] for c in p.courses for s in slots]) == p.total_time()


    # maximum one professor per slot of time
    #for p in professors:
    #    prob += pulp.lpSum([prof_slot[(p,st)] for sh in shifts for st in sh.slots]) <= 1.1


    print(professors)
    print(courses)
    print(semesters)
    print(days)
    print(shifts)
    print(slots)
    prob.writeLP("problem.lp")
    prob.solve()
    print("Status:", pulp.LpStatus[prob.status])
    for v in prob.variables():
        print(v.name, "=", v.varValue)



solve(ps, cs, semesters, days, shifts, slots)
