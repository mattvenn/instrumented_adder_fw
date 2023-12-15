#!/usr/bin/env python3
import random
import serial
#from mso2004 import Scope
port = '/dev/serial/by-id/usb-Arduino_Nano_33_BLE_3C48BB3E0BD44A03-if00'
port = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00' 

adders = {
    2: 'behavioural',
    3: 'sklansky',
    4: 'brent kung',
    5: 'ripple',
    6: 'kogge' 
}

def add(a, b):
    ser.write(b'a')
    resp = ser.readline()
    assert resp == b'waiting for 8 characters\r\n'
    ser.write(f"{a:08x}".encode())
    resp = ser.readline()
    assert resp == b'waiting for 8 characters\r\n'
    ser.write(f"{b:08x}".encode())
    resp = int(ser.readline().decode(), 16)
    return resp

def select_project(p):
    ser.write(b'p')
    resp = ser.readline()
    assert resp == b'choose project 2 -> 6: '
    ser.write(str(p).encode())
    resp = ser.readline()
    assert resp == f'set project to  00{p}\r\n'.encode()
    print(f"set project to {adders[p]}")

def test_all_adders(ser):
    for project in [2,3,4,5,6]:
        select_project(project)
    
        num_tests = 1000
        for i in range(num_tests):
            a = random.randint(0, 2**32)
            b = random.randint(0, 2**32)
            result = (a + b) % (2**32)
            #print(f"{a:08x} + {b:08x} = {result:08x}")
            assert add(a, b) == result
        print(f"completed {num_tests} tests")

def test_integration_time(ser):
    select_project(2)
    for count in [100]: #range(10, 2000):
        ser.write(b'i')
        resp = ser.readline()
        assert resp == b'waiting for 8 characters\r\n'
        count_hex = f"{count:08x}"
        ser.write(count_hex.encode())
        resp = ser.readline()
        assert resp == f'set integration count to {count_hex} and started\r\n'.encode()
        resp = ser.readline()
        assert resp == b'done\r\n'
    print("done")

def test_in_out_bit(ser, in_bit=1, out_bit=12):
#    print(f"test adder in ring with in_bit_index {in_bit} and out_bit_index {out_bit}")
    ser.write(b'u')
    resp = ser.readline()
    assert resp == b'test adder in ring. set in bit:\r\n'

    resp = ser.readline()
    assert resp == b'waiting for 2 characters\r\n'

    in_bit_hex = f"{in_bit:02x}"
    ser.write(in_bit_hex.encode())
    resp = ser.readline()
    assert resp == b'set out bit:\r\n'

    resp = ser.readline()
    assert resp == b'waiting for 2 characters\r\n'

    out_bit_hex = f"{out_bit:02x}"
    ser.write(out_bit_hex.encode())
    resp = ser.readline()
    assert resp == f'running 20x adder with in bit 0x{in_bit_hex} and out bit 0x{out_bit_hex}\r\n'.encode()

    integration_total = 0
    for i in range(20):
        resp = ser.readline()
        integration_count = int(resp.decode().strip(), 16)
        integration_total += integration_count

    resp = ser.readline()
    assert resp == b'done\r\n'
    #print(f"average over 20 was {integration_total / 20}")
    return integration_total / 20

if __name__ == '__main__':
    with serial.Serial(port, 9600, timeout=2) as ser:
        # test_all_adders(ser)
#        test_integration_time(ser)
        select_project(4)
        print("running in/out bit adder test")
        in_bit = 1
        for out_bit in range(0,32,4):
            integration_count = test_in_out_bit(ser, in_bit = in_bit, out_bit=out_bit)
            print(f"{in_bit:2}, {out_bit:2}, {integration_count}")
