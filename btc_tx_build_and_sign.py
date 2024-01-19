from bitcoinlib.keys import Key
from bitcoinlib.transactions import Transaction
from bit.format import bytes_to_wif
import hashlib

def brain_wallet(passphrase):
    # Use SHA256 to hash the passphrase
    hashed_passphrase = hashlib.sha256(passphrase.encode()).hexdigest()
    
    # Convert hashed passphrase to a Bitcoin private key
    private_key = bytes_to_wif(bytes.fromhex(hashed_passphrase), version='main', compressed=True)

    # Create a Bitcoin Key object
    #key = Key(private_key.decode())
    key = Key(private_key)

    # # Get the public address
    address = key.address(script_type='p2wpkh', encoding='bech32')

    return key, address

def sign_transaction(raw_tx, key, network='bitcoin'):
    """
    Sign a raw, unsigned Bitcoin transaction.

    :param raw_tx: str - Raw, unsigned transaction in hex format.
    :param wif_key: str - Private key in WIF format.
    :param network: str - Bitcoin network, 'bitcoin' or 'testnet'.
    :return: str - Signed transaction in hex format.
    """
    # Load the transaction from the raw transaction hex
    tx = Transaction.parse(raw_tx)

    tx.inputs[0].value = 550
    # Sign the transaction with the private key
    tx.sign(key)
    tx.sign_and_update()

    # Return the signed transaction in hex format
    return tx

tx = Transaction(network='bitcoin', witness_type='segwit', version=2)
tx.add_input(prev_txid="853c26e1629085081b47e67520dafc626a2d2c18f94c149ce731c65ec69c1446", output_n=1, value=550, script_type='p2wpkh',
             public_hash=b'notused')
tx.add_output(250, address='bc1qkjhasvhac9d47662xp85s93ev7wv26ggtqu3cy')
tx.sign_and_update()
print(tx.txid)

private_key, address = brain_wallet("correct horse battery staple")
tx2 = sign_transaction(tx.raw_hex(), private_key)
print(tx2.raw_hex())