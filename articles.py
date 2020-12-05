with open("text.txt") as file:
	data = [line.strip(" the").strip(" a") for line in file]
	print("n".join(data))