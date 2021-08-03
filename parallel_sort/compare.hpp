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
