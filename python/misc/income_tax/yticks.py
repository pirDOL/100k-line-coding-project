import matplotlib.pyplot as plt
import numpy as np

data = [(' whitefield', 65299), (' bellandur', 57061), (' kundalahalli', 51769), (' marathahalli', 50639),
(' electronic city', 44041), (' sarjapur road junction', 34164), (' indiranagar 2nd stage', 32459),
(' malleswaram', 32171), (' yelahanka main road', 28901), (' domlur', 28869)]

freequency = []
words = []

for line in data:
    freequency.append(line[1])
    words.append(line[0])

y_axis = np.arange(1, len(words) + 1, 1)

plt.barh(y_axis, freequency, align='center')
plt.yticks(y_axis, words)
plt.show()