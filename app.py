import streamlit as st

st.set_page_config(page_title="PeerHub Prototype", page_icon="🚀", layout="centered")

st.title("🚀 PeerHub — Interactive Skill Exchange")
st.subheader("منصة التبادل التفاعلي للمهارات والتعلم التشاركي")

st.markdown("---")

st.sidebar.header("📝 بيانات المستخدم الجديد")
user_name = st.sidebar.text_input("اسمك الكريم", "فريال")
teach_skill = st.sidebar.selectbox("ماذا يمكنك أن تقدم؟", ["البرمجة (Python)", "الإسبانية", "التصميم (Canva)"])
learn_skill = st.sidebar.selectbox("ماذا تريد أن تتعلم؟", ["الإسبانية", "البرمجة (Python)", "الإنجليزية"])

st.write(f"### أهلاً بكِ يا {user_name} في لوحة التحكم التجريبية!")

users_db = [
    {"name": "أحمد", "teach": "البرمجة (Python)", "learn": "الإسبانية", "credits": 2, "badge": "شريك مثالي ⭐"},
    {"name": "مريم", "teach": "الإسبانية", "learn": "البرمجة (Python)", "credits": 1, "badge": "مبتدئ ملتزم 📌"},
    {"name": "سارة", "teach": "التصميم (Canva)", "learn": "الإنجليزية", "credits": 3, "badge": "شريك مثالي ⭐"}
]

if st.button("🔍 ابحث عن شريك مطابق"):
    match_found = False
    for partner in users_db:
        if partner["teach"] == learn_skill and partner["learn"] == teach_skill:
            st.success(f"🎉 تم العثور على مطابقة مثالية (Win-Win) مع الشريك: {partner['name']}!")
            st.info(f"🏆 الشارة: {partner['badge']} | 💰 رصيد بنك الساعات: {partner['credits']} ساعات")
            match_found = True
            break
    if not match_found:
        st.warning("⚠️ لم يتم العثور على مطابقة فورية. تم تسجيل طلبك في بنك المهارات بانتظار شريك جديد.")

st.markdown("---")
st.caption("تم تطوير هذا النموذج الأولي (MVP) خصيصاً لمنصة Thirduni - أكتوبر 2026")
