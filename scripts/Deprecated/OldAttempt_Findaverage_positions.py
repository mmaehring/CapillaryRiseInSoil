### Find places distance between adjacent points

swa = np.array([i.mean(axis=1) for i in [step_wedge_1, step_wedge_2, step_wedge_3]])

length = len(swa[1]) - 1
deltas = np.array([[swa[j, i+1] - swa[j, i] for i in range(length)] for j in [0,1,2]])

deltas = abs(deltas)

###### Testing background noise removal 

means = np.array([np.mean(deltas[i]) for i in range(3)])
sample_noise_means = np.array([np.mean(deltas[i, 200:240]) for i in range(3)])

# get_five_biggest_values = [np.argpartition(deltas[i], -5)[-5:] for i in range(3)]
# five_biggest_means = np.array([deltas[i][get_five_biggest_values[i]] for iin range(3)]).mean(axis=1)
# big_mean_correction = five_biggest_means / len(deltas)

backgrounds = np.array([np.full(499, means[i]) for i in range(3)])
adv_backgr = np.array([np.full(499, means[i] - sample_noise_means[i]) for i in range(3)]) # didn't work -> overcompensated

# backgrounds
# adv_backgr
# np.linalg.norm(backgrounds - adv_backgr)

# # print(get_five_biggest_values)
# for i in range(3):
#     print(3*"****", f"{i}", 3*"****") 
#     print("Indices")
#     print(get_five_biggest_values[i])
#     print(5*"****")
#     print("Values")
#     print(deltas[i, get_five_biggest_values[i]])

### Plotting distances between adjacent points with and without background removal 

# Setup
fig, ax = plt.subplots(2, 3)
ax = ax.ravel()
fig.set_size_inches(20, 12)

# x vals
xvals = np.arange(0, 499, 1)

# plotting
ax[0].plot(xvals, deltas[0], label="Raw distances")
ax[0].set_xlim(150, 450)
ax[0].set_ylim(0, 0.025)
ax[0].grid()
ax[0].legend()

ax[1].plot(xvals, deltas[1], label="Raw distances")
ax[1].set_xlim(150, 450)
ax[1].set_ylim(0, 0.1)
ax[1].grid()
ax[1].legend()

ax[2].plot(xvals, deltas[2], label="Raw distances")
ax[2].set_xlim(120, 450)
ax[2].set_ylim(0, 0.16)
ax[2].grid()
ax[2].legend()

ax[3].plot(xvals, deltas[0] - backgrounds[0], ".-", label = "Simple background removal")
ax[3].plot(xvals, deltas[0] - adv_backgr[0], ":", label = "Sample noise background removal")
ax[3].set_xlim(150, 450)
ax[3].set_ylim(0, 0.025)
ax[3].grid()
ax[3].legend()

ax[4].plot(xvals, deltas[1] - backgrounds[1], ".-", label = "Simple background removal")
ax[4].plot(xvals, deltas[1] - adv_backgr[1], ":", label = "Sample noise background removal")
ax[4].set_xlim(150, 450)
ax[4].set_ylim(0, 0.1)
ax[4].grid()
ax[4].legend()

ax[5].plot(xvals, deltas[2] - backgrounds[2], ".-", label = "Simple background removal")
ax[5].plot(xvals, deltas[2] - adv_backgr[2], ":", label = "Sample noise background removal")
ax[5].set_xlim(120, 450)
ax[5].set_ylim(0, 0.16)
ax[5].grid()
ax[5].legend()

# get_five_biggest_values
# deltas[1, get_five_biggest_values]

peaks = np.array([deltas[i] - adv_backgr[i] for i in range(3)])

peaks.mean(axis=1)

big_points = [np.where( (peaks[i] > peaks[i].mean()) & (peaks[i] > 0)) for i in range(3)]

for i in range(3):
    values = big_points[i][0]
    values = peaks[i][values]  
#     print(values)
#     print(len(values))
# peaks[1][big_points[1][0]]  

##### Plotting segments, differences and noise removed differences 



#### Finding the star / end points to the staircase structure



## Black body correction
Scattered neutrons introduce a bias in the values. This can be corrected using black body images.











# Abandoned attempts 

# fig, ax = plt.subplots(3, 3)
# # fig.set_size_inches(18, 10)
# fig.set_size_inches(18, 15)
# # fig.set_dpi(800)
# ax = ax.ravel()

# xvals = np.arange(0, 499, 1)

# ax[0].plot(xvals, deltas[0])
# ax[0].set_title("||x[i] - x[i+1]|| without noise removal")
# ax[0].set_xlim(150, 450)
# ax[0].set_ylim(0, 0.025)
# ax[0].grid()

# ax[1].plot(xvals, deltas[1])
# ax[1].set_title("||x[i] - x[i+1]|| without noise removal")
# ax[1].set_xlim(150, 450)
# ax[1].set_ylim(0, 0.1)
# ax[1].grid()

# ax[2].plot(xvals, deltas[2])
# ax[2].set_title("||x[i] - x[i+1]|| without noise removal")
# ax[2].set_xlim(120, 450)
# ax[2].set_ylim(0, 0.16)
# ax[2].grid()


# ax[3].plot(deltas[0] - adv_backgr[0])
# ax[3].set_title("||x[i] - x[i+1]|| with noise removal")
# ax[3].set_xlim(150, 450)
# ax[3].set_ylim(0, 0.025)
# ax[3].grid()

# ax[4].plot(deltas[1] - adv_backgr[1])
# ax[4].set_title("||x[i] - x[i+1]|| with noise removal")
# ax[4].set_xlim(150, 450)
# ax[4].set_ylim(0, 0.1)
# ax[4].grid()


# ax[5].plot(deltas[2] - adv_backgr[2])
# ax[5].set_title("||x[i] - x[i+1]|| with noise removal")
# ax[5].set_xlim(120, 450)
# ax[5].set_ylim(0, 0.16)
# ax[5].grid()


# ax[6].plot(step_wedge_1.mean(axis=1))
# # ax[6].scatter(big_points[0][0], peaks[0][big_points[0][0]])
# ax[6].set_title('Profile of wedge 0.5-2.5 mm')
# ax[6].set_xlabel('Pixel position (can be converted into distances)')
# ax[6].set_xlim(150, 450)
# ax[6].set_ylim(0, 0.5)
# ax[6].set_ylabel(r'$\mu\times thickness$')
# ax[6].grid()

# ax[7].plot(step_wedge_2.mean(axis=1))
# ax[7].set_title('Profile of wedge 3.0-5.0 mm')
# # ax[7].scatter(big_points[1][0], step_wedge_1.mean(axis=1)[big_points[1][0]])
# ax[7].set_xlabel('Pixel position (can be converted into distances)')
# ax[7].set_xlim(150, 450)
# ax[7].set_ylim(0.4, 0.7)
# ax[7].grid()

# ax[8].plot(step_wedge_3.mean(axis=1), label = "Wedge")
# ax[8].set_title('Profile of wedge 3.0-5.0 mm')
# ax[8].set_xlabel('Pixel position (can be converted into distances)')
# ax[8].set_xlim(120, 450)
# ax[8].set_ylim(0.4,0.7)
# ax[8].grid()