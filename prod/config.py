import os

SCRIPT_DIR = os.getcwd()

LOGS_DIR = f"{SCRIPT_DIR}/logs"
CHANIFY_URL = "https://api.chanify.net/v1/sender/"
CHANIFY_TOKEN = "CICswLUGEiJBQUZIR0pJQ0VVNkxUTlZCMk1DRElCWU1RSlNWMktCS0NFIgIIAQ.vj8gcfxM4jD9Zv0mBMSlFlY51EL_jC5dB8LWdWX1tAs"

IBKR_ACCOUNT_1 = "U10394496"
IBKR_ACCOUNT_2 = "U2340948"

# IBKR_SERVER = "192.168.1.82"  # "127.0.0.1"
IBKR_SERVER = "127.0.0.1"
# IBKR_SERVER = "100.119.138.60"
IBKR_PORT = 4001

import random
CLIENT_ID = random.randint(1, 999)


BUY_SCALP_NQ = {
    "margin_cushion_pct": 0,
    "account": IBKR_ACCOUNT_1,
    "close_qty": 2,
    "close_type": "LIMIT",
    "close_action": "SELL",
    "close_ref": "open_fill",
    "close_permid": None,
    "strategy": "BUY TO OPEN SCALP",
    "contract": "NQU4",
    "open_qty": 2,
    "open_type": "LIMIT",
    "open_action": "BUY",
    "open_ob_sum_bid_ask_size_ratio_min": 1,
    "open_ob_sum_bid_ask_size_ratio_max": 30,
    "open_min": 0,
    "open_max": 20950,
    "open_permid": None,
    "open_ref": "max_bid_size",
    "open_ticks": 1,
    "cancel_permid": None,
    "pause_replace": 60,
    "pause_restart": 15,
    "tick_increment": 0.25,
}

SELL_SCALP_NQ = {
    "margin_cushion_pct": 0,
    "account": IBKR_ACCOUNT_1,
    "strategy": "SELL TO OPEN SCALP",
    "contract": "NQU4",
    "tick_increment": 0.25,
    "open_qty": 2,
    "open_max": 23475,
    "open_min": 20075,
    "open_type": "LIMIT",
    "open_action": "SELL",
    "open_ob_sum_bid_ask_size_ratio_min": 2,
    "open_ob_sum_bid_ask_size_ratio_max": 30,
    "open_ref": "ask",
    "close_qty": 2,
    "close_type": "LIMIT",
    "close_action": "BUY",
    "close_ref": "open_fill",
    "open_permid": None,
    "close_permid": None,
    "cancel_permid": None,
    "open_ticks": 10,
    "close_ticks": -10,
    "pause_replace": 15,
    "pause_restart": 10,
}

CONTRACT_SYM = {
    "NQU4": 637533450,
    "MNQU4": 637533593,
    "RTYU4": 637533627,
}

ORDER_COLS = [
    "localSymbol",
    "permId",
    "status",
    "orderType",
    "action",
    "lmtPrice",
    "remaining",
]

TRADE_COLS = [
    "permId",
    "clientId",
    "localSymbol",
    "status",
    "orderType",
    "action",
    "lmtPrice",
    "remaining",
    "filledQuantity",
    "fills",
]

OPEN_TRADE_COLS = [
    "permId",
    "orderId",
    "symbol",
    "lastTradeDateOrContractMonth",
    "orderType",
    "action",
    "lmtPrice",
    "totalQuantity",
    "remaining",
]
