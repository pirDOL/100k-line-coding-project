import numpy as np
import matplotlib.pyplot as plt

def func_tax(income):
    if income <= 3500:
        return 0
    income -= 3500
    if income <= 1500:
        tax = income * 0.03
    elif income <= 4500:
        tax = income * 0.1 - 105
    elif income <= 9000:
        tax = income * 0.2 - 555
    elif income <= 35000:
        tax = income * 0.25 - 1005
    elif income <= 55000:
        tax = income * 0.3 - 2755
    elif income <= 80000:
        tax = income * 0.35 - 5505
    else:
        tax = income * 0.45 - 13505
    return tax

# income = np.arange(13000,26000,0.02)
income = range(6500, 26000, 1)
tax = map(func_tax, income)
# print(tax)
# print func_tax(6500)

# plt.figure(figsize=(8,7), dpi=98)
# p1 = plt.subplot(211)
# p2 = plt.subplot(212)

# p1.plot(t,f1(t),"g-",label="$f(t)=e^{-t} \cdot \cos (2 \pi t)$")
# p2.plot(t,f2(t),"r-.",label="$g(t)=\sin (2 \pi t) \cos (3 \pi t)$",linewidth=2)

# p1.axis([0.0,5.01,-1.0,1.5])

# p1.set_ylabel("v",fontsize=14)
# p1.set_title("A simple example",fontsize=18)
# p1.grid(True)
# p1.legend()

# p2.axis([0.0,5.01,-1.0,1.5])
# p2.set_ylabel("v",fontsize=14)
# p2.set_xlabel("t",fontsize=14)
# p2.legend()


max_income = 20000
max_tax = max_income * 0.25 - 1005
fig = plt.figure(figsize=(7, 7))

x = [0, 3500, 5000, 8000, 12500, max_income]
plt.xticks(x, map(lambda i : str(i), x), rotation='vertical')
# ax.set_xticklabels(['0', '3500', '5000', '8000', '12500', str(max_income)])

plt.plot([0, 3500], [0, 0])
plt.plot([3500, 3500], [0, max_tax], 'r--')
plt.plot([3500, 5000], map(lambda i:0.03*(i-3500), [3500, 5000]))

income = [5000, 8000]
plt.plot([5000, 5000], [0, max_tax], 'r--')
plt.plot([5000, 8000], map(lambda i:0.1*(i-3500)-105, [5000, 8000]))

income = [8000, 12500]
plt.plot([8000, 8000], [0, max_tax], 'r--')
plt.plot([8000, 12500], map(lambda i:0.2*(i-3500)-555, [8000, 12500]))

plt.plot([12500, 12500], [0, max_tax], 'r--')
plt.plot([12500, max_income], map(lambda i:0.25*(i-3500)-1005, [12500, max_income]))
plt.show()