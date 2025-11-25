import sys
import sx126x
import time
import json
import paho.mqtt.client as mqtt

# --- CẤU HÌNH LORA ---
SERIAL_PORT = "/dev/ttyS0"
MY_ADDR     = 0      
TEST_SPEED  = 2400   # PHẢI GIỐNG MÁY GỬI

# --- CẤU HÌNH MQTT (CLOUD) ---
MQTT_BROKER = "broker.hivemq.com"  # Server công cộng miễn phí
MQTT_PORT   = 1883
MQTT_TOPIC  = "do_an_tot_nghiep/du_lieu_lora" # Đổi tên này để không bị trùng người khác

# ---------------------------------------------------------

# 1. KHỞI TẠO KẾT NỐI MQTT
print(f"-> Đang kết nối đến {MQTT_BROKER}...")
client = mqtt.Client()

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() # Chạy luồng mạng ngầm (Background thread)
    print("-> KẾT NỐI MQTT THÀNH CÔNG!")
except Exception as e:
    print(f"-> Lỗi kết nối MQTT: {e}")

# 2. KHỞI TẠO LORA
print(f"--- RECEIVER LISTENING | Speed: {TEST_SPEED} ---")
# Lưu ý: rssi=True để lấy được byte RSSI cuối cùng
node = sx126x.sx126x(serial_num=SERIAL_PORT, freq=433, addr=MY_ADDR, 
                     power=22, rssi=True, air_speed=TEST_SPEED, relay=False)

print("Waiting for packets...")

received_count = 0
rssi_list = []
EXPECTED_PACKETS = 100

try:
    while True:
        # Kiểm tra bộ đệm Serial
        if node.ser.inWaiting() > 0:
            time.sleep(0.1) # Chờ dữ liệu về đủ
            r_buff = node.ser.read(node.ser.inWaiting())
            
            # Kiểm tra độ dài gói tin (Ít nhất phải có 3 byte header + 1 byte RSSI)
            if len(r_buff) > 4:
                # --- XỬ LÝ THEO LOGIC FILE GỐC ---
                
                # 1. Lấy thông tin người gửi (3 byte đầu)
                sender_addr = (r_buff[0] << 8) + r_buff[1]
                sender_freq = r_buff[2] + node.start_freq
                
                # 2. Lấy giá trị RSSI (Byte cuối cùng)
                rssi_val = 256 - r_buff[-1]
                rssi_list.append(rssi_val)
                
                # 3. Lấy nội dung tin nhắn (Bỏ 3 byte đầu và 1 byte cuối)
                msg_bytes = r_buff[3:-1]
                
                try:
                    msg_str = msg_bytes.decode('utf-8', errors='ignore')
                except:
                    msg_str = str(msg_bytes)

                received_count += 1
                
                # In ra màn hình Pi
                print(f"#{received_count} | From: {sender_addr} | Msg: {msg_str} | RSSI: -{rssi_val}dBm")

                # --- PHẦN MỚI: ĐẨY LÊN CLOUD ---
                try:
                    # Đóng gói dạng JSON: {"id": 1, "message": "Pkt:1", "rssi": -45}
                    payload_json = json.dumps({
                        "count": received_count,
                        "sender": sender_addr,
                        "message": msg_str,
                        "rssi": -rssi_val
                    })
                    
                    # Gửi đi
                    client.publish(MQTT_TOPIC, payload_json)
                    # print("-> Đã đẩy lên Cloud")
                    
                except Exception as e:
                    print(f"Lỗi gửi MQTT: {e}")
                # -------------------------------
        
        # Nghỉ ngắn để giảm tải CPU
        time.sleep(0.01)

except KeyboardInterrupt:
    # --- TÍNH TOÁN KẾT QUẢ ---
    print("\n\n====== BÁO CÁO KẾT QUẢ ======")
    if received_count > 0:
        avg_rssi = sum(rssi_list) / len(rssi_list)
        loss = EXPECTED_PACKETS - received_count
        if loss < 0: loss = 0 # Trường hợp chạy dư
        
        print(f"Tổng nhận: {received_count}/{EXPECTED_PACKETS}")
        print(f"RSSI Trung bình: -{avg_rssi:.2f} dBm")
        print(f"Tỷ lệ mất gói: {(loss/EXPECTED_PACKETS)*100:.1f}%")
    else:
        print("Không nhận được gói nào.")
    
    # Ngắt kết nối mạng khi dừng
    client.loop_stop()
    client.disconnect()