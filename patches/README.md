# Music Assistant 2.10.6 legacy Noise handshake compatibility

Music Assistant 2.10.6 pins `aiosendspin[server]==9.1.1`. That server sends a Noise msg1
payload containing `psk_id` without `psk_category`. `sendspin-cpp` v0.9.3 rejects it.

`noise_handshake_legacy_aiosendspin_9_1_1.patch` is a proposed compatibility patch
against `Sendspin/sendspin-cpp` v0.9.3's `src/noise_handshake.cpp`. It accepts an
omitted category only by looking up the PSK ID in the existing credential store.
It does not disable the Noise encrypted handshake or relax server-ID binding.

**Not active:** This project still downloads the upstream `sendspin-cpp` component.
Putting a patch file in the ESPHome external-component repository does not patch
an ESP-IDF managed dependency. A fork of `Sendspin/sendspin-cpp` with the patch
applied, followed by updating `SENDSPIN_CPP_REPO` / `SENDSPIN_CPP_REF`
(or the `esp32.add_idf_component` invocation), is required.

This patch is **uncompiled and untested**. Check against the library source, compile,
then test pairing and PCM audio before treating it as working.
