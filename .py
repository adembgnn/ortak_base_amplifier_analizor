import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  # Görsel işleme için eklendi


class AdvancedCommonBaseAmplifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ortak Bazlı Yükselteç Analizörü")
        self.root.geometry("1500x850")

        # Fiziksel Sabitler
        self.q = 1.602e-19
        self.k = 1.38e-23
        self.VBE_on = 0.7

        self.create_layout()
        self.create_block1_inputs()
        self.create_block2_dc_analysis()
        self.create_block3_ac_analysis()

        self.calculate_all()

    def create_layout(self):
        self.block1 = tk.Frame(self.root, width=450, bg="#f4f6f7", relief=tk.RAISED, bd=2)
        self.block1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.block2 = tk.Frame(self.root, width=400, bg="#eaf2f8", relief=tk.RAISED, bd=2)
        self.block2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.block3 = tk.Frame(self.root, width=650, bg="#e9f7ef", relief=tk.RAISED, bd=2)
        self.block3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_block1_inputs(self):
        tk.Label(self.block1, text="BLOK I: Parametreler", font=("Arial", 12, "bold"), bg="#f4f6f7").pack(pady=5)

        # --- GÖRSEL EKLEME ALANI: ANA DEVRE ---
        try:
            img1 = Image.open("devre.png")
            img1 = img1.resize((380, 180))
            self.photo1 = ImageTk.PhotoImage(img1)
            tk.Label(self.block1, image=self.photo1, bg="white", relief=tk.SUNKEN).pack(pady=5)
        except:
            tk.Label(self.block1, text="[Resim Bulunamadı: devre_ana.png]", bg="white", width=40, height=6,
                     relief=tk.SUNKEN).pack(pady=5)

        self.params = {
            "VCC (V)": {"val": 12.0, "min": 1.0, "max": 30.0, "res": 0.1},
            "VEE (V)": {"val": 5.0, "min": 1.0, "max": 15.0, "res": 0.1},
            "RE (kΩ)": {"val": 2.2, "min": 0.1, "max": 20.0, "res": 0.1},
            "RC (kΩ)": {"val": 4.7, "min": 0.1, "max": 20.0, "res": 0.1},
            "RL (kΩ)": {"val": 10.0, "min": 1.0, "max": 100.0, "res": 1.0},
            "RS (Ω)": {"val": 50.0, "min": 1.0, "max": 1000.0, "res": 10.0},
            "Beta (β)": {"val": 150.0, "min": 50.0, "max": 400.0, "res": 10.0},
            "VA (V)": {"val": 100.0, "min": 10.0, "max": 300.0, "res": 10.0},
            "Cin (μF)": {"val": 10.0, "min": 0.1, "max": 100.0, "res": 0.1},
            "Cout (μF)": {"val": 10.0, "min": 0.1, "max": 100.0, "res": 0.1},
            "Cπ (pF)": {"val": 20.0, "min": 1.0, "max": 100.0, "res": 1.0},
            "Cμ (pF)": {"val": 2.0, "min": 0.1, "max": 10.0, "res": 0.1},
            "Sıcaklık (°C)": {"val": 25.0, "min": -40.0, "max": 125.0, "res": 1.0}
        }

        self.slider_vars = {}
        controls_frame = tk.Frame(self.block1, bg="#f4f6f7")
        controls_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        for name, p in self.params.items():
            frame = tk.Frame(controls_frame, bg="#f4f6f7")
            frame.pack(fill=tk.X, pady=2)

            tk.Label(frame, text=name, width=12, anchor="w", bg="#f4f6f7", font=("Arial", 9)).pack(side=tk.LEFT)

            val_label = tk.Label(frame, text=str(p["val"]), width=6, bg="#ffffff", relief=tk.SUNKEN, font=("Arial", 9))
            val_label.pack(side=tk.RIGHT, padx=5)

            var = tk.DoubleVar(value=p["val"])
            slider = tk.Scale(frame, from_=p["min"], to=p["max"], resolution=p["res"], variable=var,
                              orient=tk.HORIZONTAL, showvalue=0,
                              command=lambda v, l=val_label, var=var: self.update_slider(l, var))
            slider.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.slider_vars[name] = var

    def update_slider(self, label, var):
        label.config(text=f"{var.get():.1f}")
        self.calculate_all()

    def create_block2_dc_analysis(self):
        tk.Label(self.block2, text="BLOK II: DC Eşdeğer & Analiz", font=("Arial", 12, "bold"), bg="#eaf2f8").pack(
            pady=5)

        # --- GÖRSEL EKLEME ALANI: DC EŞDEĞER ---
        try:
            img2 = Image.open("dc.png")
            img2 = img2.resize((250, 180))
            self.photo2 = ImageTk.PhotoImage(img2)
            tk.Label(self.block2, image=self.photo2, bg="white", relief=tk.SUNKEN).pack(pady=5)
        except:
            tk.Label(self.block2, text="[Resim Bulunamadı: devre_dc.png]", bg="white", width=40, height=6,
                     relief=tk.SUNKEN).pack(pady=5)

        self.res_labels = {}
        results = [
            ("Çalışma Bölgesi", "-"), ("Ib (μA)", "-"), ("Ic (mA)", "-"), ("Ie (mA)", "-"),
            ("Vce (V)", "-"), ("Vcb (V)", "-"), ("Vbe (V)", "-"),
            ("--- AC Eşdeğer ---", ""),
            ("Zin (Ω)", "-"), ("Zout (kΩ)", "-"), ("Av(mid) (V/V)", "-"), ("Av(mid) (dB)", "-")
        ]

        for res, init_val in results:
            if res.startswith("---"):
                tk.Label(self.block2, text=res, font=("Arial", 10, "italic"), bg="#eaf2f8", fg="gray").pack(pady=5)
                continue
            frame = tk.Frame(self.block2, bg="#eaf2f8")
            frame.pack(fill=tk.X, padx=20, pady=2)
            tk.Label(frame, text=res + ":", width=15, anchor="w", font=("Arial", 10, "bold"), bg="#eaf2f8").pack(
                side=tk.LEFT)
            lbl = tk.Label(frame, text=init_val, font=("Arial", 10), bg="#eaf2f8", fg="#333333")
            lbl.pack(side=tk.LEFT)
            self.res_labels[res] = lbl

    def create_block3_ac_analysis(self):
        tk.Label(self.block3, text="BLOK III: Yüksek Frekans Analizi", font=("Arial", 12, "bold"), bg="#e9f7ef").pack(
            pady=5)

        # --- GÖRSEL EKLEME ALANI: AC EŞDEĞER ---
        try:
            img3 = Image.open("ac.png")
            img3 = img3.resize((500, 180))
            self.photo3 = ImageTk.PhotoImage(img3)
            tk.Label(self.block3, image=self.photo3, bg="white", relief=tk.SUNKEN).pack(pady=5)
        except:
            tk.Label(self.block3, text="[Resim Bulunamadı: devre_ac.png]", bg="white", width=40, height=4,
                     relief=tk.SUNKEN).pack(pady=5)

        self.freq_labels = {}
        frame_ac = tk.Frame(self.block3, bg="#e9f7ef")
        frame_ac.pack(fill=tk.X, padx=20, pady=5)

        metrics = [("Sayısal fL", "-"), ("Sayısal fh", "-"), ("|Kv(fh)| Kazancı", "-"), ("Geçiş Frek. (fT)", "-")]
        for i, (name, val) in enumerate(metrics):
            tk.Label(frame_ac, text=name + ":", font=("Arial", 10, "bold"), bg="#e9f7ef").grid(row=i // 2,
                                                                                               column=(i % 2) * 2,
                                                                                               sticky="w", pady=2,
                                                                                               padx=5)
            lbl = tk.Label(frame_ac, text=val, font=("Arial", 10), bg="#e9f7ef")
            lbl.grid(row=i // 2, column=(i % 2) * 2 + 1, sticky="w")
            self.freq_labels[name] = lbl

        self.fig = Figure(figsize=(6, 4.5), dpi=100)
        self.fig.patch.set_facecolor('#e9f7ef')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.block3)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

    def calculate_all(self, *args):
        VCC = self.slider_vars["VCC (V)"].get()
        VEE = self.slider_vars["VEE (V)"].get()
        RE = max(self.slider_vars["RE (kΩ)"].get() * 1e3, 1e-3)
        RC = max(self.slider_vars["RC (kΩ)"].get() * 1e3, 1e-3)
        RL = max(self.slider_vars["RL (kΩ)"].get() * 1e3, 1e-3)
        RS = self.slider_vars["RS (Ω)"].get()
        beta = self.slider_vars["Beta (β)"].get()
        VA = self.slider_vars["VA (V)"].get()
        Cin = self.slider_vars["Cin (μF)"].get() * 1e-6
        Cout = self.slider_vars["Cout (μF)"].get() * 1e-6
        Cpi = self.slider_vars["Cπ (pF)"].get() * 1e-12
        Cmu = self.slider_vars["Cμ (pF)"].get() * 1e-12
        T_celsius = self.slider_vars["Sıcaklık (°C)"].get()

        VT = (self.k * (T_celsius + 273.15)) / self.q
        alpha = beta / (beta + 1)

        Ie = (VEE - self.VBE_on) / RE if VEE > self.VBE_on else 0.0

        if Ie <= 0:
            self.set_cutoff_state()
            return

        Ic = alpha * Ie
        Ib = Ic / beta
        Vc = VCC - Ic * RC
        Vce = Vc - (-self.VBE_on)
        Vcb = Vc - 0.0

        if Vcb < 0:
            self.set_saturation_state()
            return

        gm = Ic / VT
        re = VT / Ie
        ro = VA / Ic

        Zin = (RE * re) / (RE + re)
        Zout = (RC * ro) / (RC + ro)
        RL_prime = (Zout * RL) / (Zout + RL)

        Av_mid = gm * RL_prime * (Zin / (RS + Zin))
        Av_mid_dB = 20 * np.log10(Av_mid) if Av_mid > 0 else 0

        self.res_labels["Çalışma Bölgesi"].config(text="AKTİF BÖLGE", fg="green")
        self.res_labels["Ib (μA)"].config(text=f"{Ib * 1e6:.2f}")
        self.res_labels["Ic (mA)"].config(text=f"{Ic * 1e3:.2f}")
        self.res_labels["Ie (mA)"].config(text=f"{Ie * 1e3:.2f}")
        self.res_labels["Vce (V)"].config(text=f"{Vce:.2f}")
        self.res_labels["Vcb (V)"].config(text=f"{Vcb:.2f}")
        self.res_labels["Vbe (V)"].config(text=f"{self.VBE_on:.3f}")
        self.res_labels["Zin (Ω)"].config(text=f"{Zin:.2f}")
        self.res_labels["Zout (kΩ)"].config(text=f"{Zout / 1000:.2f}")
        self.res_labels["Av(mid) (V/V)"].config(text=f"{Av_mid:.2f}")
        self.res_labels["Av(mid) (dB)"].config(text=f"{Av_mid_dB:.2f}")

        # Zaman Sabitleri (Zin ve Rpi_eq ilişkisi fiziken doğrudur)
        f_L1 = 1 / (2 * np.pi * (RS + Zin) * Cin)
        f_L2 = 1 / (2 * np.pi * (Zout + RL) * Cout)
        R_pi_eq = (RS * Zin) / (RS + Zin)
        f_H1 = 1 / (2 * np.pi * R_pi_eq * Cpi)
        f_H2 = 1 / (2 * np.pi * RL_prime * Cmu)

        fT = gm / (2 * np.pi * (Cpi + Cmu))

        # Sinyal Dizisi (1 Hz - 10 GHz)
        f = np.logspace(0, 10, 50000)
        s = 1j * 2 * np.pi * f

        w_L1, w_L2 = 2 * np.pi * f_L1, 2 * np.pi * f_L2
        w_H1, w_H2 = 2 * np.pi * f_H1, 2 * np.pi * f_H2

        # Tam Transfer Fonksiyonu (H(s))
        H_s = Av_mid * (s / w_L1) / (1 + s / w_L1) * (s / w_L2) / (1 + s / w_L2) * (1 / (1 + s / w_H1)) * (
                1 / (1 + s / w_H2))
        Gain_dB = 20 * np.log10(np.abs(H_s) + 1e-12)

        # SAYISAL KÖK BULMA (Kesin Milimetrik -3dB)
        max_gain_idx = np.argmax(Gain_dB)
        max_gain_val = Gain_dB[max_gain_idx]
        target_gain = max_gain_val - 3.0

        # -3dB Noktalarını Kesen İndeksleri Bulma
        crossings = np.where(np.diff(np.sign(Gain_dB - target_gain)))[0]
        fL_exact, fh_exact = 0.0, 0.0

        if len(crossings) >= 1:
            # İlk kesişim alt kutuptur (Doğrusal İnterpolasyon)
            idx = crossings[0]
            fL_exact = np.interp(target_gain, [Gain_dB[idx], Gain_dB[idx + 1]], [f[idx], f[idx + 1]])
        if len(crossings) >= 2:
            # Son kesişim üst kutuptur
            idx = crossings[-1]
            fh_exact = np.interp(target_gain, [Gain_dB[idx + 1], Gain_dB[idx]], [f[idx + 1], f[idx]])

        self.freq_labels["Sayısal fL"].config(text=f"{fL_exact:.2f} Hz" if fL_exact else "-")
        self.freq_labels["Sayısal fh"].config(text=f"{fh_exact / 1e6:.2f} MHz" if fh_exact else "-")
        self.freq_labels["|Kv(fh)| Kazancı"].config(text=f"{target_gain:.2f} dB")
        self.freq_labels["Geçiş Frek. (fT)"].config(text=f"{fT / 1e6:.2f} MHz")

        # Bode Plot
        self.ax.clear()
        self.ax.semilogx(f, Gain_dB, color='#1f77b4', linewidth=2)
        if fL_exact:
            self.ax.axvline(fL_exact, color='orange', linestyle='--', label=f'fL = {fL_exact:.1f} Hz')
        if fh_exact:
            self.ax.axvline(fh_exact, color='red', linestyle='--', label=f'fh = {fh_exact / 1e6:.1f} MHz')
        self.ax.axhline(target_gain, color='green', linestyle=':', label='-3dB Hattı')

        self.ax.set_title("Bode Diyagramı (Nümerik Analiz)")
        self.ax.set_xlabel("Frekans (Hz)")
        self.ax.set_ylabel("Kazanç (dB)")
        self.ax.grid(True, which="both", ls="--", alpha=0.4)
        self.ax.set_ylim([max(-20, max_gain_val - 40), max_gain_val + 10])
        self.ax.legend(loc='lower right', fontsize=8)
        self.canvas.draw()

    def set_cutoff_state(self):
        self.res_labels["Çalışma Bölgesi"].config(text="KESİM BÖLGESİ", fg="red")
        self._clear_metrics()

    def set_saturation_state(self):
        self.res_labels["Çalışma Bölgesi"].config(text="DOYMA BÖLGESİ", fg="red")
        self._clear_metrics()

    def _clear_metrics(self):
        for k in ["Ib (μA)", "Ic (mA)", "Ie (mA)", "Vce (V)", "Vcb (V)", "Zin (Ω)", "Zout (kΩ)", "Av(mid) (V/V)",
                  "Av(mid) (dB)"]:
            self.res_labels[k].config(text="0.00")
        for k in self.freq_labels.keys():
            self.freq_labels[k].config(text="-")
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'Transistör Aktif Değil', horizontalalignment='center', verticalalignment='center',
                     transform=self.ax.transAxes)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCommonBaseAmplifierApp(root)
    root.mainloop()
