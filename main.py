import logging
import os
import sys
import shutil
import random

folder_logs = os.getcwd()

moved = 0
removed = 0

logging.basicConfig(level = logging.DEBUG,
					format = '%(asctime)s : %(levelname)s : %(message)s',
					filename =  os.path.join(folder_logs, 'comparison.log'),
					filemode = 'w')

def comparison(file_1, file_2):
	global moved, removed
	if file_1 == file_2:
		logging.debug('file_1 == file_2')
		removed += 1
		return True
	moved += 1
	return False

folder = input('Enter folder for deleted copies: ').replace('/', '\\')
if not os.path.exists(folder):
	sys.exit()
folder_copy = input('Enter folder for copy files: ').replace('/', '\\')
if not os.path.exists(folder_copy):
	os.mkdir(folder_copy)
files = os.listdir(folder)
i = 0
unavaliable = [] # ['AVI', 'avi']
avaliable_files = []
print('Working...')
for k in range(0, len(files)):
	splitting = files[i].split('.')
	if splitting[-1] in unavaliable:
		i += 1
		continue
	else:
		avaliable_files.append(files[k])
try:
	while True:
		path_0 = os.path.join(folder, avaliable_files[i])
		logging.debug(path_0)
		try:
			if os.path.exists(path_0):
				with open(path_0, 'rb') as f:
					content_1 = f.read()
				if len(avaliable_files) == 1:
					shutil.move(path_0, folder_copy)
					logging.debug('One file')
					sys.exit()
			else:
				i += 1
				continue
			while True:
				try:
					path = os.path.join(folder, avaliable_files[i+1])
					with open(path, 'rb') as f:
						content_2 = f.read()
					result = comparison(content_1, content_2)
					if result:
						os.remove(path)
						print('File {} deleted'.format(os.path.basename(path)))
					i += 1
				except IndexError:
					try:
						shutil.move(path_0, folder_copy)
						del avaliable_files[0]
						print('File {} moved'.format(os.path.basename(path_0)))
						i = 0
						break
					except shutil.Error:
						logging.debug('except shutil.Error')
						name = os.path.basename(path_0)
						logging.debug('Name is "'+name+'"') 
						name = name.split('.')
						p = 1
						while True:
							recovery = name[-2]
							name[-2] += '(' + str(p) + ')'
							dirname = os.path.dirname(path_0)
							logging.debug('File ' + '.'.join(name) + ' in folder ' + dirname)
							if not os.path.exists(os.path.join(dirname, '.'.join(name))):
								new_name = os.path.join(dirname, '.'.join(name))
								os.rename(path_0, new_name)
								path_0 = new_name
								logging.debug('New name - ' + new_name)
								shutil.move(new_name, os.path.join(folder_copy, path_0))
								logging.debug('File ' + str(path_0) + ' renamed and removed')
								print('File ' + str(path_0) + ' renamed and removed')
								del avaliable_files[0]
								i = 0
								break
							else:
								name[-2] = recovery
								p += 1
						continue
				except FileNotFoundError:
					logging.debug('FileNotFoundError')
					i += 1
					del avaliable_files[i]
					continue
				except MemoryError:
					logging.debug('MemoryError(into)')
					del avaliable_files[i]
					shutil.move(path_0, os.path.join(folder_copy, 'not comparise'))
		except MemoryError:
			logging.debug('MemoryError')
			del avaliable_files[i]
			shutil.move(path_0, os.path.join(folder_copy, 'not comparise'))
			continue
		except IndexError:
			logging.debug('Except IndexError(into)')
			break
except IndexError:
	logging.debug('Except IndexError')
	pass
finally:
	logging.debug('Work is successfull')
	print('End of work')

print('\nMoved - {}\nRemoved - {}'.format(moved, removed))
input()