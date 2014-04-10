#!/usr/bin/python
import aiml
import logging
import os





class NanoLogic():

	def __init__(self, bot_name, bot_master, brain_file, std_startup_file, default_load_command):	
		# Initialize AIML Kernel
		self.aimlk = aiml.Kernel()

		# Name/owner settings
		self.aimlk.setBotPredicate('name', bot_name)
		self.aimlk.setBotPredicate('master', bot_master)

		# Brain files can save startup time
		# need a way to auto-update this if needed check_brain_updates
		# and need a separate save_brain function
		# file exist/write verification

		# Change path so that relative paths work
		current_path = os.getcwd()
		bot_root_path = os.path.dirname(os.path.realpath(__file__))
		if current_path != bot_root_path:
			os.chdir(bot_root_path)

		if os.path.isfile(brain_file):
		    self.aimlk.bootstrap(brainFile = brain_file)
		else:
		    self.aimlk.bootstrap(learnFiles = std_startup_file, commands = default_load_command)
		    self.aimlk.saveBrain(brain_file)

		# Change path back to orig path or else will mess up things later
		os.chdir(current_path) 




	# Process text using AIML and return response
	# Use separate sessions based on from name
	def aiml_process(self, msg):
		return self.aimlk.respond(msg['body'], msg['from'].bare) 