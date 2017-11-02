
def del_row(file_name, row_name):
  lines = open(file_name, "r").readlines()
  num_row=[]
  words=lines[0].split()
  for i in range(len(words)):
    if words[i].upper() == row_name.upper():
      num_row.append(i)
      #print words[i].upper()
  with open(file_name, "w") as f:
    for line in lines:
      words=line.split()
      for i in range(len(words)):
        if i in num_row:
          continue
        f.write("%s  "%words[i])
      f.write("\n")
