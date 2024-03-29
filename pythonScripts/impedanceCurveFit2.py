from impedance import preprocessing
from impedance.models.circuits import Randles, CustomCircuit
import matplotlib.pyplot as plt
from impedance.visualization import plot_nyquist, plot_bode
import re

# Load data from the example EIS result
frequencies, Z = preprocessing.readGamry('1618940354_SWR90456_S1_C1_9_12_POT_659.5_#5.dta')

# keep only the impedance data in the first quadrant
frequencies, Z = preprocessing.ignoreBelowX(frequencies, Z)

# see sample-ckt.jpeg image in folder for reference

# # option 1
circuit = CustomCircuit(initial_guess=[100e3, 1.3e-12, None, 1e9, 1e11, 6.6e-12, None],
                                      # CPE=True,
                                      constants={'CPE_1_1': 0.96, 'CPE_2_1': 0.9},
                                      circuit='R_0-p(CPE_1,R_1-p(R_2,CPE_2))')

# # option 2
# circuit = CustomCircuit(initial_guess=[100e3, None, None, 1e9, 1e11, None, None],
#                                      constants={'CPE_1_0': 1.3e-12, 'CPE_1_1': 0.96, 'CPE_2_0': 6.6e-12,
#                                                 'CPE_2_1': 0.9},
#                                      circuit='R_0 - p(CPE_1, R_1 - p(R_2,CPE_2) )')

circuit.fit(frequencies, Z)

Z_fit = circuit.predict(frequencies)

# nyquist
fig, ax = plt.subplots(figsize=(6, 6))
plot_nyquist(ax, Z, fmt='o')
plot_nyquist(ax, Z_fit, fmt='-')
plt.legend(['Data', 'Fit'])
plt.show()

# bode
fig, ax = plt.subplots(nrows=2, figsize=(6, 6))
plot_bode(ax, frequencies, Z, fmt='o')
plot_bode(ax, frequencies, Z_fit, fmt='-')
plt.legend(['Data', 'Fit'])
plt.show()

print(circuit)
# print(frequencies)
# print(Z)
# print(type(str(circuit)))

# csv of circuit elements
a = str(circuit)
a = a.split(':')[-1]
# a = a.replace('=',',')
# a = a.replace('\n',',')
results = re.findall('= (.*?) \(', a)
# results = re.findall('?<=\(=).*(?=\)', a)
b = ''
for result in results:
    b = b +  result + ','
print(b)
