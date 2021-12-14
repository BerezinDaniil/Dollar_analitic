import math
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
import matplotlib.patches as patches

first_data = "12.11.2021"
second_data = "13.12.2021"
DataFrame_results = pd.read_html(
    'https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From=' + first_data + '&UniDbQuery.To=' + second_data)
df = DataFrame_results[0]
#print(df)
Data = df[0]
Curs = df[2]
dict = {}
L = len(Data) - 1
for data in range(1, L):
    dict[Data[len(Data) - data]] = float(Curs[len(Data) - data]) / 10000

if (float(Curs[2])) <= (float(Curs[len(Data) - 1])):
    color_gr = "red"
else:
    color_gr = 'lime'

numbers = range(len(dict))
values = list(dict.values())
fig, ax = plt.subplots(2)
ax[0].set_title('Dynamics of dollar at ' + first_data + "-" + second_data)
ax[0].plot(numbers, values, color=color_gr, label='Real Rate')

# прогноз на N = 1 день
days = 1
# анализ данных
data_analysis = []
model_WMA = []
model_EMA = []
model_RSI = []
mistakes_EMA = []
mistakes_WMA = []
# Записываем первые 10 показаний за период(типо обучающая выборка)
for data in range(1, 11):
    data_analysis.append(float(Curs[len(Data) - data]) / 10000)
    model_EMA.append(float(Curs[len(Data) - data]) / 10000)
    model_WMA.append(float(Curs[len(Data) - data]) / 10000)

for day in range(11, L):
    segment = data_analysis[day - 11:len(data_analysis) + day - 11]
    new_EMA = (sum(segment)) / len(segment)
    model_EMA.append(new_EMA)
    mistake_EMA = abs(new_EMA - (float(Curs[L + 1 - day]) / 10000)) / new_EMA
    mistakes_EMA.append(mistake_EMA)
    data_analysis.append(float(Curs[L + 1 - day]) / 10000)
    S = 0
    for i in range(len(segment)):
        S += (i + 1) * (segment[i])
    new_WMA = S / 55
    model_WMA.append(new_WMA)
    mistake_WMA = abs(new_WMA - (float(Curs[L + 1 - day]) / 10000)) / new_WMA
    mistakes_WMA.append(mistake_WMA)
# ошибка
mistake_sr_EMA = sum(mistakes_EMA) / len(mistakes_EMA)
mistake_sr_WMA = sum(mistakes_WMA) / len(mistakes_WMA)

# анализ RSI с периодом 7 днtq1
period = 7
for data in range(1, period + 1):
    model_RSI.append(float(Curs[len(Data) - data]) / 10000)
# сам анализ
for j in range(8, len(data_analysis)):
    RSI_up = []
    RSI_down = []
    object_ = data_analysis[j:j + period + 1]
    for index in range(0, len(object_) - 1):
        if object_[index] >= object_[index + 1]:
            RSI_down.append(object_[index] - object_[index + 1])
        else:
            RSI_up.append(object_[index + 1] - object_[index])
    if (sum(RSI_down) > 0) and (sum(RSI_up) > 0):
        SR = mean(RSI_up) / mean(RSI_down)
        model_RSI.append(100 - (100 / (1 + SR)))
#print(model_RSI)
# само предсказание EMA
for i in range(days):
    value = sum(model_EMA[len(model_EMA) - 10:len(model_EMA)]) / len(model_EMA[len(model_EMA) - 10:len(model_EMA)])
    model_EMA.append(value * (1 - mistake_sr_EMA))
# само предсказание WMA
for i in range(days):
    segment = model_WMA[len(model_WMA) - 10:len(model_WMA)]
    S = 0
    for i in range(len(segment)):
        S += (i + 1) * (segment[i])
    new_WMA = S / 55
    model_WMA.append(new_WMA * (1 - mistake_sr_WMA))
dict_RSI = {}
for data1 in range(0, len(model_RSI)):
    dict_RSI[data1] = model_RSI[data1]
dict_EMA = {}
for data1 in range(0, L - 1 + days):
    dict_EMA[data1] = model_EMA[data1]
dict_WMA = {}

for data1 in range(0, L - 1 + days):
    dict_WMA[data1] = model_WMA[data1]
# print(model)
# print(data_analysis)
print("Estimated price(EMA):", model_EMA[-1])
print("Estimated price(WMA):", model_WMA[-1])
print("Probability of error(EMA):", mistake_sr_EMA * 100, "%")
print("Probability of error(WMA):", mistake_sr_WMA * 100, "%")
if color_gr == "red":
    print("Over the entire period, the dollar has fallen")
else:
    print("Over the entire period, the dollar has grown")
numbers_EMA = range(len(dict_EMA))
values_EMA = list(dict_EMA.values())
ax[0].plot(numbers_EMA, values_EMA, color="cyan", label='EMA')

numbers_WMA = range(len(dict_WMA))
values_WMA = list(dict_WMA.values())
ax[0].plot(numbers_WMA, values_WMA, color="magenta", label='WMA')
ax[0].patch.set_facecolor('k')
#  включить второстепенные деления осей
ax[0].minorticks_on()

#  Определяем внешний вид линий основной сетки:
ax[0].grid(which='major',
           color='white',
           linewidth=1)

#  Определяем внешний вид линий вспомогательной сетки
ax[0].grid(which='minor',
           color='white',
           linestyle=':')

leg = ax[0].legend()
plt.xlabel("Time in days")
plt.ylabel("Price in rubles")

numbers_RSI = range(len(dict_RSI))
values_RSI = list(dict_RSI.values())
ax[1].plot(numbers_RSI, values_RSI, color="blue", label='RSI')
ax[1].patch.set_facecolor('k')
#  включить второстепенные деления осей
ax[1].minorticks_on()

#  Определяем внешний вид линий основной сетки:
ax[1].grid(which='major',
           color='white',
           linewidth=1)

#  Определяем внешний вид линий вспомогательной сетки
ax[1].grid(which='minor',
           color='white',
           linestyle=':')
# поиск облостей с ПЕРЕКУПЛЕННОСТЬ/ПЕРЕПРОДАННОСТЬ

#print(dict_RSI)
for k in range(len(dict_RSI)):
    #print(k)
    if dict_RSI[k] >= 70:
        W = []
        k0 = k
        while dict_RSI[k] >= 70:
            W.append(dict_RSI[k])
            k += 1
            if k >= len(dict_RSI):
                break
        #print(W)
        ax[1].add_patch(
            patches.Rectangle(
                (k0 - math.ceil(len(dict_RSI) / 10), dict_RSI[k0]),
                len(W) // 2 + math.ceil(len(dict_RSI) / 10),
                5,
                edgecolor='red',
                fill=False
            ))
    elif dict_RSI[k] <= 30:
        L = []
        k0 = k
        while dict_RSI[k] <= 30:
            L.append(dict_RSI[k])
            k += 1
            if k >= len(dict_RSI):
                break
        #print(L)
        ax[1].add_patch(
            patches.Rectangle(
                (k0 - math.ceil(len(dict_RSI) / 10), dict_RSI[k0]),
                len(L) // 2 + math.ceil(len(dict_RSI) / 10),
                5,
                edgecolor='lime',
                fill=False
            ))

leg = ax[1].legend()
# plt.xlabel("Time in days")
# plt.ylabel("Price in rubles")
plt.show()
