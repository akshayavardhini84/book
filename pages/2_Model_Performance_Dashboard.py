import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NextRead", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    [data-testid="stSidebar"] {
        width: 300px;
    }
    </style>
""", unsafe_allow_html=True)
about_html = """
<div style='background-color: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333;'>
    <h3 style='color: #4B8BBE;'>👩‍💻 Akshaya Vardhini</h3>
    <p style='color: #ccc;'><strong>🎓 Education:</strong><br>M.Tech Integrated Software Engineering at VIT</p>
    <p style='color: #ccc;'><strong>Project:</strong><br>AI Book Recommendation System</p>
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
    <h1 style='color: #4B8BBE;'>📊 Model Performance Dashboard</h1>
    <h4 style='color: #bbb;'>Compare different recommendation models and their metrics.</h4>
</div><hr>
""", unsafe_allow_html=True)
data = {
    'Model': [
        'Baseline Model',
        'User-Based Collaborative Filtering',
        'Item-Based Collaborative Filtering',
        'SVD (Matrix Factorization)',
        'NMF (Matrix Factorization)',
        'Neural CF (Before Tuning)',
        'Neural CF (After Tuning)'
    ],
    'RMSE': [3.69, 2.41, 0.35, 0.8403, 0.8813, 0.63, 0.80],
    'Precision@10': [0.04, 0.02, 0.03, 0.84, 0.82, 0.79, 0.72],
    'Recall@10': [0.02, 0.73, 0.78, 0.67, 0.65, 0.75, 0.70],
    'Description': [
        "Baseline average model.",
        "User-based collaborative filtering.",
        "Item-based collaborative filtering.",
        "SVD matrix factorization.",
        "Non-negative matrix factorization.",
        "Neural collaborative filtering (before tuning).",
        "Neural collaborative filtering (after tuning)."
    ]
}
df = pd.DataFrame(data)
df['F1@10'] = 2 * df['Precision@10'] * df['Recall@10'] / (df['Precision@10'] + df['Recall@10'])
model_selected = st.selectbox("Select a Model to Explore:", df['Model'], index=6)
model_row = df[df['Model'] == model_selected].iloc[0]
st.subheader("Model Summary")
st.markdown(f"**{model_row.Description}**")
col1, col2 = st.columns(2)
with col1:
    st.metric("RMSE", f"{model_row.RMSE:.2f}")
    st.metric("Recall", f"{model_row['Recall@10']:.2f}")
with col2:
    st.metric("Precision", f"{model_row['Precision@10']:.2f}")
    st.metric("F1", f"{model_row['F1@10']:.2f}")
st.markdown("### Metric Comparison Chart (Interactive)")
metrics_data = {
    "Metric": ['RMSE', 'Precision', 'Recall', 'F1'],
    "Value": [model_row['RMSE'], model_row['Precision@10'], model_row['Recall@10'], model_row['F1@10']],
    "Color": ['#E76F51', '#2A9D8F', '#264653', '#4B8BBE']
}
chart_df = pd.DataFrame(metrics_data)
fig = px.bar(
    chart_df,
    x="Value",
    y="Metric",
    orientation="h",
    color="Metric",
    color_discrete_sequence=chart_df["Color"],
    title=f"Performance Metrics for {model_selected}",
    text=chart_df["Value"].apply(lambda x: f"{x:.2f}")
)
fig.update_traces(textposition='outside', textfont_color='black')
fig.update_layout(
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="#f9f9f9",
    title_font=dict(size=20, color="#4B8BBE"),
    font=dict(color='black'),
    xaxis_title="Metric Value",
    yaxis_title="",
    xaxis=dict(showgrid=False, color='black', tickfont=dict(color='black')),
    yaxis=dict(showgrid=False, color='black', tickfont=dict(color='black')),
    showlegend=False,
    margin=dict(l=10, r=10, t=60, b=10)
)
st.plotly_chart(fig, use_container_width=True)