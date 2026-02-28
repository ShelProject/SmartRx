import streamlit as st
import pandas as pd
import os
import math
import datetime

st.set_page_config(page_title="SmartRx", page_icon="🩺", layout="wide", initial_sidebar_state="expanded")

# --- HIDE STREAMLIT BRANDING ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            [data-testid="stToolbarActions"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if 'lang' not in st.session_state:
    st.session_state.lang = "English"
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "🏠 Home / Beranda"

def switch_page(page_name):
    st.session_state.menu_selection = page_name

def change_language():
    st.session_state.lang = st.session_state.lang_widget

# --- SIDEBAR NAV ---
st.sidebar.title("Navigation / Navigasi")
menu_options = [
    "🏠 Home / Beranda",
    "💊 Auto-Calc / Kalkulator Otomatis", 
    "🧮 Manual Calculator / Manual", 
    "💉 Injection Drugs / Obat Injeksi",
    "💧 IV Fluid / Cairan Infus",
    "👶 Peds Dehydration / Dehidrasi Anak", 
    "⚖️ BMI & BSA / Antropometri", 
    "🤰 Obstetric Calc / Kandungan",
    "📚 Drug References / Referensi"
]

menu = st.sidebar.radio("Menu", menu_options, key="menu_selection")

# --- SIDEBAR FOOTER ---
st.sidebar.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.sidebar.divider()
if st.session_state.lang == "English":
    st.sidebar.markdown("<p style='font-size: 14px; text-align: center;'>For more information you can contact:<br><b>dr. Shelly Lesmana</b></p>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<p style='font-size: 14px; text-align: center;'>Untuk informasi lebih lanjut Anda dapat menghubungi:<br><b>dr. Shelly Lesmana</b></p>", unsafe_allow_html=True)

file_path = "drugs_database.xlsx"

# --- 1. HOME PAGE ---
if menu == "🏠 Home / Beranda":
    if st.session_state.lang == "English":
        st.title("🩺 SmartRx Clinical Assistant")
        st.markdown("Welcome to SmartRx. This tool is designed to provide quick, accurate, and safe dosage calculations to streamline your clinical workflow.")
    else:
        st.title("🩺 Asisten Klinis SmartRx")
        st.markdown("Selamat datang di SmartRx. Alat ini dirancang untuk memberikan perhitungan dosis yang cepat, akurat, dan aman untuk membantu alur kerja klinis Anda.")
        
    st.write("### 🌐 Select Language / Pilih Bahasa")
    st.radio("", 
             ["English", "Bahasa Indonesia"], 
             index=0 if st.session_state.lang == "English" else 1,
             key="lang_widget", 
             on_change=change_language, 
             horizontal=True)
    
    
    st.divider()

    col1, col2 = st.columns(2)
    
    if st.session_state.lang == "English":
        with col1:
            st.info("⚡ **Common Drugs Auto-Calc**\n\nAutomatically calculate safe dosage ranges and exact prescription amounts.")
            st.button("Go to Auto-Calc", use_container_width=True, on_click=switch_page, args=("💊 Auto-Calc / Kalkulator Otomatis",))

            st.error("💉 **Injection Calculator**\n\nCalculate exact mL for emergency IV/IM drugs.")
            st.button("Go to Injection Drugs", use_container_width=True, on_click=switch_page, args=("💉 Injection Drugs / Obat Injeksi",)) 

            st.success("💧 **IV Fluid Calculator**\n\nCalculate maintenance fluids and exact nursing drip rates.")
            st.button("Go to IV Fluid", use_container_width=True, on_click=switch_page, args=("💧 IV Fluid / Cairan Infus",))
            
            st.warning("👶 **Pediatric Dehydration**\n\nCalculate WHO Plan B (ORS) and Plan C (IV Fluids) for children.")
            st.button("Go to Peds Dehydration", use_container_width=True, on_click=switch_page, args=("👶 Peds Dehydration / Dehidrasi Anak",))

        with col2:
            st.warning("🧮 **Manual Calculator**\n\nPerform manual mg/kg calculations for any custom drug or syrup.")
            st.button("Go to Manual Calculator", use_container_width=True, on_click=switch_page, args=("🧮 Manual Calculator / Manual",))
            
            st.info("⚖️ **BMI & BSA Calculator**\n\nCalculate Body Mass Index and Body Surface Area.")
            st.button("Go to BMI & BSA", use_container_width=True, on_click=switch_page, args=("⚖️ BMI & BSA / Antropometri",))

            st.success("🤰 **Obstetric Calculator**\n\nCalculate Gestational Age and Estimated Date of Delivery.")
            st.button("Go to Obstetric Calc", use_container_width=True, on_click=switch_page, args=("🤰 Obstetric Calc / Kandungan",))

            st.error("📚 **Drug References**\n\nSearch your digital database for dosages, indications, and clinical warnings.")
            st.button("Go to Drug References", use_container_width=True, on_click=switch_page, args=("📚 Drug References / Referensi",))
            
    else:
        with col1:
            st.info("⚡ **Kalkulator Otomatis Obat**\n\nHitung otomatis rentang dosis aman dan jumlah resep yang tepat.")
            st.button("Buka Kalkulator Otomatis", use_container_width=True, on_click=switch_page, args=("💊 Auto-Calc / Kalkulator Otomatis",))

            st.error("💉 **Kalkulator Obat Injeksi**\n\nHitung mL persis untuk obat darurat IV/IM.")
            st.button("Buka Kalkulator Injeksi", use_container_width=True, on_click=switch_page, args=("💉 Injection Drugs / Obat Injeksi",))

            st.success("💧 **Kalkulator Cairan Infus**\n\nHitung cairan pemeliharaan dan kecepatan tetesan infus perawat.")
            st.button("Buka Kalkulator Infus", use_container_width=True, on_click=switch_page, args=("💧 IV Fluid / Cairan Infus",))
            
            st.warning("👶 **Dehidrasi Anak (MTBS)**\n\nHitung Rencana B (Oralit) dan Rencana C (Infus) berdasarkan panduan WHO.")
            st.button("Buka Kalkulator Dehidrasi", use_container_width=True, on_click=switch_page, args=("👶 Peds Dehydration / Dehidrasi Anak",))

        with col2:
            st.warning("🧮 **Kalkulator Manual**\n\nLakukan perhitungan mg/kg manual untuk sediaan obat atau sirup apa pun.")
            st.button("Buka Kalkulator Manual", use_container_width=True, on_click=switch_page, args=("🧮 Manual Calculator / Manual",))
            
            st.info("⚖️ **Kalkulator BMI & BSA**\n\nHitung Indeks Massa Tubuh dan Luas Permukaan Tubuh.")
            st.button("Buka Kalkulator Antropometri", use_container_width=True, on_click=switch_page, args=("⚖️ BMI & BSA / Antropometri",))

            st.success("🤰 **Kalkulator Kehamilan**\n\nHitung Usia Kehamilan (UK) dan Hari Perkiraan Lahir (HPL).")
            st.button("Buka Kalkulator Kehamilan", use_container_width=True, on_click=switch_page, args=("🤰 Obstetric Calc / Kandungan",))

            st.error("📚 **Referensi Obat**\n\nCari database digital Anda untuk dosis, indikasi, dan peringatan klinis.")
            st.button("Buka Referensi Obat", use_container_width=True, on_click=switch_page, args=("📚 Drug References / Referensi",))


