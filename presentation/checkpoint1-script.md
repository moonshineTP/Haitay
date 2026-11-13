# Kịch bản trình bày Checkpoint 1

Bài nói dài khoảng 12 phút cho 16 trang của `checkpoint1.pdf`, cộng 1 phút demo mô phỏng. Mỗi trang ghi thời lượng và các ý cần nói, còn số liệu đều lấy từ báo cáo `writing/main.pdf`.

| Trang | Nội dung | Thời lượng | Người nói |
|---|---|---|---|
| 1 | Trang bìa | 0:20 | |
| 2 | 1. Giới thiệu dự án | 0:40 | |
| 3 | 2. Vấn đề và người dùng | 0:50 | |
| 4 | 3. Bốn use case | 0:45 | |
| 5 | 3. Core logic | 0:40 | |
| 6 | 3. Phi chức năng | 1:00 | |
| 7 | 4. Kiến trúc bốn lớp | 1:10 | |
| 8 | 4. Luồng đồng bộ | 0:50 | |
| 9 | 5. Thiết bị, chi phí | 0:50 | |
| 10 | 6. Công nghệ | 0:50 | |
| 11 | 7. Luồng đầu cuối | 0:50 | |
| 12 | 7. Kết quả 17/17 | 0:40 | |
| (demo) | Chạy mô phỏng | 1:00 | |
| 13 | 7. Hình kết quả | 0:40 | |
| 14 | 7. Wokwi | 0:40 | |
| 15 | 8. Phân công, khó khăn | 0:50 | |
| 16 | Cảm ơn | 0:10 | |
| | **Tổng** | **12:45** | |

## Từng trang

**Trang 1. Bìa (0:20)**
- Chào thầy và các bạn, nhóm Hai Người trình bày dự án Haitay, thiết bị bấm giờ speedcubing.

**Trang 2. Giới thiệu dự án (0:40)**
- Haitay là bộ bấm giờ hai pad theo kiểu Stackmat: đặt hai tay để sẵn sàng, nhấc tay để chạy, đặt lại để dừng.
- Thiết bị tự lưu mọi lượt solve, tính Ao5, Ao12, Ao100, rồi đồng bộ qua Bluetooth LE sang máy tính.
- Nhóm có bốn thành viên như trong bảng; khẩu hiệu là "Đo từng giây, thấy từng tiến bộ".

**Trang 3. Vấn đề và người dùng (0:50)**
- Stackmat G5 không tự lưu lịch sử, và nối nó với csTimer bằng dây cáp hay gặp trục trặc.
- Vì vậy người chơi muốn thấy tiến bộ phải tự nhập, tự tính Ao5, Ao12, Ao100.
- Người dùng chính là người tự luyện tại bàn; thiết bị cũng hỗ trợ nhiều người dùng chung nhờ chuyển user, còn PIN trên máy tính là tùy chọn.
- Haitay là timer luyện tập, bổ trợ cho timer thi đấu.

**Trang 4. Bốn use case (0:45)**
- Mỗi use case là một nhu cầu của người dùng, đặt tên theo động từ cộng tân ngữ; tác nhân chính là Người chơi, tác nhân phụ là Người chơi kế tiếp.
- UC1 Bấm giờ lượt giải (trên thiết bị): giữ tay, bấm giờ, chọn OK, +2, DNF, xem Ao, sửa lượt cũ, mở session mới.
- UC2 Theo dõi tiến bộ (dashboard trên máy tính, lịch sử trên thiết bị) và UC3 Sao lưu lịch sử luyện tập (thiết bị, bridge, máy chủ).
- UC4 Chuyển thiết bị cho người khác luôn gồm UC3: chỉ xóa thiết bị sau khi đã sao lưu.
- Dòng nhỏ trong mỗi hình elip là 10 chức năng của Chương 1; Smart Cube là tùy chọn, ngoài phạm vi.

