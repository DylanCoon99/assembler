

bin_file = "dump.bin"
bin_file2 = "dump2.bin"


print(f"Printing Bytes... \n")


with open(bin_file, "rb") as f,	open(bin_file2, "rb") as f2:
	
	bytes_1 = f.read()
	bytes_2 = f2.read()
	print("Address    Higher Bytes    Lower Bytes")
	for i in range(10):
		b = bytes_1[i]
		b2 = bytes_2[i]
		print(f"{i}          {b2:08b}       {b:08b}")


print(f"Done!")


 