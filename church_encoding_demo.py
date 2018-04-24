#Patryk Wegrzyn
#Zadanie 2

#Liczebniki:
ZERO = lambda f: lambda x: x
ONE = lambda f: lambda x: f(x)
TWO = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))
FOUR = lambda f: lambda x: f(f(f(f(x))))
FIVE = lambda f: lambda x: f(f(f(f(f(x)))))
SIX = lambda f: lambda x: f(f(f(f(f(f(x))))))
SEVEN = lambda f: lambda x: f(f(f(f(f(f(f(x)))))))
EIGHT = lambda f: lambda x: f(f(f(f(f(f(f(f(x))))))))
NINE = lambda f: lambda x: f(f(f(f(f(f(f(f(f(x)))))))))

#Operacje arytmetyczne:
SUCC = (lambda n: lambda f: lambda x: f(n(f)(x)))
PRED = (lambda n: lambda f: lambda x: ((n(lambda g: lambda h: h(g(f))))(lambda u: x))(lambda u: u))
ADD = (lambda m: lambda n: lambda f: lambda x: (m)(f)(n(f)(x)))
#funckje SUB zdefiniuje przy pomocy funkcji PRED, z uwagi ze implementacja bedzie bardziej czytelna i prostsza
SUB = (lambda m: lambda n: (n(PRED))(m))	
#funckje MULT i EXP wprost bazuja na matematycznych definicjach aplikowania funkcji to zmiennych
MULT = (lambda m: lambda n: lambda f: m(n(f)))
EXP = (lambda m: lambda n: lambda f: lambda x: (n(m))(f)(x))

#Wartosci logczine:
TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y

#Operatory logiczne:
AND = (lambda p: lambda q: (p(q))(p))						# p&&q
OR = (lambda p: lambda q: (p(p))(q))						# p||q
NOT = (lambda p: lambda a: lambda b: (p(b))(a))				# !p
XOR = (lambda a: lambda b: (a(NOT(b)))(b))					# a^b
IF = (lambda p: lambda a: lambda b: (p(a))(b))				# if p then a else b

#Binarne i unarne operatory liczbowe zwracajace wartosci logczine
ISZERO = (lambda n: (n(lambda x: FALSE))(TRUE))				# n == 0
LEQ = (lambda m: lambda n: ISZERO(SUB(m)(n)))				# m <= n
EQ = (lambda m: lambda n: AND(LEQ(m)(n))(LEQ(n)(m)))		# m == n
NEQ = (lambda m: lambda n: NOT(EQ(m)(n)))					# m != n
LESS = (lambda m: lambda n: AND(LEQ(m)(n))(NEQ(m)(n)))		# m < n
GEQ = (lambda m: lambda n: NOT(LESS(m)(n)))					# m >= n
GREATER = (lambda m: lambda n: AND(GEQ(m)(n))(NEQ(m)(n)))	# m > n

#Pary i listy:
#Implementacja, w ktorej kazdemu node'owe listy odpowiada jedna para, cos jak linked list tylko rekurencyjnie
PAIR = (lambda x: lambda y: lambda z: (z(x))(y))
LEFT = (lambda p: p(lambda x: lambda y: x))
RIGHT = (lambda p: p(lambda x: lambda y: y))
EMPTY = PAIR(TRUE)(FALSE)
UNSHIFT = (lambda l: lambda x: PAIR(FALSE)(PAIR(x)(l)))
ISEMPTY = LEFT
FIRST = (lambda l: LEFT(RIGHT(l)))
REST = (lambda l: RIGHT(RIGHT(l)))

