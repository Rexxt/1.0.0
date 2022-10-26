import requests

def get_releases(repository):
	response = requests.get(f'https://api.github.com/repos/{repository}/releases')
	releases = response.json()
	latest_response = requests.get(f'https://api.github.com/repos/{repository}/releases/latest')
	latest_release = latest_response.json()
	return releases, latest_release

def get_tags(repository):
	response = requests.get(f'https://api.github.com/repos/{repository}/tags')
	tags = response.json()
	return tags

def is_latest_release(release, latest_release):
	return release['tag_name'] == latest_release['tag_name']