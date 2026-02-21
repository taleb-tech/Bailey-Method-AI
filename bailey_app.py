import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# إعدادات الصفحة
st.set_page_config(page_title="Bailey Method Expert System", layout="wide")

st.title("🏗️ نظام بايلي الخبير لتصميم خلطات الإسفلت")
st.write("بناءً على دراسة: Jebur & Abedali (2020) - جامعة المستنصرية")

# --- القائمة الجانبية لإدخال البيانات ---
st.sidebar.header("📥 بيانات المدخلات")
nmps = st.sidebar.selectbox("الحجم الاسمي الأقصى (NMPS) ملم", [19.0, 12.5, 9.5])
luw_coarse = st.sidebar.number_input("الوزن الحجمي السائب للركام الخشن (LUW)", value=1550)
cacuw_percent = st.sidebar.slider("نسبة CACUW المختارة (%)", 60, 105, 100)

st.sidebar.subheader("📊 نسب العبور من المناخل (بعد المزج)")
pass_hs = st.sidebar.number_input("% Passing HS", value=65.0)
pass_pcs = st.sidebar.number_input("% Passing PCS", value=42.0)
pass_scs = st.sidebar.number_input("% Passing SCS", value=18.0)
pass_tcs = st.sidebar.number_input("% Passing TCS", value=8.0)

# --- الحسابات المنطقية بناءً على التقرير ---
# حساب المناخل الضابطة [cite: 24-27]
pcs_val = nmps * 0.22
hs_val = nmps * 0.50
scs_val = pcs_val * 0.22
tcs_val = scs_val * 0.22

# حساب نسب بايلي [cite: 31-33]
ca_ratio = (pass_hs - pass_pcs) / (100 - pass_hs)
fac_ratio = pass_scs / pass_pcs
faf_ratio = pass_tcs / pass_scs

# --- عرض النتائج ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📌 المناخل الضابطة المحسوبة")
    st.write(f"**PCS:** {pcs_val:.2f} mm")
    st.write(f"**HS:** {hs_val:.2f} mm")
    st.write(f"**SCS:** {scs_val:.2f} mm")
    st.write(f"**TCS:** {tcs_val:.2f} mm")

with col2:
    st.subheader("🧪 نتائج نسب بايلي")
    
    # دالة لعرض الحالة بلون معين
    def check_limit(val, min_v, max_v):
        if min_v <= val <= max_v:
            return f"✅ {val:.3f} (مقبول)"
        else:
            return f"❌ {val:.3f} (خارج الحدود)"

    st.write(f"**CA Ratio (0.50-0.65):** {check_limit(ca_ratio, 0.50, 0.65)}")
    st.write(f"**FAc Ratio (0.35-0.50):** {check_limit(fac_ratio, 0.35, 0.50)}")
    st.write(f"**FAf Ratio (0.35-0.50):** {check_limit(faf_ratio, 0.35, 0.50)}")

st.divider()

# --- تحليل الذكاء الاصطناعي والتوصيات ---
st.subheader("🤖 تحليل النظام الخبير وتوصيات الدراسة")

if cacuw_percent == 100:
    st.success("توصية الدراسة: استخدام CACUW = 100% يوفر أفضل تعبئة وأقل VMA.")
elif cacuw_percent < 90:
    st.info("هذه خلطة ناعمة (Fine-Graded)، قد يكون محتوى الإسفلت فيها مرتفعاً[cite: 145].")
elif cacuw_percent > 95:
    st.warning("هذه خلطة خشنة (Coarse-Graded)، توفر مقاومة عالية للتخدد[cite: 142].")

# رسائل تحذيرية بناءً على النسب 
if ca_ratio > 0.65:
    st.error("⚠️ تحذير: نسبة CA عالية جداً، الخلطة قد تتحرك تحت أسطوانة الدحل وصعبة الدمك.")
if faf_ratio > 0.50:
    st.error("⚠️ تحذير: نسبة الغبار مرتفعة جداً، مما قد يضعف متانة الخلطة.")

# --- رسم بياني بسيط ---
st.subheader("📈 تصور منحنى التدرج (النقاط الضابطة)")
fig, ax = plt.subplots()
sieves = [nmps, hs_val, pcs_val, scs_val, tcs_val]
passing = [100, pass_hs, pass_pcs, pass_scs, pass_tcs]
ax.plot(sieves, passing, marker='o', linestyle='-', color='b')
ax.set_xscale('log')
ax.set_xlabel("Sieve Size (mm) - Log Scale")
ax.set_ylabel("Percent Passing (%)")
ax.grid(True, which="both", ls="-")
st.pyplot(fig)
