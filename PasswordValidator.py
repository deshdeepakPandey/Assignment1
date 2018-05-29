import re

def PassWordValidator(Password):
    x=[0]
    x.append(len(Password))
    if (len(Password)>=8):
        x[0]=x[0]+1
    if re.search("[0-9]",Password):
        x[0]=x[0]+1
    if re.search("[a-z]",Password):
        x[0]=x[0]+1
    if re.search("[A-Z]",Password):
        x[0]=x[0]+1
    if re.search("[!@#$%^&*()]-+",Password):
        x[0]=x[0]+1
    return x



Cotinue=True
while Cotinue:
    Password = raw_input('Enter Your Password :')
    Afterchecking=PassWordValidator(Password) 
    print 'Your password: ',Password
    if Afterchecking[1]<8:
        print 'Atleast {} more character are needed to complete it'.format(8-Afterchecking[1])
    if Afterchecking[0]==5:
        print 'password is stron'
    else:
        print 'password is week'
    print '##############################'
    quet=raw_input('\n\nEnter q to Exit or Enter to continue : ')
    if quet=='q':
        Cotinue=False
