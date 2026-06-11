# data_preprocessing.py
import numpy as np
import pandas as pd
from data_source import RAW_PLAYER_DATA

def get_prepared_dataframe():
    """Datanı Pandas DataFrame formasına salır"""
    return pd.DataFrame(RAW_PLAYER_DATA)

def prepare_ml_features():
    """Oyun saatlarını matris formasına salır və normallaşdırır"""
    df = get_prepared_dataframe()
    
    # Giriş parametrləri (Features) - Oyun saatları
    X = np.array(df['hours'].tolist(), dtype=float)
    
    # Normallaşdırma (Min-Max Scaling): Saatlar arasındakı böyük fərqlərin
    # modelə mənfi təsir etməməsi üçün datanı 0 ilə 1 arasına sıxırıq.
    max_vals = X.max(axis=0)
    # Sıfıra bölünmə xətası olmasın deyə yoxlayırıq
    max_vals[max_vals == 0] = 1.0
    X_scaled = X / max_vals
    
    return X_scaled, df

if __name__ == "__main__":
    X, df = prepare_ml_features()
    print(f"Data uğurla hazırlandı! Giriş matrisinin ölçüsü: {X.shape}")
