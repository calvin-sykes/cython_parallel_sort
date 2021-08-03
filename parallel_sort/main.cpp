#include <algorithm>
#include <array>
#include <functional>
#include <iostream>
#include <random>

#include "compare.hpp"



int main(int argc, char** argv)
{
  std::random_device r;
  std::seed_seq      seed{r(), r(), r(), r(), r(), r(), r(), r()};
  std::mt19937       eng(seed); // a source of random data

  std::uniform_int_distribution<int> dist;
  auto gen = std::bind(dist, eng);

  auto x = std::array<int, 100000>();
  auto indices = std::array<int, 100000>();

  for(int i = 0; i < x.size(); i++) {
    x[i] = gen();
    indices[i] = i;
  }

  auto cmp = IndexCompare<int>(x.data());

  std::sort(indices.begin(), indices.end(), cmp);

  for(int i = 0; i < 100; i++)
    std::cout << x[indices[i]] << ' ';
  std::cout << std::endl;
}
