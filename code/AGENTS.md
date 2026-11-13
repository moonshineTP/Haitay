# code/

Device firmware and the PC service, split by layer to match report chapter 2 (2.3 device layer, then the PC software layer). No code exists yet.

- The design baseline is the prior-art report, not yet confirmed by the team: ESP32-S3 with native touch sensing, a hardware timer capturing 1 ms timestamps in the interrupt, a CRC-protected log, BLE sync with acknowledgement, a PC bridge, SQLite, a dashboard. Check the root "Open conflicts" before fixing power or timing numbers in code.
- The timing path must never wait on the display, storage, or BLE; keep those in lower-priority tasks.
- Sync is store-and-forward: the device deletes a record only after the PC acknowledges it, and the PC deduplicates by `(user_id, seq)`.
- Keep Wi-Fi credentials and keys out of the repository.
