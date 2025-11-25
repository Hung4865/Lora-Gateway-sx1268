import sys
import sx126x
import time

# --- CẤU HÌNH ---
SERIAL_PORT = "/dev/ttyS0"
TARGET_ADDR = 0      # Địa chỉ máy nhận
TARGET_FREQ = 433    # Tần số máy nhận
MY_ADDR     = 10     # Địa chỉ máy gửi

# Khởi tạo module
print("Khởi tạo Sender...")
node = sx126x.sx126x(serial_num=SERIAL_PORT, freq=433, addr=MY_ADDR, 
                     power=22, rssi=False, air_speed=2400, relay=False)

print("--- BẮT ĐẦU GỬI 100 GÓI TIN ---")
print("Nhấn Ctrl+C để dừng sớm")

try:
    for i in range(1, 101): # Chạy từ 1 đến 100
        # Nội dung tin nhắn: "Pkt:1", "Pkt:2"...
        msg = f"Pkt:{i}"
        
        # --- ĐÓNG GÓI HEADER (Theo chuẩn Ebyte Fixed Mode) ---
        # Cấu trúc: [Addr_High, Addr_Low, Channel, Own_Addr_H, Own_Addr_L, Own_Chan, Payload]
        
        offset_freq = TARGET_FREQ - 410
        high_addr = TARGET_ADDR >> 8
        low_addr  = TARGET_ADDR & 0xFF
        
        own_high = node.addr >> 8
        own_low  = node.addr & 0xFF
        own_freq = node.offset_freq
        
        # Tạo gói tin byte
        header = bytes([high_addr, low_addr, offset_freq, own_high, own_low, own_freq])
        payload = msg.encode()
        data = header + payload
        
        # Gửi đi
        node.send(data)
        print(f"[Đã gửi] {msg}")
        
        # Nghỉ 1 giây giữa các gói (Để bên kia kịp xử lý)
        time.sleep(1)

    print("\n--- ĐÃ GỬI XONG 100 GÓI ---")

except KeyboardInterrupt:
    print("Dừng chương trình.")