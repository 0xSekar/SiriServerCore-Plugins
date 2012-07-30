#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# This is a sms plugin for SiriServerCore
# created by Eichhoernchen
# modified by Sergio Karsvnie to use contactAPI and to accept related persons
#
# This file is free for private use.
#
# If you have a SiriServerCore commercial license
# you are allowed to use this plugin commercially otherwise you are breaking the law
#
# This file can be freely modified, but this header must retain untouched
#

import datetime
import random
from plugin import *
from siriObjects.systemObjects import *
from siriApi.contactApi import *
from siriApi.contactApi import text
from siriObjects.smsObjects import SmsSms, SmsSnippet

responses = {
'mustRepeat': 
    {'de-DE': [u"Entschuldigung ich hab dich leider nicht verstanden."],
     'en-US': [u"Sorry, I did not understand, please try again", u"Sorry, I don't know what you want"],
     'es-AR': [u"Lo siento, no entiendo, por favor intente nuevamente", u"Lo siento, no entiendo lo que desea"]
    },
'askForMessage':
    {'de-DE': [u"Was willst du schreiben?", u"Was soll drin stehen?", u"Du kannst mir jetzt diktieren!"],
     'en-US': [u"What do you want to say?", u"What do you want to include in the message?", u"Please dictate me the contents!"],
     'es-AR': [u"Qué quiere decir?", u"Qué quiere incluir en el mensaje?", u"Por favor dícteme el mensaje!"]
    },
'showUpdate': 
    {'de-DE': [u"Ich hab deine Nachricht geschrieben. Willst du sie jetzt senden?", u"OK. Willst du die Nachricht jetzt senden?"],
     'en-US': [u"I updated your message. Ready to send it?", u"Ok, I got that, do you want to send it?", u"Thanks, do you want to send it now?"],
     'es-AR': [u"Ok. Listo para enviarlo?", u"Ok, lo tengo, quiere enviarlo ahora?", u"Gracias, quiere enviarlo ahora?"]
    },
'cancelSms': 
    {'de-DE': [u"OK, I schick sie nicht.", u"OK, ich hab sie verworfen"],
     'en-US': [u"OK, I won't send it.", u"OK, I deleted it."],
     'es-AR': [u"OK, no lo enviaré.", u"OK, borré el mensaje."]
    },
'cancelFail':
    {'de-DE': [u"Sorry, aber mir ist ein Fehler beim Abbrechen passiert"],
     'en-US': [u"Sorry I could not properly cancel your message"],
     'es-AR': [u"Lo siento, no puedo cancelar correctamente su mensaje"]
    },
'createSmsFail':
    {'de-DE': [u"Ich konnte keine neue Nachricht anlegen, sorry"],
     'en-US': [u"I could not create a new message, sorry!"],
     'es-AR': [u"No puedo crear su mensaje, lo lamento!"]
    },
'updateSmsFail':
    {'de-DE': [u"Entschuldigung ich konnte die Nachricht nicht schreiben"],
     'en-US': [u"Sorry, I could not update your message!"],
     'es-AR': [u"Lo siento, no puedo actualizar su mensaje!"]
    },
'sendSms':
    {'de-DE': [u"OK, ich verschicke die Nachricht"],
     'en-US': [u"OK, I'll send your message."],
     'es-AR': [u"OK, enviaré su mensaje."]
    },
'sendSmsFail':
    {'de-DE': [u"Umpf da ist was schief gelaufen, sorry"],
     'en-US': [u"Hm something gone wrong, I could not send the message, I'm very sorry"],
     'es-AR': [u"Hm, algo falló, no puedo enviar su mensaje, lo lamento mucho"]
    },
'clarification':
    {'de-DE': [u"Fortfahren mit senden, abbrechen, anschauen oder ändern."],
     'en-US': [u"To continue, you can Send, Cancel, Review, or Change it."],
     'es-AR': [u"Para continuar, puede Enviar, Cancelar, Revisar, o Cambiar el mensaje."]
    },
'lostSms':
    {
        'en-US': [u"Sorry I lost your sms."],
        'es-AR': [u"Lo siento, perdí su mensaje."],
        },
'haveNewMessages': 
    {
        'en-US': [u"You have {0} new message{1}."],
        'es-AR': [u"Tiene {0} mensaje{1} nuevo{1}."],
        },
'noNewMessages': 
    {
        'en-US': [u"You don't have any new messages."],
        'es-AR': [u"No tiene ningún mensaje nuevo."]
    }
}

