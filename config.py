# ====================== CONFIG ======================

# Режим работы
PAPER_TRADING = True          # True = симуляция | False = реальные деньги (ОЧЕНЬ ОПАСНО!)

# Капитал
STARTING_BALANCE = 50.0       # стартовый капитал в USDT

# Биржа и пара (мем-коины)
EXCHANGE_ID = "binance"
SYMBOL = "DOGE/USDT"          # Можно менять: DOGE/USDT, SHIB/USDT, PEPE/USDT, WIF/USDT, BONK/USDT
TIMEFRAME = "5m"              # Для мемов лучше короткий таймфрейм

# Стратегия
FAST_SMA = 8
SLOW_SMA = 21

# ===== РИСК-МЕНЕДЖМЕНТ для МЕМ-КОИНОВ =====
RISK_PER_TRADE = 0.015        # 1.5% риска (ещё строже из-за волатильности)
STOP_LOSS_PCT = 0.04          # 4% стоп-лосс (мемы сильно шумят)
TAKE_PROFIT_PCT = 0.08        # 8% тейк-профит (1:2)
MAX_DAILY_LOSS_PCT = 0.05     # 5% дневной лимит
MAX_DRAWDOWN_PCT = 0.15       # 15% максимальная просадка → бот стоп
MAX_POSITIONS = 1

# API ключи (только для реальной торговли)
API_KEY = ""
API_SECRET = ""

# ====================================================