#Inne:
#Y kombinator odpowiada za mechanizm rekurencji w rachunku lambda (dziala dla non-strict jezykow jak Haskell)
#Z kombinator działa dla strict jezykow jak Ruby czy Python (unika nieskonczonej rekurencji)
YCOMB = (lambda f: (lambda x: (f(x(x)))(lambda x: f(x(x)))))
ZCOMB = (lambda f: (lambda x: f(lambda u: (x(x))(u)))(lambda x: f(lambda u: (x(x))(u))))
#RANGE tworzy listow intow z zadanego przedzialu
RANGE = (ZCOMB(lambda f: lambda m: lambda n: IF(LEQ(m)(n))(lambda x: UNSHIFT(f(SUCC(m))(n))(m)(x))(EMPTY)))
#DIV to dzielenie calkowitoliczbowe
DIV = (ZCOMB(lambda f: lambda m: lambda n: IF(LEQ(n)(m))(lambda x: SUCC(f(SUB(m)(n))(n))(x))(ZERO)))
#FOLD redukuja dana liste przy pomocy odpowiednich kombinatorow
FOLD = (ZCOMB(lambda f: lambda l: lambda x: lambda g: IF(ISEMPTY(l))(x)(lambda y: g(f(REST(l))(x)(g))(FIRST(l))(y))))
#PUSH dodaje to listy
PUSH = (lambda l: lambda x: FOLD(l)(UNSHIFT(EMPTY)(x))(UNSHIFT))
#MOD operacja modulo
MOD = (ZCOMB(lambda f: lambda m: lambda n: IF(LEQ(n)(m))(lambda x: f(SUB(m)(n))(n)(x))(m)))
TEN = MULT(TWO)(FIVE)
#TODIGITS zamienia liczbe na liste cyfr
TODIGITS = (ZCOMB(lambda f: lambda n: PUSH(IF(LEQ(n)(PRED(TEN)))(EMPTY)(lambda x: f(DIV(n)(TEN))(x)))(MOD(n)(TEN))))
#MAP mapuje dana funckje na liste
MAP = (lambda k: lambda f: FOLD(k)(EMPTY)(lambda l: lambda x: UNSHIFT(l)(f(x))))
#SUM_FROM_1_TO_N liczy sume liczb on 1 to n
SUM_FROM_1_TO_N = (lambda n: FOLD(RANGE(ONE)(n))(ZERO)(ADD))
#FACTORIAL liczy n!
FACTORIAL = (lambda n: FOLD(RANGE(ONE)(n))(ONE)(MULT))

#Przydatne funkcje:		
to_int = lambda x: x(lambda y: y + 1)(0)
to_bool = (lambda f: (f(True))(False))
#funkcja to_int_array zamienia tablice napisana za pomoca rachunku lambda na tablice integerow
#chcialem zrobic to tak jak jest w eseju "Programming with nothing"
#czyli najpierw zrobic funkcje to array, ktora zamienia tablice napisana w rach. lambda na
#zwykla python'owa tablice funckji ale okazalo sie ze funkcja map nie dziala wtedy, bo
#w Pythonie nie mozna iterowac po funkcjach
def to_int_array(f):
	array = []
	while True:
		array.append(FIRST(f))
		array[len(array)-1] = to_int(array[len(array)-1])
		f = REST(f)
		if to_bool(ISEMPTY(f)):
			break
	return array

def to_char(f):
	array = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	return array[to_int(f)]

def to_string(f):
	array = []
	while True:
		array.append(FIRST(f))
		array[len(array)-1] = to_char(array[len(array)-1])
		f = REST(f)
		if to_bool(ISEMPTY(f)):
			break
	return ''.join(array)

#definiuje litery alfabetu, cyfry juz sa zdefiniowane
A = TEN
B = SUCC(A)
C = SUCC(B)
D = SUCC(C)
E = SUCC(D)
F = SUCC(E)
G = SUCC(F)
H = SUCC(G)
I = SUCC(H)
J = SUCC(I)
K = SUCC(J)
L = SUCC(K)
M = SUCC(L)
N = SUCC(M)
O = SUCC(N)
P = SUCC(O)
Q = SUCC(P)
R = SUCC(Q)
S = SUCC(R)
T = SUCC(S)
U = SUCC(T)
V = SUCC(U)
W = SUCC(V)
X = SUCC(W)
Y = SUCC(X)
Z = SUCC(Y)

#Testy:
HELLOWORLD = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(D))(L))(R))(O))(W))(O))(L))(L))(E))(H)
print(to_string(HELLOWORLD))
print('5! =', to_int(FACTORIAL(FIVE)))
print('Sum from 1 to 9 =', to_int(SUM_FROM_1_TO_N(NINE)))
print('9 / 2 =', to_int(DIV(NINE)(TWO)), 'r', to_int(MOD(NINE)(TWO)))
print('Succesor of 5 is', to_int(SUCC(FIVE)))
print('Predaccesor of 7 is', to_int(PRED(SEVEN)))
TWENTYFIVE = (EXP(FIVE)(TWO))
FIFTY = (MULT(TWENTYFIVE)(TWO))

#Przykladowy program, ktory pokazuje, ze mozna za pomoca takich mechanizmow programowac:
#Program zwraca liste, w ktorej element pod indeksem n znajduje (n mod 7)+5,
#chyba ze n mod 7 wynosi zero, wtedy pod ten indeks laduje n**2

MAP(RANGE(TEN)(FIFTY))(lambda n: IF(ISZERO(MOD(n)(SEVEN)))(EXP(n)(TWO))(ADD(FIVE)(MOD(n)(SEVEN))))

#Wizualny efekt dzialanie programu:
print(to_int_array(MAP(RANGE(TEN)(FIFTY))(lambda n: IF(ISZERO(MOD(n)(SEVEN)))(EXP(n)(TWO))(ADD(FIVE)(MOD(n)(SEVEN))))))