from IPython.core.display import HTML
from IPython.display import display, clear_output

display(HTML("<style>.output_subarea { overflow: auto; }</style>"))


def print_reqOpenOrders():
    print(f"Session Orders::")
    display(util.df([t.order for t in ib.reqOpenOrders()]))


def print_reqAllOpenOrders():
    print(f"All Session Orders:")
    display(util.df([t.order for t in ib.reqAllOpenOrders()]))
