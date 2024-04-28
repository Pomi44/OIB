#include <iostream>
#include <random>
#include <sstream>


std::string generateRandomBinarySequence(int size) {
    std::random_device rd;
    std::mt19937 gen(rd()); 
    std::uniform_int_distribution<> dis(0, 1);

    std::stringstream ss;

    for (int i = 0; i < size; ++i) {
        ss << dis(gen);
    }

    return ss.str(); 
}

int main() {
    int size;
    std::cout << "Введите размер последовательности: ";
    std::cin >> size;

    std::string randomBinarySequence = generateRandomBinarySequence(size);

    std::cout << "Случайная последовательность бинарных чисел: " << randomBinarySequence << std::endl;

    return 0;
}