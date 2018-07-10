def get_lines(filename):
	with open(filename, 'r') as file:
		return [line.strip() for line in file.readlines()]

def get_all_lines(filenames):
	return sum([get_lines(filename) for filename in filenames], [])

def write_lines(lines, output_filename='pirate.tsv'):
	text = 'line\tartist name\talbum title\talbum year\tsong title\tgenre\tpronc\tmetre\n'
	NUM_FIELDS = 8
	for line in lines:
		fields = line.split('\t')
		fields += ['Unknown'] * (NUM_FIELDS - len(fields))
		text += '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(*fields)

	with open(output_filename, 'w') as file:
		file.write(text)

if __name__ == '__main__':
	write_lines(get_all_lines(['movie_lines.txt']))
