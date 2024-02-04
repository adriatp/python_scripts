import math
def fibonacci(n):
  f0=1;f1=1;f2=1;i=1
  while i<n:
    f2=f1+f0
    f0=f1
    f1=f2
    i=i+1
  return f2

print('Fibonacci')
n = int(input("Entra n: "))
print(f"fib({n}) = {fibonacci(n)}")