questions = {
'answerSEND': 
    {'de-DE': ['yes', 'senden'], # you must include yes
     'en-US': ['yes', 'send'],
     'es-AR': ['yes', 'si', 'enviar']
    },
'answerCANCEL':
    {'de-DE': ['cancel', 'abbrechen', 'stop', 'nein'],  # you must include cancel
     'en-US': ['cancel', 'no', 'abort'],
     'es-AR': ['cancel', 'cancelar', 'no', 'abortar', 'borrar']
    },
'answerUPDATE':
    {'de-DE': ['ändern', 'verändern'],
     'en-US': ['change', 'update'],
     'es-AR': ['modificar', 'cambiar', 'actualizar']
    },
'answerREVIEW':
    {'de-DE': ['anschauen', 'zeigen', 'zeig'],
     'en-US': ['review', 'view'],
     'es-AR': ['revisar', 'ver', 'controlar']
    }
}

snippetButtons = {
'denyText':
    {'de-DE': "Cancel",
     'en-US': "Cancel",
     'es-AR': "Cancelar"
    },
'cancelLabel':
    {'de-DE': "Cancel",
     'en-US': "Cancel",
     'es-AR': "Cancelar"
    },
'submitLabel':
    {'de-DE': "Send",
     'en-US': "Send",
     'es-AR': "Enviar"
    },
'confirmText':
    {'de-DE': "Send",
     'en-US': "Send",
     'es-AR': "Enviar"
    },
'cancelTrigger':
    {'de-DE': "Deny",
     'en-US': "Deny",
     'es-AR': "Deny"
    }
}

responseRegex = {
    "yes": {'en-US': ".*(yes|ya|yeah|yup|please|ok).*", 'es-AR': ".*(yes|si|por favor|ok).*"},
    "no":  {'en-US': ".*(no|nope|negative|negatory).*", 'es-AR': ".*(no|nop|negativo).*"},
    "read": {'en-US': ".*read.*", 'es-AR': ".*leer.*"},
    "reply": {'en-US': ".*reply.*", 'es-AR': ".*responder.*"},
    "cancel": {'en-US': ".*(cancel|neither|done).*", 'es-AR': ".*(cancelar|listo).*"},
    "next": {'en-US': ".*(next|continue).*", 'es-AR': u".*(próximo|proximo|continuar).*"}
}

