btc-e.com TollBOX console viewer

Now you should be able to see chat in appropriate window size.
Script requires an external library: websocket-client

By default script connect to the Russian channel.
You can switch the language by providing a parameter:

	chat_en | chat_ru | chat_cn

For example:

	btce-trollbox.py chat_en

INSTALL:
	
	pip install --user websocket-client
	wget -c https://raw.github.com/gloryman/btce-trollbox/master/btce-trollbox.py
