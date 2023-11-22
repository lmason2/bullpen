import base64
import json
import threading
import random
import time
import uuid 
import requests

seats = [
    '1a', '2a', '3a', '4a', '5a',
    '1b', '2b', '3b', '4b', '5b',
    '1c', '2c', '3c', '4c', '5c']

def perform_order(round, index, session_id, products):
    print(f'Round: {round} - Order: {index} - Session_id: {session_id}')
    order_id = str(uuid.uuid4())
    PAYLOAD = {
        'order_id': order_id,
        "session_id": session_id,
        'product_ids': products,
        'seat': random.choice(seats),
    }
    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())
    response = requests.post('http://localhost:8000/api/bullpen/v1/open-order', data=encoded_payload)
    print('open order')
    print(json.dumps(response.text))
    print()

    time.sleep(1)
    print('update 1')
    PAYLOAD = {
        "order_id": order_id,
        "session_id": session_id,
        'status': 'received',
    }

    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())
    response = requests.post('http://localhost:8000/api/bullpen/v1/update-order', data=encoded_payload)

    time.sleep(1)
    print('update 2')
    PAYLOAD = {
        "order_id": order_id,
        "session_id": session_id,
        'status': 'fulfilled',
    }

    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())
    response = requests.post('http://localhost:8000/api/bullpen/v1/update-order', data=encoded_payload)

    time.sleep(1)
    print('update 3')
    PAYLOAD = {
        "order_id": order_id,
        "session_id": session_id,
        'status': 'delivered',
    }

    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())
    response = requests.post('http://localhost:8000/api/bullpen/v1/update-order', data=encoded_payload)

    print(f'finished: {round} - {index}')

def main():
    HEADERS = {
    }

    PAYLOAD = {
    }

    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())
    response = requests.post('http://localhost:8000/api/bullpen/v1/get-products', data=encoded_payload, headers=HEADERS)
    products = json.loads(response.text)['data']
    product_ids = []
    for product in products:
        product_ids.append(product['product_id'])

    PAYLOAD = {
        'session_name': 'test_session_one',
        'team_id': "5fa7a7f1-7a35-40a1-b830-038d942a48d0",
    }

    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

    response = requests.post('http://localhost:8000/api/bullpen/v1/open-session', data=encoded_payload)
    session_id = json.loads(response.text)['data']['session_id']
    print('opening session')

    round = 1
    generate_transactions = True
    while generate_transactions:
        time.sleep(5)

        threads = list()
        for index in range(random.randint(5, 10)):
            x = threading.Thread(target=perform_order, args=(round, index + 1, session_id, random.sample(product_ids, random.randint(1, len(products) - 1))))
            threads.append(x)
            x.start()
        
        for index, thread in enumerate(threads):
            thread.join()

        round += 1
        if round == 15:
            generate_transactions = False

    print('closing session')

    PAYLOAD = {
        'session_id': session_id,
    }

    encoded_payload = base64.b64encode(json.dumps(PAYLOAD).encode())

    response = requests.post('http://localhost:8000/api/bullpen/v1/close-session', data=encoded_payload)


if __name__ == '__main__':
    main()