# --- 2. AUTO CALCULATOR ---
elif menu == "💊 Auto-Calc / Kalkulator Otomatis":
    st.header("Auto Calculator" if st.session_state.lang == "English" else "Kalkulator Otomatis Obat")
    
    if os.path.exists(file_path):
        try:
            df_autocalc = pd.read_excel(file_path, sheet_name="AutoCalc")
            
            drug_db = {}
            for index, row in df_autocalc.iterrows():
                drug_db[row["Drug Name"]] = {
                    "type": row["Type"],
                    "min_dose": float(row["Min Daily Dose (mg/kg)"]),
                    "max_dose": float(row["Max Daily Dose (mg/kg)"]),
                    "avail": float(row["Available (mg)"]),
                    "info": str(row["Clinical Info"])
                }
            
            # --- NEW SEARCH FEATURE ---
            search_label = "🔍 Search Drug:" if st.session_state.lang == "English" else "🔍 Cari Obat:"
            search_query = st.text_input(search_label, key="search_auto")
            
            # Filter the list based on search
            filtered_drugs = [drug for drug in drug_db.keys() if search_query.lower() in drug.lower()]
            
            if filtered_drugs:
                sel_label = "Select Drug" if st.session_state.lang == "English" else "Pilih Obat"
                selected_drug = st.selectbox(sel_label, filtered_drugs)
                
                st.info(drug_db[selected_drug]["info"])
                
                col1, col2 = st.columns(2)
                with col1:
                    w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan Pasien (kg)"
                    weight = st.number_input(w_label, min_value=0.0, step=0.1)
                with col2:
                    f_label = "Frequency (Times a day)" if st.session_state.lang == "English" else "Frekuensi (Kali sehari)"
                    freq = st.selectbox(f_label, [1, 2, 3, 4], index=2)
                
                calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
                
                if st.button(calc_txt) and weight > 0:
                    drug_info = drug_db[selected_drug]
                    
                    min_daily_total = drug_info["min_dose"] * weight
                    max_daily_total = drug_info["max_dose"] * weight
                    
                    min_per_dose = min_daily_total / freq
                    max_per_dose = max_daily_total / freq
                    
                    if st.session_state.lang == "English":
                        st.success(f"**Total 24h Dose Range:** {min_daily_total:.1f} - {max_daily_total:.1f} mg/day")
                        st.success(f"**Target Amount Per Dose Range:** {min_per_dose:.1f} - {max_per_dose:.1f} mg/dose")
                        
                        if drug_info["type"] == "tab":
                            min_tabs, max_tabs = min_per_dose / drug_info["avail"], max_per_dose / drug_info["avail"]
                            st.warning(f"📝 **Prescription Range:** Take {min_tabs:.2f} - {max_tabs:.2f} tablet(s), {freq} time(s) a day.")
                        else:
                            min_vol, max_vol = min_per_dose / drug_info["avail"], max_per_dose / drug_info["avail"]
                            min_s, max_s = min_vol / 5.0, max_vol / 5.0
                            st.warning(f"📝 **Prescription Range:** Take {min_vol:.1f} - {max_vol:.1f} mL ({min_s:.1f} - {max_s:.1f} measuring spoon(s) of 5mL), {freq} time(s) a day.")
                    else:
                        st.success(f"**Rentang Dosis Total 24 Jam:** {min_daily_total:.1f} - {max_daily_total:.1f} mg/hari")
                        st.success(f"**Rentang Target Per Dosis:** {min_per_dose:.1f} - {max_per_dose:.1f} mg/dosis")
                        
                        if drug_info["type"] == "tab":
                            min_tabs, max_tabs = min_per_dose / drug_info["avail"], max_per_dose / drug_info["avail"]
                            st.warning(f"📝 **Resep:** Minum {min_tabs:.2f} - {max_tabs:.2f} tablet, {freq} kali sehari.")
                        else:
                            min_vol, max_vol = min_per_dose / drug_info["avail"], max_per_dose / drug_info["avail"]
                            min_s, max_s = min_vol / 5.0, max_vol / 5.0
                            st.warning(f"📝 **Resep:** Minum {min_vol:.1f} - {max_vol:.1f} mL ({min_s:.1f} - {max_s:.1f} sendok takar 5mL), {freq} kali sehari.")
            else:
                st.warning("Drug not found." if st.session_state.lang == "English" else "Obat tidak ditemukan.")
                
        except ValueError:
             st.error("⚠️ Column mismatch in Excel.")
    else:
        st.error(f"⚠️ Could not find '{file_path}'.")

