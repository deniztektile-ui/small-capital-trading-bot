#!/usr/bin/env python3
"""
Small Capital Trading Bot - Meme Coins Edition
Strict risk management for small deposits
"""

import time
import ccxt
import pandas as pd
from datetime import datetime, date
from config import *

class SmallCapitalBot:
    def __init__(self):
        self.balance = STARTING_BALANCE
        self.peak_balance = STARTING_BALANCE
        self.position = None
        self.daily_pnl = 0.0
        self.today = date.today()
        self.trades_today = 0

        print("=" * 60)
        print("  Small Capital Meme Coin Bot")
        print("=" * 60)

        if PAPER_TRADING:
            print("[MODE] PAPER TRADING (simulation)")
            self.exchange = ccxt.binance({"enableRateLimit": True})
        else:
            if not API_KEY or not API_SECRET:
                print("[ERROR] API_KEY or API_SECRET is empty!")
                print("Open config.py and put your Binance API keys.")
                raise ValueError("API keys missing")
            print("[MODE] LIVE TRADING - REAL MONEY")
            print("[WARNING] You can lose all your money!")
            self.exchange = ccxt.binance({
                "apiKey": API_KEY,
                "secret": API_SECRET,
                "enableRateLimit": True,
                "options": {"defaultType": "spot"}
            })

        print(f"Symbol:        {SYMBOL}")
        print(f"Timeframe:     {TIMEFRAME}")
        print(f"Start balance: {STARTING_BALANCE} USDT")
        print(f"Risk/trade:    {RISK_PER_TRADE*100}%")
        print("=" * 60)
        print("Press Ctrl+C to stop\n")

    def reset_daily_if_needed(self):
        if date.today() != self.today:
            self.today = date.today()
            self.daily_pnl = 0.0
            self.trades_today = 0
            print(f"[{self.now()}] New day - daily PnL reset")

    def now(self):
        return datetime.now().strftime("%H:%M:%S")

    def check_risk_limits(self):
        drawdown = (self.peak_balance - self.balance) / self.peak_balance if self.peak_balance > 0 else 0
        if drawdown >= MAX_DRAWDOWN_PCT:
            print(f"[{self.now()}] MAX DRAWDOWN {drawdown*100:.1f}% reached. Bot stopped.")
            return False

        if self.daily_pnl <= -STARTING_BALANCE * MAX_DAILY_LOSS_PCT:
            print(f"[{self.now()}] DAILY LOSS LIMIT reached ({self.daily_pnl:.2f} USDT). Waiting next day.")
            return False

        return True

    def fetch_data(self):
        ohlcv = self.exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=100)
        df = pd.DataFrame(ohlcv, columns=["ts", "open", "high", "low", "close", "volume"])
        df["sma_fast"] = df["close"].rolling(FAST_SMA).mean()
        df["sma_slow"] = df["close"].rolling(SLOW_SMA).mean()
        return df

    def get_signal(self, df):
        if len(df) < SLOW_SMA + 2:
            return None
        prev_fast = df["sma_fast"].iloc[-2]
        prev_slow = df["sma_slow"].iloc[-2]
        curr_fast = df["sma_fast"].iloc[-1]
        curr_slow = df["sma_slow"].iloc[-1]

        if prev_fast <= prev_slow and curr_fast > curr_slow:
            return "BUY"
        if prev_fast >= prev_slow and curr_fast < curr_slow:
            return "SELL"
        return None

    def calculate_position_size(self, price):
        risk_amount = self.balance * RISK_PER_TRADE
        size_usdt = risk_amount / STOP_LOSS_PCT
        size_usdt = min(size_usdt, self.balance * 0.95)
        return max(size_usdt, 0)

    def open_long(self, price):
        if self.position is not None:
            return

        size_usdt = self.calculate_position_size(price)
        if size_usdt < 6:
            print(f"[{self.now()}] Position size too small ({size_usdt:.2f} USDT), skip")
            return

        stop = price * (1 - STOP_LOSS_PCT)
        tp = price * (1 + TAKE_PROFIT_PCT)

        self.position = {
            "side": "long",
            "entry": price,
            "size_usdt": size_usdt,
            "stop": stop,
            "tp": tp,
        }
        self.trades_today += 1
        print(f"[{self.now()}] >>> OPEN LONG | Entry: {price:.6f} | Size: {size_usdt:.2f} USDT | SL: {stop:.6f} | TP: {tp:.6f}")

    def close_position(self, price, reason):
        if self.position is None:
            return

        entry = self.position["entry"]
        size = self.position["size_usdt"]
        pnl_pct = (price - entry) / entry
        pnl_usdt = size * pnl_pct

        self.balance += pnl_usdt
        self.daily_pnl += pnl_usdt
        self.peak_balance = max(self.peak_balance, self.balance)

        print(f"[{self.now()}] <<< CLOSE ({reason}) | Price: {price:.6f} | PnL: {pnl_usdt:+.2f} USDT ({pnl_pct*100:+.2f}%) | Balance: {self.balance:.2f}")
        self.position = None

    def manage_position(self, price):
        if self.position is None:
            return
        if price <= self.position["stop"]:
            self.close_position(price, "STOP-LOSS")
        elif price >= self.position["tp"]:
            self.close_position(price, "TAKE-PROFIT")

    def run(self):
        while True:
            try:
                self.reset_daily_if_needed()

                if not self.check_risk_limits():
                    time.sleep(60)
                    continue

                df = self.fetch_data()
                price = float(df["close"].iloc[-1])
                signal = self.get_signal(df)

                self.manage_position(price)

                if signal == "BUY" and self.position is None:
                    self.open_long(price)
                elif signal == "SELL" and self.position is not None:
                    self.close_position(price, "SIGNAL")

                pos = "LONG" if self.position else "FLAT"
                print(f"[{self.now()}] {SYMBOL} {price:.6f} | {pos} | Balance: {self.balance:.2f} | Daily: {self.daily_pnl:+.2f}")

                time.sleep(20)

            except KeyboardInterrupt:
                print("\nBot stopped by user.")
                break
            except Exception as e:
                print(f"[{self.now()}] Error: {e}")
                time.sleep(15)

if __name__ == "__main__":
    bot = SmallCapitalBot()
    bot.run()
