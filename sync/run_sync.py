from mt5_connector import MT5Connector

print("--------------------------------")
print("TradeHub Sync")
print("--------------------------------")

MT5Connector.connect()

account = MT5Connector.account()

print(account)

positions = MT5Connector.positions()

print(f"Open Positions: {len(positions)}")

MT5Connector.disconnect()

print("Finished.")