from tools import *
from monitor import *
from strategies import *
from alerts import *


parser = argparse.ArgumentParser(description="IBKR Script")
parser.add_argument(
    "--dur",
    type=int,
    default=1,
    help="Duration for monitoring overview (in minutes)",
)
parser.add_argument(
    "--strat",
    type=str,
    choices=["ss_buy", "ss_sell", "monitor"],
    help="Strategy details: 1) ss_buy, 2) ss_sell, 3) monitor",
)
parser.add_argument(
    "--open",
    type=int,
    help="Open permId",
    default=None
)
parser.add_argument(
    "--close",
    type=int,
    help="Close permId",
    default=None,
)
args = parser.parse_args()


if __name__ == "__main__":
    print_line()
    print(args)

    # monitor_overview(duration=args.dur)

    if args.strat == "ss_buy":
        run_simple_scalp(
            strategy_details=BUY_SCALP,
            open_permId=args.open,
            close_permId=args.close,
            cancel_permids=[],
        )
    elif args.strat == "ss_sell":
        run_simple_scalp(
            strategy_details=SELL_SCALP,
            open_permId=args.open,
            close_permId=args.close,
            cancel_permids=[],
        )
    elif args.strat is None:
        if args.dur:
            monitor_overview(duration=args.dur)
        else:
            monitor_overview()

    print_line()
