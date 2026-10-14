#pragma once

#include "esphome/core/defines.h"

#ifdef USE_ESP_IDF

#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/core/component.h"
#include "sendspin_hub.h"

namespace esphome::sendspin_ {

// Pairing tokens are long-lived credentials. This entity is opt-in and
// never writes the token to the ESPHome logger.
class SendspinPairingTokenTextSensor : public text_sensor::TextSensor,
                                       public PollingComponent,
                                       public Parented<SendspinHub> {
 public:
  void update() override {
    const auto token = this->parent_->get_pairing_token();
    if (token.has_value() && (!this->has_state() || this->state != *token)) {
      this->publish_state(*token);
    }
  }
};

}  // namespace esphome::sendspin_

#endif  // USE_ESP_IDF
