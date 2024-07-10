from tools import *


def run_ss_2(strategy_details, open_permid = None, close_permid = None, push = False):

    def get_open_close_trades(open_permid, close_permid):
        open_trade = get_trade_by_permid(open_permid)
        close_trade = get_trade_by_permid(close_permid)

        push_notifications(
            f"{strategy_details} / {open_permid} / {close_permid}", push
        )

        push_notifications(f"OPEN TRADE:: {open_trade}", push)
        push_notifications(f"CLOSE TRADE:: {close_trade}", push)

        return open_trade, close_trade


    def print_summary():
        print_clear()
        print(f"------- {strategy_details['strategy']} / {strategy_details['open_ticks']}:{strategy_details['close_ticks']} / {strategy_details['pause_seconds']} seconds -------")
        print_line()
        
        if open_trade is not None:
            print_order(open_trade)
        else:
            print("Open trade not placed yet")
        print_line()

        if close_trade is not None:
            print_order(close_trade)
        else:
            print("Close trade not placed yet")
        print_line()

        print_line()
        print_orderbook()
        print_line()

    open_trade, close_trade = get_open_close_trades(open_permid, close_permid)
    close_order_timestamp = None
    open_order_timestamp = None

    while ib.sleep(1):

        print_summary()

        if close_order_timestamp is not None and (datetime.datetime.now() - close_order_timestamp < datetime.timedelta(seconds=strategy_details["pause_seconds"])):
            print(f'Waiting {strategy_details["pause_seconds"] - (datetime.datetime.now() - close_order_timestamp).seconds} seconds...')
            continue
            
        if DEBUG:
            proceed = input("Proceed? ")

            if proceed.lower() != "y":
                continue

        # execution part - first order of the strategy
        if open_trade is None and close_trade is None:
            action = strategy_details["open_action"]
            qty = strategy_details["open_qty"]

            if ticker is None or len(ticker.domBids) == 0 or len(ticker.domAsks) == 0:
                print(f"************ Issue getting orderbook tickers *************** ")
                alert(True)
                ib.waitOnUpdate()
                continue

            if strategy_details["open_ref"] == "bid":
                price_ref = ticker.domBids[0].price
            elif strategy_details["open_ref"] == "ask":
                price_ref = ticker.domAsks[0].price
            elif strategy_details["open_ref"] == "mid":
                price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
            else:
                raise Exception("Not implemented")

            limit_price = (
                price_ref
                + strategy_details["open_ticks"] * strategy_details["tick_increment"]
            )

            if strategy_details["open_type"] == "LIMIT":
                open_order = LimitOrder(
                    action=action,
                    totalQuantity=qty,
                    lmtPrice=limit_price,
                    account="U10394496",
                )
            else:
                raise Exception("Not implemented")

            print(f"Placing order for open_trade {open_order} ")

            if LIVE:
                open_trade = ib.placeOrder(NQM4, open_order)
                ib.sleep(1)
                open_order_timestamp = datetime.datetime.now()

                trade = open_trade
                push_notifications(f"OPEN ORDER PLACED :: #{trade.order.permId} {trade.orderStatus.status} {trade.contract.symbol} {trade.order.action} {trade.orderStatus.filled}/{trade.orderStatus.remaining} @ {trade.order.lmtPrice}", push)

            else:
                print(f"[NOT LIVE] OPEN ORDER PLACED :: {open_order}")        

        if open_trade is not None:
            if (
                open_trade.orderStatus.status == "Inactive"
                or open_trade.orderStatus.status == "Cancelled"
            ) and close_trade is None:                
                push_notifications(f"OPEN TRADE CANCELLED:: {open_trade.order}", push)
                open_trade = None
            elif open_trade.orderStatus.status == "Submitted" and close_trade is None:
                print(
                    f"Waiting to get filled on order #{open_trade.order.permId} ({open_trade.orderStatus.status})"
                )

                if (
                    open_order_timestamp is None
                    or datetime.datetime.now() - open_order_timestamp
                    > datetime.timedelta(seconds=strategy_details["pause_seconds"])
                ):
                    print(f"OPEN Trade submitted, but not filled. Modifying order limit price: {open_trade.order.lmtPrice}")

                    # find the price of opening the trade
                    if strategy_details["open_ref"] == "bid":
                        price_ref = ticker.domBids[0].price
                    elif strategy_details["open_ref"] == "ask":
                        price_ref = ticker.domAsks[0].price
                    elif strategy_details["open_ref"] == "mid":
                        price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
                    else:
                        raise Exception("Not implemented")

                    limit_price = (
                        price_ref
                        + strategy_details["open_ticks"] * strategy_details["tick_increment"]
                    )

                    open_trade.order.lmtPrice = limit_price

                    print(f"Modifying order: {open_trade.order}")

                    if LIVE:
                        open_trade = ib.placeOrder(NQM4, open_trade.order)
                        push_notifications(f"MODIFIED ORDER PLACED:: {open_trade.order}", push)
                    else:
                        print(f"[NOT LIVE] MODIFIED ORDER PLACED:: {open_trade.order}")
                        
                    open_order_timestamp = datetime.datetime.now()

            elif open_trade.orderStatus.status == "Filled" and close_trade is None:
                exec_price = open_trade.fills[0].execution.price
                print(f"Filled on open_trade: {open_trade.orderStatus.status} {exec_price} {open_trade.fills[0].execution.side}")

                action = strategy_details["close_action"]
                qty = strategy_details["close_qty"]

                # find the price to close the trade
                if strategy_details["close_ref"] == "open_fill":
                    price_ref = exec_price
                elif strategy_details["close_ref"] == "bid":
                    price_ref = ticker.domBids[0].price
                elif strategy_details["close_ref"] == "ask":
                    price_ref = ticker.domAsks[0].price
                elif strategy_details["close_ref"] == "mid":
                    price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
                else:
                    raise Exception("Not implemented")

                limit_price = (
                    price_ref
                    + strategy_details["close_ticks"]
                    * strategy_details["tick_increment"]
                )

                if strategy_details["close_type"] == "LIMIT":
                    close_order = LimitOrder(
                        action=action,
                        totalQuantity=qty,
                        lmtPrice=limit_price,
                        account="U10394496",
                    )
                else:
                    raise Exception("Not implemented")

                print(f"Placing close_order {close_order}")

                if LIVE:
                    close_trade = ib.placeOrder(NQM4, close_order)
                    ib.sleep(1)
                    push_notifications(f"OPEN ORDER FILLED:: {open_trade.order}", push)
                    push_notifications(f"CLOSE ORDER PLACED:: {close_trade.order}", push)
                    alert(False)
                else:
                    print(f"[NOT LIVE] CLOSE ORDER PLACED:: {close_order}")
                    # print(f"CLOSE ORDER PLACED:: {close_trade.order}")

                ib.reqAllOpenOrders()
                ib.reqPositions()

        if close_trade is not None:
            if close_trade.orderStatus.status == "Filled":
                print(f"Close trade filled @ {close_trade.orderStatus.avgFillPrice}")
                print_line()
                push_notifications(f"CLOSE TRADE FILLED:: {close_trade.order}", push)
                alert(True)

                close_order_timestamp = datetime.datetime.now()

                open_trade = None
                close_trade = None

                ib.reqAllOpenOrders()
                ib.reqPositions()
            elif (
                close_trade.orderStatus.status == "Inactive"
                or close_trade.orderStatus.status == "Cancelled"
            ):                
                push_notifications(f"CLOSE TRADE CANCELLED:: {close_trade.order}", push)
                close_trade = None

        ib.accountValues()


