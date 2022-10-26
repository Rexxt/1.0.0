import githandlers.github as github
import json
import sys
from blessed import Terminal
term = Terminal()

def list_array(l, indent=0):
	for i in range(len(l)):
		v = l[i]
		if type(v) == list:
			print(' '*indent + str(i), '->')
			list_array(v, indent+4)
		elif type(v) == dict:
			print(' '*indent + str(i), '->')
			print_properties(v, indent+4)
		elif type(v) == str:
			print(' '*indent + str(i), '->', f'"{v}"')
		else:
			print(' '*indent + str(i), '->', v)
	print()

def print_properties(d: dict, indent=0):
	for k in list(d.keys()):
		v = d[k]
		if type(v) == dict:
			print(' '*indent + k, '->')
			print_properties(v, indent+4)
		elif type(v) == list:
			print(' '*indent + k, '->')
			list_array(v, indent+4)
		elif type(v) == str:
			print(' '*indent + k, '->', f'"{v}"')
		else:
			print(' '*indent + k, '->', v)
	print()

def main(argv):
	with open('repos.json', encoding='utf-8') as rf:
		repositories = json.load(rf)

	if len(argv) < 2:
		print('Missing <repository> argument.')
		print('Can be one of:', end=' ')
		print(', '.join(list(repositories.keys())))
		sys.exit(1)

	repo = repositories[sys.argv[1]]
	versions = {}

	if repo['host'] == 'github':

		releases, latest_release = github.get_releases(repo['path'])
		for release in releases:
			if github.is_latest_release(release, latest_release):
				release['latest'] = True
			release['cl_ver_type'] = 'release'
			
			versions[release['tag_name']] = release
		
		tags = github.get_tags(repo['path'])
		for tag in tags:
			tag['cl_ver_tag'] = 'tag'
			if not tag['name'] in versions.keys():
				versions[tag['name']] = tag
		
	print(f'{len(versions.keys())} versions, of which {len(releases)} releases ({len(releases)/len(versions.keys())*100}%) and {(len(tags) - len(releases))} tags ({(len(tags) - len(releases))/len(versions.keys())*100}%)')

if __name__ == '__main__':
	main(sys.argv)