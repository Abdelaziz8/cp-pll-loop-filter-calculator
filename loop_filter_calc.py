import numpy as np
import matplotlib.pyplot as plt

def calculate_kc(pm_deg):
    """
    Calculates the capacitor ratio and spread factor based on 
    the geometric mean optimization.
    """
    pm_rad = np.radians(pm_deg)
    tan_pm = np.tan(pm_rad)
    sec_pm = 1 / np.cos(pm_rad) 
    
    # Capacitor ratio Kc = C1 / C2
    kc = 2 * (tan_pm**2 + tan_pm * sec_pm)
    
    # Spread Factor S = wu/wz = wp3/wu = sqrt(1+Kc)
    spread = np.sqrt(1 + kc)
    
    return kc, spread

# --- Generate the curve for visualization ---
pm_range = np.linspace(30, 80, 500)
kc_curve = [calculate_kc(pm)[0] for pm in pm_range] 

# --- Selected Design Point ---
pm_input = 60
kc_sel, spread_sel = calculate_kc(pm_input)

# --- Plotting ---
plt.figure(figsize=(10, 7))
plt.plot(pm_range, kc_curve, 'b-', label=r'Optimal $K_C$ curve', linewidth=2)
plt.plot(pm_input, kc_sel, 'ro', markersize=8, label=fr'Design Point ($\Phi_M={pm_input}^\circ$)')

annotation_text = (fr'Target $\Phi_M$: {pm_input}$^\circ$' + '\n'
                   fr'$K_C$ ($C_1/C_2$): {kc_sel:.2f}' + '\n'
                   fr'Spread ($S$): {spread_sel:.2f}')

plt.annotate(annotation_text,
             xy=(pm_input, kc_sel),
             xytext=(pm_input - 15, kc_sel + 20), 
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8),
             bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
             fontsize=10)

plt.title(r'PLL Loop Filter Design: $K_C$ and Spread Factor vs. Phase Margin', fontsize=14)
plt.xlabel(r'Phase Margin ($\Phi_M$) [Degrees]', fontsize=12)
plt.ylabel(r'Capacitor Ratio ($K_C = C_1 / C_2$)', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend(loc='upper left')

plt.xlim(25, 85)
plt.ylim(0, max(kc_curve) * 1.2)

plt.savefig('kc_vs_pm_annotated.png')
print(f"Plot generated successfully for PM = {pm_input}!")
print(f"Kc = {kc_sel:.4f}, Spread = {spread_sel:.4f}")

plt.show()

def calculate_by_current(f_u, icp, n_div, kvco_hz_v, kc, spread):
    """
    Calculates R1, C1, and C2 based on a fixed loop bandwidth and fixed ICP.
    """
    omega_u = 2 * np.pi * f_u
    
    # 1. Calculate C2 based on the magnitude balance at omega_u
    mag_correction = np.sqrt((1 + (1/spread)**2) / (1 + spread**2))
    c2 = (icp * kvco_hz_v * mag_correction) / (n_div * (omega_u**2))
    
    # 2. Calculate C1
    c1 = c2 * kc
    
    # 3. Calculate R1 to set the zero correctly
    r1 = spread / (omega_u * c1)
    
    return {
        "C1": c1,
        "C2": c2,
        "R1": r1,
        "wz_rad": omega_u / spread,
        "wp3_rad": omega_u * spread
    }

# --- Design Execution ---
params = calculate_by_current(
    f_u=300e3, 
    icp=3e-3, 
    n_div=44, 
    kvco_hz_v=150e06, 
    kc=kc_sel, 
    spread=spread_sel
)

fz_hz = params['wz_rad'] / (2 * np.pi)
fp3_hz = params['wp3_rad'] / (2 * np.pi)

print(f"--- Results for fixed Icp = 3 mA ---")
print(f"R1: {params['R1']/1e3:.2f} kOhm")
print(f"C1: {params['C1']*1e12:.2f} pF")
print(f"C2: {params['C2']*1e12:.2f} pF")
print(f"Zero Location (fz): {fz_hz/1e3:.2f} kHz")
print(f"Third Pole Location (fp3): {fp3_hz/1e6:.2f} MHz")
