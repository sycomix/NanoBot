#!/usr/bin/python
import aiml
import logging
import os

bot_name = "NanoBot"
bot_master = "NanoDano"

brain_file = "brains/standard.brn"
std_startup_file = "std-startup.xml"
default_load_command = "load aiml b"


class NanoLogic():

	def __init__(self):	
		# Initialize AIML Kernel
		self.aimlk = aiml.Kernel()

		# Name/owner settings
		self.aimlk.setBotPredicate('name', bot_name)
		self.aimlk.setBotPredicate('master', bot_master)

		# Brain files can save startup time
		# need a way to auto-update this if needed check_brain_updates
		# and need a separate save_brain function
		# file exist/write verification
		if os.path.isfile(brain_file):
		    self.aimlk.bootstrap(brainFile = brain_file)
		else:

		    self.aimlk.bootstrap(learnFiles = std_startup_file, commands = default_load_command)
		    self.aimlk.saveBrain(brain_file)



	# Process text using AIML and return response
	# Use separate sessions based on from name
	def aiml_process(self, msg):
		return self.aimlk.respond(msg['body'], msg['from'].bare) 