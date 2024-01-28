import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interpn
from matplotlib import cm

machs = np.array([0.82, 0.83, 0.84, 0.85])
altitudes = np.arange(36000, 40001, 1000) / 1000
print(altitudes)
X, Y = np.meshgrid(machs, altitudes)

Z = np.array([[70516.3, 69409.1, 68698.4, 70034.3, 73386.7],
              [72956.2, 74121.6, 76456.4, 80448.2, 83921.8],
              [84121, 87628.9, 92277.4, 96230.7, 101000.9],
              [89469.2+9000, 95273+9000, 100000+10000, 105000+10000, 110128+10000]]).T / 1000

interp = RegularGridInterpolator((machs, altitudes), Z.T, method="cubic")

mach_vec = np.linspace(0.8201, 0.834999, 100)
alt_vec = np.linspace(36001, 39999, 100) / 1000
Xd, Yd = np.meshgrid(mach_vec, alt_vec)
Zd = np.empty([len(mach_vec), len(alt_vec)])
for i, ma in enumerate(mach_vec):
    for j, alt in enumerate(alt_vec):
        Zd[j, i] = interp([ma, alt]).T
        #Zd[j, i] = interpn((machs, altitudes), Z.T, [ma, alt], method="linear")

plt.rc('font', size=12)
# plt.style.use('dark_background')
# fig = plt.figure(facecolor=(0.129, 0.129, 0.129))
# ax = fig.add_subplot(111, projection="3d", facecolor=(0.129, 0.129, 0.129))

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(Xd, Yd, Zd, cmap="viridis_r")
ax.set_xlabel('Cruise Mach')
ax.set_ylabel('Mid Cruise Altitude [kft]')
ax.set_xticks([0.82, 0.83, 0.84, 0.85])
ax.set_yticks([36, 38, 40])
ax.set_zlabel('Mission Fuel [t]')
plt.show()

# plt.style.use('dark_background')
# fig, ax = plt.subplots(facecolor=(0.129, 0.129, 0.129))

fig, ax = plt.subplots()
levels = 15# np.array([68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, , 100000]) / 1000
contour = ax.contour(Xd, Yd, Zd, levels=levels, colors="black", linewidths=0.5)
contourf = ax.contourf(Xd, Yd, Zd, levels=levels, cmap="viridis_r")
plt.colorbar(contourf, label='Mission Fuel [t]')

ax.set_xlabel('Cruise Mach')
ax.set_ylabel('Mid Cruise Altitude [kft]')
ax.set_xticks([0.82, 0.825, 0.83, 0.835])
ax.set_yticks([36, 37, 38, 39, 40])

#ax.set_facecolor('#f0f0f0')

plt.show()


# plt.style.use('dark_background')
# fig, ax = plt.subplots(facecolor=(0.129, 0.129, 0.129))


#plt.style.use('dark_background')
fig, ax = plt.subplots()

ar_vec = [12., 13.44, 14.89, 16.33, 17.78, 19.22, 20.67, 22.11, 23.56, 25.]
fuel_vec = [94.424, 89.465, 85.708, 82.819, 80.578, 78.833, 77.3685, 76.1708, 75.2154, 74.4585]
plt.plot(ar_vec, fuel_vec, label="Fuel")
plt.vlines(13.5, 74, 95, label="Validity limit Cantilever Wing", linestyles='dashed', colors='red')
plt.vlines(20, 74, 95, label="Validity limit Truss Braced Wing", linestyles='dashed', colors='green')
plt.legend()
#plt.grid('on')
ax.set_xlabel('Main Wing Aspect Ratio')
ax.set_ylabel('Mission fuel [t]')

#ax.set_xticks([0.82, 0.83, 0.84])
#ax.set_yticks([36, 38, 40, 42])

plt.show()

fig, ax = plt.subplots()
x = [0, 0.2, 0.24962406015037594, 0.30075187969924816, 0.35037593984962406, 0.4, 0.449624060150376, 0.5007518796992482, 0.5518796992481203, 0.5714285714285715, 0.6000000000000001, 0.6511278195488722, 0.7007518796992481, 0.7503759398496241]
y = [0, 16.304347826086957, 19.00621118012422, 20.96273291925466, 22.45341614906832, 23.43167701863354, 23.944099378881987, 24.03726708074534, 23.1055900621118, 22.45341614906832, 20.77639751552795, 17.748447204968944, 13.183229813664596, 7.8726708074534155]
plt.plot(x, y, label="Reference Aircraft")

x2 = [0, 0.02706766917293233, 0.06917293233082707, 0.10827067669172932, 0.14887218045112782, 0.18947368421052632, 0.23007518796992482, 0.2721804511278196, 0.3112781954887218, 0.35037593984962406, 0.3924812030075188, 0.4330827067669173, 0.47067669172932336, 0.5112781954887219, 0.5548872180451128, 0.5924812030075188, 0.6330827067669174, 0.6751879699248121, 0.7127819548872181, 0.7548872180451128, 0.7954887218045114, 0.8330827067669173]
y2 = [0, 1.7236024844720497, 4.285714285714286, 6.754658385093167, 9.177018633540373, 11.599378881987578, 13.928571428571427, 16.024844720496894, 17.981366459627328, 19.93788819875776, 21.754658385093165, 23.24534161490683, 24.642857142857142, 25.90062111801242, 27.065217391304348, 27.763975155279503, 28.22981366459627, 27.111801242236023, 22.63975155279503, 16.490683229813662, 10.714285714285714, 6.475155279503105]
plt.plot(x2, y2, label="Truss Braced Wing")
plt.legend()
plt.grid()
plt.ylabel(r'$\frac{L}{D}$')
plt.xlabel(r"$C_L$")
ax.set_yticks([0, 5, 10, 15, 20, 25, 30])

plt.show()
