from sympy import *
from sympy import plotting
from sympy import geometry

# Поиск экстремума
x, y, a, b, c = symbols('x y a b c', positive = True) # Символьные переменные
f = x**2 + y**2 - ( (x**2 + y**2 - ((x - a)**2 + (b - y)**2) + a**2 + b**2) / (2 * sqrt(a**2 + b**2)) )**2 + (x - a)**2 + (b - y)**2 - (((x - a)**2 + (b - y)**2 - ((c - x)**2 + y**2) + (c - a)**2 + b**2) / (2 * sqrt((c - a)**2 + b**2)))**2 + (c - x)**2 + y**2 - (((c - x)**2 + y**2 - (x**2 + y**2) + c**2) / (2 * sqrt(c**2)))**2  # Целевая функция
#f = 68 * x ** 2 + 39 * y ** 2 - 80 * x - 120 * y - 28 * x * y + 400 # Целевая функция
print(f'f(x,y): {f}')
fExpanded = expand(f.subs([(a, 2), (b, 4), (c, 5)])) # Раскрытие скобок, подстановка констант
print(f'f(x,y) expanded: {fExpanded}') 
print(f'\n')

fx = diff(f, x) # Частная производная по x
print(f'df(x,y)/dx: {fx}')
fy = diff(f, y) # Частная производная по y
print(f'df(x,y)/dy: {fy}')
fxExpanded = expand(fx.subs([(a, 2), (b, 4), (c, 5)])) # Раскрытие скобок, подстановка констант
fyExpanded = expand(fy.subs([(a, 2), (b, 4), (c, 5)])) # Раскрытие скобок, подстановка констант
print(f'df(x,y)/dx expanded: {fxExpanded}')
print(f'df(x,y)/dy expanded: {fyExpanded}')
print(f'\n')

xy = solve([fx, fy], [x, y]) # Решаем систему уравнений
print(f'df(x,y)/dx = df(x,y)/dy = 0: {xy}')
xExpanded = xy[x].subs([(a, 2), (b, 4), (c, 5)])
yExpanded = xy[y].subs([(a, 2), (b, 4), (c, 5)])
print(f'df(x,y)/dx = df(x,y)/dy = 0 expanded: ({xExpanded}, {yExpanded})')
print(f'\n')

# Графики производных
p = plot_implicit(fxExpanded, (x, 0, 6), (y, 0, 6), show = False, aspect_ratio = (1, 1))
p.extend(plot_implicit(fyExpanded, (x, 0, 6), (y, 0, 6), show = False))
p.extend(plot(0, markers=[{'args': [xExpanded, yExpanded], 'color': "red", 'marker': "x", 'ms': 7}], show = False))
p.show()

# График целевой функции
p = plotting.plot_contour(fExpanded, (x, 0, 6), (y, 0, 6), markers=[{'args': [xExpanded, yExpanded], 'color': "red", 'marker': "x", 'ms': 7}], show = False, aspect_ratio = (1, 1))
p.show()

# График целевой функции
ab = geometry.Line(geometry.Point(0, 0), geometry.Point(2, 4))
bc = geometry.Line(geometry.Point(2, 4), geometry.Point(5, 0))
ac = geometry.Line(geometry.Point(0, 0), geometry.Point(5, 0))
ma = ab.perpendicular_line(geometry.Point(xExpanded, yExpanded))
mb = bc.perpendicular_line(geometry.Point(xExpanded, yExpanded))
mc = ac.perpendicular_line(geometry.Point(xExpanded, yExpanded))
getLineFunc = lambda f: f.coefficients[0] * x + x**2 - x**2 + f.coefficients[1] * y + f.coefficients[2]
p = plot_implicit(getLineFunc(ab), (x, 0, 6), (y, 0, 6), show = False, aspect_ratio = (1, 1), line_color = "blue")
p.extend(plot_implicit(getLineFunc(bc), (x, 0, 6), (y, 0, 6), show = False, line_color = "blue"))
#p.extend(plot_implicit(getLineFunc(ac), (x, 0, 6), (y, 0, 6), show = False))
p.extend(plot_parametric(y, 0-ac.coefficients[2], (y, 0, 6), show = False, line_color = "blue"))
p.extend(plot_implicit(getLineFunc(ma), (x, 0, 6), (y, 0, 6), show = False, line_color = "green"))
p.extend(plot_implicit(getLineFunc(mb), (x, 0, 6), (y, 0, 6), show = False, line_color = "green"))
p.extend(plot_implicit(getLineFunc(mc), (x, 0, 6), (y, 0, 6), show = False, line_color = "green"))
p.extend(plot(0, markers=[{'args': [xExpanded, yExpanded], 'color': "red", 'marker': "x", 'ms': 7}], show = False))
p.show()