import asyncio
import logging
from dotenv import load_dotenv
import os
import aiohttp
from datetime import datetime, timedelta
from bot import marketplay_bot, send_excel
from database import session, Order, Sale, Chat
import pandas as pd
import sys
load_dotenv()

WB_TOKEN = os.getenv('WB_TOKEN')



async def process_orders_data(orders_data):
    for order_data in orders_data:
        existing_order = session.query(Order).filter_by(nm_id=order_data['nmId']).first()
        if existing_order:
            existing_order.last_change_date = datetime.strptime(order_data['lastChangeDate'], '%Y-%m-%dT%H:%M:%S')
            existing_order.total_price = order_data['totalPrice']
            existing_order.order_type = order_data['orderType']
            existing_order.g_number = order_data['gNumber']
            existing_order.srid = order_data['srid']
        else:
            new_order = Order(
                date=datetime.strptime(order_data['date'], '%Y-%m-%dT%H:%M:%S'),
                last_change_date=datetime.strptime(order_data['lastChangeDate'], '%Y-%m-%dT%H:%M:%S'),
                warehouse_name=order_data['warehouseName'],
                country_name=order_data['countryName'],
                oblast_okrug_name=order_data['oblastOkrugName'],
                region_name=order_data['regionName'],
                supplier_article=order_data['supplierArticle'],
                nm_id=order_data['nmId'],
                barcode=order_data['barcode'],
                category=order_data['category'],
                subject=order_data['subject'],
                brand=order_data['brand'],
                total_price=order_data['totalPrice'],
                order_type=order_data['orderType'],
                sticker=order_data['sticker'],
                g_number=order_data['gNumber'],
                srid=order_data['srid']
            )
            session.add(new_order)
    session.commit()


async def process_sales_data(sales_data):
    for sale_data in sales_data:
        existing_sale = session.query(Sale).filter_by(nm_id=sale_data['nmId']).first()
        if existing_sale:
            existing_sale.last_change_date = datetime.strptime(sale_data['lastChangeDate'], '%Y-%m-%dT%H:%M:%S')
            existing_sale.total_price = sale_data['totalPrice']
            existing_sale.for_pay = sale_data['forPay']
            existing_sale.order_type = sale_data['orderType']
            existing_sale.g_number = sale_data['gNumber']
            existing_sale.srid = sale_data['srid']
        else:
            new_sale = Sale(
                date=datetime.strptime(sale_data['date'], '%Y-%m-%dT%H:%M:%S'),
                last_change_date=datetime.strptime(sale_data['lastChangeDate'], '%Y-%m-%dT%H:%M:%S'),
                warehouse_name=sale_data['warehouseName'],
                country_name=sale_data['countryName'],
                oblast_okrug_name=sale_data['oblastOkrugName'],
                region_name=sale_data['regionName'],
                supplier_article=sale_data['supplierArticle'],
                nm_id=sale_data['nmId'],
                barcode=sale_data['barcode'],
                category=sale_data['category'],
                subject=sale_data['subject'],
                brand=sale_data['brand'],
                total_price=sale_data['totalPrice'],
                for_pay=sale_data['forPay'],
                order_type=sale_data['orderType'],
                sticker=sale_data['sticker'],
                g_number=sale_data['gNumber'],
                srid=sale_data['srid']
            )
            session.add(new_sale)
    session.commit()


async def create_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)


async def fetch_data(url, headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error fetching data: {response.status}")
                return None


async def main():
    while True:
        chats = session.query(Chat).all()
        current_datetime = datetime.now()
        date_from = current_datetime - timedelta(minutes=30)
        date_from_str = date_from.strftime('%Y-%m-%dT%H:%M:%S')
        headers = {
            'Authorization': f'Bearer {WB_TOKEN}'
        }
        orders_url = f'https://statistics-api.wildberries.ru/api/v1/supplier/orders?dateFrom={date_from_str}&flag=0'
        sales_url = f'https://statistics-api.wildberries.ru/api/v1/supplier/sales?dateFrom={date_from_str}&flag=0'

        orders_data = await fetch_data(orders_url, headers)
        sales_data = await fetch_data(sales_url, headers)

        if orders_data:
            await process_orders_data(orders_data)
            await create_excel(orders_data, 'orders.xlsx')
            print("Orders data retrieved successfully.")
        if sales_data:
            await process_sales_data(sales_data)
            await create_excel(sales_data, 'sales.xlsx')
            print("Sales data retrieved successfully.")
        for chat in chats:
            await send_excel(chat.chat_id, "orders.xlsx")
            await send_excel(chat.chat_id, "sales.xlsx")
        await asyncio.sleep(1800)


async def run_both():
    await asyncio.gather(main(), marketplay_bot())


if __name__ == "__main__":
    asyncio.run(run_both())
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
