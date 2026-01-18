# API Endpoints - School & Crypto Timing

## MEXC Futures API

### OHLCV (Klines)
```
GET https://contract.mexc.com/api/v1/contract/kline/{symbol}

Params:
- symbol: BTC_USDT, ETH_USDT, etc.
- interval: Min1, Min5, Min15, Min30, Min60, Hour4, Hour8, Day1
- start: Unix timestamp (ms)
- end: Unix timestamp (ms)

Example:
curl "https://contract.mexc.com/api/v1/contract/kline/BTC_USDT?interval=Min60&start=1609992674000&end=1610113500000"
```

### Funding Rate
```
GET https://contract.mexc.com/api/v1/contract/funding_rate/{symbol}

Response:
{
  "symbol": "BTC_USDT",
  "fundingRate": 0.0001,
  "maxFundingRate": 0.003,
  "minFundingRate": -0.003,
  "collectCycle": 8,
  "nextSettleTime": 1610000000000
}

History:
GET https://contract.mexc.com/api/v1/contract/funding_rate/history?symbol=BTC_USDT&page_num=1&page_size=20
```

### Open Interest
```
GET https://contract.mexc.com/api/v1/contract/open_interest/{symbol}
```

### Ticker 24h
```
GET https://contract.mexc.com/api/v1/contract/ticker?symbol=BTC_USDT
```

## Via CCXT (Python)

```python
import ccxt

exchange = ccxt.mexc({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'options': {'defaultType': 'swap'}
})

# OHLCV
ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', limit=100)

# Ticker
ticker = exchange.fetch_ticker('BTC/USDT')

# Funding Rate
funding = ticker['info'].get('fundingRate', 0)
```

## Fear & Greed Index

```
GET https://api.alternative.me/fng/

Response:
{
  "data": [{
    "value": "45",
    "value_classification": "Fear",
    "timestamp": "1610000000"
  }]
}

Limits: Free, no auth required
```

## Coinglass (Liquidations)

```
GET https://open-api.coinglass.com/public/v2/liquidation_history

Params:
- symbol: BTC, ETH
- time_type: all, h1, h4, h12, h24

Note: Requires API key for full access
Free tier: Limited requests
```

## WebSocket (Real-time)

```
wss://contract.mexc.com/ws

Subscribe:
{
  "method": "sub.kline",
  "param": {"symbol": "BTC_USDT", "interval": "Min1"}
}

Funding Rate:
{
  "method": "sub.funding.rate",
  "param": {"symbol": "BTC_USDT"}
}
```

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Public REST | 20 req/s |
| Private REST | 10 req/s |
| WebSocket | 10 msg/s |

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 400 | Bad Request |
| 401 | Unauthorized |
| 429 | Rate Limited |
| 500 | Server Error |
