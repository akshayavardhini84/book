import streamlit as st
st.set_page_config(page_title="NextRead", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] 
    {
        display: none;
    }
    [data-testid="stSidebar"] 
    {
        width: 300px;
    }
    </style>
""", unsafe_allow_html=True)
about_html = """
<div style='background-color: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333;'>
    <h3 style='color: #4B8BBE;'>👩‍💻 Akshaya Vardhini</h3>
    <p style='color: #ccc;'><strong>🎓 Education:</strong><br>M.Tech Integrated Software Engineering at VIT</p>
    <p style='color: #ccc;'><strong>Project:</strong><br>AI-Based Book Recommendation System</p>
    <p style='color: #ccc;'><strong>🌐 Connect:</strong><br>
        <a href='https://github.com/akshayavardhini84' target='_blank' style='color:#4B8BBE;'>🐙 GitHub</a><br>
        <a href='linkedin.com/in/akshaya-vardhini-001725278' target='_blank' style='color:#4B8BBE;'>💼 LinkedIn</a>
    </p>
</div>
"""
with st.sidebar:
    st.markdown(about_html, unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>
    <h1 style='color: #4B8BBE;'>📖 NextRead</h1>
    <h3 style='color: #bbb;'>Discover books tailored to your taste.</h3>
    <p style='font-size: 16px; color: #aaa;'>AI-driven recommendations based on your favorite titles and genres.</p>
</div>
""", unsafe_allow_html=True)
button_css = """
<style>
div.stButton > button 
{
    background-color: #4B8BBE;
    color: white;
    padding: 8px 16px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    width: 80%;
    margin: 10px 0px;
    margin-left: 70px;
    transition: background-color 0.3s ease;
    text-align: center;
}
div.stButton > button:hover 
{
    background-color: #3a6f9e;
}
</style>
"""
st.markdown(button_css, unsafe_allow_html=True)
st.markdown("## Use the Buttons below to navigate:")
st.markdown("""
<div style='margin-left: 200px;'>
""", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("📖 Recommend Books"):
        st.switch_page("pages/1_Frontend_Recommendation.py")
with col2:
    if st.button("📊 View Model Dashboard"):
        st.switch_page("pages/2_Model_Performance_Dashboard.py")
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br><hr><br>", unsafe_allow_html=True)