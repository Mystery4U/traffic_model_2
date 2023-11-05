import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file into a DataFrame
df = pd.read_excel('metrics_summary_3000_3lanes.xlsx')

# Extract the required columns
columns_to_plot_1 = ['Chi2_Stat_Burr', 'Chi2_Stat_Recipn', 'Chi2_Stat_Normal', 'Chi2_Stat_Gamma', 'Chi2_Stat_Lognormal']
columns_to_plot_2 = ['Chi2_PValue_Burr', 'Chi2_PValue_Recipn', 'Chi2_PValue_Normal', 'Chi2_PValue_Gamma', 'Chi2_PValue_Lognormal']

# Create a figure with 1 row and 2 columns
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), sharex=True)

# Plot the first set of columns (Chi2 Statistics) in the first subplot
x_values = df.index + 10
axes[0].plot(x_values, df['Chi2_Stat_Normal'], label='$\chi^2_{normal}$', color='blue')
axes[0].plot(x_values, df['Chi2_Stat_Gamma'], label='$\chi^2_{gamma}$', color='red')
axes[0].plot(x_values, df['Chi2_Stat_Lognormal'], label='$\chi^2_{lognormal}$', color='green')
axes[0].plot(x_values, df['Chi2_Stat_Burr'], label='$\chi^2_{burr}$', color='purple')
axes[0].plot(x_values, df['Chi2_Stat_Recipn'], label='$\chi^2_{reciprocal}$', color='orange')

# Set labels and titles for the first subplot
axes[0].set_xlabel('Vehicle Rate $r$')
axes[0].set_ylabel('$\chi^2$ Test Statistic')
axes[0].set_title('$\chi^2$ Test Statistic vs Vehicle Rate $r$')
# axes[0].set_yscale('log')
axes[0].grid()
axes[0].legend()

# Plot the second set of columns (Chi2 P-Values) in the second subplot
axes[1].plot(x_values, df['Chi2_PValue_Normal'], label='$p_{normal}$', color='blue')
axes[1].plot(x_values, df['Chi2_PValue_Gamma'], label='$p_{gamma}$', color='red')
axes[1].plot(x_values, df['Chi2_PValue_Lognormal'], label='$p_{lognormal}$', color='green')
axes[1].plot(x_values, df['Chi2_PValue_Burr'], label='$p_{burr}$', color='purple')
axes[1].plot(x_values, df['Chi2_PValue_Recipn'], label='$p_{reciprocal}$', color='orange')

# Set labels and titles for the second subplot
axes[1].set_xlabel('Vehicle Rate $r$')
axes[1].set_ylabel('$p$-value')
axes[1].set_title('$p$-value vs Vehicle Rate $r$')
axes[1].set_yscale('log')
axes[1].grid()
axes[1].legend()

# Adjust layout to prevent clipping of labels
plt.tight_layout()
plt.savefig('chisquare_300_vrachtwagen')
# Show the plot
plt.show()

columns_to_plot_rmse = ['RMSE_Burr', 'RMSE_Normal', 'RMSE_Gamma', 'RMSE_Lognormal', 'RMSE_Recipn']
# Create a new figure
fig, ax = plt.subplots(figsize=(15, 10))

# Plot each column on a linear scale
x_values_rmse = df.index + 10

# Plot RMSE_Normal
y_values_rmse_normal = df['RMSE_Normal']
ax.plot(x_values_rmse, y_values_rmse_normal, label='$RMSE_{normal}$', color = 'blue')

# Plot RMSE_Gamma
y_values_rmse_gamma = df['RMSE_Gamma']
ax.plot(x_values_rmse, y_values_rmse_gamma, label='$RMSE_{gamma}$', color = 'red')

# Plot RMSE_Lognormal
y_values_rmse_lognormal = df['RMSE_Lognormal']
ax.plot(x_values_rmse, y_values_rmse_lognormal, label='$RMSE_{lognormal}$', color = 'green')

# Plot RMSE_Burr
y_values_rmse_burr = df['RMSE_Burr']
ax.plot(x_values_rmse, y_values_rmse_burr, label='$RMSE_{burr}$', color = 'purple')

# Plot RMSE_Recipn
y_values_rmse_recipn = df['RMSE_Recipn']
ax.plot(x_values_rmse, y_values_rmse_recipn, label='$RMSE_{reciprocal}$', color = 'orange')

# Set labels and title for the plot
ax.set_xlabel('Vehicle Rate $r$')
ax.set_ylabel('Root Mean Squared Error (RMSE)')
ax.set_title('RMSE of each distribution vs Vehicle Rate $r$')

ax.legend()
plt.grid()
plt.savefig('RMSE_300_vrachtwagen')
plt.show()


columns_to_plot_aic = ['AIC_Burr', 'AIC_Normal', 'AIC_Lognormal', 'AIC_Gamma', 'AIC_Recipn']

# Create a new figure for AIC
fig, ax = plt.subplots(figsize=(15, 10))

# Plot each column on a linear scale
x_values_aic = df.index + 10

# Plot AIC_Normal
y_values_aic_normal = df['AIC_Normal']
ax.plot(x_values_aic, y_values_aic_normal, label='$AIC_{normal}$', color='blue')

# Plot AIC_Gamma
y_values_aic_gamma = df['AIC_Gamma']
ax.plot(x_values_aic, y_values_aic_gamma, label='$AIC_{gamma}$', color='red')

# Plot AIC_Lognormal
y_values_aic_lognormal = df['AIC_Lognormal']
ax.plot(x_values_aic, y_values_aic_lognormal, label='$AIC_{lognormal}$', color='green')

# Plot AIC_Burr
y_values_aic_burr = df['AIC_Burr']
ax.plot(x_values_aic, y_values_aic_burr, label='$AIC_{burr}$', color='purple')

# Plot AIC_Recipn
y_values_aic_recipn = df['AIC_Recipn']
ax.plot(x_values_aic, y_values_aic_recipn, label='$AIC_{reciprocal}$', color='orange')

# Set labels and title for the AIC plot
ax.set_xlabel('Vehicle Rate $r$')
ax.set_ylabel('Akaike Information Criterion (AIC)')
ax.set_title('AIC of each distribution vs Vehicle Rate $r$')

ax.legend()
plt.grid()
plt.savefig('AIC_300_vrachtwagen')
plt.show()