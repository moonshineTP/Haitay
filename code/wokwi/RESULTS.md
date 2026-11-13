# Wokwi run 1 results

Run date 13-11-2026, 08:08 to 08:22 +07, on wokwi.com (new unsaved ESP32-S3 project, Arduino core, libraries Adafruit SSD1306, Adafruit GFX Library, RTClib). Verdict: **pass**. The sketch compiled, simulated, and every record it emitted reached SQLite through the real `PcService.sync` with zero CRC failures.

## What ran, real versus scripted

The firmware logic ran unmodified in the simulator: 1 kHz `esp_timer` pad sampling, debounce with back-dating, the five-state machine, the 16-byte CRC record, the RAM ring, on-device Ao5/Ao12/Ao100, the SSD1306 OLED over I2C, and the DS1307 RTC. Only the pad input was scripted.

| Part | Real or scripted | Note |
|---|---|---|
| Pad samples (GPIO 4, 5) | **Scripted** (`#define AUTOPLAY`) | Synthetic `bits` OR-ed into each 1 kHz sample; real buttons stay active |
| Solve durations | Scripted | 2,870 / 3,240 / 2,530 / 3,610 / 3,050 / 2,420 ms, shortened to fit the slow host |
| Debounce, state machine, timing | Real firmware | Measured times equal the scripted ones to the millisecond |
| Chọn (+2) on solve 6 | Real button | Key `1` on the Wokwi canvas, serial shows `# penalty +2` |
| Đồng bộ (sync) | Real button | Key `3`, commits solve 6 and resends all 6 records |
| OLED, RTC, CRC self-test | Real simulated parts | `# crc selftest 29b1 OK`, `# oled ok, rtc ok` |
| Serial to PC | Manual copy | Serial monitor text saved to `serial_run1.txt` |

AUTOPLAY exists because the browser tools press keys one at a time, so they cannot hold `a` and `l` together; synthetic `KeyboardEvent`s did not reach the Wokwi buttons either.

## Numbers

| Quantity | Value |
|---|---|
| `REC` lines in the log | 12 (6 at commit time, 6 resent on sync) |
| Unique records (seq 1 to 6) | 6 |
| CRC failures | 0 |
| PC sync | new 6, dup 0, bad frames 0, acked 6 |
| Rows in SQLite (`solve`) | 6 |
| Ao5 on device (serial and OLED) | 3.30 s |
| Ao5 recomputed on PC from SQLite | 3.30 s |
| Ao12, Ao100 | undefined on both sides (fewer than 12 solves) |

Hand check: the last five effective times are 3,240, 2,530, 3,610, 3,050 and 4,420 ms (2,420 + 2,000). Trimming 2,530 and 4,420 leaves a mean of 3,300 ms. After five solves the device also printed Ao5 3.05 s, which equals (2,870 + 3,240 + 3,050) / 3.

SQLite rows (`device_id, seq, session_id, time_ms, penalty, deleted, ts, ts_estimated, edit_seq`), from `Haitay/tmp/sim/wokwi-20261113-082022/pc.sqlite`:

```
('HT-WOKWI', 1, 1, 2870, 0, 0, 1794557628, 0, 0)
('HT-WOKWI', 2, 1, 3240, 0, 0, 1794557674, 0, 0)
('HT-WOKWI', 3, 1, 2530, 0, 0, 1794557732, 0, 0)
('HT-WOKWI', 4, 1, 3610, 0, 0, 1794557859, 0, 0)
('HT-WOKWI', 5, 1, 3050, 0, 0, 1794557895, 0, 0)
('HT-WOKWI', 6, 1, 2420, 1, 0, 1794557994, 0, 0)
```

## Problems hit and fixes

| Problem | Fix |
|---|---|
| `diagram.json` lacked the serial monitor wiring | Added `esp:TX`/`esp:RX` to `$serialMonitor` |
| Build failed: `'State' was not declared`, `'Sample' does not name a type`, `'Button'` (Arduino auto-prototypes land above the type definitions) | Moved `enum State`, `struct Sample`, `struct Button` above the first function |
| Simulation at 2 to 8 % of real time | `delay(1)` in `loop()` lets the core idle, OLED redraw cut to 4 Hz and skipped when unchanged, I2C at 400 kHz. Speed then swung between 3 and 36 %, apparently with host load from parallel sessions |
| Two keys cannot be held at once from the browser tools | `#define AUTOPLAY` scripted pad samples; durations shortened to about 3 s so the run fit the time box |
| The circuit's Chọn button sits under Wokwi's stopwatch overlay | Used the keyboard binding (`1`) after clicking the canvas |

Two observations for the report. Wokwi seeds the DS1307 with the browser's local time (+07), so `ts` reads 08:13 as if it were UTC; on the real device the PC's `SET_TIME` writes the true epoch. The RTC also follows wall-clock time while the simulator ran slower, so the six `ts` values span 366 s for about 30 s of simulated play.

## Files

- `Haitay/code/wokwi/sketch.ino`, `diagram.json`, `README.md`: synced with the browser copy that ran
- `Haitay/code/wokwi/serial_run1.txt`: full serial monitor text
- `Haitay/code/wokwi/ingest_run1.txt`: `wokwi_ingest.py` output plus the SQLite rows
- `Haitay/writing/figures/wokwi_circuit.png`, `wokwi_serial.png`

## LaTeX for chapter 4

```latex
Để kiểm tra luồng dữ liệu từ đầu đến cuối trước khi có phần cứng, nhóm chạy firmware trên trình mô phỏng Wokwi với bo ESP32-S3, màn hình OLED SSD1306 và đồng hồ thời gian thực DS1307 (Hình~\ref{fig:wokwi-circuit}).
Vì Wokwi không mô phỏng cảm biến điện dung và BLE, hai pad được thay bằng nút nhấn, còn mỗi bản ghi 16 byte có CRC được in ra cổng nối tiếp dưới dạng dòng \texttt{REC}.
Do công cụ trình duyệt không giữ được hai phím cùng lúc, tín hiệu pad của sáu lượt giải được sinh theo kịch bản với thời lượng biết trước, trong khi nút phạt +2 và nút đồng bộ được bấm thật.
Máy trạng thái, bộ lọc nhiễu và phép đo thời gian vẫn là mã firmware thật, nên thời gian đo được khớp kịch bản đến từng mili giây.
Sau khi đồng bộ, 12 dòng \texttt{REC} (sáu bản ghi cùng sáu bản gửi lại) đi qua \texttt{PcService.sync} vào SQLite với 0 lỗi CRC và đúng 6 hàng mới (Hình~\ref{fig:wokwi-serial}).
Ao5 tính trên thiết bị và Ao5 tính lại trên PC từ cơ sở dữ liệu cùng bằng 3,30~s, nhờ đó chuỗi cảm biến, giao thức và cơ sở dữ liệu được kiểm chứng trọn vẹn.

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.92\textwidth]{figures/wokwi_circuit.png}
    \caption{Mạch Haitay trên Wokwi: ESP32-S3, OLED hiển thị lượt cuối 4,42~s (2,42~s cộng phạt +2) và Ao5 3,30~s}
    \label{fig:wokwi-circuit}
\end{figure}

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.78\textwidth]{figures/wokwi_serial.png}
    \caption{Cổng nối tiếp Wokwi: phạt +2, Ao5 trên thiết bị và sáu dòng \texttt{REC} gửi lại khi đồng bộ}
    \label{fig:wokwi-serial}
\end{figure}
```
