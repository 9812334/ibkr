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