# --- 3. MANUAL CALCULATOR ---
elif menu == "🧮 Manual Calculator / Manual":
    st.header("Manual Calculator" if st.session_state.lang == "English" else "Kalkulator Dosis Manual")
    
    w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan Pasien (kg)"
    d_label = "Dose per kg (mg/kg)" if st.session_state.lang == "English" else "Dosis per kg (mg/kg)"
    weight = st.number_input(w_label, min_value=0.0, step=0.1)
    dose_per_kg = st.number_input(d_label, min_value=0.0, step=0.1)
    
    form_label = "Formulation" if st.session_state.lang == "English" else "Sediaan"
    calc_type = st.radio(form_label, ["Tablet", "Syrup" if st.session_state.lang == "English" else "Sirup"])
    
    calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
    
    if calc_type == "Tablet":
        avail_label = "Available Tablet Dosage (mg/tablet)" if st.session_state.lang == "English" else "Dosis Tablet Tersedia (mg/tablet)"
        avail_dose = st.number_input(avail_label, min_value=0.0, step=10.0)
        
        if st.button(calc_txt) and avail_dose > 0:
            total_dose = weight * dose_per_kg
            tabs = total_dose / avail_dose
            
            if st.session_state.lang == "English":
                st.success(f"**Target Dose:** {total_dose:.1f} mg")
                st.info(f"**Instruction:** Give {tabs:.2f} tablet(s) per dose.")
            else:
                st.success(f"**Dosis Target:** {total_dose:.1f} mg")
                st.info(f"**Instruksi:** Berikan {tabs:.2f} tablet per dosis.")
            
    else:
        syr_label = "Syrup Concentration (mg per 5 mL)" if st.session_state.lang == "English" else "Konsentrasi Sirup (mg per 5 mL)"
        mg_per_5ml = st.number_input(syr_label, min_value=0.0, step=1.0)
        
        if st.button(calc_txt) and mg_per_5ml > 0:
            total_dose = weight * dose_per_kg
            volume_ml = total_dose / (mg_per_5ml / 5.0)
            spoons = volume_ml / 5.0
            
            if st.session_state.lang == "English":
                st.success(f"**Target Dose:** {total_dose:.1f} mg")
                st.info(f"**Instruction:** Give {volume_ml:.1f} mL ({spoons:.2f} measuring spoon(s) of 5mL) per dose.")
            else:
                st.success(f"**Dosis Target:** {total_dose:.1f} mg")
                st.info(f"**Instruksi:** Berikan {volume_ml:.1f} mL ({spoons:.2f} sendok takar 5mL) per dosis.")

# --- 6.5 INJECTION DRUGS ---
elif menu == "💉 Injection Drugs / Obat Injeksi":
    st.header("Injection Drugs" if st.session_state.lang == "English" else "Kalkulator Obat Injeksi Darurat")
    
    if os.path.exists(file_path):
        try:
            df_inject = pd.read_excel(file_path, sheet_name="Injections")
            
            inj_db = {}
            for index, row in df_inject.iterrows():
                inj_db[row["Drug Name"]] = {
                    "dose_per_kg": float(row["Standard Dose (mg/kg)"]),
                    "max_dose": float(row["Max Dose (mg)"]),
                    "concentration": float(row["Concentration (mg/mL)"]),
                    "info": str(row["Clinical Info"]) if "Clinical Info" in df_inject.columns and not pd.isna(row["Clinical Info"]) else ""
                }
            
            # --- NEW SEARCH FEATURE ---
            search_label_inj = "🔍 Search Injection:" if st.session_state.lang == "English" else "🔍 Cari Obat Injeksi:"
            search_query_inj = st.text_input(search_label_inj, key="search_inj")
            
            # Filter the list based on search
            filtered_injs = [inj for inj in inj_db.keys() if search_query_inj.lower() in inj.lower()]
            
            if filtered_injs:
                sel_label = "Select Injection Drug" if st.session_state.lang == "English" else "Pilih Obat Injeksi"
                selected_inj = st.selectbox(sel_label, filtered_injs)
                
                if inj_db[selected_inj]["info"]:
                    st.info(inj_db[selected_inj]["info"])
                
                w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan Pasien (kg)"
                weight = st.number_input(w_label, min_value=0.0, step=0.1, key="inj_w")
                
                calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
                
                if st.button(calc_txt) and weight > 0:
                    drug_info = inj_db[selected_inj]
                    
                    target_dose = weight * drug_info["dose_per_kg"]
                    
                    is_maxed = False
                    if drug_info["max_dose"] > 0 and target_dose > drug_info["max_dose"]:
                        target_dose = drug_info["max_dose"]
                        is_maxed = True
                        
                    vol_ml = target_dose / drug_info["concentration"]
                    
                    if st.session_state.lang == "English":
                        st.write(f"**Dose Standard:** {drug_info['dose_per_kg']} mg/kg")
                        
                        if is_maxed:
                            st.warning(f"⚠️ **Target Dose capped at Max Single Dose:** {target_dose:.1f} mg")
                        else:
                            st.success(f"**Target Dose:** {target_dose:.1f} mg")
                            
                        st.error(f"💉 **Draw into syringe (Volume):** {vol_ml:.2f} mL")
                    else:
                        st.write(f"**Standar Dosis:** {drug_info['dose_per_kg']} mg/kg")
                        
                        if is_maxed:
                            st.warning(f"⚠️ **Target Dosis dibatasi pada Dosis Maksimal:** {target_dose:.1f} mg")
                        else:
                            st.success(f"**Target Dosis:** {target_dose:.1f} mg")
                            
                        st.error(f"💉 **Tarik ke dalam spuit (Volume):** {vol_ml:.2f} mL")
            else:
                st.warning("Drug not found." if st.session_state.lang == "English" else "Obat Injeksi tidak ditemukan.")
                    
        except ValueError:
            st.error("⚠️ Sheet 'Injections' not found in Excel, or column names do not match. Please check your Excel file.")
        except Exception as e:
            st.error(f"⚠️ Error reading Excel: {e}")
    else:
        st.error(f"⚠️ Could not find '{file_path}'.")

