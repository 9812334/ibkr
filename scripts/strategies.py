from tools import *

DEBUG = True
LIVE = True

def get_cencelled_orders():
    return [trade for trade in ib.trades() if trade.fills != []]

def get_trade_by_permid(permid):
    return next((trade for trade in ib.trades() if trade.order.permId == permid), None)

def get_last_executed_trade():
    return get_trade_by_permid(permid = (ib.executions()[-1].permId))


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
    "pause_seconds": 90,
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
    "pause_seconds": 70,
}


def run_simple_scalp(strategy_details, open_permId, close_permId, cancel_permids=[], push = False):
    open_trade = None
    close_trade = None
    open_order = None
    close_order = None
    open_order_ts = None

    push_notifications(
        f"-------- {strategy_details} / {open_permId} / {close_permId} / {cancel_permids}", push
    )

    if open_permId is not None:
        orders = [t.order for t in ib.openOrders()]
        for o in orders:
            if o.permId == open_permId:
                open_order = o

    if open_order is not None:
        push_notifications(f"OPEN ORDER:: {open_order}", push)

    if open_trade is None:
        trades = ib.trades()
        for o in trades:
            if o.orderStatus.permId == open_permId:
                open_trade = o

    # push_msg(f"OPEN TRADE:: {open_trade.order}")

    if close_permId is not None:
        for o in orders:
            if o.permId == close_permId:
                close_order = o

    if close_order is not None:
        push_notifications(f"CLOSE ORDER:: {close_order}")

    if close_trade is None:
        trades = ib.trades()
        for o in trades:
            if o.orderStatus.permId == close_permId:
                close_trade = o

    # print(f"CLOSE TRADE:: {close_trade}")

    for permId in cancel_permids:
        cancelled_order = None
        for o in orders:
            if o.permId == permId:
                print(f"Cancelling order.permId {o.permId}")
                cancelled_order = ib.cancelOrder(o)
                ib.sleep(2)
                if cancelled_order.orderStatus.status == "Cancelled":
                    print(f"Order {o.permId} has been cancelled")
                else:
                    raise Exception("Unable to cancel order {o.permId}")

        if cancelled_order is None:
            raise Exception(":: ORDER TO CANCEL NOT FOUND ::  {permId}")

    pause = False
    ib.sleep(1)

    while True:

        print(f"------- {strategy_details['strategy']} / {strategy_details['open_ticks']}-{strategy_details['close_ticks']} / {strategy_details['pause_seconds']} seconds -------")

        print_line()

        # first order of the strategy
        if open_trade is None and close_trade is None:
            action = strategy_details["open_action"]
            qty = strategy_details["open_qty"]

            if ticker is None or len(ticker.domBids) == 0 or len(ticker.domAsks) == 0:
                print(f"************ Issue getting orderbok *************** ")
                ib.sleep(1)
                continue

            if strategy_details["open_ref"] == "bid":
                price_ref = ticker.domBids[0].price
            elif strategy_details["open_ref"] == "ask":
                price_ref = ticker.domAsks[0].price
            elif strategy_details["open_ref"] == "mid":
                price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
            else:
                raise Exception("Not implemented")

            lmtPrice = (
                price_ref
                + strategy_details["open_ticks"] * strategy_details["tick_increment"]
            )
            print(
                f"Placing open trade: {action}, {strategy_details['open_type']}, totalQuantity {qty}, lmtPrice {lmtPrice}"
            )

            if strategy_details["open_type"] == "LIMIT":
                open_order = LimitOrder(
                    action=action,
                    totalQuantity=qty,
                    lmtPrice=lmtPrice,
                    account="U10394496",
                )
            else:
                raise Exception("Not implemented")

            open_trade = ib.placeOrder(NQM4, open_order)
            trade = open_trade

            push_notifications(
                f"OPEN ORDER PLACED :: #{trade.order.permId} {trade.orderStatus.status} {trade.contract.symbol} {trade.order.action} {trade.orderStatus.filled}/{trade.orderStatus.remaining} @ {trade.order.lmtPrice}"
            )

            open_order_ts = datetime.datetime.now()

        print_order(open_trade)
        print_line()

        if open_trade is not None:
            if open_trade.orderStatus.status == "Submitted" and close_trade is None:
                print(
                    f"Waiting to get filled on order #{open_trade.order.permId} ({open_trade.orderStatus.status})"
                )

                if (
                    open_order_ts is None
                    or datetime.datetime.now() - open_order_ts
                    > datetime.timedelta(seconds=strategy_details["pause_seconds"])
                ):
                    print(f"Cancelling order due to timeout:")
                    ib.cancelOrder(open_trade.order)

            if open_trade.orderStatus.status == "Filled" and close_trade is None:
                print(f"Filled on open_trade {open_trade.orderStatus.status} {open_trade.orderStatus.avgFillPrice} {open_trade.orderStatus.status}")

                action = strategy_details["close_action"]
                qty = strategy_details["close_qty"]

                if strategy_details["close_ref"] == "open_price_fill":
                    price_ref = open_trade.orderStatus.avgFillPrice
                if strategy_details["close_ref"] == "bid":
                    price_ref = ticker.domBids[0].price
                elif strategy_details["close_ref"] == "ask":
                    price_ref = ticker.domAsks[0].price
                elif strategy_details["close_ref"] == "mid":
                    price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
                else:
                    raise Exception("Not implemented")

                lmtPrice = (
                    price_ref
                    + strategy_details["close_ticks"]
                    * strategy_details["tick_increment"]
                )

                if strategy_details["close_type"] == "LIMIT":
                    close_order = LimitOrder(
                        action=action,
                        totalQuantity=qty,
                        lmtPrice=lmtPrice,
                        account="U10394496",
                    )
                else:
                    raise Exception("Not implemented")

                close_trade = ib.placeOrder(NQM4, close_order)

                alert(False)
                # push_notifications(msg=f"OPEN ORDER FILLED:: {open_trade.order}")
                push_notifications(msg=f"CLOSE ORDER PLACED:: {close_trade.order}")

            elif (
                open_trade.orderStatus.status == "Inactive"
                or open_trade.orderStatus.status == "Cancelled"
            ) and close_trade is None:
                # push_notifications(f"OPEN TRADE CANCELLED:: {open_trade.order}")
                open_trade = None

        print_order(close_trade)
        print_line()

        if close_trade is not None:
            if close_trade.orderStatus.status == "Filled":
                print(f"Close trade filled @ {close_trade.orderStatus.avgFillPrice}")
                alert(True)
                push_notifications(f"CLOSE TRADE FILLED:: {close_trade.order}")
                open_trade = None
                close_trade = None
                pause = True

            print_line()

        print_orderbook()
        print_line()

        print_positions()
        print_line()
        print_openOrders()

        # openOrders = parse_ibrecords(ib.openOrders())
        # print_ibrecords_table(
        #     openOrders,
        #     cols=[
        #         "localSymbol",
        #         "permId",
        #         "status",
        #         "orderType",
        #         "action",
        #         "lmtPrice",
        #         "remaining",
        #     ],
        # )

        print('-')
        print_account_summary()

        if pause:
            open_orders = ib.reqAllOpenOrders()
            executions = ib.reqExecutions()

            ib.sleep(strategy_details["pause_seconds"])
            pause = False
        else:
            ib.sleep(1)

        print_clear()


run_ss_2(strategy_details=SELL_SCALP, open_permid=1622695088, close_permid = None)
