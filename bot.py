#!/usr/bin/python
import os
import json
import requests
import hmac
import base64
import time
import hashlib
import requests
import websocket


tradingApiUrl = "https://api.hotbit.io/api/v1"
Api_key = "db35aa17-df09-df84-69a06822294e6d2e"
secret = "882c54dc544140033fbcc8073b1d528f"


def sendGetRequest(url):
    r = requests.get(tradingApiUrl + url)
    return r.json()


def sendPostRequest(url):
    r = requests.post(tradingApiUrl + url)
    return r.json()


def getBalance():
    # Parameters
    assets = '["BTC","CPU"]'
    query = "/balance.query?"
    callString = 'api_key=' + Api_key + '&assets=' + assets + '&secret_key=' + secret
    Sign = hashlib.md5(callString.encode('utf-8')).hexdigest().upper()
    SignString = 'api_key=' + Api_key + '&sign=' + Sign + '&assets=' + assets
    # End Parameters
    response = sendGetRequest(query + SignString)
    BTCBalance = response['result']['BTC']['available']
    CPUBalance = response['result']['CPU']['available']
    print(BTCBalance)
    print(CPUBalance)
    return BTCBalance, CPUBalance


def getLatestPrice():
    query = "/market.last?market=CPU/BTC"
    response = sendGetRequest(query)
    LastTrade = response['result']
    print(LastTrade)
    return LastTrade


def getOrderBook():
    # Get Sell Price
    market = "CPU/BTC"
    side = "1"  # 1 = Sell, 2 = Buy
    offset = "0"  # Default to 0
    limit = "10"  # Amount of orders to return
    http = "/order.book?"  # request method
    query = http + 'market=' + market + '&side=' + \
        side + '&offset=' + offset + '&limit=' + limit
    response = sendGetRequest(query)
    SellPrice = response['result']['orders'][0]['price']
    # Get Buy Price
    query = "/order.book?market=CPU/BTC&side=2&offset=0&limit=10"
    response = sendGetRequest(query)
    BuyPrice = response['result']['orders'][0]['price']
    return SellPrice, BuyPrice


def Deals():
    query = '/market.user_deals?'
    CallString = 'api_key=' + Api_key + \
        '&limit=1&market=CPU/BTC&offset=0&secret_key=' + secret
    Sign = hashlib.md5(CallString.encode('utf-8')).hexdigest().upper()
    SignString = 'api_key=' + Api_key + '&sign=' + \
        Sign + '&market=CPU/BTC&offset=0&limit=1'
    response = sendGetRequest(query + SignString)
    showSide = response['result']['records'][0]['side']
    print(showSide)
    return showSide

    # print(SignString)


SellPrice, BuyPrice = getOrderBook()
LastTrade = getLatestPrice()
BTCBalance, CPUBalance = getBalance()

BuyPrice = '{0:.8f}'.format(float(BuyPrice))
SellPrice = '{0:.8f}'.format(float(SellPrice))


def sellOrder():
    query = '/order.put_limit?'
    CallString = 'amount=100&api_key=' + Api_key + \
        '&isfee=1&market=CPU/BTC&price=' + \
        str(LastTrade) + '&side=1&secret_key=' + secret
    Sign = hashlib.md5(CallString.encode('utf-8')).hexdigest().upper()
    SignString = 'api_key=' + Api_key + '&sign=' + \
        Sign + '&market=CPU/BTC&side=1&amount=100&price=' + \
        str(LastTrade) + '&isfee=1'
    response = sendGetRequest(query + SignString)
    print(response)


def buyOrder():
    query = '/order.put_limit?'
    CallString = 'amount=100&api_key=' + Api_key + \
        '&isfee=1&market=CPU/BTC&price=' + LastTrade + '&side=2&secret_key=' + secret
    Sign = hashlib.md5(CallString.encode('utf-8')).hexdigest().upper()
    SignString = 'api_key=' + Api_key + '&sign=' + \
        Sign + '&market=CPU/BTC&side=2&amount=100&price=' + LastTrade + '&isfee=1'
    response = sendGetRequest(query + SignString)
    print(response)


def getOpenOrders():
    query = '/order.pending?'
    CallString = 'api_key=' + Api_key + \
        '&limit=10&market=CPU/BTC&offset=0&secret_key=' + secret
    Sign = hashlib.md5(CallString.encode('utf-8')).hexdigest().upper()
    SignString = 'api_key=' + Api_key + '&sign=' + \
        Sign + '&limit=10&market=CPU/BTC&offset=0'
    response = sendGetRequest(query + SignString)
    # builder = [0, 1, 2, 3]
    counter = 0
    # orderList = []
    if True:
        try:
            orderID = response['result']['CPUBTC']['records'][counter]['id']
        except:
            orderID = "empty"
    # for i in builder:
    #     while i < 3:
    #         counter += 1
    #         orderID = response['result']['CPUBTC']['records'][counter]['id']
    #         appender = str(orderID)
    #         orderList.append(appender)
    #         i += 1
    # print(orderList)
    return orderID


orderID = getOpenOrders()


def cancelOrders():
    query = '/order.batch_cancel?'
    CallString = 'api_key=' + Api_key + \
        '&market=CPU/BTC&orders_id=[' + str(orderID) + ']&secret_key=' + secret
    Sign = hashlib.md5(CallString.encode('utf-8')).hexdigest().upper()
    SignString = 'api_key=' + Api_key + '&sign=' + \
        Sign + '&market=CPU/BTC&orders_id=[' + str(orderID) + ']'
    response = sendGetRequest(query + SignString)
    # print(response)


showSide = Deals()


def makeTrades():
    print("Sold")
    sellOrder()
    print(CPUBalance)
    print("Bought")
    buyOrder()
    print(CPUBalance)


set_cut_off_balance = 0.0000032

if float(BTCBalance) < set_cut_off_balance and orderID != "empty":
    cancelOrders()
else:
    makeTrades()
    print("executing trade")

os.system("python bot.py")