# --- 3. IV FLUID & ELECTROLYTES ---
elif menu == "💧 IV Fluid / Cairan Infus":
    st.header("IV Fluid & Electrolytes" if st.session_state.lang == "English" else "Terapi Cairan & Elektrolit")
    
    tab_titles = ["💧 Maintenance", "🏜️ Dehydration", "⚖️ Ion Correction", "🧪 Fluid Types"]
    tab1, tab2, tab3, tab4 = st.tabs(tab_titles)
    
    # ==========================================
    # TAB 1: MAINTENANCE FLUID
    # ==========================================
    with tab1:
        st.subheader("Maintenance Fluid" if st.session_state.lang == "English" else "Cairan Rumatan (Maintenance)")
        
        # Display Formulas
        st.info("**Formula (Holliday-Segar):**\n\n"
                "• 0 - 10 kg = 100 mL/kg\n\n"
                "• 11 - 20 kg = 1000 mL + (50 mL x every kg > 10)\n\n"
                "• > 20 kg = 1500 mL + (20 mL x every kg > 20)\n\n"
                "*Drops: Macro = 20 drops/mL | Micro = 60 drops/mL*")
        
        w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan Pasien (kg)"
        weight_m = st.number_input(w_label, min_value=0.0, step=0.1, key="maint_w")
        
        if weight_m > 0:
            if weight_m <= 10:
                maint_vol = weight_m * 100
            elif weight_m <= 20:
                maint_vol = 1000 + ((weight_m - 10) * 50)
            else:
                maint_vol = 1500 + ((weight_m - 20) * 20)
                
            drops_macro = (maint_vol * 20) / (24 * 60)
            drops_micro = (maint_vol * 60) / (24 * 60)
            
            if st.session_state.lang == "English":
                st.success(f"**Total 24h Maintenance:** {maint_vol:.0f} mL")
                st.write(f"💧 **Macro Drip (20 drops/mL):** {drops_macro:.0f} drops per minute (tpm)")
                st.write(f"💧 **Micro Drip (60 drops/mL):** {drops_micro:.0f} drops per minute (tpm)")
                st.caption("⚖️ **Disclaimer:** This is baseline maintenance. Adjust volumes based on fever, tachypnea, or ongoing fluid losses.")
            else:
                st.success(f"**Total Rumatan 24 Jam:** {maint_vol:.0f} mL")
                st.write(f"💧 **Makro (20 tetes/mL):** {drops_macro:.0f} tetes per menit (tpm)")
                st.write(f"💧 **Mikro (60 tetes/mL):** {drops_micro:.0f} tetes per menit (tpm)")
                st.caption("⚖️ **Penafian:** Ini adalah rumatan dasar. Sesuaikan volume jika ada demam, takipnea, atau kehilangan cairan berkelanjutan.")

    # ==========================================
    # TAB 2: DEHYDRATION FLUID
    # ==========================================
    with tab2:
        st.subheader("Dehydration Deficit" if st.session_state.lang == "English" else "Defisit Cairan Dehidrasi")
        
        # Pediatric Diarrhea Warning
        if st.session_state.lang == "English":
            st.error("⚠️ **Pediatric Warning:** For children with dehydration due to diarrhea/gastroenteritis, please use the dedicated **👶 Peds Dehydration (MTBS)** tab.")
        else:
            st.error("⚠️ **Peringatan Pediatri:** Untuk anak dengan dehidrasi akibat diare/gastroenteritis, harap gunakan tab khusus **👶 Dehidrasi Anak (MTBS)**.")
        
        # Display Formulas
        st.info("**Formulas:**\n\n"
                "• Deficit Volume = Weight x Dehydration % x 1000\n\n"
                "• First 8 Hours = 50% Deficit + 33% Daily Maintenance\n\n"
                "• Next 16 Hours = 50% Deficit + 67% Daily Maintenance")
        
        col1, col2 = st.columns(2)
        with col1:
            weight_d = st.number_input(w_label, min_value=0.0, step=0.1, key="dehyd_w")
        with col2:
            deg_label = "Dehydration Level" if st.session_state.lang == "English" else "Tingkat Dehidrasi"
            deg_options = ["Mild (5%) / Ringan", "Moderate (10%) / Sedang"]
            deg = st.selectbox(deg_label, deg_options)
            
        if weight_d > 0:
            pct = 0.05 if "5%" in deg else 0.10
            deficit_vol = weight_d * pct * 1000
            
            if weight_d <= 10:
                maint = weight_d * 100
            elif weight_d <= 20:
                maint = 1000 + ((weight_d - 10) * 50)
            else:
                maint = 1500 + ((weight_d - 20) * 20)
                
            total_fluid = deficit_vol + maint
            
            if st.session_state.lang == "English":
                st.warning(f"**Fluid Deficit:** {deficit_vol:.0f} mL")
                st.success(f"**Total 24h Requirement (Deficit + Maintenance):** {total_fluid:.0f} mL")
                st.markdown("---")
                st.write("**Recommended Delivery (Standard Protocol):**")
                st.write(f"⏱️ **First 8 Hours:** {(deficit_vol/2) + (maint/3):.0f} mL (Use RL or NS)")
                st.write(f"⏱️ **Next 16 Hours:** {(deficit_vol/2) + (maint*(2/3)):.0f} mL")
                st.caption("⚖️ **Disclaimer:** Always evaluate the patient clinically. Stop or slow infusion if signs of fluid overload (e.g., crackles, edema) occur.")
            else:
                st.warning(f"**Defisit Cairan:** {deficit_vol:.0f} mL")
                st.success(f"**Total Kebutuhan 24 Jam (Defisit + Rumatan):** {total_fluid:.0f} mL")
                st.markdown("---")
                st.write("**Rekomendasi Pemberian (Protokol Standar):**")
                st.write(f"⏱️ **8 Jam Pertama:** {(deficit_vol/2) + (maint/3):.0f} mL (Gunakan RL atau NS)")
                st.write(f"⏱️ **16 Jam Berikutnya:** {(deficit_vol/2) + (maint*(2/3)):.0f} mL")
                st.caption("⚖️ **Penafian:** Selalu evaluasi klinis pasien. Hentikan atau perlambat infus jika muncul tanda kelebihan cairan (misal: ronkhi, edema).")

    # ==========================================
    # TAB 3: ION CORRECTION (Na & K)
    # ==========================================
    with tab3:
        st.subheader("Electrolyte Correction" if st.session_state.lang == "English" else "Koreksi Elektrolit")
        
        ion_choice = st.radio("Select Ion / Pilih Ion:", ["Sodium (Na+) / Natrium", "Potassium (K+) / Kalium"], horizontal=True)
        
        # Display formulas based on choice
        if "Na" in ion_choice:
            st.info("**Na+ Formulas:**\n\n"
                    "• Na Deficit (mEq) = (Target - Actual) x TBW x Weight\n\n"
                    "• 3% NaCl Volume (mL) = (Na Deficit / 513) x 1000\n\n"
                    "*(TBW Multipliers: Male/Child = 0.6, Female/Elderly Male = 0.5, Elderly Female = 0.45)*")
        else:
            st.info("**K+ Formula:**\n\n"
                    "• K Deficit (mEq) = (Target - Actual) x Weight x 0.3")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            weight_i = st.number_input(w_label, min_value=0.0, step=0.1, key="ion_w")
        with col2:
            act_label = "Actual Lab Result" if st.session_state.lang == "English" else "Hasil Lab Aktual"
            actual_val = st.number_input(act_label, value=125.0 if "Na" in ion_choice else 3.0, step=0.1)
        with col3:
            tar_label = "Target Level" if st.session_state.lang == "English" else "Target"
            target_val = st.number_input(tar_label, value=135.0 if "Na" in ion_choice else 4.0, step=0.1)
            
        if "Na" in ion_choice:
            tbw_label = "Patient Type (for TBW)" if st.session_state.lang == "English" else "Tipe Pasien (untuk TBW)"
            tbw_type = st.selectbox(tbw_label, ["Male/Child (0.6)", "Female/Elderly Male (0.5)", "Elderly Female (0.45)"])
            tbw_mult = float(tbw_type.split("(")[1].replace(")", ""))
            
            if st.button("Calculate Na+" if st.session_state.lang == "English" else "Hitung Na+") and weight_i > 0:
                na_deficit = (target_val - actual_val) * tbw_mult * weight_i
                vol_3pct = (na_deficit / 513) * 1000
                
                st.error(f"**Total Na+ Deficit:** {na_deficit:.1f} mEq")
                st.warning(f"💉 **Correction with 3% NaCl:** Give {vol_3pct:.1f} mL")
                
                if st.session_state.lang == "English":
                    st.caption("⚠️ **Safety Warning:** Do not correct Na+ faster than 8-10 mEq/L per 24 hours. Rapid correction can cause severe osmotic demyelination syndrome.")
                else:
                    st.caption("⚠️ **Peringatan Keamanan:** Jangan koreksi Na+ lebih cepat dari 8-10 mEq/L per 24 jam. Koreksi terlalu cepat dapat menyebabkan sindrom demielinasi osmotik.")
                
        else: # Potassium
            if st.button("Calculate K+" if st.session_state.lang == "English" else "Hitung K+") and weight_i > 0:
                k_deficit = (target_val - actual_val) * weight_i * 0.3
                
                st.error(f"**Total K+ Deficit:** {k_deficit:.1f} mEq")
                st.warning(f"💉 **Correction:** Give {k_deficit:.1f} mEq of KCl IV")
                
                if st.session_state.lang == "English":
                    st.caption("⚠️ **Safety Warning:** Infusion rate must not exceed 10 mEq/hour via peripheral IV (Adults) or 0.5-1 mEq/kg/hour (Pediatrics) to avoid life-threatening cardiac arrhythmias. Must be diluted.")
                else:
                    st.caption("⚠️ **Peringatan Keamanan:** Kecepatan infus tidak boleh melebihi 10 mEq/jam via IV perifer (Dewasa) atau 0.5-1 mEq/kg/jam (Anak) untuk menghindari aritmia mematikan. Harus diencerkan.")