class shortMessaging(Plugin):

    helpPhrases = {
        "en-US": ["\nSend SMS:\n", "-Send message|text to <contact> [<number type>]\n", "-Ex: Send text to John Smith work\n"],
        "es-AR": [u"\nEnviar SMS:\n", "-Enviar un mensaje a <contacto> [a <tipo tel.>]\n", u"-Enviar mensaje a mi <relación> [a <tipo tel.>]\n", " Ej:-Enviar mensaje a Juan Perez al trabajo\n", " Ej:-Enviar mensaje a mi hijo\n"]
    }

    def finalSend(self, sms, language):
        
        commitCMD = DomainObjectCommit(self.refId)
        commitCMD.identifier = SmsSms()
        commitCMD.identifier.identifier = sms.identifier
        
        answer = self.getResponseForRequest(commitCMD)
        if ObjectIsCommand(answer, DomainObjectCommitCompleted):
            answer = DomainObjectCommitCompleted(answer)
            # update the sms object with current identifier and time stamp
            sms.identifier = answer.identifier
            # the timestamp should be timezone aware
            # we could use the pytz lib for that
            # get the timezone from the assistant
            # and supply it to pytz which we can
            # supply to now()
            sms.dateSent = datetime.datetime.now() 
            # tell the user we sent the sms
            createAnchor = UIAddViews(self.refId)
            createAnchor.dialogPhase = createAnchor.DialogPhaseConfirmedValue
            
            # create a view to ask for the message
            askCreateView = UIAssistantUtteranceView()
            askCreateView.dialogIdentifier = "CreateSms#sentSMS"
            askCreateView.text = askCreateView.speakableText = random.choice(responses['sendSms'][language])
            askCreateView.listenAfterSpeaking = False
            
           
            snippet = SmsSnippet()
            snippet.smss = [sms]
            
            createAnchor.views = [askCreateView, snippet]
            
            self.sendRequestWithoutAnswer(createAnchor)
            self.complete_request()
        else:
            self.say(random.choice(responses['sendSmsFail'][language]))
            self.complete_request()
            
            
    def createSmsSnippet(self, sms, addConfirmationOptions, dialogIdentifier, text, language):
        createAnchor = UIAddViews(self.refId)
        createAnchor.dialogPhase = createAnchor.DialogPhaseConfirmationValue
        
        # create a view to ask for the message
        askCreateView = UIAssistantUtteranceView()
        askCreateView.dialogIdentifier = dialogIdentifier
        askCreateView.text = askCreateView.speakableText = text
        askCreateView.listenAfterSpeaking = True
        
        # create a snippet for the sms
        snippet = SmsSnippet()
        if addConfirmationOptions:
            # create some confirmation options
            conf = UIConfirmSnippet({})
            conf.requestId = self.refId
            
            confOpts = UIConfirmationOptions()
            confOpts.submitCommands = [SendCommands([conf, StartRequest(False, "^smsConfirmation^=^yes^")])]
            confOpts.confirmCommands = confOpts.submitCommands
            
            cancel = UICancelSnippet({})
            cancel.requestId = self.refId
            
            confOpts.cancelCommands = [SendCommands([cancel, StartRequest(False, "^smsConfirmation^=^cancel^")])]
            confOpts.denyCommands = confOpts.cancelCommands
            
            confOpts.denyText = snippetButtons['denyText'][language]
            confOpts.cancelLabel = snippetButtons['cancelLabel'][language]
            confOpts.submitLabel = snippetButtons['submitLabel'][language]
            confOpts.confirmText = snippetButtons['confirmText'][language]
            confOpts.cancelTrigger = snippetButtons['cancelTrigger'][language]
            
            snippet.confirmationOptions = confOpts
            
        snippet.smss = [sms]
        
        createAnchor.views = [askCreateView, snippet]
        
        return createAnchor
            
    def createNewMessage(self, phone, person):
        # create a new domain object the sms...
        x = SmsSms()
        x.recipients = [phone.number]
        msgRecipient = PersonAttribute()
        msgRecipient.object = ABPerson()
        msgRecipient.object.identifier = person.identifier
        msgRecipient.data = phone.number
        msgRecipient.displayText = person.fullName
        x.msgRecipients = [msgRecipient]
        x.outgoing = True
        answer = self.getResponseForRequest(DomainObjectCreate(self.refId, x))
        if ObjectIsCommand(answer, DomainObjectCreateCompleted):
            answer = DomainObjectCreateCompleted(answer)
            x = SmsSms()
            x.outgoing = True
            x.identifier = answer.identifier
            return x
        else:
            return None
        
    def getSmssForIdentifier(self, identifier):
        # fetch the current version
        retrieveCMD = DomainObjectRetrieve(self.refId)
        x = SmsSms()
        x.identifier = identifier
        retrieveCMD.identifiers = [x]
        answer = self.getResponseForRequest(retrieveCMD)
        if ObjectIsCommand(answer, DomainObjectRetrieveCompleted):
            answer = DomainObjectRetrieveCompleted(answer)
            if len(answer.objects) > 1:
                self.logger.warning("I do not support multiple messages!")
            result = SmsSms()
            result.initializeFromPlist(answer.objects[0].to_plist())
            return result
        else:
            return None
        
    def askAndSetMessage(self, sms, language):
        createAnchor = self.createSmsSnippet(sms, False, "CreateSms#smsMissingMessage", random.choice(responses['askForMessage'][language]), language)

        smsText = self.getResponseForRequest(createAnchor)
        # update the domain object
        
        updateCMD = DomainObjectUpdate(self.refId)
        updateCMD.identifier = sms
        updateCMD.addFields = SmsSms()
        updateCMD.setFields = SmsSms()
        updateCMD.setFields.message = smsText
        updateCMD.removeFields = SmsSms()
        
        answer = self.getResponseForRequest(updateCMD)
        if ObjectIsCommand(answer, DomainObjectUpdateCompleted):
            return sms
        else:
            return None
            
    def showUpdateAndAskToSend(self, sms, language):
        createAnchor = self.createSmsSnippet(sms, True, "CreateSms#updatedMessageBody", random.choice(responses['showUpdate'][language]), language)
        
        response = self.getResponseForRequest(createAnchor)
        match = re.match("\^smsConfirmation\^=\^(?P<answer>.*)\^", response)
        if match:
            response = match.group('answer')
        
        return response
    
    def cancelSms(self, sms, language):
        # cancel the sms
        cancelCMD = DomainObjectCancel(self.refId)
        cancelCMD.identifier = SmsSms()
        cancelCMD.identifier.identifier = sms.identifier
        
        answer = self.getResponseForRequest(cancelCMD)
        if ObjectIsCommand(answer, DomainObjectCancelCompleted):
            createAnchor = UIAddViews(self.refId)
            createAnchor.dialogPhase = createAnchor.DialogPhaseCanceledValue
            cancelView = UIAssistantUtteranceView()
            cancelView.dialogIdentifier = "CreateSms#wontSendSms"
            cancelView.text = cancelView.speakableText = random.choice(responses['cancelSms'][language])
            createAnchor.views = [cancelView]
            
            self.sendRequestWithoutAnswer(createAnchor)
            self.complete_request()
        else:
            self.say(random.choice(responses['cancelFail'][language]))
            self.complete_request()
    
    def askForClarification(self, sms, language):
        createAnchor = self.createSmsSnippet(sms, True, "CreateSms#notReadyToSendSms", random.choice(responses['clarification'][language]), language)
        
        response = self.getResponseForRequest(createAnchor)
        match = re.match("\^smsConfirmation\^=\^(?P<answer>.*)\^", response)
        if match:
            response = match.group('answer')
            
        return response
        
    def message(self, phone, person, language):
        smsObj = self.createNewMessage(phone, person)
        if smsObj == None:
            self.say(random.choice(responses['createSmsFail'][language]))
            self.complete_request()
            return
        smsObj = self.askAndSetMessage(smsObj, language)
        if smsObj == None:
            self.say(random.choice(responses['updateSmsFail'][language]))
            self.complete_request()
            return
        satisfied = False
        state = "SHOW"
        
        # lets define a small state machine 
        while not satisfied:
            smsObj = self.getSmssForIdentifier(smsObj.identifier)
            if smsObj == None:
                self.say(responses['lostSms'][language])
                self.complete_request()
                return
            
            if state == "SHOW":
                instruction = self.showUpdateAndAskToSend(smsObj, language).strip().lower()
                if any(k in instruction for k in (questions['answerSEND'][language])):
                    state = "SEND"
                    continue
                if any(k in instruction for k in (questions['answerCANCEL'][language])):
                    state = "CLARIFY"
                    continue
                self.say(random.choice(responses['mustRepeat'][language]))
                continue
            
            elif state == "WRITE":
                smsObj = self.askAndSetMessage(smsObj, language)
                if smsObj == None:
                    self.say(random.choice(responses['updateSmsFail'][language]))
                    self.complete_request()
                    return
                state = "SHOW"
                continue
            
            elif state == "CLARIFY":
                instruction = self.askForClarification(smsObj, language).strip().lower()
                if any(k in instruction for k in (questions['answerSEND'][language])):
                    state = "SEND"
                    continue
                if any(k in instruction for k in (questions['answerCANCEL'][language])):
                    state = "CANCEL"
                    continue
                if any(k in instruction for k in (questions['answerUPDATE'][language])):
                    state = "WRITE"
                    continue
                if any(k in instruction for k in (questions['answerREVIEW'][language])):
                    state = "SHOW"
                    continue
                self.say(random.choice(responses['mustRepeat'][language]))
                continue
            
            elif state == "CANCEL":
                self.cancelSms(smsObj, language)
                satisfied = True
                continue
            
            elif state == "SEND":
                self.finalSend(smsObj, language)
                satisfied = True
                continue
        
    @register("en-US", "(Write |Send |Compose |New )?(a |an )?(message|sms|text)( to| for)? (?P<recipient>[\w ]+?)( (?P<type>work|home|mobile|main|iPhone|pager))?$")
    @register("de-DE", "(Sende|Schreib.)( eine)?( neue)? (Nachricht|sms) an (?P<recipient>[\w ]+?)( (?P<type>arbeit|zuhause|privat|mobil|handy.*|iPhone.*|pager))?$")
    @register("es-AR", u"(Enviar|Escribir|Componer|Nuevo)( un)?( nuevo)? (mensaje|texto|sms)( para| a) (?!mi )(?P<recipient>[\w ]+?)((a (la |el )?|al )?(?P<type>trabajo|casa|móvil|movil|principal|iPhone|busca))?$")
    def sendSMS(self, speech, lang, regex):
        recipient = regex.group('recipient')
        numberType = regex.group('type').lower() if "type" in regex.groupdict() and regex.group('type') is not None else None
        numberType = getNumberTypeForName(numberType, lang)
        possibleRecipients =  searchPerson(self, scope = ABPersonSearch.ScopeLocalValue, name = recipient)
        personToMessage = personAction(self, possibleRecipients, lang)

        if personToMessage != None:
	    self.message(findPhoneForNumberType(self, personToMessage, numberType, lang), personToMessage, lang)
            return # complete_request is done there
        else:
            self.say(text['notFound'][lang].format(regex.group('recipient')))
            self.complete_request()

    @register("es-AR", u"(Enviar|Escribir|Componer|Nuevo)( un)?( nuevo)? (mensaje|texto|sms)( para| a) mi (?P<recipient>[\w ]+?)((a (la |el )?|al )?(?P<type>trabajo|casa|móvil|movil|principal|iPhone|busca))?$")
    def sendSMSRelated(self, speech, lang, regex):
        recipient = regex.group('recipient').strip()
        numberType = regex.group('type').lower() if "type" in regex.groupdict() and regex.group('type') is not None else None
        numberType = getNumberTypeForName(numberType, lang)

	personToMessage = definePerson(self, scope = ABPersonSearch.ScopeLocalValue, name = None, relation=recipient, me=True, language=lang)

        if personToMessage != None:
            self.message(findPhoneForNumberType(self, personToMessage, numberType, lang), personToMessage, lang)
            return # complete_request is done there