**Trang 5. Core logic: máy trạng thái bấm giờ (0:40)**
- Đặt hai tay lên hai pad, giữ đủ 1,5 giây thì Sẵn sàng; nhả sớm thì quay về Chờ, chống chạm nhầm.
- Nhấc ít nhất một tay thì đồng hồ chạy (mốc t0), đặt lại hai tay thì dừng (mốc t1), rồi chọn OK, +2 hoặc DNF.
- Chống nảy cần ba mẫu ổn định, nhưng mốc giờ lùi về mẫu đầu tiên, nên không cộng thêm độ trễ.

**Trang 6. Phi chức năng (1:00)**
- Mười hai chỉ tiêu N1 đến N12, mỗi chỉ tiêu có con số và cách kiểm chứng.
- Tách hai con số về thời gian: độ phân giải dưới 1 ms (N1) và độ trễ phát hiện chạm 2 đến 10 ms (N2).
- Toàn vẹn dữ liệu: 0 bản ghi đã chốt bị mất qua 100 lần cắt điện, 0 mất và 0 trùng khi rơi Bluetooth.

**Trang 7. Kiến trúc bốn lớp (1:10)**
- Lớp cảm nhận: hai pad lá đồng nối kênh chạm của ESP32-S3; firmware đo giờ, ghi nhật ký vào flash trong chip, giữ giờ bằng DS3231.
- Chặng thiết bị tới gateway là Bluetooth LE, dịch vụ GATT: notify bản ghi, write lệnh.
- Gateway là bridge Python dùng bleak, gửi HTTP/REST JSON tới dịch vụ FastAPI chỉ nghe trên 127.0.0.1; dữ liệu nằm trong SQLite.
- Dashboard web truy vấn bằng REST và nhận báo dữ liệu mới qua SSE; ba lớp trên cùng chạy trên máy tính người chơi.

**Trang 8. Luồng đồng bộ (0:50)**
- Thiết bị lưu trước, gửi sau: mỗi khung LOG mang 11 bản ghi 16 byte.
- Máy tính chỉ gửi ACK sau khi SQLite COMMIT, nên thiết bị không bao giờ xóa thứ máy tính chưa lưu.
- Gửi lại không tạo bản sao nhờ khóa chính (device_id, seq).

**Trang 9. Thiết bị, chi phí (0:50)**
- Tổng vật tư 1.775.000 đồng. Mọi linh kiện có ít nhất hai bản; bo ESP32-S3 và bộ pad có ba bản vì hỏng một trong hai thì không đo giờ được. Dòng có dấu sao là ước lượng.
- Tính riêng một bộ và bỏ MPR121, một bộ hoàn chỉnh khoảng 650.000 đồng, trong khi Stackmat G5 giá 0,9 đến 1,0 triệu và không lưu lịch sử.
- Lợi ích chính: không nhập tay từ lượt solve tới biểu đồ, dữ liệu ở lại máy người chơi.

**Trang 10. Công nghệ (0:50)**
- Bluetooth LE vì thiết bị và máy tính cách vài mét, mỗi buổi chỉ vài KB, máy tính có sẵn bộ thu; USB-C làm dự phòng.
- Nhật ký trên flash trong chip vì không tốn linh kiện, mua đâu cũng có, và ghi thêm cùng CRC giữ bản ghi khi rút cáp; HTTP/REST thay MQTT vì PUBACK chỉ báo broker đã nhận, chưa báo cơ sở dữ liệu đã lưu.
- SQLite vì dữ liệu vài MB, cần quan hệ và khóa chống trùng; SSE vì dashboard chỉ cần nhận một chiều.

**Trang 11. Luồng đầu cuối (0:50)**
- Linh kiện chưa về đủ, nên nhóm chạy toàn bộ luồng cảm biến, giao thức, cơ sở dữ liệu, giao diện bằng mô phỏng Python.
- Khung xanh là phần đã chạy; logic bản ghi, CRC, đồng bộ và lược đồ là mã thật sẽ chuyển sang firmware và máy chủ.
- Khung xám là việc còn lại: phần cứng thật, GATT với bleak, FastAPI, Chart.js.

