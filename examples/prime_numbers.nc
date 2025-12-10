// Prime Number Checker and Generator
// Demonstrates: Nested loops, boolean logic, modulo operation

function bool isPrime(int n) {
    if (n <= 1) {
        return false;
    }
    if (n <= 3) {
        return true;
    }
    int i = 2;
    while (i * i <= n) {
        if (n % i == 0) {
            return false;
        }
        i = i + 1;
    }
    return true;
}

print("First 15 Prime Numbers:");
int count = 0;
int num = 2;
while (count < 15) {
    if (isPrime(num)) {
        print(num);
        count = count + 1;
    }
    num = num + 1;
}
