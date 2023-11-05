import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, optimize
from sklearn.metrics import mean_squared_error

def func1(data, mean, std):
    return (5000 / (np.sqrt(2*np.pi) * std * (data)**2)) * np.exp(-1/2*((5000/data - mean)/std)**2)

# Function to fit distributions and calculate RMSE, AIC, and KS test
def fit_and_calculate_metrics(file_number):
    file_path = f'ttd_3000_{file_number}.3lanes.csv'
    # data = pd.read_csv(file_path)
    #
    df = pd.read_csv(file_path)
    time_travel_data = df['Time_Travel'].dropna()[10:2700]

    # Fit the distributions using MLE
    c_burr, d_burr, loc_burr, scale_burr = stats.burr12.fit(time_travel_data)
    mu_norm, std_norm = stats.norm.fit(time_travel_data)
    a_gamma, loc_gamma, scale_gamma = stats.gamma.fit(time_travel_data)
    s_ln, loc_ln, scale_ln = stats.lognorm.fit(time_travel_data)

    # Generate the empirical distribution
    hist, bins = np.histogram(time_travel_data, bins=30, density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    params, _ = optimize.curve_fit(func1, bin_centers, hist, p0=[28, 1])

    # Calculate the PDF values of the fitted distributions
    fitted_pdf_burr = stats.burr12.pdf(bin_centers, c_burr, d_burr, loc_burr, scale_burr)
    fitted_pdf_norm = stats.norm.pdf(bin_centers, mu_norm, std_norm)
    fitted_pdf_gamma = stats.gamma.pdf(bin_centers, a_gamma, loc_gamma, scale_gamma)
    fitted_pdf_lognorm = stats.lognorm.pdf(bin_centers, s_ln, loc_ln, scale_ln)
    fitted_pdf_recipn = func1(bin_centers, params[0], params[1])

    # Calculate RMSE for each distribution using non-normalized data
    rmse_burr = np.sqrt(mean_squared_error(hist, fitted_pdf_burr))
    rmse_norm = np.sqrt(mean_squared_error(hist, fitted_pdf_norm))
    rmse_gamma = np.sqrt(mean_squared_error(hist, fitted_pdf_gamma))
    rmse_lognorm = np.sqrt(mean_squared_error(hist, fitted_pdf_lognorm))
    rmse_recipn = np.sqrt(mean_squared_error(hist, fitted_pdf_recipn))

    # Calculate MAPE for each distribution
    mape_burr = np.mean(np.abs((hist - fitted_pdf_burr) / hist)) * 100
    mape_norm = np.mean(np.abs((hist - fitted_pdf_norm) / hist)) * 100
    mape_gamma = np.mean(np.abs((hist - fitted_pdf_gamma) / hist)) * 100
    mape_lognorm = np.mean(np.abs((hist - fitted_pdf_lognorm) / hist)) * 100
    mape_recipn = np.mean(np.abs((hist - fitted_pdf_recipn) / hist)) * 100


    # Plot histogram and fits
    # plt.figure(figsize=(10, 6))
    # plt.hist(time_travel_data, bins=30, density=True, alpha=0.5, label='Empirical Data')
    # plt.plot(bin_centers, fitted_pdf_burr, label=f'Burr Fit (RMSE={rmse_burr:.2f})')
    # plt.plot(bin_centers, fitted_pdf_norm, label=f'Normal Fit (RMSE={rmse_norm:.2f})')
    # plt.plot(bin_centers, fitted_pdf_gamma, label=f'Gamma Fit (RMSE={rmse_gamma:.2f})')
    # plt.plot(bin_centers, fitted_pdf_lognorm, label=f'Lognormal Fit (RMSE={rmse_lognorm:.2f})')
    # plt.plot(bin_centers, fitted_pdf_recipn, label=f'Reciprocal normal Fit')
    #
    # plt.title(f'Histogram and Fits for {file_path}')
    # plt.xlabel('Time Travel')
    # plt.ylabel('Probability Density')
    # plt.legend()
    # plt.show()

    # Calculate AIC for each distribution
    n = len(time_travel_data)
    k_burr = 4  # Number of parameters for Burr distribution
    k_norm = 2  # Number of parameters for Normal distribution
    k_gamma = 3  # Number of parameters for Gamma distribution
    k_lognorm = 3  # Number of parameters for Lognormal distribution
    k_recipn = 2

    aic_burr = 2 * k_burr - 2 * np.log(stats.burr12.pdf(time_travel_data, c_burr, d_burr, loc_burr, scale_burr)).sum()
    aic_norm = 2 * k_norm - 2 * np.log(stats.norm.pdf(time_travel_data, mu_norm, std_norm)).sum()
    aic_gamma = 2 * k_gamma - 2 * np.log(stats.gamma.pdf(time_travel_data, a_gamma, loc_gamma, scale_gamma)).sum()
    aic_lognorm = 2 * k_lognorm - 2 * np.log(stats.lognorm.pdf(time_travel_data, s_ln, loc_ln, scale_ln)).sum()
    aic_recipn = 2 * k_recipn - 2 * np.log(func1(time_travel_data, params[0], params[1])).sum()

    # Calculate KS statistic and p-value for each distribution
    ks_stat_burr = stats.ks_2samp(hist, fitted_pdf_burr)[0]
    ks_stat_norm = stats.ks_2samp(hist, fitted_pdf_norm)[0]
    ks_stat_gamma = stats.ks_2samp(hist, fitted_pdf_gamma)[0]
    ks_stat_lnorm = stats.ks_2samp(hist, fitted_pdf_lognorm)[0]
    ks_stat_recipn = stats.ks_2samp(hist, fitted_pdf_recipn)[0]

    # Calculate Chi-squared statistic and p-value for each distribution
    chi2_stat_burr, chi2_pvalue_burr = stats.chisquare(hist*len(time_travel_data), fitted_pdf_burr*len(time_travel_data))
    chi2_stat_norm, chi2_pvalue_norm = stats.chisquare(hist*len(time_travel_data), fitted_pdf_norm*len(time_travel_data))
    chi2_stat_gamma, chi2_pvalue_gamma = stats.chisquare(hist*len(time_travel_data), fitted_pdf_gamma*len(time_travel_data))
    chi2_stat_lognorm, chi2_pvalue_lognorm = stats.chisquare(hist*len(time_travel_data), fitted_pdf_lognorm*len(time_travel_data))
    chi2_stat_recipn, chi2_pvalue_recipn = stats.chisquare(hist*len(time_travel_data), fitted_pdf_recipn*len(time_travel_data))

    return {
        'File': f'ttd_3000_{file_number}.csv',
        'RMSE_Burr': rmse_burr,
        'RMSE_Normal': rmse_norm,
        'RMSE_Gamma': rmse_gamma,
        'RMSE_Lognormal': rmse_lognorm,
        'RMSE_Recipn': rmse_recipn,
        'MAPE_Burr': mape_burr,
        'MAPE_Normal': mape_norm,
        'MAPE_Gamma': mape_gamma,
        'MAPE_Lognormal': mape_lognorm,
        'MAPE_Recipn': mape_recipn,
        'AIC_Burr': aic_burr,
        'AIC_Normal': aic_norm,
        'AIC_Gamma': aic_gamma,
        'AIC_Lognormal': aic_lognorm,
        'AIC_Recipn': aic_recipn,
        'KS_Stat_Burr': ks_stat_burr,
        'KS_Stat_Norm': ks_stat_norm,
        'KS_Stat_Gamma': ks_stat_gamma,
        'KS_Stat_Lognormal': ks_stat_lnorm,
        'KS_Stat_Recipn': ks_stat_recipn,
        'Chi2_Stat_Burr': chi2_stat_burr,
        'Chi2_PValue_Burr': chi2_pvalue_burr,
        'Chi2_Stat_Normal': chi2_stat_norm,
        'Chi2_PValue_Normal': chi2_pvalue_norm,
        'Chi2_Stat_Gamma': chi2_stat_gamma,
        'Chi2_PValue_Gamma': chi2_pvalue_gamma,
        'Chi2_Stat_Lognormal': chi2_stat_lognorm,
        'Chi2_PValue_Lognormal': chi2_pvalue_lognorm,
        'Chi2_Stat_Recipn': chi2_stat_recipn,
        'Chi2_PValue_Recipn': chi2_pvalue_recipn
    }

# Iterate over file numbers (10 to 49)
results = []
for file_number in range(10, 81):
    result = fit_and_calculate_metrics(file_number)
    results.append(result)

# Create a summary DataFrame
summary_df = pd.DataFrame(results)

# Save the summary DataFrame to a CSV file
summary_df.to_csv('metrics_summary_3000_3lanes.csv', index=False)
