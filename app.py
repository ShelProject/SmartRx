import streamlit as st
import pandas as pd
import os
import math

st.set_page_config(page_title="SmartRx", layout="wide", initial_sidebar_state="expanded")

if 'lang' not in st.session_state:
    st.session_state.lang = "English"
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "🏠 Home / Beranda"

def switch_page(page_name):
    st.session_state.menu_selection = page_name

# --- SIDEBAR NAV ---
st.sidebar.title("Navigation / Navigasi")
menu_options = [
    "🏠 Home / Beranda",
    "💊 Auto-Calc / Kalkulator Otomatis", 
    "🧮 Manual Calculator / Manual", 
    "💧 IV Fluid / Cairan Infus",
    "👶 Peds Dehydration / Dehidrasi Anak", 
    "⚖️ BMI & BSA / Antropometri", 
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
    lang_choice = st.radio("", ["English", "Bahasa Indonesia"], index=0 if st.session_state.lang == "English" else 1, horizontal=True)
    st.session_state.lang = lang_choice
    
    st.divider()

    col1, col2 = st.columns(2)
    
    if st.session_state.lang == "English":
        with col1:
            st.info("⚡ **Common Drugs Auto-Calc**\n\nAutomatically calculate safe dosage ranges and exact prescription amounts.")
            st.button("Go to Auto-Calc", use_container_width=True, on_click=switch_page, args=("💊 Auto-Calc / Kalkulator Otomatis",))
                
            st.success("💧 **IV Fluid Calculator**\n\nCalculate maintenance fluids and exact nursing drip rates.")
            st.button("Go to IV Fluid", use_container_width=True, on_click=switch_page, args=("💧 IV Fluid / Cairan Infus",))
            
            st.warning("👶 **Pediatric Dehydration**\n\nCalculate WHO Plan B (ORS) and Plan C (IV Fluids) for children.")
            st.button("Go to Peds Dehydration", use_container_width=True, on_click=switch_page, args=("👶 Peds Dehydration / Dehidrasi Anak",))

        with col2:
            st.warning("🧮 **Manual Calculator**\n\nPerform manual mg/kg calculations for any custom drug or syrup.")
            st.button("Go to Manual Calculator", use_container_width=True, on_click=switch_page, args=("🧮 Manual Calculator / Manual",))
            
            st.primary("⚖️ **BMI & BSA Calculator**\n\nCalculate Body Mass Index and Body Surface Area.")
            st.button("Go to BMI & BSA", use_container_width=True, on_click=switch_page, args=("⚖️ BMI & BSA / Antropometri",))
                
            st.error("📚 **Drug References**\n\nSearch your digital database for dosages, indications, and clinical warnings.")
            st.button("Go to Drug References", use_container_width=True, on_click=switch_page, args=("📚 Drug References / Referensi",))
            
    else:
        with col1:
            st.info("⚡ **Kalkulator Otomatis Obat**\n\nHitung otomatis rentang dosis aman dan jumlah resep yang tepat.")
            st.button("Buka Kalkulator Otomatis", use_container_width=True, on_click=switch_page, args=("💊 Auto-Calc / Kalkulator Otomatis",))
                
            st.success("💧 **Kalkulator Cairan Infus**\n\nHitung cairan pemeliharaan dan kecepatan tetesan infus perawat.")
            st.button("Buka Kalkulator Infus", use_container_width=True, on_click=switch_page, args=("💧 IV Fluid / Cairan Infus",))
            
            st.warning("👶 **Dehidrasi Anak (MTBS)**\n\nHitung Rencana B (Oralit) dan Rencana C (Infus) berdasarkan panduan WHO.")
            st.button("Buka Kalkulator Dehidrasi", use_container_width=True, on_click=switch_page, args=("👶 Peds Dehydration / Dehidrasi Anak",))

        with col2:
            st.warning("🧮 **Kalkulator Manual**\n\nLakukan perhitungan mg/kg manual untuk sediaan obat atau sirup apa pun.")
            st.button("Buka Kalkulator Manual", use_container_width=True, on_click=switch_page, args=("🧮 Manual Calculator / Manual",))
            
            st.primary("⚖️ **Kalkulator BMI & BSA**\n\nHitung Indeks Massa Tubuh dan Luas Permukaan Tubuh.")
            st.button("Buka Kalkulator Antropometri", use_container_width=True, on_click=switch_page, args=("⚖️ BMI & BSA / Antropometri",))
                
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
            
            sel_label = "Select Drug" if st.session_state.lang == "English" else "Pilih Obat"
            selected_drug = st.selectbox(sel_label, list(drug_db.keys()))
            
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

# --- 4. IV FLUID ---
elif menu == "💧 IV Fluid / Cairan Infus":
    st.header("IV Hydration Calculator" if st.session_state.lang == "English" else "Kalkulator Cairan Infus")
    
    w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan Pasien (kg)"
    weight = st.number_input(w_label, min_value=0.0, step=0.1)
    
    df_label = "Select Drop Factor" if st.session_state.lang == "English" else "Pilih Faktor Tetes"
    if st.session_state.lang == "English":
        drop_factor = st.radio(df_label, [20, 60], format_func=lambda x: f"{x} gtt/mL (Macro)" if x==20 else f"{x} gtt/mL (Micro)")
    else:
        drop_factor = st.radio(df_label, [20, 60], format_func=lambda x: f"{x} tpm (Makro)" if x==20 else f"{x} tpm (Mikro)")
    
    calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
    
    if st.button(calc_txt) and weight > 0:
        if weight <= 10:
            vol = 100 * weight
        elif weight <= 20:
            vol = 1000 + 50 * (weight - 10)
        else:
            vol = 1500 + 20 * (weight - 20)
            
        drip_rate = (vol * drop_factor) / (24 * 60)
        
        if st.session_state.lang == "English":
            st.success(f"**Total 24h Volume Requirement:** {vol:.1f} mL")
            st.info(f"**Nursing Instruction:** Run IV fluid at {drip_rate:.0f} drops per minute.")
        else:
            st.success(f"**Kebutuhan Volume 24 Jam:** {vol:.1f} mL")
            st.info(f"**Instruksi Perawat:** Berikan cairan infus dengan kecepatan {drip_rate:.0f} tetes per menit (tpm).")

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
elif menu == "⚖️ BMI & BSA / Antropometri":
    st.header("BMI & BSA Calculator" if st.session_state.lang == "English" else "Kalkulator BMI & BSA (Antropometri)")
    
    col1, col2 = st.columns(2)
    with col1:
        w_label = "Patient Weight (kg)" if st.session_state.lang == "English" else "Berat Badan (kg)"
        weight = st.number_input(w_label, min_value=0.0, step=0.1)
    with col2:
        h_label = "Patient Height (cm)" if st.session_state.lang == "English" else "Tinggi Badan (cm)"
        height = st.number_input(h_label, min_value=0.0, step=1.0)
        
    calc_txt = "Calculate" if st.session_state.lang == "English" else "Hitung"
    
    if st.button(calc_txt) and weight > 0 and height > 0:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        if bmi < 18.5:
            cat_en, cat_id = "Underweight", "Kekurangan Berat Badan"
            color = "blue"
        elif 18.5 <= bmi <= 24.9:
            cat_en, cat_id = "Normal weight", "Berat Badan Normal"
            color = "green"
        elif 25.0 <= bmi <= 29.9:
            cat_en, cat_id = "Overweight", "Kelebihan Berat Badan"
            color = "orange"
        else:
            cat_en, cat_id = "Obesity", "Obesitas"
            color = "red"
            
        bsa = math.sqrt((weight * height) / 3600)
        
        if st.session_state.lang == "English":
            st.success(f"**Body Surface Area (BSA):** {bsa:.2f} m²")
            st.info(f"**Body Mass Index (BMI):** {bmi:.1f} kg/m²")
            st.markdown(f"**Category:** :{color}[{cat_en}]")
        else:
            st.success(f"**Luas Permukaan Tubuh (BSA):** {bsa:.2f} m²")
            st.info(f"**Indeks Massa Tubuh (BMI):** {bmi:.1f} kg/m²")
            st.markdown(f"**Kategori:** :{color}[{cat_id}]")

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