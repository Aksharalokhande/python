sub1=int(input(" Enter subject1 marks: "))
sub2=int(input(" Enter subject2 marks: "))
sub3=int(input(" Enter subject3 marks: "))
sub4=int(input(" Enter subject4 marks: "))
sub5=int(input(" Enter subject5 marks: "))

total=sub1+sub2+sub3+sub4+sub5
percentage=total/5

print("Total marks=",total)
print("Percentage=",percentage)

if percentage>=75:
    print(" Result:Distinction")
elif percentage>=65:
    print("Result:first class")   
elif percentage>=45:
    print("Result:pass")   
else:
    print("Result:fail")    
    