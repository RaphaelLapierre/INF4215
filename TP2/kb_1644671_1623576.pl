isQualite(ChoixDeCours):-
    sommeCredit(ChoixDeCours, Somme),
    Somme =< 18,
    Somme >= 12.
    
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

aborde(C, S) :-
    prop(aborde, C, S).

aborde(C, S) :-
    prop(aborde, C, S2),
    sousSujet(S2, S).

utiliseLangage(C, L):-
	prop(langage, C, L).

programmeOffrantCours(P, C):-
	prop(programme, C, P).

coursClasseInverse(C):-
	prop(inverse, C).

coursObligatoire(C):-
	prop(obligatoire, C).

coursOptionel(C):-
	prop(optionel, C).

coursProjet(C):-
	prop(projet, C).

coursObligatoiresSuivi(E, []).
coursObligatoiresSuivi(E, [H|T]):-
	coursComplete(E, C),
	member(H, C),
	prop(obligatoire, H),
	coursObligatoiresSuivi(E, T).

coursOptionelsSuivi(E, []).
coursOptionelsSuivi(E, [H|T]):-
	coursComplete(E, C),
	member(H, C),
	prop(optionel, H),
	coursOptionelsSuivi(E, T).

coursProjetSuivi(E, []).
coursProjetSuivi(E, [H|T]):-
	coursComplete(E, C),
	member(H, C),
	prop(projet, H),
	coursProjetSuivi(E, T).

inscritOrientation(E, O):-
	orientation(E, O).

orientationThematique(O):-
	prop(thematique, O).

inscriptionEchange(E, []).
inscriptionEchange(E, [H|T]):-
	propEtudiant(echange, E),
	prop(echange, H),
	inscriptionEchange(E, T).

equivalence(C, []).
equivalence(C, [H|T]):-
	aborde(C, H),
	equivalence(C, T).

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
cours(inf3500).
cours(inf4215).
cours(inf8702).
cours(inf4710).
cours(inf8601).
cours(inf8225).

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

sujet(informatique).
%Sujet
sousSujet(A,B) :- 
    prop(sous_sujet, A, B).
sousSujet(X, C2) :-
    prop(sous_sujet,X, C1),
    sousSujet(C1, C2).
    
prop(sous_sujet, algorithmie, informatique).
prop(sous_sujet, qualite_logiciel, informatique).
prop(sous_sujet, compilateur, informatique ).
prop(sous_sujet, math_discrete, mathematique).
prop(sous_sujet, algebre, mathematique ).
prop(sous_sujet, calculus, mathematique).
prop(sous_sujet, methode_numerique, mathematique).
prop(sous_sujet, comptabilite, economie ).
prop(sous_sujet, technologie, sociologie).
prop(sous_sujet, loi, ethique).
prop(sous_sujet, strucuture_donne, algorithmie).
prop(sous_sujet, base_donne, algorithmie).
prop(sous_sujet, test, qualite_logiciel).
prop(sous_sujet, processus, qualite_lociel).
prop(sous_sujet, conception, informatique).
prop(sous_sujet, systeme_exploitation, informatique).
prop(sous_sujet, uml, conception).
prop(sous_sujet, patron, conception).
prop(sous_sujet, design, conception).
prop(sous_sujet, anti_patron, conception).
prop(sous_sujet, interface, conception).
prop(sous_sujet, langage, compilateur).
prop(sous_sujet, architecture, conception).
prop(sous_sujet, web, informatique).
prop(sous_sujet, html, web).
prop(sous_sujet, javascript, web).
prop(sous_sujet, complexite, algorithmie).
prop(sous_sujet, reseau, informatique).
prop(sous_sujet, mecanique, physique).
prop(sous_sujet, physique_multimedia, physique).
prop(sous_sujet, strucuture_donne, qualite_lociel).


prop(aborde, inf1005c, algorithmie).
prop(aborde, inf1500, system_numerique).
prop(aborde, mth1101, calculus).
prop(aborde, mth1006, algebre).
prop(aborde, log3005i, communication).
prop(aborde, inf1040, informatique).
prop(aborde, inf1010, algorithmie).
prop(aborde, log1000, informatique).
prop(aborde, inf1600, micro_ordinateur).
prop(aborde, mth1102, calculus).
prop(aborde, inf1995, informatique).
prop(aborde, inf2010, strucuture_donne).
prop(aborde, log2420, interface).
prop(aborde, log2810, math_discrete).
prop(aborde, mth2302d, probabilite).
prop(aborde, log2420, conception).
prop(aborde, mth1210, methode_numerique).
prop(aborde, inf2610, systeme_exploitation).
prop(aborde, inf3710, base_donne).
prop(aborde, inf2990, informatique).
prop(aborde, ssh5100, sociologie).
prop(aborde, inf3405, reseau).
prop(aborde, phs1101, mecanique).
prop(aborde, ssh5201, comptabilite).
prop(aborde, log3430, test).
prop(aborde, ssh5501, technologie).
prop(aborde, inf4705, algorithmie).
prop(aborde, log3210, langage).
prop(aborde, log3000, processus).
prop(aborde, log3900, informatique).
prop(aborde, log3005, communication).
prop(aborde, log4410, methode_formelles).
prop(aborde, log4430, architecture).
prop(aborde, phs4700, physique_multimedia).
prop(aborde, log4900, informatique).
prop(aborde, inf8301, qualite_lociel).
prop(aborde, inf4215, algorithmie).
prop(aborde, inf4215, ia).

