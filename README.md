Siri Server Core Plugins
========================

Do you like this?
-----------------
If you like this plugins you can help me by donating.
But don't worry the code will remain free, you don't have to donate.

[<img alt="PayPal — The safer, easier way to pay online." src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG_global.gif">](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FBD3VSLQDX6FQ&item_number=SSC%2dPlugins)

What is this?
-------------
This repository contains plugins I coded or adapted for Eichhoernchen's SiriServerCore (a Siri server based on Google's speech API).

This plugins were tested against [my fork](https://github.com/0xSekar/SiriServerCore) which has some bug fixes on the contactApi.

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

* **Help Plugin**:
  This plugin tells you the phrases you can use on the server (based on the installed plugins).

* **RequestHandler Plugin**:
  This plugin enables you to react on search button presses if something was not recognized by SiriServer.
  It will probably be extended to other delayed requests that might be handeled in the future.

* **Short Message Plugin**:
  This plugin allows you to send short messages using your voice to any contact. It also detect related persons.

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

==============================================================


Te resulta útil este desarrollo?
--------------------------------
Si estos plugins te resultan útiles, puedes considerar realizar una donación.
Pero no te preocupes, el código permanecerá libre y no tienes ninguna obligación de donar.

[<img alt="PayPal — The safer, easier way to pay online." src="https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG_global.gif">](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FBD3VSLQDX6FQ&item_number=SSC%2dPlugins)

Que es este software?
---------------------
Este repositorio contiene plugins para SiriServerCore (un emulador de servidor Siri basado en las API de google para reconocimiento de voz) desarrollado por Eichhoernchen.

Estos plugins fueron testeados contra [mi propio fork](https://github.com/0xSekar/SiriServerCore) del servidor, que tiene algunas correcciones a la API de contactos.

Que plugins están disponibles?
------------------------------
Por el momento los plugins son los siguientes:

* **LLamadas telefónicas**:
  Permite realizar llamadas telefónicas utilizando Siri a cualquier contacto.
  También detecta personas relacionadas para permitir realizar llamadas del tipo "Llamar a mi hermano".

* **Yahoo Clima**:
  Este plugin te dará el pronóstico en tu posición actual o en cualquier otro punto que indiques.
  También puede darte información sobre Presión, humedad, visibilidad, etc.

* **Fecha y Hora**:
  Este plugin te permite consultar por la hora actual en tu posición o en cualquier lugar que desees. Además te permite consultar la fecha actual.

* **Ayuda**:
  Este plugin te informa las frases que puedes utilizar en el servidor en función de los plugins instalados.

* **RequestHandler Plugin**:
  Este plugin permite la utilización del botón "Buscar en la WEB" que muestra Siri cuando no entiende un pedido.

* **Mensajes cortos**:
  Permite enviar SMS utiilzando siri a cualquier contacto.
  También detecta personas relacionadas para permitir enviar mensajes del tipo "Enviar SMS a mi hermano".

Cómo habilito los plugins?
--------------------------
Para habilitar un plugin en particular, debes ingresar su nombre (el nombre de la carpeta que lo contiene) en el archivo plugins.conf de tu instalación de SiriServerCore.
La prioridad de los plugins queda establecida por el orden de aparición (el primero el más importante y el último el menos importante) en el archivo plugins.conf.

Si un plugin necesita una clave (API-Key) de algún proveedor, esta clave debe ser ingresada en el archivo apiKeys.conf de tu instalación de SiriServerCore.


Licencia de los plugins
-----------------------
La mayoría de los plugins contienen un encabezado indicando su licencia. Usualmente puedes modificar los mismos siempre que no modifiques el encabezado.
Los plugins pueden utilizarse en forma gratuita para uso personal no comercial. Si deseas utilizarlos comercialmente, necesitarás una licencia comercial para ellos y para el servidor SiriServerCore.
Además, debes cumplir con los términos de licencia de cualquier servicio que el plugin utilice (por ejemplo, Yahoo clima no permite el uso comercial de su API, por lo tanto, no puede utilizarse el plugin de clima de Yahoo comercialmente aunque se disponga de un licencia comercial para estos plugins y para el servidor SiriServerCore.


Renuncia de responsabilidad
---------------------------
Apple posee todos los derechos sobre Siri. No doy ninguna garantía o apoyo garantizado por este software. Usalo como es.
 
