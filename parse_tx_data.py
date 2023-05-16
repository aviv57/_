def parse_tx_data(tx_data):
    parsed = []
    index = tx_data[:128].index(b'\x03ord')
    _len = len(tx_data)
    while index < _len:
        # OP_PUSH 0 to 0x4b pushes at most 0x4b bytes to the stack
        if (tx_data[index] < 0x4c):
           size = tx_data[index]
           index += 1
           parsed.append(tx_data[index: index+size])
           index += size
           continue
        # OP_PUSHDATA1 pushes at most 0xff bytes to the stack
        if (tx_data[index] == 0x4c):
           index += 1
           size = tx_data[index]
           index += 1
           parsed.append(tx_data[index: index+size])
           index += size
           continue
        # OP_PUSHDATA2 pushes at most 0xffff bytes to the stack
        if (tx_data[index] == 0x4d):
           index += 1
           size = tx_data[index] + 256*tx_data[index+1]
           index += 2
           parsed.append(tx_data[index: index+size])
           index += size
           continue
        index += 1
    print(parsed[2])
    return b''.join(parsed[3:])