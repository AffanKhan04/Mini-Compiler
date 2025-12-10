// String operations demonstration
// Shows string concatenation, substring, and length operations

print("=\n");
print("=== String Operations Demo ===\n");
print("=\n");
print("\n");
print("--- Basic Concatenation ---\n");

string greeting = "Hello";
string name = "World";

// String concatenation
string message = concat(greeting, concat(" ", name));
print("Concatenated:", message);

// String length
print("\n");
print("--- String Length ---\n");
print("Length of message:", len(message));
print("Length of greeting:", len(greeting));

// Substring operations
print("\n");
print("--- Substring Extraction ---\n");
string sub1 = substr(message, 0, 5);  // "Hello"
string sub2 = substr(message, 6, 11); // "World"
print("First word:", sub1);
print("Second word:", sub2);

// Build a sentence
string part1 = "Programming";
string part2 = " is";
string part3 = " fun!";
string sentence = concat(part1, concat(part2, part3));
print("Sentence:", sentence);

// Extract substring from middle
string text = "NumCalc Language";
string extracted = substr(text, 0, 7);  // "NumCalc"
print("Extracted:", extracted);

// String length comparison
string short = "Hi";
string long = "Hello World";
if (len(short) < len(long)) {
    print("Short string is shorter");
}

// Multiple concatenations
string a = "A";
string b = "B";
string c = "C";
string alphabet = concat(a, concat(b, c));
print("First three letters:", alphabet);