# ==========================================
    # TAB 4: FLUID TYPES & RECOMMENDATIONS
    # ==========================================
    with tab4:
        st.subheader("Fluid Composition & Guidelines" if st.session_state.lang == "English" else "Komposisi Cairan & Panduan")
        
        fluid_dict = {
            "Fluid / Cairan": ["RL (Ringer Lactate)", "NS (0.9% NaCl)", "D5% 1/2 NS", "D5% 1/4 NS", "KA-EN 3B", "3% NaCl", "KCl 7.46% (Additive/Ampule)"],
            # Using strings below so we can add the specific 'mEq/mL' text for KCl
            "Na+ (mEq/L)": ["130", "154", "77", "38.5", "50", "513", "0"],
            "K+ (mEq/L)": ["4", "0", "0", "0", "20", "0", "1 mEq / mL"],
            "Best For / Indikasi Utama": [
                "Resuscitation, Dehydration, Surgery, Dengue",
                "Resuscitation, Shock, Hyponatremia",
                "Maintenance fluid (Adults/Older Kids)",
                "Maintenance fluid (Infants/Neonates)",
                "Maintenance with K+ deficit (Hypokalemia)",
                "Severe symptomatic hyponatremia ONLY",
                "Hypokalemia correction. ⚠️ MUST BE DILUTED before IV."
            ]
        }
        df_fluids = pd.DataFrame(fluid_dict)
        st.dataframe(df_fluids, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        if st.session_state.lang == "English":
            st.write("### 💡 Quick Clinical Recommendations:")
            st.write("- **Severe Dehydration/Shock:** Push isotonic fluids (RL or NS) as fast as possible.")
            st.write("- **Dengue Fever:** RL is preferred as it limits hyperchloremic acidosis compared to NS.")
            st.write("- **Maintenance:** Avoid using pure RL/NS for multi-day maintenance as they lack glucose and adequate potassium. Switch to D5% 1/2 NS or KA-EN 3B.")
            st.write("- **KCl Additive:** Never give KCl as an IV push. Always dilute in maintenance fluid and run slowly.")
            st.caption("⚖️ **Disclaimer:** Fluid selection should be tailored to individual patient lab results and clinical status.")
        else:
            st.write("### 💡 Rekomendasi Klinis Cepat:")
            st.write("- **Dehidrasi Berat/Syok:** Berikan cairan isotonik (RL atau NS) secepat mungkin.")
            st.write("- **Demam Berdarah (DHF):** RL lebih disukai karena mencegah asidosis hiperkloremik dibandingkan NS.")
            st.write("- **Rumatan (Maintenance):** Hindari RL/NS murni untuk rumatan berhari-hari karena tidak mengandung glukosa dan kalium yang cukup. Gunakan D5% 1/2 NS atau KA-EN 3B.")
            st.write("- **Aditif KCl:** Jangan pernah memberikan KCl secara bolus/push IV. Selalu encerkan dalam cairan infus dan berikan perlahan.")
            st.caption("⚖️ **Penafian:** Pemilihan cairan harus disesuaikan dengan hasil lab individu dan status klinis pasien.")
# --- 5. PEDIATRIC DEHYDRATION (NEW) ---
elif menu == "👶 Peds Dehydration / Dehidrasi Anak":
    st.header("Pediatric Dehydration (WHO)" if st.session_state.lang == "English" else "Kalkulator Dehidrasi Anak (MTBS / WHO)")
    
    w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan Pasien (kg)"
    weight = st.number_input(w_label, min_value=0.0, step=0.1, key="dehyd_w")
    
    age_label = "Age Category" if st.session_state.lang == "English" else "Kategori Umur"
    age_cat = st.radio(age_label, 
                       ["< 12 Months" if st.session_state.lang == "English" else "< 12 Bulan", 
                        "1 - 5 Years" if st.session_state.lang == "English" else "1 - 5 Tahun", 
                        "> 5 Years" if st.session_state.lang == "English" else "> 5 Tahun"])
    
    sev_label = "Dehydration Severity" if st.session_state.lang == "English" else "Tingkat Dehidrasi"
    severity = st.radio(sev_label, 
                        ["Mild-Moderate (Plan B)" if st.session_state.lang == "English" else "Ringan-Sedang (Rencana B - Oralit)", 
                         "Severe (Plan C)" if st.session_state.lang == "English" else "Berat (Rencana C - Infus RL/NaCl)"])
    
    calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
    
    if st.button(calc_txt) and weight > 0:
        if "Plan B" in severity or "Rencana B" in severity:
            # Plan B: 75 ml / kg over 4 hours
            vol = 75 * weight
            if st.session_state.lang == "English":
                st.success(f"**Total ORS Volume:** {vol:.1f} mL")
                st.info("**Instruction:** Give this volume of Oral Rehydration Solution (ORS) slowly over 4 hours.")
            else:
                st.success(f"**Total Volume Oralit:** {vol:.1f} mL")
                st.info("**Instruksi:** Berikan volume Oralit ini secara perlahan selama 4 jam pertama.")
        else:
            # Plan C: 100 ml / kg IV
            total_vol = 100 * weight
            vol_1 = 30 * weight
            vol_2 = 70 * weight
            
            if "< 12" in age_cat:
                time_1 = "1 hour" if st.session_state.lang == "English" else "1 jam"
                time_2 = "5 hours" if st.session_state.lang == "English" else "5 jam"
            else:
                time_1 = "30 minutes" if st.session_state.lang == "English" else "30 menit"
                time_2 = "2.5 hours" if st.session_state.lang == "English" else "2,5 jam"
            
            if st.session_state.lang == "English":
                st.success(f"**Total IV Fluid Volume (RL/NaCl 0.9%):** {total_vol:.1f} mL")
                st.warning(f"**Step 1:** Give {vol_1:.1f} mL fast over {time_1}.")
                st.info(f"**Step 2:** Then give the remaining {vol_2:.1f} mL over {time_2}.")
                st.error("⚠️ *Reassess continuously. If radial pulse is still weak after Step 1, repeat Step 1.*")
            else:
                st.success(f"**Total Cairan Infus (RL/NaCl 0.9%):** {total_vol:.1f} mL")
                st.warning(f"**Langkah 1:** Berikan {vol_1:.1f} mL secara cepat dalam {time_1}.")
                st.info(f"**Langkah 2:** Kemudian berikan sisanya {vol_2:.1f} mL dalam {time_2}.")
                st.error("⚠️ *Evaluasi terus menerus. Jika nadi radialis masih lemah/tidak teraba setelah Langkah 1, ulangi Langkah 1.*")

# --- 6. BMI & BSA CALCULATOR ---
# --- 5. BMI & BSA / ANTROPOMETRI ---
elif menu == "⚖️ BMI & BSA / Antropometri":
    st.header("Anthropometry & Z-Scores" if st.session_state.lang == "English" else "Antropometri & Z-Score (WHO/CDC)")
    
    tab1, tab2 = st.tabs(["🧍 Adult (BMI & BSA)", "👶 Pediatric Z-Scores (LMS)"])
    
    # ==========================================
    # TAB 1: ADULT BMI & BSA
    # ==========================================
    with tab1:
        st.subheader("Adult BMI & BSA" if st.session_state.lang == "English" else "BMI & BSA Dewasa")
        
        col1, col2 = st.columns(2)
        with col1:
            w_label = "Weight (kg)" if st.session_state.lang == "English" else "Berat Badan (kg)"
            weight = st.number_input(w_label, min_value=0.0, step=0.1, key="bmi_w")
        with col2:
            h_label = "Height (cm)" if st.session_state.lang == "English" else "Tinggi Badan (cm)"
            height_cm = st.number_input(h_label, min_value=0.0, step=0.1, key="bmi_h")
            
        calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
        
        if st.button(calc_txt, key="calc_adult") and weight > 0 and height_cm > 0:
            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)
            bsa = math.sqrt((weight * height_cm) / 3600)
            
            if st.session_state.lang == "English":
                st.success(f"**BMI:** {bmi:.1f} kg/m²")
                if bmi < 18.5: st.warning("Classification: Underweight")
                elif bmi < 24.9: st.info("Classification: Normal weight")
                elif bmi < 29.9: st.warning("Classification: Overweight")
                else: st.error("Classification: Obese")
                st.success(f"**Body Surface Area (BSA):** {bsa:.2f} m²")
            else:
                st.success(f"**Indeks Massa Tubuh (BMI):** {bmi:.1f} kg/m²")
                if bmi < 18.5: st.warning("Klasifikasi: Underweight (Kurang)")
                elif bmi < 24.9: st.info("Klasifikasi: Normal")
                elif bmi < 29.9: st.warning("Klasifikasi: Overweight (Berlebih)")
                else: st.error("Klasifikasi: Obesitas")
                st.success(f"**Luas Permukaan Tubuh (BSA):** {bsa:.2f} m²")

    # ==========================================
    # TAB 2: PEDIATRIC Z-SCORES (WHO/CDC LMS)
    # ==========================================
    with tab2:
        st.subheader("Pediatric True Z-Scores" if st.session_state.lang == "English" else "Z-Score Pediatri Akurat (LMS)")
        
        st.info("⚠️ **Clinical Note:** This tool requires the official WHO/CDC `.xlsx` LMS data files to be present in your GitHub repository." if st.session_state.lang == "English" else "⚠️ **Catatan Klinis:** Alat ini membutuhkan file data LMS `.xlsx` resmi WHO/CDC di repositori GitHub Anda.")
        
        col1, col2 = st.columns(2)
        with col1:
            sex_label = "Sex" if st.session_state.lang == "English" else "Jenis Kelamin"
            sex = st.radio(sex_label, ["Boy / Laki-laki", "Girl / Perempuan"], horizontal=True)
            
            age_y_label = "Age (Years)" if st.session_state.lang == "English" else "Usia (Tahun)"
            age_y = st.number_input(age_y_label, min_value=0, max_value=20, step=1, value=2)
            
            age_m_label = "Age (Months)" if st.session_state.lang == "English" else "Usia (Bulan)"
            age_m = st.number_input(age_m_label, min_value=0, max_value=11, step=1, value=0)
            
        with col2:
            weight_p = st.number_input(w_label, min_value=0.0, step=0.1, key="ped_w")
            height_p = st.number_input(h_label, min_value=0.0, step=0.1, key="ped_h")
            
        total_months = (age_y * 12) + age_m
        
        if st.button(calc_txt, key="calc_ped") and weight_p > 0 and height_p > 0:
            st.markdown("---")
            
            # Helper function for LMS math
            def calculate_z(x, l, m, s):
                if l == 0:
                    return math.log(x / m) / s
                return (((x / m) ** l) - 1) / (l * s)

            try:
                is_boy = "Boy" in sex
                total_months = (age_y * 12) + age_m
                
                # Convert age to total days for the WHO 'Day' column
                # (365.25 days/year to account for leap years, 30.4375 days/month)
                target_days = (age_y * 365.25) + (age_m * 30.4375)
                
                if total_months <= 60:
                    if st.session_state.lang == "English":
                        st.write(f"📊 **Using WHO Standards (Target: ~{int(target_days)} Days)**")
                    else:
                        st.write(f"📊 **Menggunakan Standar WHO (Target: ~{int(target_days)} Hari)**")
                        
                    wfa_file = "who_wfa_boys.xlsx" if is_boy else "who_wfa_girls.xlsx"
                    hfa_file = "who_lfa_boys.xlsx" if is_boy else "who_lfa_girls.xlsx"
                    
                    # Read Weight-for-Age and find closest 'Day'
                    df_wfa = pd.read_excel(wfa_file)
                    row_w = df_wfa.iloc[(df_wfa['Day'] - target_days).abs().argsort()[:1]].iloc[0]
                    z_weight = calculate_z(weight_p, row_w['L'], row_w['M'], row_w['S'])
                    
                    # Read Height-for-Age and find closest 'Day'
                    df_hfa = pd.read_excel(hfa_file)
                    row_h = df_hfa.iloc[(df_hfa['Day'] - target_days).abs().argsort()[:1]].iloc[0]
                    z_height = calculate_z(height_p, row_h['L'], row_h['M'], row_h['S'])
                    
                else:
                    if st.session_state.lang == "English":
                        st.write(f"📊 **Using CDC Charts (Target: {total_months} Months)**")
                    else:
                        st.write(f"📊 **Menggunakan Standar CDC (Target: {total_months} Bulan)**")
                        
                    cdc_sex_code = 1 if is_boy else 2
                    
                    # Read Weight-for-Age and find closest 'Agemos'
                    df_cdc_w = pd.read_excel("cdc_wfa.xlsx")
                    df_filtered_w = df_cdc_w[(df_cdc_w['Sex'] == cdc_sex_code)]
                    closest_row_w = df_filtered_w.iloc[(df_filtered_w['Agemos'] - total_months).abs().argsort()[:1]].iloc[0]
                    z_weight = calculate_z(weight_p, closest_row_w['L'], closest_row_w['M'], closest_row_w['S'])
                    
                    # Read Height-for-Age and find closest 'Agemos'
                    df_cdc_h = pd.read_excel("cdc_hfa.xlsx")
                    df_filtered_h = df_cdc_h[(df_cdc_h['Sex'] == cdc_sex_code)]
                    closest_row_h = df_filtered_h.iloc[(df_filtered_h['Agemos'] - total_months).abs().argsort()[:1]].iloc[0]
                    z_height = calculate_z(height_p, closest_row_h['L'], closest_row_h['M'], closest_row_h['S'])

                # Display Results
                st.success(f"⚖️ **Weight-for-Age Z-Score (BB/U):** {z_weight:.2f} SD")
                if z_weight < -3: st.error("Status: Severely Underweight (Gizi Buruk)")
                elif z_weight < -2: st.warning("Status: Underweight (Gizi Kurang)")
                elif z_weight > 2: st.warning("Status: Possible Overweight (Risiko BB Lebih)")
                else: st.info("Status: Normal Weight")
                
                st.success(f"📏 **Height-for-Age Z-Score (TB/U):** {z_height:.2f} SD")
                if z_height < -3: st.error("Status: Severely Stunted (Sangat Pendek)")
                elif z_height < -2: st.warning("Status: Stunted (Pendek)")
                elif z_height > 3: st.warning("Status: Very Tall (Sangat Tinggi)")
                else: st.info("Status: Normal Height")

            except FileNotFoundError as e:
                st.error(f"⚠️ **Missing File:** Could not find `{e.filename}`. Make sure it is uploaded to GitHub and named correctly.")
            except KeyError as e:
                st.error(f"⚠️ **Column Error:** Could not find column {e}. Check if your CDC file uses 'Agemos' and WHO uses 'Day'.")
            except Exception as e:
                st.error(f"⚠️ **Error calculating Z-score:** {e}")
                
