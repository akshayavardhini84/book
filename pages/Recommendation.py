import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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
    <p style='color: #ccc;'><strong> Project:</strong><br>AI Book Recommendation System</p>
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
    <h1 style='color: #4B8BBE;'>📖 Book Recommendation</h1>
    <h4 style='color: #bbb;'>Get personalized suggestions based on titles or genres.</h4>
</div><hr>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    books_df = pd.read_csv("data/books.csv")
    tags_df = pd.read_csv("data/tags.csv")
    book_tags = pd.read_csv("data/book_tags.csv")
    merged_tags = book_tags.merge(tags_df, on='tag_id')
    grouped = merged_tags.groupby('goodreads_book_id')['tag_name'].apply(lambda tags: ' '.join(tags)).reset_index()
    grouped.columns = ['book_id', 'tags']
    books_df = books_df.merge(grouped, on='book_id', how='left')
    books_df['title_clean'] = books_df['title'].fillna('').str.lower().str.strip()
    books_df['tags'] = books_df['tags'].fillna('')
    return books_df
books_df = load_data()
tfidf_title = TfidfVectorizer(stop_words='english')
tfidf_matrix_title = tfidf_title.fit_transform(books_df['title_clean'])
def recommend_by_title(user_input, top_n=5):
    user_input_clean = user_input.lower().strip()
    matches = books_df[books_df['title_clean'].str.contains(user_input_clean)]
    if matches.empty:
        return None, None
    idx = matches.index[0]
    cosine_sim = linear_kernel(tfidf_matrix_title[idx], tfidf_matrix_title).flatten()
    similar_indices = cosine_sim.argsort()[::-1][1:top_n+1]
    recommended = books_df.iloc[similar_indices][['title', 'authors']]
    return books_df.iloc[idx]['title'], recommended
def recommend_by_genre(selected_tag, top_n=5):
    idx_list = books_df[books_df['tags'].str.contains(selected_tag, case=False)].index.tolist()
    if not idx_list:
        return None
    recommended = books_df.iloc[idx_list][['title', 'authors']].sample(n=min(top_n, len(idx_list)))
    return recommended
mode = st.radio("🔍 Choose Recommendation Mode:", ["By Book Title", "By Genre"])
if mode == "By Book Title":
    user_input = st.text_input("Enter Book Title:")
    if st.button("Get Recommendations"):
        matched_title, recommendations = recommend_by_title(user_input)
        if matched_title is None:
            st.error(f"No book found for '{user_input}'.")
        else:
            st.markdown(f"<h3 style='color:#4B8BBE;'>If you like <b>{matched_title}</b>, You may also like:</h3>", unsafe_allow_html=True)
            for idx, row in recommendations.iterrows():
                st.markdown(f"- **{row['title']}** by *{row['authors']}*")
else:
    all_tags = " ".join(books_df['tags']).split()
    unique_tags = sorted(set(all_tags))
    selected_tag = st.selectbox("Choose a Genre:", unique_tags)
    if st.button("Get Recommendations"):
        recommendations = recommend_by_genre(selected_tag)
        if recommendations is None or recommendations.empty:
            st.error(f"No books found in genre '{selected_tag}'.")
        else:
            st.markdown(f"<h3 style='color:#4B8BBE;'>Top picks of # <b>{selected_tag}</b></h3>", unsafe_allow_html=True)
            for idx, row in recommendations.iterrows():
                st.markdown(f"- **{row['title']}** by *{row['authors']}*")