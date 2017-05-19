from model import Professor, Course, Slot, Semester, dias

alg_extra    = Course("ALG+"    , 5)
ed1          = Course("ED1"     , 5)
ed1_extra    = Course("ED1+"    , 5)
dig          = Course("DIG"     , 5)
ed2_extra    = Course("ED2+"    , 5)
bd1          = Course("BD1"     , 5)
prog2        = Course("PROG2"   , 5)
teo          = Course("TEORIA"  , 5)
grafos       = Course("GRAFOS"  , 5)
grafos_extra = Course("GRAFOS+" , 5)
es2          = Course("ES2"     , 5)
redes        = Course("REDES"   , 5)
cg           = Course("CG"      , 5)
pgp          = Course("PGP"     , 5)
comp         = Course("COMP"    , 5)
opt3         = Course("OPT3"    , 5)
opt4         = Course("OPT4"    , 5)
seg          = Course("SEG"     , 5)
tcc2         = Course("TCC2"    , 5)

iinf    = Course("I.INF"  , 4)
alg     = Course("ALG"    , 4)
circ    = Course("CIRC"   , 4)
ed2     = Course("ED2"    , 4)
prog1   = Course("PROG1"  , 4)
bd2     = Course("BD2"    , 4)
es1     = Course("ES1"    , 4)
ipc     = Course("IPC"    , 4)
teo2    = Course("TEORIA" , 4)
grafos2 = Course("GRAFOS" , 4)
ia      = Course("IA"     , 4)
comp2   = Course("COMP"   , 4)
cg2     = Course("CG"     , 4)
so      = Course("SO"     , 4)
cdist   = Course("C.D."   , 4)
seg2    = Course("SEG"    , 4)
opt2    = Course("OPT2"   , 4)
tcc1    = Course("TCC1"   , 4)

cs = [ alg_extra    , iinf    
     , ed1          , alg     
     , ed1_extra    , circ    
     , dig          , ed2     
     , ed2_extra    , prog1   
     , bd1          , bd2     
     , prog2        , es1     
     , teo          , ipc     
     , grafos       , teo2    
     , grafos_extra , grafos2 
     , es2          , ia      
     , redes        , comp2   
     , cg           , cg2     
     , pgp          , so    
     , comp         , cdist   
     , opt3         , seg2    
     , opt4         , opt2    
     , seg          , tcc1    
     , tcc2 ]

ps = [ Professor([alg, alg_extra, prog1, prog2], "Priscila")
     , Professor([ed1, grafos, grafos_extra, grafos2], "Doglas")
     , Professor([ed1_extra, ed2_extra, seg, seg2], "Jacson")
     , Professor([circ, dig], "Emilio")
     , Professor([bd1, teo, teo2, ed2], "Ricardo")
     , Professor([ipc, opt4, es2], "Grazi")
     , Professor([ia, cg, cg2], "Jose")
     , Professor([tcc1, redes, so], "Marco")
     , Professor([pgp, es1], "Raquel")
     , Professor([comp, comp2, cdist], "Braulio")
     , Professor([circ, opt3], "Padilha")
     , Professor([iinf], "Andressa")
     , Professor([alg, bd2], "Guilherme")
     , Professor([opt2, tcc1], "Pavan") ]

m1s = [Slot("M1_seg", 2.9)] + [Slot("M1_%s" % d, 3) for d in dias[1:]]
m2s = [Slot("M2_seg", 1.9)] + [Slot("M2_%s" % d, 2) for d in dias[1:]]
t1s = [Slot("T1_seg", 2.9)] + [Slot("T1_%s" % d, 3) for d in dias[1:]]
t2s = [Slot("T2_seg", 1.9)] + [Slot("T2_%s" % d, 2) for d in dias[1:]]
#t1s = [Slot("T1_%s" % d, 3) for d in dias]
#t2s = [Slot("T2_%s" % d, 2) for d in dias]
n1s = [Slot("N1_%s" % d, 2) for d in dias[:-1]] + [Slot("N1_sexta", 1.9)]
n2s = [Slot("N2_%s" % d, 1.95) for d in dias[:-1]] + [Slot("N2_sexta", 1.8)]

slots = m1s + m2s + t1s + t2s + n1s + n2s

#extras = Semester(m1s + m2s + t1s + t2s, "Extra")
extras = Semester(t1s + t2s, "Extra")
extras.add_courses([alg_extra, ed1_extra, ed2_extra, grafos_extra])

vesp2 = Semester(t1s + t2s, "2a Fase - Vespertino")
vesp2.add_courses([ed1, dig])

mat4 = Semester(m1s + m2s, "4a Fase - Matutino")
mat4.add_courses([bd1, prog2, teo, grafos])

mat6 = Semester(m1s + m2s, "6a Fase - Matutino")
mat6.add_courses([es2, redes, cg, pgp, comp])

mat8 = Semester(m1s + m2s, "8a Fase - Matutino")
#mat8.add_courses([opt3, opt4, seg, tcc2])
mat8.add_courses([opt3, opt4, seg])

not1 = Semester(n1s + n2s, "1a Fase - Noturno")
not1.add_courses([iinf, alg, circ])

not3 = Semester(n1s + n2s, "3a Fase - Noturno")
not3.add_courses([ed2, prog1])

not5 = Semester(n1s + n2s, "5a Fase - Noturno")
not5.add_courses([bd2, es1, ipc, teo2, grafos2])

not7 = Semester(n1s + n2s, "7a Fase - Noturno")
not7.add_courses([ia, comp2, cg2, so])

not9 = Semester(n1s + n2s, "9a Fase - Noturno")
#not9.add_courses([cdist, seg2, opt2, tcc1])
not9.add_courses([cdist, seg2, opt2])


semesters = [ extras
            , vesp2
            , mat4, mat6, mat8
            , not1, not3, not5, not7, not9 ]

proibidos = []

for x in zip(m1s, n1s):
    proibidos.append(x)
for x in zip(m1s, n2s):
    proibidos.append(x)
for x in zip(m2s, n1s):
    proibidos.append(x)
for x in zip(m2s, n2s):
    proibidos.append(x)

evitar = []
for x in zip(m1s, m2s):
    evitar.append(x)
for x in zip(t1s, t2s):
    proibidos.append(x)
for x in zip(n1s, n2s):
    proibidos.append(x)


for x in zip(m1s[1:], n2s):
    proibidos.append(x)


