from sympy import *
from sympy import plotting
from sympy import geometry
import random
from typing import Callable

def getDXYSum(population: list[tuple[float, float]]) -> float:
	'''
	Получение суммы расстоний между точками популяции (x, y)
	
	:param population: популяция точек

	:return: сумма расстояний между точками
	'''
	if not population:
		return None

	dXYSum = 0.0
	for i in population:
		for j in population:
			if i == j:
				continue
			dXYSum += sqrt((j[0] - i[0])**2 + (j[1] - i[1])**2)
	return dXYSum

def getDEMinimum(fXY: Callable[[float, float], float], limX: tuple[float, float], limY: tuple[float, float], n: int, f: float, p: float, cycles: int = None, e: float = None, pointPopulations: list[list[tuple[float, float]]] = None) -> tuple[float, float]:
	'''
	Получение точки минимума f(x,y) дифференицальной эволюции

	:param fXY: f(x,y)
	:param limX: интервал поиска по x
	:param limY: интервал поиска по y
	:param n: размер популяции точек поиска
	:param f: сила мутации
	:param p: вероятность мутации
	:param cycles: ограничение по количеству итераций
	:param e: ограничение по сумме расстояний между точками популяции
	:pointPopulations: массив для помещения массивов точек популяций
	
	:return: точка минимума
	'''
	if not fXY or not limX or not limY or (n or 0) < 4 or f is None or f < 0.0 or f > 1.0 or p is None or p < 0.0 or p > 1.0 or ((cycles or 0) <= 0 and (e or 0.0) <= 0.0):
		return None

	getMutantCoordinate = lambda cA, cB, cC: cC + f * (cA - cB)
	xyMin: tuple[float, float] = None
	currentPopulation: list[tuple[float, float]] = []
	for i in range(n):
		currentPopulation.append((random.uniform(limX[0], limX[1]), random.uniform(limY[0], limY[1])))
	currentCycle = 0

	while True:
		not pointPopulations is None and pointPopulations.append(currentPopulation)
		fMin = min(fXY(p[0], p[1]) for p in currentPopulation)
		xyMin = next(p for p in currentPopulation if fXY(p[0], p[1]) == fMin) 
		# Достигнут лимит итераций или суммы расстояний между точками
		if (not cycles is None and currentCycle >= cycles) or (not e is None and getDXYSum(currentPopulation) < e):
			break
		currentCycle += 1
		nextPopulation: list[tuple[float, float]] = []
		for xi in currentPopulation:
			remainingPoints = list(filter(lambda p: p != xi, currentPopulation))
			xA = remainingPoints[random.randint(0, len(remainingPoints) - 1)]
			remainingPoints.remove(xA)
			xB = remainingPoints[random.randint(0, len(remainingPoints) - 1)]
			remainingPoints.remove(xB)
			xC = remainingPoints[random.randint(0, len(remainingPoints) - 1)]
			xM = (getMutantCoordinate(xA[0], xB[0], xC[0]), getMutantCoordinate(xA[1], xB[1], xC[1]))
			xT = (xM[0] if random.random() > p else xi[0], xM[1] if random.random() > p else xi[1])
			nextPopulation.append(xT if fXY(xT[0], xT[1]) < fXY(xi[0], xi[1]) else xi)
		currentPopulation = nextPopulation
		
	return xyMin

x, y = symbols('x y', positive = True) # Символьные переменные

# Функция 39
f1 = sin(x) * exp((1 - cos(y))**2) + cos(y) * exp((1 - sin(x))**2) + (x - y)**2
lim1 = (-6.0, 6.0)
minF1XY1 = (4.70104, 3.15294)
minF1XY2 = (-1.58214, -3.13024)

f1Eval = lambda xVal, yVal: f1.subs([(x, xVal), (y, yVal)]).evalf()
pointPopulations: list[tuple[float, float]] = []
calculatedMin = getDEMinimum(f1Eval, lim1, lim1, 10, 0.5, 0.9, e=0.001, pointPopulations=pointPopulations)
dXY1 = sqrt((minF1XY1[0] - calculatedMin[0])**2 + (minF1XY1[1] - calculatedMin[1])**2)
dXY2 = sqrt((minF1XY2[0] - calculatedMin[0])**2 + (minF1XY2[1] - calculatedMin[1])**2)
print(f'f1(x, y): {f1}')
print(f'f1(x, y) -> min1 analytical: ({minF1XY1[0]},{minF1XY1[1]})')
print(f'f1(x, y) -> min2 analytical: ({minF1XY2[0]},{minF1XY2[1]})')
print(f'f1(x, y) -> min computed: ({calculatedMin[0]},{calculatedMin[1]})')
print(f'd f(x,y) -> min1: {dXY1}')
print(f'd f(x,y) -> min2: {dXY2}')
print(f'Iterations: {len(pointPopulations) - 1}')
print(f'\n')
#print(f'Search populations: {pointPopulations}')
#print(f'\n')

