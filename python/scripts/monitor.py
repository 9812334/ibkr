from tools import *

parser = argparse.ArgumentParser(description="IBKR Script")
parser.add_argument(
    "--dur",
    type=int,
    default=1,
    help="Duration for monitoring overview (in seconds)",
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



def monitor_overview(duration=5):
    executions = []
    positions = []
    open_orders = []
    
    while ib.sleep(duration):        
        print_clear()
        print("-" * 50)

        print_account_summary(accounts = ["U10394496"])
        print("-" * 50)

        current_executions = print_executions()
        print("-" * 50)

        if len(current_executions) != len(executions):
            alert()        

        current_open_orders = print_openOrders()
        
        if len(current_open_orders) != len(open_orders):
            ib.reqExecutions()
            
        print("-" * 50)

        current_positions = print_positions(contract=NQM4)
        print("-" * 50)
        
        print_orderbook()
        print("-" * 50)

        executions = current_executions
        open_orders = current_open_orders
        positions = current_positions



if __name__ == "__main__":
    print(args)
    # ticker = ticker_init()
    monitor_overview(duration=args.dur)
