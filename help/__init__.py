#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This is a help plugin for SiriServerCore
#
# Created by Sergio Karsvnie
#
# This file is free for private use.
#
# If you have a SiriServerCore commercial license
# you are allowed to use this plugin commercially otherwise you are breaking the law
#
# This file can be freely modified, but this header must retain untouched
#

import re,os

from plugin import *

from PluginManager import plugins

response = {
	"en-US": u"Here are the commands which are possible in your language:",
	"de-DE": u"Das sind die Befehle die in Deiner Sprache verfügbar sind:",
	"es-AR": u"Estos son los comandos que puede utilizar en su lenguaje:"
}

class help(Plugin):

# List of help phrases used by the helpPlugin
    helpPhrases = {
	"en-US": ["\nHelp:\n", "-Help\n", "-Commands\n"],
        "de-DE": ["\nHilfe:\n", "-Hilfe\n", "-Befehle\n"],
	"es-AR": ["\nAyuda:\n", "-Ayuda\n", "-Comandos\n", u"-¿Qué puedo hacer?\n"]
    }

    @register("de-DE", "(Hilfe)|(Befehle)")
    @register("en-US", "(Help)|(Commands)")
    @register("es-AR", "(Ayuda)|(Comandos)|((Que|Qué) puedo hacer)")
    def st_hello(self, speech, language):
        resp = {}
        for lang in plugins: # This dict may change, no way to cache reliably
            langresp = resp.setdefault(lang, [])
            if not lang == language: continue
            
            classes = []
            for rexp, Class, func in plugins.get(lang, []):
                if not Class in classes:
                    classes.append(Class)

            for Class in classes:
                if hasattr(Class, "helpPhrases"):
                    langresp.append(Class.helpPhrases.get(lang, "N/A"))

	r = ''	
	y = ''
	for x in resp[language]:
	        y = ''.join(x)
		r += y
	self.say(response[language]);
        self.say(r.strip(), " ")
        self.complete_request()
