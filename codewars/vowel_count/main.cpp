#include <iostream>
#include <string>

int getCount(const std::string& inputStr){
  int num_vowels = 0;
  for (char c : inputStr) {
    // https://stackoverflow.com/a/47846874
    num_vowels += (0x208222>>(c&0x1f))&1;
  }
  return num_vowels;
}

int main() {
 std::cout << getCount("abracadabra") << '\n';
 return 0;
}
