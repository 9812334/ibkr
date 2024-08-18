from tools import *


def refresh():
    ib.reqAllOpenOrders()
    ib.reqPositions()


def simple_scalp(strat):

    def get_open_close_trades(open_permid, close_permid, push):
        open_trade = get_trade_by_permid(open_permid)
        close_trade = get_trade_by_permid(close_permid)

        if open_trade is not None:
            push_notifications(
                f"OPEN TRADE:: #{open_trade.order.permId} {open_trade.order.action} {open_trade.contract.localSymbol} {open_trade.order.orderType} @{open_trade.order.lmtPrice} filled {open_trade.order.filledQuantity}'",
                push,
            )

        if close_trade is not None:
            push_notifications(
                f"CLOSE TRADE:: #{close_trade.order.permId} {close_trade.order.action} {close_trade.contract.localSymbol} {close_trade.order.orderType} @{close_trade.order.lmtPrice} filled {close_trade.order.filledQuantity}'",
                push,
            )

        return open_trade, close_trade

    ticker, contract = ticker_init(contract_id = strat['contract_id'])

    # def onTickerUpdate(ticker):
    #     print(ticker.time, ' ', ticker.domBids[0].price)

    # ticker.updateEvent += onTickerUpdate

    # ib.sleep(3)

    if strat["cancel_permid"] is not None:
        cxl_order = get_order_by_permid(strat["cancel_permid"])

        if cxl_order is None:
            print(f"Failed to find order by permid {strat['cancel_permid']}")
        else:
            cxl_trade = ib.cancelOrder(cxl_order.order)
            ib.sleep(1)

            if cxl_trade.orderStatus.status == 'Cancelled':
                print("Successfully canceled {cancel.order}")
            else:
                print(f"Failed to cancel {cxl_order}")

    if strat["push"]:
        push_notifications(
            f"{strat['strategy']} / {strat['open_ticks']}:{strat['close_ticks']} tickers / ({strat['pause_replace']}_replace_sec)({strat['pause_restart']}_restart_sec)",
        )

    open_trade, close_trade = get_open_close_trades(
        strat["open_permid"], strat["close_permid"], strat["push"]
    )

    filled_close_order_ts = None
    submitted_open_order_ts = None
    total_tick_counter = 0

    if strat["debug"]:
        proceed = input("Proceed? ")

        if proceed.lower() != "y":
            exit()

    while ib.waitOnUpdate():
        print_clear()
        print_trades(status = 'Filled', tail = 5, symbol = strat["contract"])
        print("-" * 50)

        print_trades(status="Submitted", tail=5, symbol=strat["contract"])
        print("-" * 50)

        print_strategy_summary(strat, open_trade, close_trade, ticker)
        print("-" * 50)

        print_positions(contract=contract)
        print("-" * 50)

        print_account_summary(accounts=[IBKR_ACCOUNT_1])
        print(f"Session Ticks: {total_tick_counter}")
        print("-" * 50)

        if filled_close_order_ts is not None and (datetime.datetime.now() - filled_close_order_ts < datetime.timedelta(seconds=strat["pause_restart"])):
            print(
                f'Pause Restart: {strat["pause_restart"] - (datetime.datetime.now() - filled_close_order_ts).seconds} seconds ...'
            )
            continue

        # execution part - first order of the strategy
        if open_trade is None and close_trade is None:
            ib.reqPositions()

            action = strat["open_action"]
            qty = strat["open_qty"]

            if ticker is None or len(ticker.domBids) == 0 or len(ticker.domAsks) == 0:
                print(f"************ Issue getting orderbook tickers *************** ")
                # alert(True)
                ib.waitOnUpdate()
                continue

            if strat["open_ref"] == "bid":
                price_ref = ticker.domBids[0].price
            elif strat["open_ref"] == "ask":
                price_ref = ticker.domAsks[0].price
            elif strat["open_ref"] == "mid":
                price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
            elif strat["open_ref"] == "max_bid_size":
                price_ref = max(ticker.domBids, key=lambda x: x.size).price
            elif strat["open_ref"] == "max_ask_size":
                price_ref = max(ticker.domAsks, key=lambda x: x.size).price
            else:
                print("************ Invalid open_ref *************** ")
                ib.disconnect()
                exit()

            limit_price = price_ref + strat["open_ticks"] * strat["tick_increment"]

            balance_ratio = sum(bid.size for bid in ticker.domBids) / sum(ask.size for ask in ticker.domAsks)

            # orderbook balance bias checks
            if strat["open_ob_sum_bid_ask_size_ratio_min"] is not None:
                if balance_ratio < strat["open_ob_sum_bid_ask_size_ratio_min"]:
                    print(
                        f"***** Bid/Ask Size ratio {balance_ratio} < {strat['open_ob_sum_bid_ask_size_ratio_min']}"
                    )
                    continue

            if strat["open_ob_sum_bid_ask_size_ratio_max"] is not None:
                if balance_ratio > strat["open_ob_sum_bid_ask_size_ratio_max"]:
                    print(
                        f"***** Bid/Ask Size ratio {balance_ratio} > {strat['open_ob_sum_bid_ask_size_ratio_max']}"
                    )
                    continue

            # open trade checks
            if limit_price > strat["open_max"]:
                print(f"************ Limit price {limit_price} > {strat['open_max']}")
                ib.sleep(1)
                continue
            elif limit_price < strat["open_min"]:
                print(f"************ Limit price {limit_price} < {strat['open_min']} ***************")
                ib.sleep(1)
                continue
            else:
                print(f"Pre-submitting order for open_trade limit price {limit_price}")

            if strat["open_type"] == "LIMIT":
                open_order = LimitOrder(
                    action=action,
                    totalQuantity=qty,
                    lmtPrice=limit_price,
                    account=strat["account"],
                )
            else:
                raise Exception("Not implemented")

            open_order_state = ib.whatIfOrder(contract, open_order)

            print(f"Order state: {open_order_state}")

            if open_order_state is None:
                raise Exception(
                    f"************ Issue placing whatIfOrder *************** "
                )
            else:
                accountSummary = util.df(ib.accountSummary(account=strat["account"]))

                net_liquidation_value = float(
                    accountSummary[
                        accountSummary["tag"] == "NetLiquidation"
                    ].value.iloc[0]
                )

                cushion = net_liquidation_value * strat["margin_cushion_pct"] / 100

                if net_liquidation_value - cushion > float(
                    open_order_state.initMarginAfter
                ) and net_liquidation_value - cushion > float(
                    open_order_state.maintMarginAfter
                ):
                    if strat["live"]:
                        open_trade = ib.placeOrder(contract, open_order)
                        ib.sleep(0.1)

                        trade = open_trade

                        push_notifications(
                            f"OPEN ORDER PLACED :: #{trade.order.permId} {trade.orderStatus.status} {trade.contract.symbol} {trade.order.action} {trade.orderStatus.filled}/{trade.orderStatus.remaining} @ {trade.order.lmtPrice}",
                            strat["open_push"],
                        )

                    else:
                        # TODO: mock trades here
                        print(f"[NOT LIVE] OPEN ORDER PLACED :: {open_order}")

                    submitted_open_order_ts = datetime.datetime.now()

                else:
                    print(
                        f"************ Failed Margin Check: Net Liq Value {net_liquidation_value} - {cushion} cushion < (initMarginAfter {open_order_state.initMarginAfter} | maintMarginAfter {open_order_state.maintMarginAfter}) *************** "
                    )

                    # ib.cancelOrder(open_order)

                    if strat['margin_check']:
                        # alert(False)
                        print("Retrying in 25 seconds...")
                        ib.sleep(25)
                        continue

        if open_trade is not None:
            if (
                open_trade.orderStatus.status == "Inactive"
                or open_trade.orderStatus.status == "Cancelled"
            ):
                print(
                    f"OPEN TRADE STATUS CANCELLED:: {open_trade.order}",
                    strat["open_push"],
                )

                for trade_entry in open_trade.log:
                    if trade_entry.status == "Cancelled":
                        push_notifications(f"{trade_entry}", strat["open_push"])
                open_trade = None
                submitted_open_order_ts = None

            elif open_trade.orderStatus.status == "Submitted" and close_trade is None:

                if submitted_open_order_ts is not None:
                    print(
                        f'Waiting to get filled on open order #{open_trade.order.permId} ({open_trade.orderStatus.status}) / {strat["pause_replace"] - (datetime.datetime.now() - submitted_open_order_ts).seconds} seconds ...'
                    )

                    if datetime.datetime.now() - submitted_open_order_ts > datetime.timedelta(seconds=strat["pause_replace"]):
                        # find the price of opening the trade
                        if strat["open_ref"] == "bid":
                            price_ref = ticker.domBids[0].price
                        elif strat["open_ref"] == "ask":
                            price_ref = ticker.domAsks[0].price
                        elif strat["open_ref"] == "mid":
                            price_ref = (
                                ticker.domAsks[0].price + ticker.domBids[0].price
                            ) / 2
                        elif strat["open_ref"] == "max_bid_size":
                            price_ref = max(ticker.domBids, key=lambda x: x.size).price
                        elif strat["open_ref"] == "max_ask_size":
                            price_ref = max(ticker.domAsks, key=lambda x: x.size).price
                        else:
                            raise Exception("Not implemented")

                        limit_price = (
                            price_ref + strat["open_ticks"] * strat["tick_increment"]
                        )

                        # open/modify trade checks
                        if limit_price > strat["open_max"]:
                            print(f"************ Limit price {limit_price} > {strat['open_max']} ***************")
                            continue
                        elif limit_price < strat["open_min"]:
                            print(f"************ Limit price {limit_price} < {strat['open_min']} ***************")
                            continue
                        else:
                            print(f"Modifying order limit price: {open_trade.order.lmtPrice}")

                        submitted_open_order_ts = datetime.datetime.now()

                        if open_trade.order.lmtPrice == limit_price:
                            print(
                                f"Limit price of open_trade order already at {limit_price}"
                            )
                        else:
                            open_trade.order.lmtPrice = limit_price

                            print(f"Modifying open_trade order: {open_trade.order}")

                            if strat["live"]:
                                open_trade = ib.placeOrder(contract, open_trade.order)
                                push_notifications(
                                    f"MODIFIED ORDER PLACED:: {open_trade.order}",
                                    strat["modify_push"],
                                )
                            else:
                                print(
                                    f"[NOT LIVE] MODIFIED ORDER PLACED:: {open_trade.order}"
                                )

            elif open_trade.orderStatus.status == "Filled" and close_trade is None:
                ib.reqPositions()
                exec_price = open_trade.fills[0].execution.price
                print(
                    f"Filled on open_trade: {open_trade.orderStatus.status} {exec_price} {open_trade.fills[0].execution.side}"
                )

                action = strat["close_action"]
                qty = strat["close_qty"]

                # find the price to close the trade
                if strat["close_ref"] == "open_fill":
                    price_ref = exec_price
                elif strat["close_ref"] == "bid":
                    price_ref = ticker.domBids[0].price
                elif strat["close_ref"] == "ask":
                    price_ref = ticker.domAsks[0].price
                elif strat["close_ref"] == "mid":
                    price_ref = (ticker.domAsks[0].price + ticker.domBids[0].price) / 2
                else:
                    print("************ Invalid close_ref *************** ")
                    alert(True)
                    ib.sleep(10)
                    continue

                limit_price = price_ref + strat["close_ticks"] * strat["tick_increment"]

                if strat["close_type"] == "LIMIT":
                    close_order = LimitOrder(
                        action=action,
                        totalQuantity=qty,
                        lmtPrice=limit_price,
                        account=strat["account"],
                    )
                else:
                    print("************ Invalid close_type *************** ")
                    ib.disconnect()
                    exit()

                print(f"Placing close_order {close_order}")

                if strat["live"]:
                    close_trade = ib.placeOrder(contract, close_order)

                    # delay push until later for speed
                    push_notifications(
                        f"OPEN ORDER FILLED:: {open_trade.order}", strat["open_push"]
                    )
                    push_notifications(
                        f"CLOSE ORDER PLACED:: {close_trade.order}", strat["close_push"]
                    )
                    # alert(False)
                else:
                    print(f"[NOT LIVE] CLOSE ORDER PLACED:: {close_order}")
                    # print(f"CLOSE ORDER PLACED:: {close_trade.order}")

                refresh()

        if close_trade is not None:
            if close_trade.orderStatus.status == "Filled":
                push_notifications(
                    f"CLOSE TRADE FILLED:: {close_trade.order}", strat["close_push"]
                )
                alert(True)

                submitted_open_order_ts = None
                filled_close_order_ts = datetime.datetime.now()

                total_tick_counter += strat['close_qty'] * abs(
                    close_trade.orderStatus.avgFillPrice
                    - open_trade.orderStatus.avgFillPrice
                ) / strat["tick_increment"]

                open_trade = None
                close_trade = None

                refresh()

            elif (
                close_trade.orderStatus.status == "Inactive"
                or close_trade.orderStatus.status == "Cancelled"
            ):
                push_notifications(
                    f"CLOSE TRADE CANCELLED:: {close_trade.order}", strat["close_push"]
                )
                close_trade = None
                refresh()
            else:
                print(
                    f"Waiting to get filled on close_trade"
                )


