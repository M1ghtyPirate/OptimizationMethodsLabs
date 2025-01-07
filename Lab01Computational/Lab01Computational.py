from sympy import *
from sympy import plotting
from sympy import geometry
from typing import Callable
from spb import *

def getHookeJeevesMin(f: Callable[[float, float], float], xB: tuple[float, float], s: float, e: float, basisPoints: list[tuple[float, float]] = None) -> tuple[float, float]:
	'''
	Получение точки минимума f(x,y) методом Хука-Дживса

	:param f: f(x,y)
	:param xB: начальная базисная точка поиска
	:param s: шаг изменения координат
	:param e: погрешность поиска
	:param basisPoints: массив для помещения базисных точек

	:return: точка минимума
	'''
	if not f or not xB or (s or 0) <= 0 or (e or 0) <= 0:
		return None

	not basisPoints is None and basisPoints.append(xB)
	while True:
		# Этап исследования
		# Точность достигнута, завершаем поиск
		if s < e:
			break
		xT = (xB[0], xB[1])
		while True:
			for i in range(2):
				for j in [s, -s]:
					#xT = (xB[0], xB[1])
					xT = (xB[0] + (j if i == 0 else 0), xB[1] + (j if i == 1 else 0))
					#xT[i] += j
					# Шаг удачный
					if f(xT[0], xT[1]) < f(xB[0], xB[1]):
						print(f'xB({xB[0]:.3f}, {xB[1]:.3f}): {f(xB[0], xB[1]):.3f}; xT({xT[0]:.3f}, {xT[1]:.3f}): {f(xT[0], xT[1]):.3f}')
						break
				else:
					continue
				# Шаг удачный
				break
			else:
				# Точность достигнута
				if s < e:
					break
				s /= 2
				continue
			# Шаг удачный, переходим к поиску по шаблону
			break

		# Этап поиска по шаблону
		while true:
			xG = (xB[0], xB[1])
			xB = (xT[0], xT[1])
			not basisPoints is None and basisPoints.append(xB)
			# Шаг от нового базиса xB
			#xTa = (xB[0]+2*(xB[0] - xG[0]), xB[1]+2*(xB[1] - xG[1]))
			# Шаг от старого базиса xG
			xTa = (xG[0]+2*(xB[0] - xG[0]), xG[1]+2*(xB[1] - xG[1]))
			print(f'xTa({xTa[0]:.3f}, {xTa[1]:.3f})')
			for i in range(2):
				for j in [s, -s]:
					#xT = (xTa[0], xTa[1])
					xT = (xTa[0] + (j if i == 0 else 0), xTa[1] + (j if i == 1 else 0))
					#xT[i] += j
					# Шаг удачный
					# Сравниваем с точкой шага xTa
					#if f(xT[0], xT[1]) < f(xTa[0], xTa[1]):
						#print(f'xTa({xTa[0], xTa[1]}): {f(xTa[0], xTa[1])}; xT({xT[0], xT[1]}): {f(xT[0], xT[1])}')
					# Сравниваем с точкой базиса xB
					if f(xT[0], xT[1]) < f(xB[0], xB[1]):
						print(f'xB({xB[0]:.3f}, {xB[1]:.3f}): {f(xB[0], xB[1]):.3f}; xT({xT[0]:.3f}, {xT[1]:.3f}): {f(xT[0], xT[1]):.3f}')
						break
				else:
					continue
				# Шаг удачный
				break
			else:
				# Шаг неудачный, возвращаемся к исследованию
				break
			# Шаг удачный, продолжаем поиск по шаблону
			continue

	return xB

# Поиск экстремума
x, y, a, b, c = symbols('x y a b c', positive = True) # Символьные переменные
f = x**2 + y**2 - ( (x**2 + y**2 - ((x - a)**2 + (b - y)**2) + a**2 + b**2) / (2 * sqrt(a**2 + b**2)) )**2 + (x - a)**2 + (b - y)**2 - (((x - a)**2 + (b - y)**2 - ((c - x)**2 + y**2) + (c - a)**2 + b**2) / (2 * sqrt((c - a)**2 + b**2)))**2 + (c - x)**2 + y**2 - (((c - x)**2 + y**2 - (x**2 + y**2) + c**2) / (2 * sqrt(c**2)))**2  # Целевая функция
fExpanded = expand(f.subs([(a, 2), (b, 4), (c, 5)])) # Раскрытие скобок, подстановка констант
print(f'f(x,y) expanded: {fExpanded}') 
print(f'\n')

fx = diff(f, x) # Частная производная по x
fy = diff(f, y) # Частная производная по y
fxExpanded = expand(fx.subs([(a, 2), (b, 4), (c, 5)])) # Раскрытие скобок, подстановка констант
fyExpanded = expand(fy.subs([(a, 2), (b, 4), (c, 5)])) # Раскрытие скобок, подстановка констант

xy = solve([fx, fy], [x, y]) # Решаем систему уравнений
xExpanded = xy[x].subs([(a, 2), (b, 4), (c, 5)])
yExpanded = xy[y].subs([(a, 2), (b, 4), (c, 5)])
print(f'f(x,y) -> min analytical: ({xExpanded}, {yExpanded})')
print(f'\n')

# Поиск минимума методом Хука-Дживса
#testVal = fExpanded.subs([(x, xExpanded), (y, yExpanded)]).evalf()
fEval = lambda xVal, yVal: fExpanded.subs([(x, xVal), (y, yVal)]).evalf()
#testVal2 = fEval(xExpanded, yExpanded)
basisPoints: list[tuple[float, float]] = []
xyCalc = getHookeJeevesMin(fEval, (0, 0), 0.4, 0.01, basisPoints)
dXY = sqrt((xExpanded - xyCalc[0])**2 + (yExpanded - xyCalc[1])**2)
print(f'f(x,y) -> min analytical: ({xExpanded.evalf()}, {yExpanded.evalf()})')
print(f'f(x,y) -> min computed: ({xyCalc[0]}, {xyCalc[1]})')
print(f'd f(x,y) -> min: {dXY}')
# График целевой функции
p = plotting.plot_contour(fExpanded, (x, 0, 6), (y, 0, 6), xlim=(0, 6), ylim=(0, 6), markers=[{'args': [xExpanded, yExpanded], 'color': "red", 'marker': "x", 'ms': 7}], show = False, aspect_ratio = (1, 1))
basisMarkers = []
lastPoint = None
for point in basisPoints:
	mColor = "green" if point == xyCalc else "purple"
	mMS = 7 if point == xyCalc else 3
	basisMarkers.append({'args': [point[0], point[1]], 'color': mColor, 'marker': "x", 'ms': mMS})
	if not lastPoint is None:
		currentPoint = Point(point[0], point[1])
		p.extend(plot_geometry(lastPoint, currentPoint, Line(lastPoint, currentPoint), line_color = "blue", show = False))
		lastPoint = currentPoint
	else:
		lastPoint = Point(point[0], point[1])
p.extend(plot(0, markers=basisMarkers, show = False))
p.show()