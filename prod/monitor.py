from tools import *

import argparse
import random

parser = argparse.ArgumentParser(description="IBKR Monitor Script")
parser.add_argument(
    "--dur",
    type=int,
    default=1,
    help="Duration for monitoring overview (in seconds)",
)
parser.add_argument(
    "--sym",
    type=str,
    default="RTYU4",
    help="Symbol for monitoring overview (eg RTYU4)",
)
parser.add_argument(
    "--push",
    type=bool,
    default=False,
    help="Duration for monitoring overview (in seconds)",
)
parser.add_argument(
    "--alert",
    type=bool,
    default=True,
    help="Duration for monitoring overview (in seconds)",
)

args = parser.parse_args()

import datetime



def monitor_overview(local_symbol, accounts = [IBKR_ACCOUNT_1], duration = 1):
    executions = []
    positions = []
    previous_orders = []

    ticker, contract = ticker_init(contract_id = CONTRACT_SYM[local_symbol])

    # every 5 seconds reqExecutions()
    t1 = datetime.datetime.now().timestamp()
    now = datetime.datetime.now().timestamp()

    while ib.sleep(duration):
        current_orders = util.df(parse_ibrecords(ib.reqAllOpenOrders()))

        if len(previous_orders) != len(current_orders):
            alert()
            # ib.reqPositions()

        ib.reqPositions()
        ib.reqAllOpenOrders()
        print_clear()
        # now = datetime.datetime.now().timestamp()
        # if now - t1 > datetime.timedelta(seconds=duration).total_seconds():
        #     print(f"Time elapsed: {now - t1}")

        #     t1 = datetime.datetime.now().timestamp()

        current_positions = print_positions(contract=contract)
        print("-" * 50)

        print_account_summary(accounts=accounts)
        print("-" * 50)

        print_trades(status = 'Filled', tail = 10, symbol = local_symbol)
        print("-" * 50)

        print_trades(status="Submitted", tail=10)
        print("-" * 50)

        # current_executions = print_executions(tail = 6)
        # print("-" * 50)

        print_orderbook(ticker=ticker)
        print("-" * 50)

        # executions = current_executions
        previous_orders = current_orders
        positions = current_positions


if __name__ == "__main__":
    try:
        monitor_overview(local_symbol=args.sym, duration=args.dur)
    except KeyboardInterrupt:
        print("Interrupted by user")

    ib.disconnect()
    exit(0)