# --- 6.7 OBSTETRIC CALC ---
elif menu == "🤰 Obstetric Calc / Kandungan":
    st.header("Obstetric Calculator" if st.session_state.lang == "English" else "Kalkulator Kehamilan (HPL & UK)")
    
    st.info("Calculate Gestational Age and Estimated Date of Delivery (EDD) based on the First Day of Last Menstrual Period (LMP)." if st.session_state.lang == "English" else "Hitung Usia Kehamilan (UK) dan Hari Perkiraan Lahir (HPL) berdasarkan Hari Pertama Haid Terakhir (HPHT).")
    
    st.divider()
    
    lmp_label = "Select LMP / Pilih HPHT:"
    
    today = datetime.date.today()
    default_lmp = today - datetime.timedelta(days=70) # Defaults to ~10 weeks pregnant for convenience
    
    lmp_date = st.date_input(lmp_label, value=default_lmp, max_value=today)
    
    calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
    
    if st.button(calc_txt):
        # Naegele's Rule: EDD = LMP + 280 days
        edd = lmp_date + datetime.timedelta(days=280)
        
        # Calculate Gestational Age
        days_pregnant = (today - lmp_date).days
        weeks = days_pregnant // 7
        days = days_pregnant % 7
        
        edd_str = edd.strftime("%d %B %Y")
        
        if st.session_state.lang == "English":
            st.success(f"👶 **Estimated Date of Delivery (EDD):** {edd_str}")
            
            if days_pregnant > 294: # 42 weeks
                st.warning(f"📅 **Current Gestational Age:** {weeks} weeks, {days} days *(Post-term)*")
            else:
                st.info(f"📅 **Current Gestational Age:** {weeks} weeks, {days} days")
        else:
            st.success(f"👶 **Hari Perkiraan Lahir (HPL):** {edd_str}")
            
            if days_pregnant > 294: # 42 minggu
                st.warning(f"📅 **Usia Kehamilan Saat Ini:** {weeks} minggu, {days} hari *(Post-term / Serotinus)*")
            else:
                st.info(f"📅 **Usia Kehamilan Saat Ini:** {weeks} minggu, {days} hari")

