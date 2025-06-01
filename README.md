# Звіт про Проєкт: CLI Аналізатор Текстових Файлів

---

## Короткий Опис Проєкту

* **Назва проєкту:** CLI Аналізатор Текстових Файлів
* **Основна мета:** Розробити консольний застосунок, який приймає текстовий файл та повертає статистику щодо його вмісту у форматі `.json`. Отримати практичний досвід використання асистивних технологій розробки ПЗ на основі ШІ. Ознайомитись з можливостями ефективного використання Amazon CodeWhisperer при вирішенні конкретного програмного завдання.
* **Реалізована функціональність:**
    * Вибір текстових файлів з доступних у директорії `./src/text-files/`
    * Генерація результату у `.json` файлі в директорії `./src/text-analyzed/`, що містить:
      * Загальну кількість слів
      * Загальну кількість символів (з пробілами та без)
      * Кількість речень
      * `N` слів, що зустрічаються найчастіше в порядку спадання (`N` обирає користувач)
      * Середня довжина слова (округленна до 1 знака після коми)
      * Підрахунок частоти кожного символу в порядку спадання
    * **OOP** та **SRP**
    * Валідація вводу користувача
    * Менеджер конфігурацій
    * Обробка помилок
    * Docstrings та type hints
    * Unit-тести

---

## Рефлексія Щодо Використання Amazon CodeWhisperer

### Завдання, що вирішувалися з CodeWhisperer

Детально опишіть, для яких конкретних завдань ви використовували CodeWhisperer.

* **Генерація першої функції `def analyze_text_file()`:** CodeWhisperer допоміг швидко створити початковий шаблон функції для читання даних з файлу та обробки їх з наступним створенням `.json` файлу з статистикою.
* **Рефакторинг файлу `analyzer.py` та структури проєкту для реалізації SRP:** Інструмент переписав код під ООП та розбив функціонал по методах окремих класів, для покращення чистоти проєкту та простоти подальшого рефакторингу.
* **Створення детальних докстрингів для класів та методів проєкту:** Для кращої документації класів, CodeWhisperer генерував детальні докстринги на основі сигнатури та передбачуваної логіки.
* **Пошук помилки у класі `FileHandler`:** CodeWhisperer додав підтримку UTF-8 для інших мов.
* **Написання unit-тестів для методів класів з `./src/modules/`:** CodeWhisperer допоміг швидко написати детальні тести для функціоналу програми та вирішити помилки, що виникли.

### Ефективність

Оцініть, наскільки ефективним був CodeWhisperer для кожного з цих завдань.

* **Що вийшло добре:** 
  * CodeWhisperer допоміг розпочати розробку, реалізувавши початковий функціонал за текстовим описом однієї функції.
  * Інструмент легко та без помилок переписав функціонал програми у класи та швидко реалізував SRP.
  * Докуметування чітке та створене за секунди, що економить час на технічні завдання.
* **Що не дуже:** 
  * Іноді виникали проблеми через втрату контексту.
  * Реалізувати unit-тести вийшло з третього разу, відновлюючись до останнього коміту. ШІ асистента доводилось доводити до рішень частково здогадуючись, що йому не вистачає для правильної реалізації. 

### Складнощі та Обмеження

З якими труднощами, неточностями або обмеженнями ви зіткнулися під час роботи з CodeWhisperer?

* **Контекстні обмеження:** Часом CodeWhisperer не завжди повністю розумів глибинний контекст проєкту, що призводило до менш релевантних пропозицій.
* **Надлишкові пропозиції:** Іноді генерував занадто багато варіантів, з яких було важко вибрати найкращий.
* **Помилки в рекомендаціях:** В окремих випадках пропозиції містили синтаксичні або логічні помилки, які потрібно було виправляти вручну.
* **Залежність від якості коментарів:** Ефективність значною мірою залежала від того, наскільки чітко та детально я формулював коментарі-запити.

### Вдалі Запити

Які типи ваших запитів (коментарі, розпочатий код) до CodeWhisperer виявилися найбільш продуктивними?

* **Коментарі, що описують намір:** Це дозволяло CodeWhisperer чітко зрозуміти, що потрібно згенерувати.
* **Частково написаний код:** Початок функції допомагав CodeWhisperer "зловити" контекст і запропонувати релевантне продовження.
* **Чому:** Ці запити забезпечували достатній контекст для CodeWhisperer, щоб він міг генерувати точніші та корисніші фрагменти коду, зменшуючи необхідність у подальшому редагуванні.

### Враження

Що вас найбільше здивувало (приємно чи неприємно), сподобалося чи не сподобалося в роботі з інструментом?

* **Приємно здивувало:** 
  * Швидкість розробки
  * Рекомендації з покращення проєкту та відповідності найкращим практикам.
* **Не сподобалося:** 
  * Обмежені можливості аналізувати контекст проєкту, вміст файлів, в порівнянні з іншими конкурентами на ринку.

### Вплив на Розробку

Як, за вашим особистим відчуттям, використання ШІ-асистента вплинуло на швидкість вашої розробки та на якість підсумкового коду?

* **Швидкість розробки:** Значно прискорило розробку, особливо на початкових етапах написання коду та для рутинних задач.
* **Якість підсумкового коду:** Допомогло уникнути типових помилок та підвищити читабельність коду, пропонуючи усталені патерни. Однак, іноді згенерований код потребував ретельного рев'ю для забезпечення оптимальності та відповідності стилю проєкту.

---

## Приклади Вдалих Промптів

