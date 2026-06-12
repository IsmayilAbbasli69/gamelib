# data_preprocessing.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matchmaking_ai.py import RAW_PLAYER_DATA

def load_and_preprocess_data():
    """Xam datanı oxuyur, təmizləyir və ML üçün normallaşdırır"""
    # Datanı DataFrame formasına salırıq
    df = pd.DataFrame(RAW_PLAYER_DATA)
    
    # Oyun saatlarını (hours) ayrıca bir matris (X) edirik
    X = np.array(df['hours'].tolist(), dtype=float)
    
    # Min-Max Scaling: Saat fərqləri modelin ağlını qarışdırmasın deyə 0-1 aralığına gətiririk
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    return df, X_scaled

if __name__ == "__main__":
    df, X_scaled = load_and_preprocess_data()
    print(f"✅ Data ML üçün uğurla hazırlandı!")
    print(f"Oyunçu sayı: {df.shape[0]}, Giriş matrisinin ölçüsü: {X_scaled.shape}")