# --- 7. DRUG REFERENCES ---
elif menu == "📚 Drug References / Referensi":
    st.header("Drug References" if st.session_state.lang == "English" else "Referensi Obat & Dosis Standar")
    
    if os.path.exists(file_path):
        xls = pd.ExcelFile(file_path)
        sheet_names = [sheet for sheet in xls.sheet_names if sheet != "AutoCalc"]
        
        cat_label = "Select Drug Category" if st.session_state.lang == "English" else "Pilih Kategori Obat"
        category = st.selectbox(cat_label, sheet_names)
        
        if category:
            df = pd.read_excel(xls, sheet_name=category, header=1)
            df = df.fillna("") 
            
            search_label = f"🔍 Search within {category}:" if st.session_state.lang == "English" else f"🔍 Cari di dalam {category}:"
            search_query = st.text_input(search_label)
            
            if search_query:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
                df = df[mask]
            
            df = df.reset_index(drop=True)
            df.index = df.index + 1
            
            st.dataframe(df, use_container_width=False)
    else:
        st.error(f"⚠️ Could not find '{file_path}'. Please place the Excel file in the same folder.")

# --- GLOBAL FOOTER & DISCLAIMER (Visible on all pages) ---
st.divider()
if st.session_state.lang == "English":
    st.caption("**Medical Disclaimer:** This application is designed strictly as a supplementary clinical calculation tool for healthcare professionals. It does not replace professional clinical judgment. Always verify calculations, drug dosages, and contraindications with standard medical guidelines before prescribing treatment.")
   
else:
    st.caption("**Informasi:** Aplikasi ini dirancang sebagai alat bantu perhitungan klinis tambahan untuk tenaga medis profesional. Aplikasi ini tidak menggantikan penilaian klinis profesional. Selalu verifikasi perhitungan, dosis obat, dan kontraindikasi dengan panduan standar medis sebelum memberikan resep atau perawatan pada pasien.")
    