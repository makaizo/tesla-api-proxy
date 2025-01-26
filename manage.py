from mqtt_service import MQTTClient
import time
import requests
import credential_reader
import tesla_api_handler


# Example of subscribing to commands
def notify(message):
    print(f"Handling command: {message}")
    call_command(message)

def call_command(message):
    global is_running_forward
    global is_running_backward
    global engine_sound_type
    global is_illumi_initialized
    
    if message["command"] == "door_lock":
        print("door_lock command")
        tesla_api_handler.door_lock(auth_token, vin)


    if "wake_up" in message:
        if message[""] == "ON":
            light_controller.headlight_on()
        elif message["headLight"] == "OFF":
            light_controller.headlight_off()
        else:
            print("Invalid wake_up command")
    
    if "engine_sound" in message:
        engine_sound_type = message["engine_sound"]

    if "accel" in message:
        accel_value = message["accel"]
        if accel_value > 0:
            accel_value = max(accel_value, 50)
            accel_value = min(accel_value, 80)
            motor_controller.set_accel_speed(speed=accel_value, direction="forward")
            # print(f"[set_accel]speed:{accel_value}, direction:forward")

            if is_running_backward:
                engine_sound_controller.stop()
                is_running_backward = False
            if not is_running_forward:
                engine_sound_controller.play(sound_type= engine_sound_type, volume=1.0)
                is_running_forward = True

        elif accel_value < 0:
            accel_value = -accel_value
            accel_value = max(accel_value, 50)
            accel_value = min(accel_value, 100)
            motor_controller.set_accel_speed(speed=accel_value, direction="backward")
            # print(f"[set_accel]speed:{accel_value}, direction:backward")

            if is_running_forward:
                engine_sound_controller.stop()
                is_running_forward = False
            if not is_running_backward:
                engine_sound_controller.play(sound_type= "back", volume=1.0)
                is_running_backward = True
        
        # stop motor and engine sound
        else:
            is_running_backward = False
            is_running_forward = False
            accel_value = 0
            motor_controller.set_accel_speed(speed=accel_value, direction="forward")
            engine_sound_controller.stop()
        
        set_remote_motion_control_mode()

    if "steer" in message:
        direction = message["steer"]
        if direction == "left":
            motor_controller.set_steer(direction="left")

        elif direction == "right":
            motor_controller.set_steer(direction="right")
        set_remote_motion_control_mode()
        
    if "illumi" in message:
        illumi_data = message["illumi"]
        
        # Illumination On/Off control
        if "status" in illumi_data:
            if illumi_data["status"] == "on":
                if not is_illumi_initialized:
                    illumi_controller.initialize()
                    is_illumi_initialized = True
            elif illumi_data["status"] == "off":
                illumi_controller.turn_off()
            else:
                print("Invalid on command in illumi data")
        
        # Color control
        if all(color_key in illumi_data for color_key in ["r", "g", "b", "a"]):
            red = illumi_data["r"]
            green = illumi_data["g"]
            blue = illumi_data["b"]
            alpha = illumi_data["a"]
            
            # Set the illumination color (example method)
            illumi_controller.set_color(red, green, blue, alpha)
        else:
            print("invalid color data in illumi")

def initialize_mqtt(mqtt_token):
    # Initialize the MQTT client with broker address, port, and username token
    mqtt_client = MQTTClient(mqtt_token=mqtt_token, subscribe_topic="LC500/command")
    mqtt_client.subscribe(notify_callback=notify)

    # Start the MQTT client
    mqtt_client.start()


if __name__ == "__main__":
    credentials_path = "./credentials.json"
    auth_token, vin, mqtt_token = credential_reader.read_credentials(credentials_path)
    initialize_mqtt(mqtt_token)

    # Keep the script running
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")

