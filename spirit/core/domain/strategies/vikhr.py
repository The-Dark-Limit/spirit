import logging

import torch
from core.domain.strategies.base import ProcessingStrategy
from core.domain.value_objects import BotResponse, MessageText, UserId

logger = logging.getLogger(__name__)


class VikhrStrategy(ProcessingStrategy):
    """Статегия обработки сообщений с использованием модели Vikhr-Nemo"""

    def __init__(
        self,
        max_length: int = 512,
        temperature: float = 0.7
    ) -> None:
        self.max_length = max_length
        self.temperature = temperature
        self.model_initialized = False

    def matches(self, text: str) -> bool:
        """Всегда срабатывает, но с низким приоритетом"""
        return True

    def initialize_model(self) -> None:
        """Загружает модель (заглушка - в реальном проекте здесь будет инициализация модели)"""
        if not self.model_initialized:
            try:
                logger.info("Initializing Vikhr-Nemo model...")
                from transformers import AutoModelForCausalLM, AutoTokenizer
                self.tokenizer = AutoTokenizer.from_pretrained("Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24")
                # В методе initialize_model()
                self.model = AutoModelForCausalLM.from_pretrained(
                    "Vikhrmodels/Vikhr-Nemo-12B-Instruct-R-21-09-24",
                    torch_dtype=torch.float16,
                    device_map="auto",
                    load_in_4bit=True  # Для экономии памяти
                )
                self.model_initialized = True
                logger.info("Vikhr-Nemo model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Vikhr-Nemo model: {e}")
                raise

    def process(
        self,
        user_id: UserId,
        text: MessageText
    ) -> BotResponse:
        try:
            # В реальном проекте здесь будет загрузка модели
            self.initialize_model()

            # Заглушка для демонстрации
            # В реальном проекте здесь будет вызов модели
            logger.info(f"Processing message with VikhrStrategy: {text.value}")

            # Пример генерации ответа (в реальном проекте заменить на вызов модели)
            prompt = f"Пользователь: {text.value}\nБот:"
            # response = self._generate_with_model(prompt)

            # Для демонстрации просто добавим префикс
            bot_response = f"[Vikhr] {text.value}"

            return BotResponse(
                text=bot_response,
                requires_echo=True
            )
        except Exception as e:
            logger.exception("Error processing message with VikhrStrategy")
            return BotResponse(
                text=f"Извините, произошла ошибка при обработке вашего запроса: {e!s}",
                requires_echo=True
            )

    def _generate_with_model(self, prompt: str) -> str:
        """Генерация ответа с помощью модели (реализация для реального проекта)"""
        # Токенизация
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # Генерация ответа
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=self.max_length,
                temperature=self.temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Декодирование
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Извлечение только ответа бота
        bot_response = response.split("Бот:")[-1].strip()

        return bot_response
