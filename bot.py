#!/usr/bin/env python3
"""
Small Capital Trading Bot
Strict risk management for $50+ accounts
Educational purpose only
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
        self.position = None          # None or dict with entry, size, stop, tp
        self.daily_pnl = 0.0
        self.today = date.today()
        self.trades_today = 0

        if PAPER_TRADING:
            print("[PAPER TRADING] Simulation mode")
            self.exchange = ccxt.binance({"enableRateLimit": True})
        else:
            if not API_KEY or not API_SECRET:
                raise ValueError("For real trading set API_KEY and API_SECRET in config.py")
            print("[LIVE TRADING] REAL MONEY - HIGH RISK!")
            self.exchange = ccxt.binance({
                "apiKey": API_KEY,
                "secret": API_SECRET,
                "enableRateLimit": True,
            })

    def reset_daily_if_needed(self):
        if date.today() != self.today:
            self.today = date.today()
            self.daily_pnl = 0.0
            self.trades_today = 0
            print(f"[{datetime.now().strftime('%H:%M:%S')}] New day — daily PnL reset")

    def check_risk_limits(self):
        # Max drawdown
        drawdown = (self.peak_balance - self.balance) / self.peak_balance
        if drawdown >= MAX_DRAWDOWN_PCT:
            print(f"!!! MAX DRAWDOWN reached ({drawdown*100:.1f}%). Bot stopped.")
            return False

        # Daily loss limit
        if self.daily_pnl <= -STARTING_BALANCE * MAX_DAILY_LOSS_PCT:
            print(f"!!! DAILY LOSS LIMIT reached ({self.daily_pnl:.2f} USDT). No more trades today.")
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
        prev_fast, prev_slow = df["sma_fast"].iloc[-2], df["sma_slow"].iloc[-2]
        curr_fast, curr_slow = df["sma_fast"].iloc[-1], df["sma_slow"].iloc[-1]

        if prev_fast <= prev_slow and curr_fast > curr_slow:
            return "BUY"
        if prev_fast >= prev_slow and curr_fast < curr_slow:
            return "SELL"
        return None

    def calculate_position_size(self, price):
        risk_amount = self.balance * RISK_PER_TRADE
        stop_distance = price * STOP_LOSS_PCT
        size_usdt = risk_amount / STOP_LOSS_PCT
        # Не больше баланса
        size_usdt = min(size_usdt, self.balance * 0.95)
        return size_usdt

    def open_long(self, price):
        if self.position is not None:
            return
        size_usdt = self.calculate_position_size(price)
        if size_usdt < 5:  # слишком мало
            print("Position size too small, skip")
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
        print(f">>> OPEN LONG | Price: {price:.2f} | Size: {size_usdt:.2f} USDT | SL: {stop:.2f} | TP: {tp:.2f}")

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

        print(f"<<< CLOSE ({reason}) | Price: {price:.2f} | PnL: {pnl_usdt:+.2f} USDT ({pnl_pct*100:+.2f}%) | Balance: {self.balance:.2f}")
        self.position = None

    def manage_position(self, price):
        if self.position is None:
            return
        if price <= self.position["stop"]:
            self.close_position(price, "STOP-LOSS")
        elif price >= self.position["tp"]:
            self.close_position(price, "TAKE-PROFIT")

    def run(self):
        print("=" * 60)
        print("  Small Capital Trading Bot")
        print(f"  Starting balance: {STARTING_BALANCE} USDT")
        print(f"  Risk per trade: {RISK_PER_TRADE*100}%")
        print(f"  Paper mode: {PAPER_TRADING}")
        print("=" * 60)
        print("Ctrl+C to stop\n")

        while True:
            try:
                self.reset_daily_if_needed()

                if not self.check_risk_limits():
                    time.sleep(60)
                    continue

                df = self.fetch_data()
                price = df["close"].iloc[-1]
                signal = self.get_signal(df)

                # Manage open position first
                self.manage_position(price)

                # New signals
                if signal == "BUY" and self.position is None:
                    self.open_long(price)
                elif signal == "SELL" and self.position is not None:
                    self.close_position(price, "SIGNAL")

                # Status
                pos_status = "LONG" if self.position else "FLAT"
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {SYMBOL} {price:.2f} | {pos_status} | Balance: {self.balance:.2f} | Daily PnL: {self.daily_pnl:+.2f}")

                time.sleep(30)

            except KeyboardInterrupt:
                print("\nBot stopped by user.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(15)

if __name__ == "__main__":
    bot = SmallCapitalBot()
    bot.run()
