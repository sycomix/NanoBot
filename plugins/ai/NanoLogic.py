#!/usr/bin env python2
"""
NanoLogic
nanodano@devdungeon.com

PyAIML wrapper for convenience
"""

import os


class NanoLogic():

	def __init__(self, bot_name, bot_master, brain_file, std_startup_file, default_load_command):	
		# Initialize AIML Kernel
		self.aimlk = plugins.ai.aiml.Kernel()

		# Name/owner settings
		self.aimlk.setBotPredicate('name', bot_name)
		self.aimlk.setBotPredicate('master', bot_master)

		# Brain files can save startup time
		# need a way to auto-update this if needed check_brain_updates
		# and need a separate save_brain function
		# file exist/write verification

		self.reload(default_load_command, brain_file, std_startup_file)
		
	# Process text using AIML and return response
	# Use separate sessions based on from name
	def aiml_process(self, msg):
		return self.aimlk.respond(msg['body'], msg['from'].bare) 

	def reload(self, load_command, brain_file, std_startup_file, force=False):
		# Change path so that relative paths work in std-startup.xml
		current_path = os.getcwd()
		bot_root_path = os.path.dirname(os.path.realpath(__file__))
		if current_path != bot_root_path:
			os.chdir(bot_root_path)
		# Check for brain file else load aiml and create brain
		if os.path.isfile(brain_file) and force == False:
		    self.aimlk.bootstrap(brainFile = brain_file)
		else:
		    self.aimlk.bootstrap(learnFiles = std_startup_file, commands = load_command)
		    self.aimlk.saveBrain(brain_file)
		    print "Saving"

		# Change path back to orig path or else will mess up things later
		os.chdir(current_path) 