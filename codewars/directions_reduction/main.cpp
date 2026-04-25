#include <iostream>
#include <string>
#include <vector>

class DirReduction
{
public:
    static std::vector<std::string> dirReduc(std::vector<std::string> &arr) {
      if (arr.size() == 0) {
        return arr;
      }
      for (size_t i=0; i<arr.size()-1; i++) {
        std::string a = arr[i];
        std::string b = arr[i+1];
        if ((a == "NORTH" && b == "SOUTH") || 
            (a == "SOUTH" && b == "NORTH") ||
            (a == "EAST" && b == "WEST")   ||
            (a == "WEST" && b == "EAST")
            ) {
          arr.erase(arr.begin()+i, arr.begin()+i+2);
          return DirReduction::dirReduc(arr);
        }
      }
      return arr;
    }
};


int main() {
  return 0;
}
