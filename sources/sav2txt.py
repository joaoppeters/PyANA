with open(
    "/Users/jpeters/Dropbox/outros/github/gitPyANA/PyANA/sistemas/IEEE14.SAV", "rb"
) as file:
    data = file.read(8)

with open("IEEE14.txt", "w") as f:
    f.write(" ".join(map(str, data)))
    f.write("\n")
