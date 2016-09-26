#Get CSV file
#convert each line to a dictionary object: {Name: 'program name', tags: ['a', 'b']}
#extract the nodes (source node is the program name +  tag nodes) --> file of program names) and the edge file has to have the source node and the tag

import requests
import csv
import sys
import pandas as pd
import io


url_start = 'https://docs.google.com/spreadsheets/d/1lAZ-mtYTIwN_WC_AGCeosYrJn_LHGV796etW7yNJfXQ/export?format=csv&id=1lAZ-mtYTIwN_WC_AGCeosYrJn_LHGV796etW7yNJfXQ&gid='

platform ='2066765238'
usage = '1374288343'

#initial parse function:
# r = requests.get(url)
# ro = io.StringIO(r.text)
# data = pd.read_csv(url)

# csv_reader = csv.reader(ro)
# keys = next(csv_reader)
# for row in csv_reader:
# 	entry = {}
# 	for key, value in zip(keys, row):
# 		if key == 'Tag':
# 			if value:
# 				tags = entry.get('Tags')
# 				if tags is None:
# 					entry['Tags'] = []
# 				entry['Tags'].append(value)
# 		else:
# 			entry[key] = value
# 	print(entry['Name'], entry.get('Tags'))

def parse_csv(param):
	r = requests.get(url_start + param)
	ro = io.StringIO(r.text)
	# data = pd.read_csv(url_start + param)
	csv_reader = csv.reader(ro)
	keys = next(csv_reader)
	entries = []
	for row in csv_reader:
		entry = {}
		for key, value in zip(keys, row):
			if key == 'Tag':
				if value:
					tags = entry.get('Tags')
					if tags is None:
						entry['Tags'] = []
					entry['Tags'].append(value)
			else:
				entry[key] = value
		# print(entry['Name'], entry.get('Tags'))
		entries.append(entry)
	return entries

# parse_csv(usage)

usage_entries = parse_csv(usage)
nodes = []
edges = []
for entry in usage_entries:
	#creer un tableau de nodes avec nom et tags
	usage_id = 'usage:' + entry['Name']
	nodes.append([usage_id, entry['Name']])
	tags = entry.get('Tags')
	if tags is not None:
		for tag in tags:
			tag_id = 'tag:' + tag
			nodes.append([tag_id, tag])
			edges.append([usage_id, tag_id, 'Tag'])

csv_out = open("node.csv",'w')
mywriter = csv.writer(csv_out)
mywriter.writerow(['id', 'label'])
for node in nodes:
    mywriter.writerow(node)
csv_out.close()

csv_out = open("edge.csv",'w')
mywriter = csv.writer(csv_out)
mywriter.writerow(['source', 'target', 'label'])
for edge in edges:
    mywriter.writerow(edge)
csv_out.close()