SELL_SCALP = {
    "strategy": "SELL TO OPEN SCALP",
    "contract": "NQM2024",
    "tick_increment": 0.25,
    "open_qty": 1,
    "open_type": "LIMIT",
    "open_action": "SELL",
    "open_ref": "ask",
    "open_ticks": 10,
    "close_qty": 1,
    "close_type": "LIMIT",
    "close_action": "BUY",
    "close_ref": "open_fill",
    "close_ticks": -10,
    "pause_seconds": 60,
}

BUY_SCALP = {
    "strategy": "BUY TO OPEN SCALP",
    "contract": "NQM2024",
    "tick_increment": 0.25,
    "open_qty": 1,
    "open_type": "LIMIT",
    "open_action": "BUY",
    "open_ref": "ask",
    "open_ticks": -10,
    "close_qty": 1,
    "close_type": "LIMIT",
    "close_action": "SELL",
    "close_ref": "open_fill",
    "close_ticks": 10,
    "pause_seconds": 60,
}


DEBUG = False
LIVE = True

if __name__ == "__main__":
    open_permid = None # get_last_trade_permid(n=0)
    close_permid = None # get_last_trade_permid()
    print(open_permid, ";", close_permid)

    run_ss_2(strategy_details=BUY_SCALP, open_permid=open_permid, close_permid = close_permid, push = True)
