// Interactive story with branching paths
// Demonstrates string operations and conditionals

print("=\n");
print("=== The Lost Treasure ===\n");
print("=\n");
print("\n");

string hero = "Alex";
string location = "forest";
int gold = 0;
bool has_key = false;

// Story introduction
string intro1 = "Welcome, ";
string intro2 = concat(intro1, concat(hero, "!"));
print(intro2);
print("You are standing in a dark", location);
print("");

// Path 1: Explore
print("You see two paths ahead:");
print("1. Go left towards the cave");
print("2. Go right towards the river");

int choice = random(1, 2);  // Simulate user choice
print("You choose path", choice);
print("");

if (choice == 1) {
    // Cave path
    location = "cave";
    print("You enter the", location);
    print("You find a rusty key!");
    has_key = true;
    gold = gold + 10;
    
    string found_msg = concat("Found ", "10 gold coins!");
    print(found_msg);
}
else {
    // River path
    location = "river";
    print("You reach the", location);
    print("You find 5 gold coins in the water!");
    gold = gold + 5;
}

print("");
print("Current gold:", gold);

// Path 2: The treasure chest
print("");
print("You discover an ancient treasure chest!");

if (has_key) {
    print("You use the key to open the chest...");
    gold = gold + 100;
    print("Amazing! You found 100 gold coins!");
    
    string victory = concat("Victory! Total gold: ", "100+");
    print(victory);
}
else {
    print("The chest is locked. You need a key!");
    print("You continue your journey...");
}

print("\n");
print("=\n");
print("=== Final Status ===\n");
print("=\n");
print("Hero:", hero);
print("Location:", location);
print("Total Gold:", gold);

// Generate ending based on gold
if (gold >= 100) {
    string ending = "Congratulations! You are a legendary treasure hunter!";
    print(ending);
}
else {
    if (gold >= 50) {
        print("Well done! You found some treasure.");
    }
    else {
        print("Better luck next time, adventurer.");
    }
}

// String manipulation for stats
string stats_line1 = concat("Journey ended in ", location);
print(stats_line1);

if (has_key) {
    print("You kept the mysterious key as a souvenir");
}