**Trang 12. Kết quả 17/17 (0:40)**
- Lần chạy 13/11/2026 đạt cả 17 phép kiểm tra.
- Đọc nhanh T1, S2, S3: sai lệch trung bình −0,01 ms, rơi Bluetooth không mất không trùng, 100 lần cắt điện không mất bản ghi đã chốt. Nói rõ: S3, S5 dùng mô hình ghi từng byte, chưa mô phỏng xóa sector flash.
- Chuyển sang demo.

**Demo mô phỏng (1:00)**, xem mục dưới.

**Trang 13. Hình kết quả (0:40)**
- Hình trái: sai lệch đo giờ đối xứng quanh 0, firmware không cộng thêm sai số ngoài độ trễ cảm biến.
- Hình phải: 90 ngày, 3.443 lượt đã đi qua giao thức thật vào SQLite; Ao100 cho thấy rõ xu hướng tiến bộ.

**Trang 14. Wokwi (0:40)**
- Sketch ESP32-S3 chạy trên Wokwi sáng nay; hai pad thay bằng nút nhấn vì Wokwi không mô phỏng cảm ứng điện dung và Bluetooth.
- 6 lượt solve sinh 12 dòng `REC` (6 khi chốt, 6 gửi lại khi bấm Đồng bộ), 0 lỗi CRC; `wokwi_ingest.py` nạp đúng 6 hàng vào SQLite.
- Ao5 bằng 3,30 s cả trên thiết bị lẫn trên máy tính.
- Nói thẳng: tín hiệu pad được lập trình sẵn (AUTOPLAY) vì Wokwi không giữ được hai phím cùng lúc; nút +2 và Đồng bộ được bấm thật.
- Link Wokwi công khai: https://wokwi.com/projects/480535692769291265 (mở được khi chưa đăng nhập).

**Trang tiếp theo. Wokwi, một lượt giải UC1 (0:20)**
- Hình động 10 khung: giữ tay, GO!, đồng hồ chạy, dừng ở 2,87 s, in dòng `REC`.
- Hình động chỉ chạy trong Adobe Reader hoặc Okular; nếu máy chiếu dùng trình duyệt, mở GIF trên GitHub hoặc link Wokwi.

**Trang 15. Phân công, khó khăn (0:50)**
- Phân công: Hưng trưởng nhóm, đặc tả, thiết kế, mô phỏng, frontend dashboard, định nghĩa dữ liệu hiển thị; Giang backend phần cứng và triển khai logic thiết bị; Bảo backend phần mềm và triển khai logic; Minh kiểm thử và QA phần cứng.
- Kho mã chung github.com/moonshineTP/Haitay, nhánh riêng, xem chéo trước khi hợp nhất.
- Khó khăn và rủi ro lớn nhất: xóa sector flash phải đợi lúc rảnh, Bluetooth LE dễ trễ tiến độ, đo trễ tuyệt đối cần thiết bị tham chiếu, cảm biến chạm có thể kích hoạt sai khi tay ẩm.

**Trang 16. Cảm ơn (0:10)**
- Cảm ơn thầy và các bạn, nhóm sẵn sàng nhận câu hỏi.

## Demo mô phỏng (1 phút)

Chuẩn bị trước khi lên: mở terminal ở thư mục `Haitay/`, phóng to chữ, chạy thử một lần để chắc máy có matplotlib.

1. Gõ lệnh, vừa chạy vừa nói "toàn bộ luồng từ cú chạm tới SQLite chạy trong một lệnh, hạt giống cố định":
   ```bash
   python -I code/sim/run_scenarios.py
   ```
2. Khi kết quả hiện ra, chỉ vào dòng tổng `17/17` và ba dòng T1, S2, S3.
3. Mở `code/sim/out/results.json` nếu thầy muốn xem số liệu thô, hoặc quay lại trang 13 để xem hai hình vừa được vẽ lại.
4. Phương án dự phòng: nếu máy lỗi, chiếu trang 12 và 13, vì cả hai lấy từ lần chạy 13/11/2026.
