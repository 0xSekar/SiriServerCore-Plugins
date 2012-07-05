#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# This is a Phone Call plugin for SiriServerCore
#
# Created by Sergio Karsvnie, based on the work by Eichhoernchen
# Modified and corrected to use contactAPI and to accept related persons
#
# This file is free for private use.
#
# If you have a SiriServerCore commercial license
# you are allowed to use this plugin commercially otherwise you are breaking the law
#
# This file can be freely modified, but this header must retain untouched
#

from plugin import *
from siriApi.contactApi import *
from siriApi.contactApi import text
from siriObjects.phoneObjects import PhoneCall
from siriObjects.systemObjects import SendCommands, StartRequest, ResultCallback, \
    PersonAttribute

responses = {
'callPersonSpeak':
    {'de-DE': u"Rufe {0}, {1} an.",
     'en-US': u"Calling {0}, {1}.",
     'es-AR': u"Llamando a {0}, {1}."
    },
'callPerson': 
    {'de-DE': u"Rufe {0}, {1} an: {2}",
     'en-US': u"Calling {0}, {1}: {2}",
     'es-AR': u"Llamando a {0}, {1}: {2}"
    }
}

errorOnCallResponse={'en-US':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Your phone is in airplane mode.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Uh, I can't seem to find a good connection. Please try your phone call again when you have cellular access.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Sorry, I can't call this number.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Oh oh, I can't make your phone call.",
                       'code': -1}],
                     'de-DE':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Dein Telefon ist im Flugmodus.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Oh je! Ich kann im Moment keine gute Verbindung bekommen. Versuch es noch einmal, wenn du wieder Funkempfang hast.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Ich kann diese Nummer leider nicht anrufen.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Tut mir leid, Ich, ich kann momentan keine Anrufe t�tigen.",
                       'code': -1}],
		     'es-AR':
                     [{'dialogIdentifier':u"PhoneCall#airplaneMode",
                       'text': u"Su teléfono está en modo avión.",
                       'code': 1201},
                      {'dialogIdentifier': u"PhoneCall#networkUnavailable",
                       'text': u"Oh, no puedo encontrar una buena conexión. Por favor intente nuevamente cuando tenga acceso a la red celular.",
                       'code': 1202},
                      {'dialogIdentifier': u"PhoneCall#invalidNumber",
                       'text': u"Lo siento, no puedo llamar a este número.",
                       'code': 1203},
                      {'dialogIdentifier': u"PhoneCall#fatalResponse",
                       'text': u"Lo siento, no puedo realizar su llamada.",
                       'code': -1}]
}

class phonecallPlugin(Plugin):

    helpPhrases = {
        "en-US": ["\nPhone Call:\n", "-Call <contact> [<number type>]\n", "-Ex: Call John Smith work\n"],
        "es-AR": [u"\nLlamadas Telefónicas:\n", "-Llamar a <contacto> [a <tipo tel.>]\n", u"-Llamar a mi <relación> [a <tipo tel.>]\n", " Ej:-Llamar a Juan Perez al trabajo\n", " Ej:-Llamar a mi hijo\n"]
    }

    def call(self, phone, person, language):
        root = ResultCallback(commands=[])
        rootView = AddViews("", temporary=False, dialogPhase="Completion", views=[])
        root.commands.append(rootView)
        rootView.views.append(AssistantUtteranceView(text=responses['callPerson'][language].format(person.fullName, numberTypesLocalized[phone.label][language], phone.number), speakableText=responses['callPersonSpeak'][language].format(person.fullName, numberTypesLocalized[phone.label][language]), dialogIdentifier="PhoneCall#initiatePhoneCall", listenAfterSpeaking=False))
        rootView.callbacks = []
        
        # create some infos of the target
        personAttribute=PersonAttribute(data=phone.number, displayText=person.fullName, obj=Person())
        personAttribute.object.identifer = person.identifier
        call = PhoneCall("", recipient=phone.number, faceTime=False, callRecipient=personAttribute)
        
        rootView.callbacks.append(ResultCallback(commands=[call]))
        
        call.callbacks = []
        # now fill in error messages (airplanemode, no service, invalidNumber, fatal)
        for i in range(4):
            errorRoot = AddViews(None, temporary=False, dialogPhase="Completion", scrollToTop=False, views=[])
            errorRoot.views.append(AssistantUtteranceView(text=errorOnCallResponse[language][i]['text'], speakableText=errorOnCallResponse[language][i]['text'], dialogIdentifier=errorOnCallResponse[language][i]['dialogIdentifier'], listenAfterSpeaking=False))
            call.callbacks.append(ResultCallback(commands=[errorRoot], code=errorOnCallResponse[language][i]['code']))
            
        self.complete_request([root])

    @register("de-DE", "ruf. (?P<name>[\w ]+?)( (?P<type>arbeit|zuhause|privat|mobil|handy.*|iPhone.*|pager))? an$")
    @register("en-US", "(make a )?call (to )?(?P<name>[\w ]+?)( (?P<type>work|home|mobile|main|iPhone|pager))?$")
    @register("es-AR", u"(Hacer (una |un ))?(llamada|llamar|llamado) a (?!mi )(?P<name>[\w ]+?)((a (la |el )?|al )?(?P<type>trabajo|casa|móvil|movil|principal|iPhone|busca))?$")
    def makeCall(self, speech, language, regex):
        personToCall = regex.group('name')
        numberType = regex.group('type').lower() if "type" in regex.groupdict() and regex.group('type') is not None else None
        numberType = getNumberTypeForName(numberType, language)
	persons = searchPerson(self, scope = ABPersonSearch.ScopeLocalValue, name = personToCall)
        personToCall = personAction(self, persons, language)
                    
        if personToCall != None:
            self.call(findPhoneForNumberType(self, personToCall, numberType, language), personToCall, language)
            return # complete_request is done there
	else:
            self.say(text['notFound'][language].format(regex.group('name')))                         
            self.complete_request()
    
    @register("es-AR", u"(Hacer (una |un ))?(llamada|llamar|llamado) a mi (?P<relation>[\w ]+?)((a (la |el )?|al )?(?P<type>trabajo|casa|móvil|movil|principal|iPhone|busca))?$")
    def makeCallRelated(self, speech, language, regex):
        personToCall = regex.group('relation').strip()
        numberType = regex.group('type').lower() if "type" in regex.groupdict() and regex.group('type') is not None else None
        numberType = getNumberTypeForName(numberType, language)

	personToCall = definePerson(self, scope = ABPersonSearch.ScopeLocalValue, name = None, relation=personToCall, me=True, language=language)
                    
        if personToCall != None:
            self.call(findPhoneForNumberType(self, personToCall, numberType, language), personToCall, language)
            return # complete_request is done there
