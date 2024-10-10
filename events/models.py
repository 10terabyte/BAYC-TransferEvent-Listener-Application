from django.db import models

class TransferEvent(models.Model):
    token_id = models.CharField(max_length=100, verbose_name='Token ID')
    from_address = models.CharField(max_length=42, verbose_name='Sender Address')  # Ethereum addresses are 42 characters long
    to_address = models.CharField(max_length=42, verbose_name='Recipient Address')
    transaction_hash = models.CharField(max_length=66, verbose_name='Transaction Hash')  # Ethereum transaction hashes are 66 characters long with "0x" prefix
    block_number = models.IntegerField(verbose_name='Block Number')

    def __str__(self):
        return f'Token {self.token_id} transferred from {self.from_address} to {self.to_address}'

    class Meta:
        verbose_name = 'Transfer Event'
        verbose_name_plural = 'Transfer Events'
        ordering = ['-block_number']  # Orders events by the block number in descending order
