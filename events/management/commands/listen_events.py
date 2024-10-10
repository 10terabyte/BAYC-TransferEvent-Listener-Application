import asyncio
from django.core.management.base import BaseCommand
from web3 import AsyncWeb3
from web3.providers.persistent import WebSocketProvider
from events.models import TransferEvent
from django.db.utils import IntegrityError
from asgiref.sync import sync_to_async
from ...constants import INFURA_PROJECT_ID, BAYC_CONTRACT_ADDRESS, TRANSFER_EVENT_SIGNATURE

class Command(BaseCommand):
    """
    Django management command to listen for BAYC Transfer events 
    using WebSocket and AsyncWeb3.
    """
    help = 'Listen for BAYC Transfer events using WebSocket and AsyncWeb3'

    def handle(self, *args, **kwargs):
        asyncio.run(self.start_event_listener())

    async def start_event_listener(self):
        infura_ws_url = f'wss://mainnet.infura.io/ws/v3/{INFURA_PROJECT_ID}'

        async with AsyncWeb3(WebSocketProvider(infura_ws_url)) as web3:
            if not await web3.is_connected():
                self.stdout.write(
                    self.style.ERROR('Failed to connect to Ethereum network')
                )
                return

            self.stdout.write(
                self.style.SUCCESS('Connected to Ethereum network via WebSocket')
            )

            subscription_id = await web3.eth.subscribe(
                "logs",
                {"address": BAYC_CONTRACT_ADDRESS, "topics": [TRANSFER_EVENT_SIGNATURE]},
            )
            await self.process_event_subscription(web3, subscription_id)

    async def process_event_subscription(self, web3, subscription_id):
        self.stdout.write(
            self.style.SUCCESS('Listening for new transfer events via WebSocket...')
        )
        try:
            async for event in web3.socket.process_subscriptions():
                print(f"{event}\n")
                await self.async_save_event(event['result'])

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))

    async def async_save_event(self, event):
        try:
            token_id = int(event['topics'][3].hex(), 16)
            from_address = '0x' + event['topics'][1].hex()[-40:]
            to_address = '0x' + event['topics'][2].hex()[-40:]
            transaction_hash = event['transactionHash'].hex()
            block_number = event['blockNumber']

            print(
                f'Transfer event received: Token {token_id} transferred '
                f'from {from_address} to {to_address}'
            )

            await sync_to_async(self.create_transfer_event)(
                token_id, from_address, to_address, transaction_hash, block_number
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Recorded event: Token {token_id} transferred '
                    f'from {from_address} to {to_address}'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to save event: {str(e)}'))

    def create_transfer_event(self, token_id, from_address, to_address, transaction_hash, block_number):
        try:
            TransferEvent.objects.create(
                token_id=token_id,
                from_address=from_address,
                to_address=to_address,
                transaction_hash=transaction_hash,
                block_number=block_number
            )
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Database error: {str(e)}'))
