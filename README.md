Siri Server Core Plugins
========================

Do you like this?
-----------------
If you like this plugins you can help me by donating.
But don't worry the code will remain free, you don't have to donate.

[<img alt="PayPal — The safer, easier way to pay online." src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG_global.gif">](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FBD3VSLQDX6FQ&item_number=SSC%2dPlugins)

What is this?
-------------
This repository contains plugins I coded or adapted for [Eichhoernchen's SiriServerCore](https://github.com/Eichhoernchen/SiriServerCore).


What plugins are available?
---------------------------
At the moment there are:

* **Phone Call Plugin**:
  This allows you making phonecalls using your voice to any contact. It also detect related persons when calling.
  
* **Yahoo Weather Plugin**:
  This plugin gives you weather forecasts of your current location or any other location.
  It can also give you current Pressure, humidity, Visibility, etc.

* **Current Time Plugin**:
  This plugin allows you to ask for the date or for the time at a specific location or at your current location

* **RequestHandler Plugin**:
  This plugin enables you to react on search button presses if something was not recognized by SiriServer.
  It will probably be extended to other delayed requests that might be handeled in the future.


How do I enable the plugins?
----------------------------
You add the specific plugin by entering the plugin name (the name of the folder) into your plugins.conf of SiriServerCore.
The priority of the plugins is specified by the order from top (higher priority) to bottom (lower priority) in the plugins.conf.

If a plugin needs an API-Key, this key must be entered into apiKeys.conf of SiriServerCore.

 
Licensing the plugins
---------------------
All plugins contain a header that describe their license. Usually you can modify them as long as the header is untouched. 
Also you can use them for free for personal non commercial use. If you want to use them commercially you need to have a license for them and for SiriServerCore.
Also you must comply with any service that a plugin might use (e.g. Yahoo weather does not allow commercial use, so you cannot use it commercially although you have a SiriServerCore or Plugins license).
  
  
Disclaimer
----------
Apple owns all the rights on Siri. I do not give any warranties or guaranteed support for this software. Use it as it is.
 
