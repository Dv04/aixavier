# Jetson Xavier Flash & Bring-Up Checklist

1. Download the target JetPack version and flash using NVIDIA SDK Manager.
2. Set device to 45W (AGX) or 25W (NX) via `sudo nvpmodel -m 0` post-boot.
3. Run `sudo /usr/bin/jetson_clocks` after thermal solution verified.
4. Apply latest security patches: `sudo apt update && sudo apt upgrade`.
5. Create service user `edgeops` with sudo-limited privileges.
6. Disable unused services (e.g., `cups`, `avahi-daemon`).
7. Provision `/media/ssd` mount (optional NVMe) with ext4 + `noatime`.
8. Configure time sync (`chrony` or PTP) referencing {{TIME_SYNC_SOURCE}}.
9. Record device serial, MAC, and GPU UUID in asset inventory.
10. Follow `docs/SETUP.md` for remaining bootstrap steps.
