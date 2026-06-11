# recommendation.py
from sklearn.metrics.pairwise import cosine_similarity
from data_preprocessing import prepare_ml_features

def recommend_teammates(steamid, top_n=4):
    """Verilən SteamID-yə görə ən çox oxşarlıq göstərən oyunçuları tapır"""
    X, df = prepare_ml_features()
    
    # Daxil edilən oyunçunun indeksini tapırıq
    player_row = df[df['steamid'] == str(steamid)]
    if player_row.empty:
        return f"Xəta: {steamid} ID-li oyunçu tapılmadı!"
    
    player_idx = player_row.index[0]
    
    # Bütün oyunçular arasındakı kosinus oxşarlığını hesablayırıq
    similarity_matrix = cosine_similarity(X)
    
    # Seçilən oyunçunun digərləri ilə olan oxşarlıq balları
    player_scores = similarity_matrix[player_idx]
    
    # Balları böyükdən kiçiyə sıralayırıq və özünü çıxarırıq (indeks [0] özüdür)
    similar_indices = player_scores.argsort()[::-1][1:top_n+1]
    
    print(f"\n🎯 Hədəf Oyunçu: {df.iloc[player_idx]['username']} ({df.iloc[player_idx]['role']})")
    print(f"==================================================")
    print(f"🤖 ML tərəfindən tövsiyə olunan oyunçular:")
    
    for idx in similar_indices:
        username = df.iloc[idx]['username']
        role = df.iloc[idx]['role']
        score = player_scores[idx] * 100 # Faizə çeviririk
        print(f" -> {username} | Rol: {role} | Uyğunluq: {score:.1f}%")

if __name__ == "__main__":
    # Nümunə olaraq siyahıdakı ilk oyunçunun (Elnur_Gamer) ID-si ilə test edirik
    recommend_teammates(steamid="76561198000000001")