###--- Los métodos de acceso a nuevos mensajes aún no funcionan ---###

    #methods for message dictation
    def readMessage(self, context):
        #get sender from the AlertContext objects for the assistant
        sender = context.msgSender.displayText
        #send the a view with the name of the sender
        summary = "New message from {0}:".format(sender)
        views = AddViews(self.refId, temporary=False, dialogPhase="Summary", scrollToTop=False, views=[])
        views.views.append(AssistantUtteranceView(text=summary, speakableText='', dialogIdentifier="FindSms#readThem"))
        self.sendRequestWithoutAnswer(views)
        #Send the SayIt command to the phone, so it will speak the contents of the message
        sayIt = UISayIt(self.refId)
        sayIt.context = context
        sayIt.message = "New message from @{obj#sender} @{tts#\x1b\\pause=300\\\x1b\\rate=90\\}@{obj#subject}@{tts#\x1b\\pause=300\\\x1b\\rate=100\\} @{tts#\x1b\\pause=300\\\x1b\\rate=90\\}@{obj#message}@{tts#\x1b\\pause=300\\\x1b\\rate=100\\}"
        self.send_object(sayIt)
    
    def postMessageReadHandler(self, msgContext, language, nextMessage=False):
        summary = u"You can \u2018Reply\u2019 or \u2018Read it\u2019 again."
        views = AddViews(self.refId, temporary=False, dialogPhase="Summary", scrollToTop=False, views=[])
        views.views.append(AssistantUtteranceView(text=summary, speakableText= "@{tts#\x1b\\pause=800\\}You can @{tts#\x1b\\pause=25\\}reply, or read it again.", listenAfterSpeaking=True, dialogIdentifier="FindSms#readingPostActions"))
        resp = self.getResponseForRequest(views).encode('ascii')
        read = re.compile(responseRegex['read'][language], re.IGNORECASE)
        reply = re.compile(responseRegex['reply'][language], re.IGNORECASE)
        cancel = re.compile(responseRegex['cancel'][language], re.IGNORECASE)
        cont = re.compile(responseRegex['next'][language], re.IGNORECASE)
        while (read.match(resp) == None) and (reply.match(resp) == None) and (cancel.match(resp) == None) and (cont.match(resp) == None):
            self.say("I didn't get that, please try again.")
            summary = u"You can \u2018Reply\u2019 or \u2018Read it\u2019 again."
            views = AddViews(self.refId, temporary=False, dialogPhase="Summary", scrollToTop=False, views=[])
            views.views.append(AssistantUtteranceView(text=summary, speakableText= "@{tts#\x1b\\pause=800\\}You can @{tts#\x1b\\pause=25\\}reply, or read it again.", listenAfterSpeaking=True, dialogIdentifier="FindSms#readingPostActions"))
            resp = self.getResponseForRequest(views).encode('ascii')
        if read.match(resp):
            self.readMessage(msgContext)
            self.postMessageReadHandler(msgContext, language, nextMessage)
        elif reply.match(resp):
            self.message(msgContext.msgSender.object.phones[0], msgContext.msgSender.object, language)                
        elif cancel.match(resp):
            return 0;
        elif nextMessage and cont.match(resp):
            return 1;
 
    @register("en-US", "(Do I have|Check)( for| many| any)?( new)? messages.*")
    @register("es-AR", "(Tengo|Controlar|Comprobar)( algún| algun| algunos| si tengo)?( nuevos| nuevo)? mensaje.*")
    def checkNewMessages(self, speech, langauge, regex):
        if hasattr(self.assistant, 'alerts') and (self.assistant.alerts != None):
            numNewMessages = len(self.assistant.alerts)
            self.say(random.choice(responses['haveNewMessages'][langauge]).format(numNewMessages, "s" if numNewMessages>1 else ""))
        else:
            self.say(random.choice(responses['noNewMessages'][langauge]))
        self.complete_request()
    
    @register("en-US", "Read( me)?( my)?( new)? (message|messages)")
    @register("es-AR", "Leer( mis)? (mensajes|mensaje)( nuevos)?")
    def readNewMessgages(self, speech, langauge, regex):
        if hasattr(self.assistant, 'alerts') and (self.assistant.alerts != None):
            for context in self.assistant.alerts:
                nextMessage = False
                if len(self.assistant.alerts)>1 and context!=self.assistant.alerts[len(self.assistant.alerts)-1]:
                    nextMessage = True; #if this isn't the last new message waiting, we pass the postReadHandler this information, so it can allow the user to read next.
                self.readMessage(context)
                #Send the alert acknowledge command to the phone, so it will clear the alert flag for the message
                alertAck = AcknowledgeAlert(self.refId)
                alertAck.object = context
                self.send_object(alertAck)
                #ask the user what they want to do
                cont = self.postMessageReadHandler(context, langauge, nextMessage)
                if cont == 0:
                    self.complete_request();
                    return; 
        else:
            self.say(random.choice(responses['noNewMessages'][langauge]))
        self.complete_request()
