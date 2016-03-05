
choixDeCoursValide(Etudiant,ChoixDeCours):-
	forall(member(C, ChoixDeCours), cours(C)),
	coursPrealableComplete(Etudiant,ChoixDeCours),
	creditPrealableValide(Etudiant, ChoixDeCours),
	corequisValide(Etudiant, ChoixDeCours).
	
coursPrealableComplete(Etudiant, []).
coursPrealableComplete(Etudiant, [A|T]) :-
	prop(coursPrealable, A, Prealables),
	coursComplete(Etudiant, I),
	forall(member(C, Prealables), member(C, I)),
	coursPrealableComplete(Etudiant, T).
	
coursPrealableComplete(Etudiant, [A|T]) :-
	\+ prop(coursPrealable, A, Prealables),
	coursPrealableComplete(Etudiant, T).

creditPrealableValide(Etudiant, []).	
creditPrealableValide(Etudiant, [A|T]):-
	coursComplete(Etudiant, Cours),
	sommeCredit(Cours, Somme),
	assezDeCredits(Somme, A),
	creditPrealableValide(Etudiant, T).
	
assezDeCredits(Somme, Cours):-
	prop(creditPrealable, Cours, Credit),
	Somme >= Credit.

assezDeCredits(Somme, Cours):-
	\+ prop(creditPrealable, Cours, Credit).
	
corequisValide(Etudiant, []).
corequisValide(Etudiant, [A|T]) :-
	prop(corequis, A, Corequis),
	forall(member(C, Corequis), member(C, T)),
	corequisValide(Etudiant, T).
	
corequisValide(Etudiant, [A|T]) :-
	prop(corequis, A, Corequis),
	coursComplete(Etudiant, I),
	forall(member(C, Corequis), member(C, I)),
	corequisValide(Etudiant, T).
	
corequisValide(Etudiant, [A|T]) :-
	\+ prop(corequis, A, Corequis),
	corequisValide(Etudiant, T).
	
sommeCredit([], 0).
sommeCredit([H|T], Sum):-
	sommeCredit(T, Rest),
	prop(credits, H, C),
	Sum is C + Rest.

% liste des cours
cours(inf1005c).
cours(inf1500).
cours(mth1101).
cours(mth1006).
cours(log3005i).
cours(inf1040).
cours(inf1010).
cours(log1000).
cours(inf1600).
cours(mth1102).
cours(inf1995).
cours(inf2010).
cours(log2420).
cours(log2810).
cours(mth2302d).
cours(log2420).
cours(mth1210).
cours(inf2610).
cours(inf3710).
cours(inf2990).
cours(ssh5100).
cours(inf3405).
cours(phs1101).
cours(ssh5201).
cours(log3430).
cours(ssh5501).
cours(inf4705).
cours(log3210).
cours(log3000).
cours(log3900).
cours(log3005).
cours(log4410).
cours(log4430).
cours(phs4700).
cours(log4900).
cours(inf8301).

%credits
prop(credits, inf1005c, 3).
prop(credits, inf1500, 3).
prop(credits, mth1101, 2).
prop(credits, mth1006, 2).
prop(credits, log3005i, 0).
prop(credits, inf1040, 3).
prop(credits, inf1010, 3).
prop(credits, log1000, 3).
prop(credits, inf1600, 3).
prop(credits, mth1102, 2).
prop(credits, inf1995, 4).
prop(credits, inf2010, 3).
prop(credits, log2420, 3).
prop(credits, log2810, 3).
prop(credits, mth2302d, 3).
prop(credits, log2420, 3).
prop(credits, mth1210, 1).
prop(credits, inf2610, 3).
prop(credits, inf3710, 3).
prop(credits, inf2990, 4).
prop(credits, ssh5100, 3).
prop(credits, inf3405, 3).
prop(credits, phs1101, 3).
prop(credits, ssh5201, 3).
prop(credits, log3430, 3).
prop(credits, ssh5501, 2).
prop(credits, inf4705, 3).
prop(credits, log3210, 3).
prop(credits, log3000, 3).
prop(credits, log3900, 4).
prop(credits, log3005, 1).
prop(credits, log4410, 3).
prop(credits, log4430, 3).
prop(credits, phs4700, 3).
prop(credits, log4900, 6).
prop(credits, inf8301, 3).

%liste des prealable
prop(coursPrealable, inf1010, [inf1005c]).
prop(coursPrealable, log1000, [inf1005c]).
prop(coursPrealable, inf1600, [inf1005c, inf1500]).
prop(coursPrealable, mth1102, [mth1101]).
prop(coursPrealable, inf1995, [inf1040]).
prop(coursPrealable, inf2010, [inf1010]).
prop(coursPrealable, log2410, [inf1010,log1000]).
prop(coursPrealable, mth1110, [mth1101,mth1006]).
prop(coursPrealable, inf2610, [inf1010,inf1600]).
prop(coursPrealable, inf3710, [inf2010]).
prop(coursPrealable, inf2990, [inf2010,log2410,inf1995]).
prop(coursPrealable, inf3405, [mth2302d]).
prop(coursPrealable, log3430, [log1000,mth2302d,log2810]).
prop(coursPrealable, inf4705, [inf2010,log2810]).
prop(coursPrealable, log3210, [inf2010,log1000,log2810]).
prop(coursPrealable, log3000, [inf2990]).
prop(coursPrealable, log3900, [inf2990]).
prop(coursPrealable, log3005, [log3005i]).
prop(coursPrealable, log4410, [log2810]).
prop(coursPrealable, log4430, [log2410]).
prop(coursPrealable, phs4700, [mth1210]).
prop(coursPrealable, log4900 ,[log3900]).

prop(creditPrealable, ssh5201, 27).
prop(creditPrealable, ssh5501, 27).
prop(creditPrealable, log4900, 85).

%liste des corequis
prop(corequis, mth1102, [mth1006]).
prop(corequis, inf1995, [inf1600, log1000]).
prop(corequis, inf2010, [log2810]).
prop(corequis, log2810, [inf2010]).
prop(corequis, mth2302d, [mth1101]).
prop(corequis, log2420, [inf2010]).
prop(corequis, mth1210, [mth1110]).
prop(corequis, inf3710, [inf2610]).
prop(corequis, inf2990, [log2420]).
prop(corequis, log3000, [log3900]).
prop(corequis, log3900, [log3000, log3005]).
prop(corequis, log3005, [log3900]).

%etudiant
etudiant(alex).
coursComplete(alex, [inf1005c]).




