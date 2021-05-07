import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy import interpolate

target_tidal_volume = 54 #mL

#Load waveform and plot
flowrate_bates = np.genfromtxt("../waveform/waveform_bates.csv",usecols=0,delimiter=',',dtype=float)
time_bates = np.genfromtxt("../waveform/waveform_bates.csv",usecols=1,dtype=float,delimiter=',')

id_sort = np.argsort(time_bates)
time_bates=time_bates[id_sort]
flowrate_bates=flowrate_bates[id_sort]


zeros = np.where(flowrate_bates==0)[0]
print(zeros)

insp_time = time_bates[zeros[1]] - time_bates[zeros[0]]
exp_time = time_bates[zeros[2]] - time_bates[zeros[1]]

print("I:E ratio", insp_time/insp_time,":",exp_time/insp_time)

tidal_volume = np.trapz(flowrate_bates[zeros[0]:zeros[1]],time_bates[zeros[0]:zeros[1]])


tidal_volume = np.trapz(flowrate_bates[zeros[1]:zeros[2]],time_bates[zeros[1]:zeros[2]])


time_infant = np.linspace(0,1.5,len(flowrate_bates))


f_tidal = interpolate.interp1d(time_bates,flowrate_bates)
time=np.linspace(0,time_bates[-1],len(flowrate_bates))
flowrate_shift = f_tidal(time)



print(np.where(np.isclose(flowrate_shift,0,atol=50)==True)[0])

zeros=[0,36,96]

maxit=100
flowrate=flowrate_shift
i=0
factor=2
while i < maxit:
	tidal_volume = np.trapz(flowrate[zeros[0]:zeros[1]],time_infant[zeros[0]:zeros[1]])

	print(tidal_volume)

	if abs((abs(tidal_volume) - target_tidal_volume)) <= 0.02*target_tidal_volume:
		break

	elif abs(tidal_volume) >= target_tidal_volume:
		flowrate = flowrate/factor


	elif abs(tidal_volume) <= target_tidal_volume:
		flowrate = flowrate*1.05


	i=i+1

mass_flow = flowrate/1e6*1.175

np.savetxt('54mL_massflowrate.csv',np.transpose([time_infant,mass_flow]),delimiter=',')

plt.figure()
plt.plot(time_infant,flowrate,'^-')
plt.axhline(y=0,linestyle='--',color='k',alpha=0.5)
plt.ylabel("Flowrate (ml/s)")
plt.xlabel("Time (s)")
plt.title("Pt109, Tidal Volume = 54mL, I:E = 1:1.3")
plt.show()
plt.savefig("../Figures/waveform1.png")






