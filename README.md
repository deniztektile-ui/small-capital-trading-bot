# Small Capital Trading Bot — Meme Coins Edition

Бот с жёстким риск-менеджментом для торговли мем-коинами на малом депозите ($50).

⚠️ **ОЧЕНЬ ВАЖНО**:
- Мем-коины — это один из самых рискованных активов.
- Они могут упасть на 50–90% за короткое время.
- По умолчанию стоит **Paper Trading**.
- Реальная торговля мемами на $50 — очень высокий риск потерять всё.

## Текущие настройки

- Пара по умолчанию: **DOGE/USDT**
- Таймфрейм: 5 минут
- Риск на сделку: **1.5%**
- Stop-Loss: 4%
- Take-Profit: 8% (1:2)
- Дневной лимит: 5%
- Макс. просадка: 15%

Можно менять пару в `config.py`:
- DOGE/USDT
- SHIB/USDT
- PEPE/USDT
- WIF/USDT
- BONK/USDT

## Запуск

```bash
git clone https://github.com/deniztektile-ui/small-capital-trading-bot.git
cd small-capital-trading-bot
pip3 install -r requirements.txt
python3 bot.py
```
