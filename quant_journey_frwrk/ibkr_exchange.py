import asyncio
import sys
import yaml
import pika
import json
import socket
from ib_async import IB, Stock, Forex, Contract, Order, util
import pandas as pd
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

# Logger setup (Assuming a similar setup as in the previous examples)
from qlib.data.utils.data_logs import data_logger
import qlib.data.utils.data_logs as dlogs

# Logger for IBKR
LOG_TO_SCREEN = False
LOG_TO_FILE = True


class IBKRExchange:
    def __init__(
        self,
        ib_client_id: int = 1,
        ib_port: int = 4001,
        ib_host: str = "127.0.0.1",
        rabbitmq_host: str = "192.168.1.64",
        rabbitmq_port: int = 5672,
        config_path="config_ibkr.json",
    ):

        # Load configuration
        try:
            with open(config_path, "r") as file:
                self.config = yaml.safe_load(file)

            # Setup IBKR connection parameters
            ibkr_config = self.config.get("ibkr", {})
            self.ib_client_id = ibkr_config.get("client_id", ib_client_id)
            self.ib_port = ibkr_config.get("port", ib_port)
            self.ib_host = ibkr_config.get("host", ib_host)

            # Setup RabbitMQ parameters
            rabbitmq_config = self.config.get("rabbitmq", {})
            self.rabbitmq_host = rabbitmq_config.get("host", rabbitmq_host)
            self.rabbitmq_port = rabbitmq_config.get("port", rabbitmq_port)

            # Other configurations like trading and logging
            self.paper_trading_mode = self.config.get("trading", {}).get(
                "paper_trading_mode", False
            )

            self.logger = self.ibkr_exchange_logger()
            self.logger.info("IBKRExchange initialized")

            ibkr_logger = self.logger

            logger.info("IBKR: Configuration loaded successfully.")
            ibkr_logger.info("IBKRExchange initialized")

        except Exception as e:
            logger.error(f"An error occurred while loading the configuration: {e}")
            raise e

        # Connect to the Interactive Brokers trading platform
        try:
            self.ib = IB()
            self.ib.connect(
                host=self.ib_host, ib_port=self.ib_port, clientId=self.ib_client_id
            )
            logger.info("IBKR: Successfully connected to Interactive Brokers.")
        except Exception as e:
            logger.error(f"Failed to connect to Interactive Brokers: {e}")
            raise e

    def close(self):
        self.disconnect()

    def __del__(self):
        self.close()

    def get_ibkr_log_filenames(self):
        # This could call get_log_filenames with the '_transactions' subdir
        return logsc.get_log_filenames(subdir="_transactions")

    def ibkr_exchange_logger(self):
        """
        Separate logger function (to log transactions, and things related to OrdersExecutor)
        """
        logger = logging.getLogger("IBKRExchange")
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()  # Clear existing handlers
        logger.propagate = False

        info_log_file, error_log_file = (
            self.get_ibkr_log_filenames()
        )  # Use the new function

        info_handler = logging.FileHandler(info_log_file)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(
            logging.Formatter("[%(asctime)s] [%(levelname)s]-%(message)s")
        )

        error_handler = logging.FileHandler(error_log_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter("[%(asctime)s] [%(levelname)s]-%(message)s")
        )

        if LOG_TO_SCREEN:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(
                dlogs.ColorFormatter()
            )  #  Color formatter for console output from data_logs
            logger.addHandler(console_handler)

        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

        return logger

    def disconnect(self):
        """
        Disconnect from the Interactive Brokers trading platform.
        """
        self.ib.disconnect()
        logger.info("IBKR: Disconnected from the Interactive Brokers trading platform.")

    def get_account_summary(self) -> Dict:
        """
        Retrieve the account summary from the IB trading account.

        Returns:
         dict: A dictionary containing various account summary metrics such as net liquid value, total cash value,
            and unrealized profit/loss.
        """
        try:
            account_summary = {
                summary.tag: summary.value for summary in self.ib.accountSummary()
            }
            logger.info("IBKR: Account summary retrieved successfully.")
            return account_summary
        except Exception as e:
            logger.error(f"IBKR: Failed to retrieve account summary: {e}")
            return {}

    def get_contract_details(
        self,
        symbol: str,
        secType: str = "STK",
        currency: str = "USD",
        exchange: str = "SMART",
    ) -> Contract:
        """
        Retrieve the contract details for a given security.

        Args:
         symbol (str): The ticker symbol of the security.
         secType (str): The security type (e.g., "STK" for stocks).
         currency (str): The currency of the security.
         exchange (str): The exchange where the security is traded.

        Returns:
         Contract: The contract object representing the security.
        """
        if secType == "STK":
            contract = Stock(symbol, exchange, currency)
        elif secType == "FX":
            contract = Forex(symbol)
        else:
            contract = Contract(
                symbol=symbol, secType=secType, exchange=exchange, currency=currency
            )

        try:
            contract_details = self.ib.reqContractDetails(contract)
            if contract_details:
                logger.info(f"Contract details found for {symbol}.")
                return contract_details[0].contract
            else:
                logger.error(f"IBKR: No contract details found for {symbol}")
                return None
        except Exception as e:
            logger.error(f"IBKR: Error retrieving contract details for {symbol}: {e}")
            return None

    def get_open_orders(self) -> List[Order]:
        """
        Retrieve open orders from the IB trading account.

        Returns:
         List[Order]: A list of open orders.
        """
        try:
            open_orders = self.ib.openOrders()
            logger.info("IBKR: Open orders retrieved successfully.")
            return open_orders
        except Exception as e:
            logger.error(f"IBKR: Failed to retrieve open orders: {e}")
            return []

    def calculate_trading_fees(
        self, contract: Contract, action: str, quantity: int, price: float
    ) -> float:
        """
        Calculate trading fees for a given order.

        Note: This is a basic implementation using IBKR's fixed rate for US stocks. You should adjust the logic
           according to the specific fee structure for your account and the asset being traded.

        Args:
         contract (Contract): The contract object representing the security.
         action (str): The action to take (e.g., "BUY" or "SELL").
         quantity (int): The quantity of shares to buy or sell.
         price (float): The price per share.

        Returns:
         float: The estimated trading fee.
        """
        if contract.secType != "STK" or contract.currency != "USD":
            logger.warning(
                f"Unsupported contract type or currency for fee calculation: {contract}"
            )
            return 0.0

        # IBKR's fixed rate for US stocks (as of April 2023): USD 0.005 per share (min USD 1.00, max 1% of trade value)
        fee_per_share = 0.005
        fee = max(1.0, min(fee_per_share * quantity * price, 0.01 * quantity * price))
        return fee

    def place_order(
        self,
        contract: Contract,
        order_type: str = "MKT",
        action: str = "BUY",
        quantity: int = 1,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> Dict:
        """
        Place an order with specified parameters.
        """

        if contract is None:
            logger.info("IBKR: Cannot place order: Contract is None.")
            return {"orderId": None, "status": "Error"}

        order = Order()
        order.action = action
        order.totalQuantity = quantity
        order.orderType = order_type
        if limit_price is not None:
            order.lmtPrice = limit_price
        if stop_price is not None:
            order.auxPrice = stop_price

        try:
            if self.paper_trading_mode:
                logger.info(
                    "IBKR: Paper trading mode: Order will be simulated without execution."
                )
                trade = self.ib.placeOrder(contract, order, transmit=False)
            else:
                trade = self.ib.placeOrder(contract, order)
            self.ib.waitOnUpdate()
            logger.info(
                f"Order placed: {trade.order.orderId}, Status: {trade.orderStatus.status}"
            )
            return {"orderId": trade.order.orderId, "status": trade.orderStatus.status}
        except Exception as e:
            logger.error(f"IBKR: Error placing order: {e}")
            return {"orderId": None, "status": "Error"}

    def modify_order(
        self,
        order_id: int,
        quantity: Optional[int] = None,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> Dict:
        """
        Modify an existing order with specified parameters.
        """
        try:
            order = self.ib.modifyOrder(order_id, quantity, limit_price, stop_price)
            self.ib.waitOnUpdate()

            logger.info(f"Modifying order: {order_id}")
            return {"orderId": order.orderId, "status": order.status}
        except Exception as e:
            logger.error(f"IBKR: Error modifying order: {e}")
            return {"orderId": order_id, "status": "Error"}

    def cancel_order(self, order_id: int) -> Dict:
        """
        Cancel an existing order.
        """
        try:
            self.ib.cancelOrder(order_id)
            self.ib.waitOnUpdate()

            logger.info(f"Order cancelled successfully: {order_id}")
            return {"orderId": order_id, "status": "Cancelled"}
        except Exception as e:
            logger.error(f"IBKR: Error cancelling order: {e}")
            return {"orderId": order_id, "status": "Error"}

    def get_positions(self) -> pd.DataFrame:
        """
        Retrieve the current positions from the IB trading account.

        Returns:
         list of dict: A list of dictionaries, where each dictionary represents a position and contains
              information such as symbol, position, average cost, and market price.
        """
        positions = []
        for position in self.ib.positions():
            contract = position.contract
            position_data = {
                "symbol": contract.symbol,
                "position": position.position,
                "avgCost": position.avgCost,
                "marketPrice": position.marketPrice,
            }
            positions.append(position_data)
        return positions

    async def get_historical_data(
        self,
        contract: Contract,
        end_date: datetime,
        duration: str = "1 Y",
        bar_size: str = "1 day",
        what_to_show: str = "TRADES",
    ) -> pd.DataFrame:
        """
        Retrieve historical data for a given security.

        Args:
         contract (Contract): The contract object representing the security.
         end_date (datetime): The end date for the historical data.
         duration (str): The duration for which to retrieve historical data (e.g., "1 Y" for 1 year).
         bar_size (str): The bar size for the historical data (e.g., "1 day", "1 hour").
         what_to_show (str): The type of historical data to retrieve (e.g., "TRADES", "MIDPOINT").

        Returns:
         pd.DataFrame: A DataFrame containing the historical data for the security.
        """
        try:
            bars = await self.ib.reqHistoricalDataAsync(
                contract,
                endDateTime=end_date,
                durationStr=duration,
                barSizeSetting=bar_size,
                whatToShow=what_to_show,
                useRTH=True,
                formatDate=1,
            )
            df = util.df(bars)
            return df
        except Exception as e:
            logger.error(f"IBKR: Error retrieving historical data: {e}")
            return pd.DataFrame()

    async def get_real_time_data(
        self, contract: Contract, data_type: str = "TRADES"
    ) -> pd.DataFrame:
        """
        Retrieve real-time market data for a given security.

        Args:
         contract (Contract): The contract object representing the security.
         data_type (str): The type of real-time data to retrieve (e.g., "TRADES", "MIDPOINT", "LEVEL2").

        Returns:
         pd.DataFrame: A DataFrame containing the real-time market data for the security.
        """
        try:
            ticks = await self.ib.reqTickDataAsync(contract, data_type)
            df = util.df(ticks)
            return df
        except Exception as e:
            logger.error(f"IBKR: Error retrieving real-time data: {e}")
            return pd.DataFrame()

    def set_stop_loss(
        self,
        contract: Contract,
        order_type: str,
        action: str,
        quantity: int,
        stop_price: float,
        trail_percent: Optional[float] = None,
    ) -> Dict:
        """
        Set a stop-loss order for a given security.

        Args:
         contract (Contract): The contract object representing the security.
         order_type (str): The type of order (e.g., "STP" for stop order).
         action (str): The action to take (e.g., "BUY" or "SELL").
         quantity (int): The quantity of shares to buy or sell.
         stop_price (float): The stop price for the stop-loss order.
         trail_percent (float, optional): The trailing amount in percentage for a trailing stop-loss order.

        Returns:
         dict: A dictionary containing the order details.
        """
        order = Order()
        order.action = action
        order.orderType = order_type
        order.totalQuantity = quantity
        order.auxPrice = stop_price
        if trail_percent is not None:
            order.trailStopPercent = trail_percent

        try:
            trade = self.ib.placeOrder(contract, order)
            self.ib.waitOnUpdate()
            return {"orderId": trade.order.orderId, "status": trade.orderStatus.status}
        except Exception as e:
            logger.error(f"IBKR: Error setting stop-loss order: {e}")
            return {"orderId": None, "status": "Error"}

    def set_take_profit(
        self,
        contract: Contract,
        order_type: str,
        action: str,
        quantity: int,
        limit_price: float,
    ) -> Dict:
        """
        Set a take-profit order for a given security.

        Args:
         contract (Contract): The contract object representing the security.
         order_type (str): The type of order (e.g., "LMT" for limit order).
         action (str): The action to take (e.g., "BUY" or "SELL").
         quantity (int): The quantity of shares to buy or sell.
         limit_price (float): The limit price for the take-profit order.

        Returns:
         dict: A dictionary containing the order details.
        """
        order = Order()
        order.action = action
        order.orderType = order_type
        order.totalQuantity = quantity
        order.lmtPrice = limit_price

        try:
            trade = self.ib.placeOrder(contract, order)
            self.ib.waitOnUpdate()
            return {"orderId": trade.order.orderId, "status": trade.orderStatus.status}
        except Exception as e:
            logger.error(f"IBKR: Error setting take-profit order: {e}")
            return {"orderId": None, "status": "Error"}

    # Websocket-based real-time market data subscription ----------------------------

    def start_real_time_market_data(self, contract: Contract):
        """
        Start receiving real-time market data for a given security using websockets.

        Args:
         contract (Contract): The contract object representing the security.
        """
        try:
            self.ws = self.ib.WebSocket(self.on_message, self.on_close, self.on_error)
            self.ws.connect()
            self.ws.reqMktData(contract)
            logger.info(f"Subscribed to real-time market data for {contract.symbol}.")
        except Exception as e:
            logger.error(f"IBKR: Error subscribing to real-time market data: {e}")

    def on_message(self, msg):
        """
        Handle incoming real-time data messages.

        Args:
         msg (dict): The received message containing real-time data.
        """
        # Process the received real-time data, update internal state or send to other parts of your application
        pass

    def on_close(self):
        """
        Handle websocket connection closure.
        """
        logger.info("IBKR: Websocket connection closed.")

    def on_error(self, error):
        """
        Handle websocket errors.

        Args:
         error (str): The error message.
        """
        logger.error(f"IBKR: Websocket error: {error}")

    # Signal Processing and Executing ----------------------------------------------

    def is_rabbitmq_available(self, host, port):
        """
        Check if RabbitMQ is available on the specified host and port.

        Args:
         host (str): The hostname or IP address of the RabbitMQ server.
         port (int): The port number of the RabbitMQ server.

        Returns:
         bool: True if RabbitMQ is available, False otherwise.
        """
        try:
            # Create a socket and attempt to connect to the RabbitMQ server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.close()
            return True
        except socket.error:
            return False

    def listen_for_signals(self):
        """
        Start listening for trading signals from RabbitMQ.
        """
        if not self.is_rabbitmq_available(self.rabbitmq_host, self.rabbitmq_port):
            logger.error("RabbitMQ is not available or not running.")
            self.logger.error("RabbitMQ is not available or not running.")
            return

        try:
            connection_parameters = pika.ConnectionParameters(
                host=self.rabbitmq_host, port=self.rabbitmq_port
            )
            connection = pika.BlockingConnection(connection_parameters)
            channel = connection.channel()
            channel.queue_declare(queue="trading_signals")

            def callback(ch, method, properties, body):
                try:
                    signal = json.loads(body)
                    logger.info(f"Received signal: {signal}")
                    self.logger.info(f"Received signal: {signal}")
                    # Process the signal to place an order
                    asyncio.run(self.process_signal(signal))
                except Exception as e:
                    logger.error(f"Error processing trading signal: {e}")
                    self.logger.error(f"Error processing trading signal: {e}")

            channel.basic_consume(
                queue="trading_signals", on_message_callback=callback, auto_ack=True
            )
            logger.info("Waiting for trading signals. To exit press CTRL+C")
            self.logger.info("Waiting for trading signals. To exit press CTRL+C")
            channel.start_consuming()

        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")
            self.logger.error(f"Error connecting to RabbitMQ: {e}")

    async def process_signal(self, signal):
        """
        Process the trading signal to execute trades.

        Args:
         signal (dict): The trading signal containing details for the trade.
        """
        try:
            # Example: Extract details from the signal
            symbol = signal.get("symbol")
            action = signal.get("action")  # BUY or SELL
            quantity = signal.get("quantity")
            order_type = signal.get("order_type", "MKT")  # Default to Market Order

            # Get the contract details
            contract = self.get_contract_details(symbol)
            if contract:
                # Place the order based on the signal
                order_response = self.place_order(
                    contract, order_type, action, quantity
                )
                logger.info(f"Order Response: {order_response}")
                self.logger.info(f"Order Response: {order_response}")
            else:
                logger.error(f"Failed to get contract details for {symbol}")
                self.logger.error(f"Failed to get contract details for {symbol}")
        except Exception as e:
            logger.error(f"Error processing trading signal: {e}")
            self.logger.error(f"Error processing trading signal: {e}")
