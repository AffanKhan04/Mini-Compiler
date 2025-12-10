// Number guessing game
// Demonstrates random numbers and user input

print("=== Number Guessing Game ===");
print("I'm thinking of a number between 1 and 10");

// Generate random number
int secret = random(1, 10);
int guess = 0;
int attempts = 0;
bool found = false;

// Game loop (3 attempts)
while (attempts < 3 and not found) {
    print("Attempt", attempts + 1, "of 3");
    
    // Note: In real execution, input() would read from user
    // For testing, we'll simulate with a predetermined value
    guess = random(1, 10);  // Simulating user guess
    print("Your guess:", guess);
    
    if (guess == secret) {
        found = true;
        print("Correct! You won!");
    }
    else {
        if (guess < secret) {
            print("Too low!");
        }
        else {
            print("Too high!");
        }
    }
    
    attempts = attempts + 1;
}

if (not found) {
    print("Game over! The number was:", secret);
}

print("\n");
print("=\n");
print("=== Random Number Examples ===\n");
print("=\n");

// Generate some random numbers
print("Random numbers between 1-100:");
int i = 0;
while (i < 5) {
    int rand_num = random(1, 100);
    print("  ", rand_num);
    i = i + 1;
}

// Simulate dice rolls
print("");
print("Rolling two dice:");
int die1 = random(1, 6);
int die2 = random(1, 6);
print("Die 1:", die1);
print("Die 2:", die2);
print("Total:", die1 + die2);

// Random boolean (0 or 1)
print("");
print("Coin flips:");
int j = 0;
while (j < 10) {
    int flip = random(0, 1);
    if (flip == 0) {
        print("Heads");
    }
    else {
        print("Tails");
    }
    j = j + 1;
}
