import math
def binomial(n,k):
  if n == k:
    return 1
  if k == 1:
    return n
  return (n*binomial(n-1,k-1))/k

print('Binomial calculator')
n = int(input("Entra n: "))
k = int(input("Entra k: "))
print(f"(n|k) = {binomial(n,k)}")
print(f"(n|k) = {math.comb(n,k)}")