# График целевой функции
for i in [0, 0.25, 0.75, 1]:
	populationIndex = round(i * (len(pointPopulations) - 1))
	currentPopulation = pointPopulations[populationIndex]
	p = plotting.plot_contour(f1, (x, -7, 7), (y, -7, 7), xlim=(-7, 7), ylim=(-7, 7), markers=[{'args': [minF1XY1[0], minF1XY1[1]], 'color': "red", 'marker': "x", 'ms': 7}, {'args': [minF1XY2[0], minF1XY2[1]], 'color': "red", 'marker': "x", 'ms': 7}], show = False, aspect_ratio = (1, 1), title = f'Population {populationIndex}')
	pointMarkers = []
	for point in currentPopulation:
		pointMarkers.append({'args': [point[0], point[1]], 'color': "magenta", 'marker': "x", 'ms': 3})
	p.extend(plot(0, markers=pointMarkers, show = False))
	p.show()

# Функция 9
f1 = (4 - 2.1*x**2 + x**4 / 3) * x**2 + x * y + (-4 + 4 * y**2) * y**2
lim1 = (-2.0, 2.0)
minF1XY1 = (0.089842, 0.7126564)
minF1XY2 = (-0.089842, -0.7126564)
minF1XY3 = (-0.089842, 0.7126564)
minF1XY4 = (0.089842, -0.7126564)

f1Eval = lambda xVal, yVal: f1.subs([(x, xVal), (y, yVal)]).evalf()
pointPopulations: list[tuple[float, float]] = []
calculatedMin = getDEMinimum(f1Eval, lim1, lim1, 10, 0.5, 0.9, e=0.001, pointPopulations=pointPopulations)
dXY1 = sqrt((minF1XY1[0] - calculatedMin[0])**2 + (minF1XY1[1] - calculatedMin[1])**2)
dXY2 = sqrt((minF1XY2[0] - calculatedMin[0])**2 + (minF1XY2[1] - calculatedMin[1])**2)
dXY3 = sqrt((minF1XY3[0] - calculatedMin[0])**2 + (minF1XY3[1] - calculatedMin[1])**2)
dXY4 = sqrt((minF1XY4[0] - calculatedMin[0])**2 + (minF1XY4[1] - calculatedMin[1])**2)
print(f'f2(x, y): {f1}')
print(f'f2(x, y) -> min1 analytical: ({minF1XY1[0]},{minF1XY1[1]})')
print(f'f2(x, y) -> min2 analytical: ({minF1XY2[0]},{minF1XY2[1]})')
print(f'f2(x, y) -> min3 analytical: ({minF1XY3[0]},{minF1XY3[1]})')
print(f'f2(x, y) -> min4 analytical: ({minF1XY4[0]},{minF1XY4[1]})')
print(f'f2(x, y) -> min computed: ({calculatedMin[0]},{calculatedMin[1]})')
print(f'd f(x,y) -> min1: {dXY1}')
print(f'd f(x,y) -> min2: {dXY2}')
print(f'd f(x,y) -> min3: {dXY3}')
print(f'd f(x,y) -> min4: {dXY4}')
print(f'Iterations: {len(pointPopulations) - 1}')
print(f'\n')
#print(f'Search populations: {pointPopulations}')
#print(f'\n')

# График целевой функции
for i in [0, 0.25, 0.75, 1]:
	populationIndex = round(i * (len(pointPopulations) - 1))
	currentPopulation = pointPopulations[populationIndex]
	p = plotting.plot_contour(f1, (x, -3, 3), (y, -3, 3), xlim=(-3, 3), ylim=(-3, 3), markers=[{'args': [minF1XY1[0], minF1XY1[1]], 'color': "red", 'marker': "x", 'ms': 7}, {'args': [minF1XY2[0], minF1XY2[1]], 'color': "red", 'marker': "x", 'ms': 7}, {'args': [minF1XY3[0], minF1XY3[1]], 'color': "red", 'marker': "x", 'ms': 7}, {'args': [minF1XY4[0], minF1XY4[1]], 'color': "red", 'marker': "x", 'ms': 7}], show = False, aspect_ratio = (1, 1), title = f'Population {populationIndex}')
	pointMarkers = []
	for point in currentPopulation:
		pointMarkers.append({'args': [point[0], point[1]], 'color': "magenta", 'marker': "x", 'ms': 3})
	p.extend(plot(0, markers=pointMarkers, show = False))
	p.show()