# model.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from data_preprocessing import load_and_preprocess_data

class TeammateRecommender:
    def __init__(self):
        # Fayllar bir-biri ilə əlaqəlidir, preprocessing-dən datanı götürürük
        self.df, self.X_scaled = load_and_preprocess_data()
        # Kosinus oxşarlığı matrisini hesablayırıq
        self.similarity_matrix = cosine_similarity(self.X_scaled)

    def recommend_teammates(self, steamid, top_n=4):
        """Daxil edilən SteamID-yə görə ən uyğun komanda yoldaşlarını tapır"""
        # Oyunçunun bazadakı indeksini tapırıq
        player_row = self.df[self.df['steamid'] == str(steamid)]
        
        if player_row.empty:
            return f"❌ Xəta: {steamid} ID-li oyunçu tapılmadı!"
        
        player_idx = player_row.index[0]
        player_info = player_row.iloc[0]
        
        # Bu oyunçunun digər bütün oyunçularla olan oxşarlıq balları
        scores = self.similarity_matrix[player_idx]
        
        # Balları böyükdən kiçiyə sıralayırıq və özünü (indeks 0) çıxarırıq
        similar_indices = scores.argsort()[::-1][1:top_n+1]
        
        print(f"\n🎯 [HƏDƏF OYUNÇU ANALİZİ]")
        print(f"İstifadəçi adı: {player_info['username']}")
        print(f"Rolu: {player_info['role']} | Üstünlük verdiyi janr: {player_info['preferred_genre']}")
        print(f"==================================================================")
        print(f"🤖 [ML MATCHMAKING RECOMTENDATIONS]:")
        
        for idx in similar_indices:
            match_user = self.df.iloc[idx]
            match_score = scores[idx] * 100  # Faizə çeviririk
            print(f" ➡️  Oyunçu: {match_user['username']:<15} | Rol: {match_user['role']:<22} | Uyğunluq: {match_score:.1f}%")

if __name__ == "__main__":
    # Modeli başladırıq
    recommender = TeammateRecommender()
    
    # Nümunə 1: Elnur_Gamer üçün CS/FPS komandası axtarışı
    recommender.recommend_teammates(steamid="76561198000000001")
    
    print("\n" + "-"*66)
    
    # Nümunə 2: Siyahıdan bir RPG/Co-Op oyunçusu üçün sınaq (Aysel_RPG)
    recommender.recommend_teammates(steamid="76561198000000051")
