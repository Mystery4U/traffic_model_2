import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import scipy.optimize as optimize
import seaborn as sns
import statsmodels.api as sm
from sklearn.metrics import r2_score

# Load the data
file_path = 'ttd_3000_60.3lanes.csv'
# file_path = 'time_travel_data_40_3.csv'
data = pd.read_csv(file_path)['Time_Travel'].values
#
# df = pd.read_csv(file_path)
# data = df[df['Vehicle_Type'] == 0]['Time_Travel'].values
# trucks = df[df['Vehicle_Type'] == 1]['Time_Travel'].values

# Fit normal distribution
def normal_distribution(x, mu, sigma):
    return stats.norm.pdf(x, loc=mu, scale=sigma)

hist_norm, bins_norm = np.histogram(data, bins=30, density=True)
bin_centers = (bins_norm[:-1] + bins_norm[1:]) / 2
params_norm, covariance_norm = optimize.curve_fit(normal_distribution, bin_centers, hist_norm, p0=[180, 10], maxfev=10000)

xA = np.linspace(min(data), max(data), 10000)
pA = stats.norm.pdf(xA, params_norm[0], params_norm[1])
mean_fitA_uncertainty, sigma_fitA_uncertainty = np.sqrt(np.diag(covariance_norm))

# Fit gamma distribution
def gamma_distribution(x, shape, loc, scale):
    return stats.gamma.pdf(x, shape, loc=loc, scale=scale)

params_gamma, covariance_gamma = optimize.curve_fit(gamma_distribution, bin_centers, hist_norm, p0=[20, 170, 1.5], maxfev = 10000)

xB = np.linspace(min(data), max(data), 10000)
pB = stats.gamma.pdf(xB, params_gamma[0], loc=params_gamma[1], scale=params_gamma[2])

shape_fitB_uncertainty, loc_fitB_uncertainty, scale_fitB_uncertainty = np.sqrt(np.diag(covariance_gamma))

# Fit lognormal distribution
def lognormal_distribution(x, shape, loc, scale):
    return stats.lognorm.pdf(x, shape, loc=loc, scale=scale)

params_lognormal, covariance_lognormal = optimize.curve_fit(lognormal_distribution, bin_centers, hist_norm, p0=[0.1, 130, 70], maxfev=10000)

xC = np.linspace(min(data), max(data), 10000)
pC = stats.lognorm.pdf(xC, params_lognormal[0], loc=params_lognormal[1], scale=params_lognormal[2])

shape_fitC_uncertainty, location_fitC_uncertainty, scale_fitC_uncertainty = np.sqrt(np.diag(covariance_lognormal))

# Fit Burr distribution
def burr12_distribution(x, c, d, loc, scale):
    return stats.burr12.pdf(x, c, d, loc=loc, scale=scale)

params_burr12, covariance_burr12 = optimize.curve_fit(burr12_distribution, bin_centers, hist_norm, p0=[11,1,150,50], maxfev=10000)

xD = np.linspace(min(data), max(data), 10000)
pD = stats.burr.pdf(xD, params_burr12[0], params_burr12[1], loc=params_burr12[2], scale=params_burr12[3])

c_fitD_uncertainty, d_fitD_uncertainty, loc_fitD_uncertainty, scale_fitD_uncertainty = np.sqrt(np.diag(covariance_burr12))

# Fit reciprocal normal distribution
def func1(data, mean, std):
    return (5000 / (np.sqrt(2*np.pi) * std * (data)**2)) * np.exp(-1/2*((5000/data - mean)/std)**2)


class ReciprocalNormal(stats.rv_continuous):
    def _pdf(self, x, mean, std):
        return (5000 / (np.sqrt(2 * np.pi) * std * (x) ** 2)) * np.exp(-1 / 2 * ((5000 / x - mean) / std) ** 2)


recipn = ReciprocalNormal(a=0, shapes='mean, std')

hist, bins = np.histogram(data, bins=30, density=True)
bin_centers = (bins[:-1] + bins[1:]) / 2
params_reciprocal, covariance_reciprocal = optimize.curve_fit(func1, bin_centers, hist, p0=[28, 1])
mean_fitE_uncertainty, sigma_fitE_uncertainty = np.sqrt(np.diag(covariance_reciprocal))
fitted_pdf_recipn = func1(bin_centers, params_reciprocal[0], params_reciprocal[1])

empirical_cdf = sorted(data)
theoretical_points = [(_-0.5)/len(data) for _ in range(1, 1+len(data))]
theoretical_cdf = [recipn.ppf(p, mean=params_reciprocal[0], std=params_reciprocal[1]) for p in theoretical_points]

# Print parameters for all distributions
print("Normal Mean: {:.4f} ± {:.4f}".format(params_norm[0], mean_fitA_uncertainty))
print("Normal Standard Deviation: {:.4f} ± {:.4f}".format(params_norm[1], sigma_fitA_uncertainty))
print("Gamma Shape: {:.4f} ± {:.4f}".format(params_gamma[0], shape_fitB_uncertainty))
print("Gamma Location: {:.4f} ± {:.4f}".format(params_gamma[1], loc_fitB_uncertainty))
print("Gamma Scale: {:.4f} ± {:.4f}".format(params_gamma[2], scale_fitB_uncertainty))
print("Lognormal Shape: {:.4f} ± {:.4f}".format(params_lognormal[0], shape_fitC_uncertainty))
print("Lognormal Location: {:.4f} ± {:.4f}".format(params_lognormal[1], location_fitC_uncertainty))
print("Lognormal Scale: {:.4f} ± {:.4f}".format(params_lognormal[2], scale_fitC_uncertainty))
print("Burr Shape (c): {:.4f} ± {:.4f}".format(params_burr12[0], c_fitD_uncertainty))
print("Burr Shape (d): {:.4f} ± {:.4f}".format(params_burr12[1], d_fitD_uncertainty))
print("Burr Location: {:.4f} ± {:.4f}".format(params_burr12[2], loc_fitD_uncertainty))
print("Burr Scale: {:.4f} ± {:.4f}".format(params_burr12[3], scale_fitD_uncertainty))
print("Reciprocal Normal Mean: {:.4f} ± {:.4f}".format(params_reciprocal[0], mean_fitE_uncertainty))
print("Reciprocal Normal Variance: {:.4f} ± {:.4f}".format(params_reciprocal[1], sigma_fitE_uncertainty))


