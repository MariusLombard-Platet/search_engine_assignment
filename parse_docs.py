import re

class Parse_cacm:

	def __init__(self, file_path):
		self.lines = open(file_path, 'r').readlines()
		self.current_line_number = 0
		self.regexes = {
			'id' : 		re.compile('^\.I\s(?P<id>\d*)'),
		}
		self.category_markers = ['.I', '.T', '.W', '.B', '.A', '.N', '.X', '.K', '.C']
		self.documents = {}


	def parse_file(self):
		while (self.current_line_number < len(self.lines)-1):
			line = self.lines[self.current_line_number]
			match = self.regexes['id'].match(line)
			if(match):
				document = self.process_document(match.group('id'))

			else:
				self.current_line_number += 1

		# print self.documents

	def process_document(self, document_id):

		title = ''
		abstract = ''
		keywords = ''

		self.current_line_number += 1
		line = self.lines[self.current_line_number]
		while(line[0:2] != '.I' and self.current_line_number < len(self.lines)-1): # We are still in the same document

			if(line[0:2] == '.T'):
				title = self.process_content()

			elif(line[0:2] == '.W'):
				abstract = self.process_content()

			elif(line[0:2] == '.K'):
				keywords = self.process_content()

			else:
				self.current_line_number += 1
			line = self.lines[self.current_line_number]

		self.documents[document_id] = {
			'title': 	title,
			'abstract': abstract,
			'keywords': keywords
		}

		# The document has been processed.

	def process_content(self):
		self.current_line_number += 1
		line = self.lines[self.current_line_number]
		content = ''

		while(line[0:2] not in self.category_markers and self.current_line_number < len(self.lines)-1):
			# Get all the content on one line
			content += line.replace('\n', ' ')

			self.current_line_number += 1
			line = self.lines[self.current_line_number]

		# TODO : tokeniser, etc.
		return content.rstrip()


test = Parse_cacm('sources/cacm.all')
test.parse_file()
