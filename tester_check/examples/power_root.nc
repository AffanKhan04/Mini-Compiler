// Power and Root Approximation
// Demonstrates: While loops, mathematical approximations

function int power(int base, int exp) {
    int result = 1;
    int i = 0;
    while (i < exp) {
        result = result * base;
        i = i + 1;
    }
    return result;
}

function int squareRoot(int n) {
    if (n < 2) {
        return n;
    }
    int guess = n / 2;
    int iterations = 0;
    while (iterations < 10) {
        guess = (guess + n / guess) / 2;
        iterations = iterations + 1;
    }
    return guess;
}

print("Power Function Demo:");
print("2^5 =", power(2, 5));
print("3^4 =", power(3, 4));
print("10^3 =", power(10, 3));

print("\nSquare Root Approximation:");
print("sqrt(16) ≈", squareRoot(16));
print("sqrt(25) ≈", squareRoot(25));
print("sqrt(100) ≈", squareRoot(100));