plt.figure(figsize=(15, 10))

# Histogram
# plt.hist([data, trucks], bins=30, edgecolor='black', color=['lightblue', 'blue'], density=True, stacked=True, alpha=0.5, label=['Regular cars', 'Semi-trucks'])
plt.hist(data, bins=30, edgecolor='black', color='lightblue', density=True, alpha=0.5, label='Regular cars')
plt.plot(xA, pA, 'blue', linewidth=2, label='Fitted normal distribution')
plt.plot(xB, pB, 'red', linewidth=2, label='Fitted gamma distribution')
plt.plot(xC, pC, 'green', linewidth=2, label='Fitted lognormal distribution')
plt.plot(xD, pD, 'purple', linewidth=2, label='Fitted Burr distribution')
plt.plot(bin_centers, fitted_pdf_recipn, 'orange', linewidth=2, label=f'Reciprocal normal Fit')
plt.xlabel('Time [s]')
plt.ylabel('Number of cars (normalized)')
plt.title('Histogram of time needed to travel 5km with fitted distributions')
plt.legend()
plt.grid()
plt.savefig('z1.png')
plt.show()

fig = plt.figure(figsize=(15, 10))

# Create subplots using subplot2grid for the first row
ax1 = plt.subplot2grid(shape=(2, 6), loc=(0, 0), colspan=2)
ax2 = plt.subplot2grid((2, 6), (0, 2), colspan=2)
ax3 = plt.subplot2grid((2, 6), (0, 4), colspan=2)

# Plot QQ plots for each distribution in the first row
sm.qqplot(data, stats.norm, fit=False, line="45", ax=ax1, loc=params_norm[0], scale=params_norm[1])
ax1.set_title('Normal')

sm.qqplot(data, stats.gamma, fit=False, line="45", ax=ax2, distargs=(params_gamma[0], ), loc=params_gamma[1], scale=params_gamma[2])
ax2.set_title('Gamma')

sm.qqplot(data, stats.lognorm, fit=False, line="45", ax=ax3, distargs=(params_lognormal[0], ), loc=params_lognormal[1], scale=params_lognormal[2])
ax3.set_title('Lognormal')

# Create an empty subplot at (1, 5) to make room for the centered subplots
ax_empty = plt.subplot2grid((2, 6), (1, 5))
ax_empty.axis('off')

# Plot QQ plots for each distribution in the second row
ax4 = plt.subplot2grid((2, 6), (1, 1), colspan=2)
ax5 = plt.subplot2grid((2, 6), (1, 3), colspan=2)

sm.qqplot(data, stats.burr, fit=False, line="45", ax=ax4, distargs=(params_burr12[0], params_burr12[1]), loc=params_burr12[2], scale=params_burr12[3])
ax4.set_title('Burr')

# Using the reciprocal normal distribution as an example, replace it with your actual distribution
sm.qqplot(data, recipn, fit=False, line="45", ax=ax5, distargs=(params_reciprocal[0], params_reciprocal[1]))
ax5.set_title('Reciprocal Normal')

x1 = sm.ProbPlot(data, stats.norm, fit=False).theoretical_quantiles
y1 = sm.ProbPlot(data, stats.norm, fit=False).sample_quantiles
r_squared1 = np.corrcoef(x1, y1)[0, 1] ** 2
r_squared11 = r2_score(x1,y1)

x2 = sm.ProbPlot(data, stats.gamma, fit=False, distargs=(params_gamma[0], )).theoretical_quantiles
y2 = sm.ProbPlot(data, stats.gamma, fit=False, distargs=(params_gamma[0], )).sample_quantiles
r_squared2 = np.corrcoef(x2, y2)[0, 1] ** 2
r_squared22 = r2_score(x2,y2)

x3 = sm.ProbPlot(data, stats.lognorm, fit=False, distargs=(params_lognormal[0],)).theoretical_quantiles
y3 = sm.ProbPlot(data, stats.lognorm, fit=False, distargs=(params_lognormal[0],)).sample_quantiles
r_squared3 = np.corrcoef(x3, y3)[0, 1] ** 2
r_squared33 = r2_score(x3,y3)

x4 = sm.ProbPlot(data, stats.burr, fit=False, distargs=(params_burr12[0], params_burr12[1])).theoretical_quantiles
y4 = sm.ProbPlot(data, stats.burr, fit=False, distargs=(params_burr12[0], params_burr12[1])).sample_quantiles
r_squared4 = np.corrcoef(x4, y4)[0, 1] ** 2
r_squared44 = r2_score(x4,y4)

x5 = theoretical_cdf
y5 = empirical_cdf
r_squared5 = np.corrcoef(x5, y5)[0, 1] ** 2
r_squared55 = r2_score(x5,y5)

print(r_squared1, r_squared2, r_squared3, r_squared4, r_squared5)
print(r_squared11, r_squared22, r_squared33, r_squared44, r_squared55)

# Adjust layout
plt.tight_layout()
plt.savefig('z2.png')
plt.show()
