from rasa.cli.utils import print_success
from rasa.nlu.model import Interpreter


# Загрузка модели Rasa NLU
model_path = "F:/Ai/rasa1_8/models/20231110-193812/nlu"
interpreter = Interpreter.load(model_path)

# Функция для обработки вопроса
def process_question(question):
    # Получение предсказания от модели Rasa NLU
    result = interpreter.parse(question)

    # Извлечение тэгов из результата
    tags = result.get("entities", [])

    # Вывод тэгов
    if tags:
        for tag in tags:
            print(f"Тэг: {tag['entity']}, Значение: {tag['value']}")
    else:
        print("Тэги не обнаружены.")

# Пример использования
question = "Hello"
process_question(question)