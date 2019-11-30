SeedRandom[0]
pool=Join[Range[65535],(2#-1)&/@RandomInteger[{2^15+1,2^31},100000],(2#-1)&/@RandomInteger[{2^31+1,2^63},1000000]]
{primes,nonprimes}=DeleteDuplicates[#[[All,2]]]&/@Split[Sort[{!PrimeQ[#],#}&/@pool],First[#1]===First[#2]&]
Print[ToUpperCase[IntegerString[#,16]]]&/@primes
Print["---"]
Print[ToUpperCase[IntegerString[#,16]]]&/@nonprimes
