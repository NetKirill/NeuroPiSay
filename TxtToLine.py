input_file = "result.txt"
output_file = "output.txt"

with open(input_file, "r") as file:
    lines = file.readlines()

# Удаляем символы новой строки ('\n') из каждой строки и объединяем их в одну строку
single_line = ' '.join([line.strip() for line in lines])

with open(output_file, "w") as file:
    file.write(single_line)