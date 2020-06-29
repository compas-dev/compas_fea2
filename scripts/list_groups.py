data = []
for i in range(100):
    data.append(i)
chunks = [data[x:x+15] for x in range(0, len(data), 15)]
print(chunks)
