# Small Capital Trading Bot

Учебный торговый бот с жёстким риск-менеджментом для малого депозита ($50+).

⚠️ **ВАЖНО**:
- По умолчанию работает в **Paper Trading** (симуляция).
- Реальная торговля возможна, но очень рискованна.
- Ты можешь потерять все деньги.
- Это не финансовый совет.

## Риск-менеджмент (под $50)

- Риск на сделку: **2%** ($1)
- Максимум 1 позиция
- Обязательный Stop-Loss
- Take-Profit минимум 1:2
- Дневной лимит убытка: 6%
- Максимальная просадка счёта: 20% (бот останавливается)

## Установка

```bash
git clone https://github.com/deniztektile-ui/small-capital-trading-bot.git
cd small-capital-trading-bot
pip3 install -r requirements.txt
```

## Запуск

```bash
python3 bot.py
```

## Включение реальной торговли

1. Создай API-ключи на Binance (только права Spot Trading, **без Withdrawal**)
2. Вставь их в `config.py`
3. Поменяй `PAPER_TRADING = False`
4. Запускай на свой страх и риск
