import re
from process_text import Process_text

class Parse_cacm:

	def __init__(self, cacm_words_path, common_words_path):
		self.lines = open(cacm_words_path, 'r').readlines()
		self.current_line_number = 0

		self.document_begin_regex = re.compile('^\.I\s(?P<id>\d*)')
		self.category_markers = ['.I', '.T', '.W', '.B', '.A', '.N', '.X', '.K', '.C']

		self.documents = {}
		self.text_processor = Process_text(common_words_path)

	def parse_file(self):
		while (self.current_line_number < len(self.lines)-1): # -1 because we do all the iteration stuff at the end of the loop, instead of the beginning
			line = self.lines[self.current_line_number]
			match = self.document_begin_regex.match(line)

			# Parses the document. Stops on a new document declaration (line = .I \d+)
			if(match):
				document = self.process_document(match.group('id'))

			else:
				self.current_line_number += 1

		# print self.documents['1369']

	def process_document(self, document_id):
		content = ''

		self.current_line_number += 1
		line = self.lines[self.current_line_number]
		while(line[0:2] != '.I' and self.current_line_number < len(self.lines)-1): # We are still in the same document

			# process_contents aggregates the content of a category (title, abstract, keywords). Stops on a new category (line starts with .[ITWABNKC])
			if(line[0:2] in ('.T', '.W', '.K')):
				content  += ' ' + self.process_content()

			else:
				self.current_line_number += 1
			line = self.lines[self.current_line_number]

		self.documents[document_id] = self.text_processor.sanitize_rawtext(content)
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

		return content.rstrip()
