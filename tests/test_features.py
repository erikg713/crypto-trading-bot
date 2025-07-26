import pandas as pd
from src.features.feature_engineer import generate_features

def test_generate_features():
    # Create mock OHLCV data
    data = {
        'timestamp': pd.date_range(start='2023-01-01', periods=50, freq='15min'),
        'open': [100 + i for i in range(50)],
        'high': [101 + i for i in range(50)],
        'low': [99 + i for i in range(50)],
        'close': [100 + i for i in range(50)],
        'volume': [5000 + i * 10 for i in range(50)]
    }
    df = pd.DataFrame(data)
    X, y = generate_features(df)
    assert not X.empty
    assert X.shape[0] == y.shape[0]

