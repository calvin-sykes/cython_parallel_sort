#ifndef PARALLEL_SORT_HPP
#define PARALLEL_SORT_HPP

#include <algorithm>
#if __cplusplus >= 201703L 
#include <execution>
#endif 

template<typename T>
class IndexCompare {
public:
  T* _a;
  IndexCompare() = default;
  IndexCompare(T* a);
  
  bool operator()(long i1, long i2);
};

template <typename T>
IndexCompare<T>::IndexCompare(T* a): _a(a) {};

template <typename T>
bool IndexCompare<T>::operator()(long i1, long i2) {
    return _a[i1] < _a[i2];
}

#if __cplusplus >= 201703L
template<typename T>
void __sort(T first, T last) {
  std::sort(std::execution::par_unseq, first, last);
}

template<typename T, typename Compare>
void __sort(T first, T last, Compare comp) {
  std::sort(std::execution::par_unseq, first, last, comp);
}
#else
template<typename T>
void __sort(T first, T last) {
  __gnu_parallel::sort(first, last);
}

template<typename T, typename Compare>
void __sort(T first, T last, Compare comp) {
  __gnu_parallel::sort(first, last, comp);
}
#endif // __cplusplus >= 201703L

#endif // PARALLEL_SORT_HPP
