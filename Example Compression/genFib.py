f = open('Router1.fib', 'w')
level = 6
for i in range(256):
    for j in range(0,256,2**level):
        f.write(f"10.0.{i}.{j}/{32-level},1\n")
        f.write(f"10.1.{i}.{j}/{32-level},2\n")
f.close()
