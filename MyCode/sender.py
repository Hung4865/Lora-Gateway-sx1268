import sys
import sx126x
import time

# --- CẤU HÌNH ---
SERIAL_PORT = "/dev/ttyS0"
TARGET_ADDR = 0      # Địa chỉ đích (Gateway)
TARGET_FREQ = 433    # Tần số đích
MY_ADDR     = 10     # Địa chỉ của tôi (Sender)
TEST_SPEED  = 2400   # Tốc độ test (Sửa thành 300, 2400, 9600...)

# Khởi tạo module
print(f"--- SENDER STARTING | Speed: {TEST_SPEED} ---")
node = sx126x.sx126x(serial_num=SERIAL_PORT, freq=433, addr=MY_ADDR, 
                     power=22, rssi=True, air_speed=TEST_SPEED, relay=False)

print("Waiting for initialization...")
time.sleep(1)

print("--- START SENDING 100 PACKETS ---")

try:
    for i in range(1, 101):
        # Nội dung tin nhắn
        msg_str = f"Pkt:{i}"
        
        # --- LOGIC ĐÓNG GÓI (GIỐNG FILE GỐC MAIN.PY) ---
        # Tính toán offset tần số (433 - 410 = 23)
        offset_frequence = TARGET_FREQ - (850 if TARGET_FREQ > 850 else 410)
        
        # Header: [Target_H, Target_L, Target_Freq, Own_H, Own_L, Own_Freq]
        # Sử dụng phép dịch bit >> 8 và AND & 0xff như file gốc
        data = bytes([TARGET_ADDR >> 8]) + bytes([TARGET_ADDR & 0xff]) + \
               bytes([offset_frequence]) + \
               bytes([node.addr >> 8]) + bytes([node.addr & 0xff]) + \
               bytes([node.offset_freq]) + \
               msg_str.encode() # Chuyển string sang bytes

        # Gửi đi
        node.send(data)
        print(f"-> Sent: {msg_str}")
        
        # Nghỉ 1 giây (Hoặc 2 giây nếu dùng tốc độ 300)
        delay = 2.0 if TEST_SPEED == 300 else 1.0
        time.sleep(delay)

    print("\n--- DONE ---")

except KeyboardInterrupt:
    print("Stop.")