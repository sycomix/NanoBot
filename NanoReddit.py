"""
NanoReddit
nanodano@devdungeon.com

Class that takes advantage of Reddit PRAW library to provide a handful
of useful functions for interacting with Reddit
"""

import praw


class NanoReddit():



	def __init__(self):
		"""
		Initalize PRAW and set user Agent
		"""
		print "Initializing PRAW and User Agent"
		user_agent = ("the_nano_bot/0.1 by nanodano@devdungeon.com")
		self.r = praw.Reddit(user_agent=user_agent)



	"""
	Get lowest subreddit/karma combo given a dict
	"""
	def get_lowest(self, dict):
		lowest = next(dict.iteritems()) # tuple - first element as base
		for subreddit, karma in dict.iteritems():
			if karma < lowest[1]:
				lowest = (subreddit,karma)
		return lowest



	"""
	Get highest subreddit/karma combo given a dict
	"""
	def get_highest(self, dict):
		highest = next(dict.iteritems()) # tuple - first element as base
		for subreddit, karma in dict.iteritems():
			if karma > highest[1]:
				highest = (subreddit,karma)
		return highest



	"""
	Analyze a user's karma
	"""
	def analyze_user_karma(self, username):
		user = self.r.get_redditor(username)

		thing_limit = 1000 
		gen = user.get_comments(limit=thing_limit)
		karma_by_subreddit = {}
		for thing in gen:
			subreddit = thing.subreddit.display_name
			karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0)
							+ thing.ups - thing.downs)

		lowest = self.get_lowest(karma_by_subreddit)
		highest = self.get_highest(karma_by_subreddit)
		
		output = "Reddit karma breakdown for " + username + "\n"
		for subreddit, karma in karma_by_subreddit.iteritems():
			output += subreddit + ": " + repr(karma) + "\n"
		output += "===============\n"
		output += "Lowest: " + lowest[0] + " (" + repr(lowest[1]) + ")\n"
		output += "Highest: " + highest[0] + " (" + repr(highest[1]) + ")\n"
		return output

	

"""
Main
Handles command line running of this script
Mostly for testing since this is intended to be used
as a class inside of a larger project
"""
if __name__ == "__main__":
	print "Running NanoReddit..."
	r = NanoReddit()

	# Analyze User - get karma by subred, highest, lowest
	output = r.analyze_user_karma(raw_input("User to analyze: "))
	print output