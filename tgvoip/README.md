# Home Assistant Addon: Telegram VOIP calls

This addon allows you to issue and receive Telegram VOIP calls.

## Installation and first boot

Before starting, read Telegram's documentation on creating your own 
[Telegram app](https://core.telegram.org/api/obtaining_api_id)

After installation, complete the relevant config parts:

- __api_id__ Your Telegram app API id
- __api_hash__ Your Telegram app API hash
- __phone__ The phone number you'll use to make calls (bots can't make calls)
- __database_key__ Your Telegram app database encryption key
- __data_dir__ Where the addon will store its data
- __mqtt_server__ IP of the MQTT server to connect to

Also make sure you select the desired audio devices in the add on config.

After installing and before starting you should monitor MQTT messages,
for example by running on your desktop:

```mosquitto_sub -h <mqtt_server_ip> -t "telegram/#" -v```

When the add on is started, it will try to log in and issue a MQTT publication
with the topic "telegram/code/request", this means that the Telegram server sent an
authentication code to your phone. The addon will wait for a message with topic
"telegram/code" with the code as payload, for example:

```mosquitto_pub -h <mqtt_server_ip> -t "telegram/code" -m "12345"```

This process is required only on the first time the add on is run, after that
it will be able to log in automatically.

# Making calls

To make a call, send a MQTT message with topic "telegram/call" and payload
of the user id (__not__ the phone number) you want to reach out to:

```mosquitto_pub -h <mqtt_server_ip> -t "telegram/call" -m "123456789"```

# Accepting calls

When an incoming call shows up, the addon will send a MQTT message with topic
"telegram/call/incoming" and the user id as payload.
To answer:

```mosquitto_pub -h <mqtt_server_ip> -t "telegram/call/answer" -m ""```

# Disconnecting calls
Finally, to finish any call (incoming or outgoing) from your side:

```mosquitto_pub -h <mqtt_server_ip> -t "telegram/call/disconnect" -m ""```

Just remember to say good bye first :)