Наведіть 2-3 приклади найбільш вдалих або цікавих промптів (коментарів-запитів), які ви давали CodeWhisperer, та коротко опишіть/покажіть отриманий від нього код.

### Приклад 1: Генерація першої загальної функції `analyze_text_file()` за допомогою функціоналу `Inline Chat`

**Промпт (коментар-запит):**
```python
# this function analyzes a text file from "./src/text-files" directory where the file is specified by the user in CLI
# and creates a json file in the "./src/text-analyzed" directory with the following keys:
# - total_words: the total number of words in the text file
# - total_symbols: the total number of symbols (with spaces and without)
# - sentences: the number of sentences in the file
# - N-most-frequent-words: N most frequent words and their frequency in descending order (where N is specified by the user)
# - average-word-length: the average length of all words in the file
# - symbols-frequency: symbols and their frequency in descending order
def analyze_text_file():
    pass
```

**Отриманий код:**
```python
def analyze_text_file():
    """
    Main function that handles text file analysis process.

    The function performs the following operations:
    1. Gets and validates file path from user
    2. Gets and validates N value for word frequency analysis
    3. Reads and analyzes text file contents
    4. Calculates various text statistics:
        - Total symbols (with and without spaces)
        - Number of sentences
        - Word count
        - N most frequent words
        - Average word length (rounded to 2 decimal places)
        - Symbol frequency (in descending order)
    5. Saves results to a JSON file
    6. Offers option to analyze another file

    The analysis results are saved in a JSON file with the following structure:
    {
        "total_symbols": {
            "with_spaces": int,
            "without_spaces": int
        },
        "sentence-count": int,
        "word-count": int,
        "N-most-frequent-words": dict[str, int],
        "average-word-length": float,
        "symbols-frequency": dict[str, int]
    }
    """
    project_root = get_project_root()
    base_input_dir = os.path.join(project_root, "src", "text-files")
    base_output_dir = os.path.join(project_root, "src", "text-analyzed")

    while True:
        # Get available files
        available_files = get_available_files(base_input_dir)

        if not available_files:
            print(f"No .txt files found in {base_input_dir}")
            return

        # Get user's file choice
        chosen_file = get_file_choice(available_files)
        if chosen_file is None:
            print("Goodbye!")
            return

        # Construct full file path
        input_path = os.path.join(base_input_dir, chosen_file)

        n = get_valid_n()

        try:
            # Read the text file
            text = get_text_file(input_path)

            # Calculate total symbols with and without spaces
            total_symbols_with_spaces = len(text)
            total_symbols_without_spaces = len(text.replace(" ", ""))

            # Count sentences
            sentences = [s.strip() for s in re.split('[.!?]', text) if s.strip()]
            sentence_count = len(sentences)

            # Get words and calculate frequencies
            words = re.findall(r'\b\w+\b', text.lower())
            word_count = len(words)
            word_freq = Counter(words)
            most_frequent_words = dict(word_freq.most_common(n))

            # Calculate average word length (rounded to 2 decimal places)
            average_word_length = round(sum(len(word) for word in words) / len(words) if words else 0, 2)

            # Calculate symbol frequency (in descending order)
            symbol_frequency = dict(sorted(
                Counter(text).items(),
                key=lambda x: (-x[1], x[0])  # Sort by frequency desc, then by character asc
            ))

            # Prepare output data structure
            output_data = {
                "total_symbols": {
                    "with_spaces": total_symbols_with_spaces,
                    "without_spaces": total_symbols_without_spaces
                },
                "sentence-count": sentence_count,
                "word-count": word_count,
                f"{n}-most-frequent-words": most_frequent_words,
                "average-word-length": average_word_length,
                "symbols-frequency": symbol_frequency
            }

            # Ensure output directory exists and create output path
            output_path = os.path.join(base_output_dir, chosen_file + ".json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save results to JSON file
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=4)

            print(f"\nAnalysis complete! Results saved to: {output_path}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Ask user if they want to analyze another file
        print("\nWould you like to analyze another file? (y/n)")
        if input().lower() != 'y':
            print("Goodbye!")
            break
```

### Приклад 2: Автодоповнення докстрингів

**Промпт (коментар-запит):**
```python
def get_available_files(self, directory: str) -> List[str]:
        """List all valid text files in the specified directory."""
```
**Отриманий код:**
```python
def get_available_files(self, directory: str) -> List[str]:
        """List all valid text files in the specified directory.

        Lists files that:
        - Have supported extensions (defined in config)
        - Don't exceed maximum file size
        - Are accessible

        Args:
            directory (str): Path to directory to search

        Returns:
            List[str]: List of valid file names, sorted alphabetically

        Raises:
            FileError: If directory access fails or other file operations failAdd commentMore actions
        """
```

### Приклад 3: Додавання та покращення обробки помилок

**Промпт (коментар-запит):**
```
Improve error handling and add custom exceptions
```

**Отриманий код:**
```python
import os
from .exceptions import FileError


class PathManager:
    def get_output_path(self, filename: str) -> str:
        return os.path.join(self.output_dir, filename + ".json")

    def ensure_output_dir_exists(self) -> None:
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
        """Ensure output directory exists with error handling"""
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            # Verify write permissions
            if not os.access(self.output_dir, os.W_OK):
                raise FileError(
                    "No write permission for output directory",
                    {"path": self.output_dir}
                )
        except OSError as e:
            raise FileError(
                f"Failed to create output directory: {e}",
                {
                    "path": self.output_dir,
                    "error": str(e),
                    "error_code": e.errno
                }
            )
```