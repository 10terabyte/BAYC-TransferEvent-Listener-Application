import asyncio
from django.core.management.base import BaseCommand
from web3 import Web3
from events.models import TransferEvent
from django.db.utils import IntegrityError
from ...constants import INFURA_PROJECT_ID, BAYC_CONTRACT_ADDRESS


BAYC_ABI = [
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "from", "type": "address"},
            {"indexed": True, "name": "to", "type": "address"},
            {"indexed": True, "name": "tokenId", "type": "uint256"}
        ],
        "name": "Transfer",
        "type": "event"
    }
]


class Command(BaseCommand):
    """
    Django management command to fetch past BAYC Transfer events.
    """
    help = 'Fetch past BAYC Transfer events'

    def handle(self, *args, **kwargs):
        self.fetch_past_events()

    def fetch_past_events(self):
        infura_ws_url = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'
        web3 = Web3(Web3.HTTPProvider(infura_ws_url))

        if not web3.is_connected():
            print('Failed to connect to Ethereum network')
            return

        print('Connected to Ethereum network')

        contract = web3.eth.contract(address=BAYC_CONTRACT_ADDRESS, abi=BAYC_ABI)

        START_BLOCK = 0xBC676B
        END_BLOCK = 0xBF5618
        BLOCK_STEP = 1000

        current_block = START_BLOCK
        while current_block < END_BLOCK:
            next_block = min(current_block + BLOCK_STEP, END_BLOCK)

            print(
                f'Fetching past transfer events from block {current_block} to {next_block}...'
            )

            events = contract.events.Transfer.create_filter(
                from_block=current_block, to_block=next_block
            ).get_all_entries()

            for event in events:
                self.save_event(event)

            print(
                f'Successfully recorded {len(events)} events from blocks {current_block} to {next_block}.'
            )

            current_block = next_block + 1

    def save_event(self, event):
        try:
            transfer_event = TransferEvent(
                token_id=event['args']['tokenId'],
                from_address=event['args']['from'],
                to_address=event['args']['to'],
                transaction_hash=event['transactionHash'].hex(),
                block_number=event['blockNumber']
            )
            transfer_event.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Recorded event: Token {event["args"]["tokenId"]} transferred '
                    f'from {event["args"]["from"]} to {event["args"]["to"]}'
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to save event: {str(e)}'))
