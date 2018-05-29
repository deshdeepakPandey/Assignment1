Number=int(input("Enter Number: "))
for j in range(2,Number+1):
    k=0
    for i in range(2,j/2+1):
        if(j%i==0):
            k=k+1
    if(k<=0):
        print(j),
