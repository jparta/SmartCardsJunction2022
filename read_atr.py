#! /usr/bin/env python3
from smartcard.ATR import ATR
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString
import sys

for reader in readers():
    try:
        connection = reader.createConnection()
        connection.connect()
        atr_bytelist = connection.getATR()
        atr_obj = ATR(atr_bytelist)
        print(reader, toHexString(atr_bytelist))
        print(atr_obj.dump())
    except NoCardException:
        print(reader, 'no card inserted')

if 'win32' == sys.platform:
    print('press Enter to continue')
    sys.stdin.read(1)