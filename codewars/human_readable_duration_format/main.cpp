#include <iostream>
#include <string>
#include <vector>

std::string format_duration(int s) {
  if (s == 0) {
    return "now";
  }
  int seconds = 1;
  int min = 60 * seconds;
  int hour = 60 * min;
  int day = 24 * hour;
  int year = 365 * day;
  int times[5] = {year, day, hour, min, seconds};
  std::string names[5] = {"year", "day", "hour", "minute", "second"};
  std::vector<std::string> out;
  int size = std::size(times);

  for (int i=0; i < size; i++) {
    int time = times[i];
    if (s >= time) {
      int n = s / time;
      out.push_back(std::to_string(n) + " " + names[i]);
      if (n > 1) {
        out.back() += 's';
      }
      s -= n * time;
    }
  }
  std::string str;
  for (int i=0; i+1 < out.size(); i++) {
    if (i+2 == out.size()) {
      str += out[i] + " and ";
    } else {
      str += out[i] + ", ";
    }
  }
  str += out.back();
  return str;
}

int main() {
  std::cout << format_duration(0) << '\n';
  std::cout << format_duration(1) << '\n';
  std::cout << format_duration(62) << '\n';
  std::cout << format_duration(120) << '\n';
  std::cout << format_duration(3662) << '\n';
  return 0;
}
