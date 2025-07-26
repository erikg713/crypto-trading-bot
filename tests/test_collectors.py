from src.collectors.fetch_historical import fetch_ohlcv

def test_fetch_ohlcv_structure():
    df = fetch_ohlcv(limit=10)
    assert df.shape[0] == 10
    assert set(['timestamp', 'open', 'high', 'low', 'close', 'volume']).issubset(df.columns)

