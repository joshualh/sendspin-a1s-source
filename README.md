# sendspin-a1s-source

ESPHome firmware that turns an ESP32-A1S Audio Kit (ES8388 variant) into a Sendspin **source**: it streams the codec's ADC (line-in jack by default) to a Sendspin server. It is a test rig for the sendspin-cpp source@v1 stack ([Sendspin/sendspin-cpp#112](https://github.com/Sendspin/sendspin-cpp/pull/112) through #117).

## What's here

- `a1s-sendspin-source.yaml` is the device config. It pulls the component below from this repo.
- `components/sendspin` is ESPHome 2026.8.2's `sendspin` component with two changes:
  - sendspin-cpp comes from the source-role branch (`SENDSPIN_CPP_REPO` / `SENDSPIN_CPP_REF` in `__init__.py`) instead of the 0.7.2 release.
  - The hub gains a `source:` block that feeds a microphone into the source role. The capture format is taken from the microphone. Codec, chunking and Opus options fall back to sendspin-cpp's defaults when omitted.

The pinout (I²C SDA 33 / SCL 32, I²S MCLK 0 / BCLK 27 / LRCK 25 / DIN 35) is the one shared by the A1S configs in the [Home Assistant community thread](https://community.home-assistant.io/t/esp32-a1s-audio-kit-media-player/522245).

## Using it

Copy `a1s-sendspin-source.yaml` into your ESPHome config directory, provide `wifi_ssid` / `wifi_password` secrets, and build with ESPHome 2026.8 or newer.

- **Picking up new sendspin-cpp pushes:** the IDF component manager locks the fetched commit, so after pushing to the sendspin-cpp branch, clean the build files before rebuilding.
- **Server:** the branch sends `client-stream/start` / `client-stream/end`. aiosendspin needs [Sendspin/aiosendspin#358](https://github.com/Sendspin/aiosendspin/pull/358) to accept those names.
- **Input:** the `ADC Input` select switches between `LINE2` (3.5 mm line-in, the boot default) and `LINE1` (onboard mics).
- **Codec variant:** the boot log's I²C scan should show `0x10`. `0x1A` is the AC101 variant, which this config does not support.

## Known quirks

- **ES8388 ADC setup:** ESPHome's `es8388` driver sets the ADC up for voice. `on_boot` switches it to line-level capture:
  - I²S framing: the driver writes left-justified (`0x0D`), but `i2s_audio` reads Philips I²S. Rewritten to `0x0C`.
  - ALC turned off.
  - Muting noise gate turned off.
- **Source only:** ESPHome's `i2s_audio` has no full-duplex mode. A speaker on the same bus would hold the lock the microphone needs.
- **Windows builds from a long path** fail while unpacking micro-opus (MAX_PATH). Set `ESPHOME_DATA_DIR` to a short directory.

## License

`components/sendspin` is derived from [ESPHome](https://github.com/esphome/esphome) and remains under the ESPHome License (MIT for the Python code, GPLv3 for the C++ code); see `LICENSE`.
