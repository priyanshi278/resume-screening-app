from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def rank_resumes(job_description, resume_texts, filenames):
    documents = [job_description] + resume_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = pd.DataFrame({
        'Filename': filenames,
        'Similarity Score': similarity_scores
    }).sort_values(by='Similarity Score', ascending=False)

    return results
