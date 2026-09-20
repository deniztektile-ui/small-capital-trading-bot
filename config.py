# ====================== CONFIG ======================

# Режим работы
PAPER_TRADING = True          # True = симуляция | False = реальные деньги (ОПАСНО!)

# Капитал
STARTING_BALANCE = 50.0       # стартовый капитал в USDT

# Биржа и пара
EXCHANGE_ID = "binance"
SYMBOL = "BTC/USDT"
TIMEFRAME = "15m"

# Стратегия
FAST_SMA = 10
SLOW_SMA = 30

# ===== РИСК-МЕНЕДЖМЕНТ (под $50) =====
RISK_PER_TRADE = 0.02         # 2% риска на сделку
STOP_LOSS_PCT = 0.025         # 2.5% стоп-лосс
TAKE_PROFIT_PCT = 0.05        # 5% тейк-профит (1:2)
MAX_DAILY_LOSS_PCT = 0.06     # 6% дневной лимит
MAX_DRAWDOWN_PCT = 0.20       # 20% максимальная просадка → бот стоп
MAX_POSITIONS = 1             # только 1 позиция

# API ключи (только для реальной торговли)
API_KEY = ""
API_SECRET = ""

# ====================================================
