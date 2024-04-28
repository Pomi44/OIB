import java.util.Random;

public class RandomBinarySequenceGenerator {

    // Функция для генерации случайной последовательности бинарных чисел
    public static String generateRandomBinarySequence(int size) {
        Random random = new Random();
        StringBuilder binarySequence = new StringBuilder();

        for (int i = 0; i < size; ++i) {
            int randomNumber = random.nextInt(2); // Генерация случайного числа 0 или 1
            binarySequence.append(randomNumber); // Добавление случайного числа к последовательности
        }

        return binarySequence.toString();
    }

    public static void main(String[] args) {
        int size = 10; // Заданный размер последовательности
        String randomBinarySequence = generateRandomBinarySequence(size);

        System.out.println("Случайная последовательность бинарных чисел: " + randomBinarySequence);
    }
}