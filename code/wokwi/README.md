# Haitay on Wokwi (ESP32-S3)

Wokwi cannot simulate capacitive touch or BLE, so the two pads are pushbuttons and the FRAM log is a RAM ring with the real record layout. Every committed solve prints `REC <32 hex chars>` on the serial port, and `sim/wokwi_ingest.py` feeds those lines into the PC simulation.

## Set up on wokwi.com

1. Create a new ESP32-S3 project (board DevKitC-1, Arduino).
2. Replace `sketch.ino` and `diagram.json` with the files in this folder.
3. Open the Library Manager and add the three entries of `libraries.txt` (Adafruit SSD1306, Adafruit GFX Library, RTClib), or paste the file into the project's `libraries.txt`.
4. Press Start. The serial monitor prints `# crc selftest 29b1 OK`.

## Play

| Button | GPIO | Action |
|---|---|---|
| Pad trai / Pad phai | 4 / 5 | Hold both 1.5 s (state READY), release one to start, press both to stop |
| Chon | 15 | In STOPPED, cycle penalty OK, +2, DNF |
| Session | 16 | Commit a pending solve, then start a new session |
| Dong bo | 17 | Commit a pending solve, then resend all unsynced records as `REC` lines |

After a stop, release a pad and touch both again (or press Dong bo) to commit the solve and print its `REC` line. Keyboard bindings in `diagram.json` let you hold both pads at once: A = left pad, L = right pad, 1 = Chon, 2 = Session, 3 = Dong bo. Click the canvas first so it has keyboard focus.

`sketch.ino` ships with `#define AUTOPLAY` on: six scripted solves of known length drive the pad samples, while the real pad buttons stay OR-ed in. Comment the define out for fully manual play. `RESULTS.md` records why and what the run showed.

## Ingest the serial output

1. Copy the serial monitor text into a file, for example `wokwi_run.txt`. Lines starting with `# ` are ignored.
2. From the `iot` folder run:

```
python -I Haitay/code/sim/wokwi_ingest.py Haitay/code/wokwi/wokwi_run.txt
```

The script prints the parsed record count, CRC failures, rows in SQLite, and Ao5, Ao12 and Ao100 recomputed on the PC. `sample_serial.txt` is a synthetic file for a first test.
