import re
from fsdprotocol import fsdprotocol
from fsdclientinfo import fsdclientinfo

class fsdapi:


	def __init__(self):
		FSD					=	fsdprotocol()
		self.FSDAddPilot	=	FSD.FSDAddPilot()
		self.FSDPlaneInfo	=	FSD.FSDPlaneInfo()
		self.FSDFlightPlan	= 	FSD.FSDFlightPlan()
		self.FSDPilotPosition = FSD.FSDPilotPosition()
		self.FSDInfoRequest	=	FSD.FSDInfoRequest()	
	
	def AddPilot(self,words,client_socket,client,registry):
		#APAAAA:SERVER:XP210:PASSWORD:11:B:14:FULL NAME ICAO
		#  0      1      2     3       4 5  6  7
		matches		= re.match(self.FSDAddPilot+'([A-Za-z0-9]+)',words[0])
		callsign 	= matches.group(1)
		username	= words[2]
		password	= words[3]
		rank		= words[4]
		fsdversion	= words[5]
		simver		= words[6]

		errorCount = 0
		
		#cleck to see if registry
		existingClient = registry.GetRegistry()

		if username in existingClient.keys():
			client.SetVerification(False)
			client.SetError(errorCount,"Already Logged In")
			errorCount+=1
		else:		
			client.SetVerification(True)
			
		for val in existingClient.keys():
			if existingClient[val]["callsign"]==callsign:
				client.SetVerification(False)
				client.SetError(errorCount,"Callsign areadly in use")
				errorCount+=1
	
		client.SetUserName(username)
		client.SetPassword(password)
		client.SetCallSign(callsign)
		client.SetRank(rank)
		client.SetFsdVer(fsdversion)
		client.SetSimVer(simver)
		client.SetFullName(words[7])
		client.SetConnection(client_socket)

		return client


	def PlaneInfo(self,words,client):
	
		airplane = words[2]
		client.SetAirPlane(airplane)
		
		return client

	
	def FlightPlan(self,words):
		matches = re.match(self.FSDPlaneInfo+'([A-Za-z0-9]+)',words[0])
		return(matches)
		
	def PilotPosition(self,words,client):
		# ident callsign transponder rating latitude longitude truealt speed pitchbankheading
		#@N:N169J:1200:3:43.12345:-78.543:12000:120:3487239347:60
	
		ident = re.match(self.FSDPilotPosition+'([A-Z])',words[0]) #Get Ident
		
		client.SetIdent(ident.group(1))
		client.SetTransponder(words[2])	
		client.SetRating(words[3])
		client.SetLatitude(words[4])
		client.SetLongitude(words[5])
		client.SetTrueAlt(words[6])
		client.SetSpeed(words[7])
		client.SetPitchBankHeading(words[8])
		client.SetGround(words[9])
		
		return client

		
		
		

		
		