%etudiant
etudiant(alex).
coursComplete(alex, [inf1005c, log1000, inf1500, inf2010, inf1995, log2995, inf4215, inf8601]).
orientation(alex, multimedia).

etudiant(raph).
coursComplete(raph, [inf1005c, inf1500, inf2010, inf1995, log2995, inf4215, inf8601, mth1102, mth1101, mth1006]).
orientation(raph, mathematique).

%Langage de programmation
prop(langage, inf1005c, cpp).
prop(langage, inf1500, vhdl).
prop(langage, inf1010, cpp).
prop(langage, log1000, scala).
prop(langage, inf1600, x86).
prop(langage, inf1995, cpp).
prop(langage, inf2010, java).
prop(langage, log2810, cpp).
prop(langage, mth1210, matlab).
prop(langage, inf2610, systeme_exploitation).
prop(langage, inf3710, sql).
prop(langage, inf2990, cpp).
prop(langage, inf3405, cpp).
prop(langage, inf4705, cpp).
prop(langage, phs4700, matlab).

%Programmes
prop(programme, inf1005c, informatique).
prop(programme, inf1005c, logiciel).
prop(programme, inf1500, informatique).
prop(programme, inf1500, logiciel).
prop(programme, mth1101, informatique).
prop(programme, mth1006, informatique).
prop(programme, log3005i, informatique).
prop(programme, inf1040, informatique).
prop(programme, inf1010, informatique).
prop(programme, inf1010, logiciel).
prop(programme, log1000, informatique).
prop(programme, inf1600, informatique).
prop(programme, inf1600, logiciel).
prop(programme, mth1102, informatique).
prop(programme, inf1995, informatique).
prop(programme, inf1995, logiciel).
prop(programme, inf2010, informatique).
prop(programme, inf2010, logiciel).
prop(programme, log2420, informatique).
prop(programme, log2810, informatique).
prop(programme, mth2302d, informatique).
prop(programme, log2420, informatique).
prop(programme, mth1210, informatique).
prop(programme, inf2610, informatique).
prop(programme, inf2610, logiciel).
prop(programme, inf3710, informatique).
prop(programme, inf2990, informatique).
prop(programme, ssh5100, informatique).
prop(programme, inf3405, informatique).
prop(programme, phs1101, informatique).
prop(programme, phs1101, physique).
prop(programme, phs1101, logiciel).
prop(programme, ssh5201, informatique).
prop(programme, log3430, informatique).
prop(programme, ssh5501, informatique).
prop(programme, inf4705, informatique).
prop(programme, log3210, logiciel).
prop(programme, log3000, logiciel).
prop(programme, log3900, logiciel).
prop(programme, log3005, logiciel).
prop(programme, log4410, logiciel).
prop(programme, log4430, logiciel).
prop(programme, phs4700, informatique).
prop(programme, phs4700, logiciel).
prop(programme, phs4700, physique).
prop(programme, log4900, informatique).
prop(programme, inf8301, informatique).

%ClasseInverse
prop(inverse, inf4215).
prop(inverse, inf3500).

%Obligatoire
prop(obligatoire, inf1005c).
prop(obligatoire, inf1010).
prop(obligatoire, inf1500).
prop(obligatoire, inf1600).
prop(obligatoire, mth1101).
prop(obligatoire, mth1006).
prop(obligatoire, mth1102).
prop(obligatoire, mth2302d).
prop(obligatoire, phs1101).
prop(obligatoire, ssh5100).
prop(obligatoire, ssh5201).

%Optionel
prop(optionel, inf4215).
prop(optionel, inf8702).
prop(optionel, inf4710).
prop(optionel, inf8601).
prop(optionel, inf8225).

%Projet
prop(projet, inf1995).
prop(projet, inf2995).
prop(projet, inf3995).
prop(projet, inf4995).
prop(projet, log1995).
prop(projet, log2995).
prop(projet, log3995).
prop(projet, log4995).

%Thematique
prop(thematique, developpementDurable).
prop(thematique, innovationTechnologique).
prop(thematique, mathematique).
prop(thematique, outilsDeGestion).
prop(thematique, projetInternationaux).

%Echange
propEtudiant(echange, brice).
prop(echange, inf1005c).
prop(echange, inf1010).
prop(echange, inf1500).
prop(echange, inf1600).
prop(echange, mth1101).
prop(echange, mth1006).
prop(echange, mth1102).
prop(echange, mth2302d).
prop(echange, phs1101).
prop(echange, ssh5100).
prop(echange, ssh5201).
