Python 3 128/16

As a former mathematician, I had a good advantage on this one. I'll only describe my solve path for part 2, since that was the interesting part.

First, we notice that the problem is now asking us to go backwards. So let's first figure out which position a particular card comes from if we only carried out the shuffle process once.

D = 119315717514047  # deck size

def reverse_deal(i):
    return D-1-i

def reverse_cut(i, N):
    return (i+N+D) % D

def reverse_increment(i, N):
    return modinv(N, D) * i % D  # modinv is modular inverse

I grabbed modinv from here. Parse your input and call these in reverse order and we can now reverse the shuffle process once. Let f denote this reversing function.

Now, note how all three operations are linear. That means their composition f is also linear. Thus, there exists integer A and B such that f(i) = A*i+B (equality in modulo D).

To find such A and B, we just need two equations. In my case, I took X=2020 (my input), Y=f(2020), and Z=f(f(2020)). We have A*X+B = Y and A*Y+B = Z. Subtracting second from the first, we get A*(X-Y) = Y-Z and thus A = (Y-Z)/(X-Y). Once A is found, B is simply Y-A*X. In code form:

X = 2020
Y = f(X)
Z = f(Y)
A = (Y-Z) * modinv(X-Y+D, D) % D
B = (Y-A*X) % D
print(A, B)

+D is a hack to get around the fact that modinv I copied can't handle negative integers for some reason.

Finally we are ready to repeadly apply f many times to get the final answer. Notice the pattern when you apply f multiple times.

f(f(f(x))) = A*(A*(A*x+B)+B)+B
           = A^3*x + A^2*B + A*B + B

In general:

f^n(x) = A^n*x + A^(n-1)*B + A^(n-2)*B + ... + B
       = A^n*x + (A^(n-1) + A^(n-2) + ... + 1) * B
       = A^n*x + (A^n-1) / (A-1) * B

In code form:

n = 101741582076661
print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)

which yields our answer.
