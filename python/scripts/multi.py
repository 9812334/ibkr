import multiprocessing
import yfinance as yf

def fetch_stock_data(ticker, conn):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    conn.send(data)
    conn.close()

def process_stock_data(queue):
    while True:
        try:
            data = queue.get(timeout=1)
            if data is None:
                break
            print(f"Processing data for {data.iloc[0].name}:")
            print(data)
        except multiprocessing.queues.Empty:
            break

def main():
    tickers = ["AAPL", "GOOGL", "MSFT"]
    queue = multiprocessing.Queue()
    processes = []

    for ticker in tickers:
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=fetch_stock_data, args=(ticker, child_conn))
        processes.append(p)
        p.start()
        queue.put(parent_conn.recv())

    processing_process = multiprocessing.Process(target=process_stock_data, args=(queue,))
    processing_process.start()

    for p in processes:
        p.join()

    queue.put(None)
    processing_process.join()