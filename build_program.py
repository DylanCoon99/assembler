import sys
import subprocess
import argparse

# device name: TL866II+



'''

For writing data to EEPROM
	minipro -p "AT28C256" -w data.bin

For reading data from EEPROM
	minipro -p "AT28C256" -r dump.bin


'''






'''
with open(bin_file, "rb") as f:
	bytes = f.read()

	


	for i in range(10):
		b = bytes[i]
		print(f"{b:08b}")
'''


DATA = {
		"lower": "",
		"upper": "",
	}



def write_bin_to_file():

	'''
	Write binary data to a file. EEPROM expects a 32k file so we
	will need to add padding.
	'''




	s = "This is a test string"
	byte_data = s.encode('utf-8')

	bytes_remaining = 32768 # 32K should be total size of file

	with open("example.bin", "wb") as file:
		file.write(byte_data)	



	return








def write_to_rom(data):
	'''
	For writing data to EEPROM
		minipro -p "AT28C256" -w data.bin

	'''
	try:
		print("Programming ROM now...")
		result = subprocess.run(["minipro", "-p", "AT28C256", "-w", data], capture_output=True, text=True)
		if result.returncode == 0:
			print("Successfully programmed ROM!")
		else:
			raise Exception("Encountered Error (Return code != 0)")
	except Exception as e:
		print(f"Failed to program ROM: {e}")

	return



if __name__ == "__main__":

	'''
	parser = argparse.ArgumentParser(description="A simple CLI tool")
	parser.add_argument("name", help="Your name") # Positional
	parser.add_argument("-a", "--age", type=int, help="Your age") # Optional

	args = parser.parse_args()
	print(f"Hello {args.name}, you are {args.age} years old.")
	'''


	try:
		bin_file = sys.argv[1]
		print(f"Writing file {bin_file} to ROM...")
		write_to_rom(bin_file)
		#write_bin_to_file()

	except Exception as e:
		print(f"Failed to write to ROM: {e}")























