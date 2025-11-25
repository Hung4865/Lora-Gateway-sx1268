import sys
import sx126x
import time

# --- CẤU HÌNH ---
SERIAL_PORT = "/dev/ttyS0"
MY_ADDR     = 0      # Địa chỉ máy này (Phải khớp với TARGET_ADDR bên gửi)

# Khởi tạo module (QUAN TRỌNG: Phải bật RSSI=True)
print("Khởi tạo Receiver...")
node = sx126x.sx126x(serial_num=SERIAL_PORT, freq=433, addr=MY_ADDR, 
                     power=22, rssi=True, air_speed=2400, relay=False)

print("--- ĐANG LẮNG NGHE (Chờ 100 gói) ---")

received_count = 0
rssi_list = []

try:
    while True:
        if node.ser.inWaiting() > 0:
            time.sleep(0.1) # Chờ buffer đầy
            r_buff = node.ser.read(node.ser.inWaiting())
            
            # --- XỬ LÝ DỮ LIỆU ---
            # Cấu trúc nhận về: [Sender_H, Sender_L, Freq, ...DATA..., RSSI_Byte]
            
            if len(r_buff) > 4: # Đảm bảo gói tin đủ dài
                # 1. Lấy RSSI (Byte cuối cùng)
                rssi_val = 256 - r_buff[-1]
                rssi_list.append(rssi_val)
                
                # 2. Lấy nội dung (Bỏ 3 byte đầu, bỏ 1 byte cuối RSSI)
                try:
                    msg_bytes = r_buff[3:-1]
                    msg_str = msg_bytes.decode('utf-8', errors='ignore')
                except:
                    msg_str = "Raw Error"

                received_count += 1
                
                # In ra màn hình
                print(f"Nhận: {msg_str} | RSSI: -{rssi_val}dBm | Tổng: {received_count}/100")

        # Logic thoát kiểm tra (Bạn có thể dừng tay bằng Ctrl+C để xem kết quả)
        time.sleep(0.05)

except KeyboardInterrupt:
    # --- TÍNH TOÁN KẾT QUẢ (Dùng số liệu này vẽ biểu đồ) ---
    print("\n\n====== KẾT QUẢ THÍ NGHIỆM ======")
    print(f"Tổng số gói nhận được: {received_count}")
    
    if received_count > 0:
        avg_rssi = sum(rssi_list) / len(rssi_list)
        print(f"RSSI Trung bình: -{avg_rssi:.2f} dBm")
        print(f"RSSI Tốt nhất: -{min(rssi_list)} dBm")
        print(f"RSSI Tệ nhất: -{max(rssi_list)} dBm")
    else:
        print("Không nhận được gói nào.")
        
    # Giả sử gửi 100 gói
    packet_loss = 100 - received_count
    loss_percent = (packet_loss / 100) * 100
    print(f"Tỷ lệ mất gói (Packet Loss): {loss_percent}%")
    print("================================")