BUY_SCALP_MNQ = {
    "margin_cushion_pct": 0,
    "account": IBKR_ACCOUNT_1,
    "close_qty": 2,
    "close_type": "LIMIT",
    "close_action": "SELL",
    "close_ref": "open_fill",
    "close_permid": None,
    "strategy": "BUY TO OPEN SCALP",
    "contract": "MNQU4",
    "open_qty": 2,
    "open_type": "LIMIT",
    "open_action": "BUY",
    "open_ob_sum_bid_ask_size_ratio_min": 0,
    "open_ob_sum_bid_ask_size_ratio_max": 1,
    "open_min": 0,
    "open_max": 19147,
    "open_permid": None,
    "open_ref": "max_bid_size",
    "open_ticks": -20,
    "close_ticks": 120,
    "cancel_permid": None,
    "pause_replace": 60,
    "pause_restart": 15,
    "tick_increment": 0.10,
}

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My Python Script')
    parser.add_argument('--contract', type=str, help='Contract', default='MNQU4')
    parser.add_argument('--strat', type=str, help='Strategy', default='buy')
    parser.add_argument("--open_id", type=int, help="Open ID", default=None)
    parser.add_argument('--close_id', type=int, help='Close ID', default=None)
    parser.add_argument("--cancel_id", type=int, help="Cancel ID", default=None)
    parser.add_argument("--open_ticks", type=int, help="Open Ticks", default=None)
    parser.add_argument("--close_ticks", type=int, help="Close Ticks", default=None)
    parser.add_argument("--open_max", type=int, help="Open Max", default=None)
    parser.add_argument("--open_min", type=int, help="Open Min", default=None)
    parser.add_argument("--debug", type=bool, help="Debug", default=False)
    parser.add_argument("--open_push", type=bool, help="Open Push", default=True)
    parser.add_argument("--modify_push", type=bool, help="Modify Push", default=False)
    parser.add_argument("--close_push", type=bool, help="Close Push", default=True)
    parser.add_argument("--push", type=bool, help="Push", default=False)
    parser.add_argument("--live", type=bool, help="Live", default=True)
    parser.add_argument("--margin_check", type=bool, help="Margin Check", default=True)
    parser.add_argument("--pause_replace", type=int, help="Pause Replace (sec)", default=None)
    parser.add_argument("--pause_restart", type=int, help="Pause Restart (sec)", default=None)

    args = parser.parse_args()

    if args.strat == "buy" or args.strat == "BUY_SCALP":
        STRATEGY = BUY_SCALP_MNQ
    else:
        print(f"*** Invalid strategy {args.strat} ***")
        ib.disconnect()
        exit(0)

    STRATEGY["contract"] = (
        args.contract if args.contract is not None else STRATEGY["contract"]
    )

    STRATEGY["contract_id"] = CONTRACT_SYM[STRATEGY["contract"]]

    STRATEGY["open_max"] = int(args.open_max) if args.open_max is not None else STRATEGY["open_max"]
    STRATEGY["open_min"] = int(args.open_min) if args.open_min is not None else STRATEGY["open_min"]
    STRATEGY["open_ticks"] = int(args.open_ticks) if args.open_ticks is not None else STRATEGY["open_ticks"]
    STRATEGY["close_ticks"] = int(args.close_ticks) if args.close_ticks is not None else STRATEGY["close_ticks"]
    STRATEGY["open_permid"] = int(args.open_id) if args.open_id is not None else STRATEGY["open_permid"]
    STRATEGY["close_permid"] = int(args.close_id) if args.close_id is not None else STRATEGY["close_permid"]
    STRATEGY["open_push"] = args.open_push if args.open_push is not None else STRATEGY["open_push"]
    STRATEGY["close_push"] = args.close_push if args.close_push is not None else STRATEGY["close_push"]
    STRATEGY["push"] = args.push if args.push is not None else STRATEGY["push"]
    STRATEGY["debug"] = args.debug if args.debug is not None else STRATEGY["debug"]
    STRATEGY["margin_check"] = args.margin_check if args.margin_check is not None else STRATEGY["margin_check"]
    STRATEGY["modify_push"] = args.modify_push if args.modify_push is not None else STRATEGY["modify_push"]
    STRATEGY["live"] = args.live if args.live is not None else STRATEGY["live"]
    STRATEGY["pause_replace"] = args.pause_replace if args.pause_replace is not None else STRATEGY["pause_replace"]
    STRATEGY["pause_restart"] = args.pause_restart if args.pause_restart is not None else STRATEGY["pause_restart"]

    try:
        pprint.pprint(f"STRATEGY CONFIG: \n {STRATEGY}")
        simple_scalp(STRATEGY)

    except KeyboardInterrupt:
        print('Interrupted')

    ib.disconnect()
    exit(0)
