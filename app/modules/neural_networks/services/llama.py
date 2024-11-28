from aiogram import types
from transformers import AutoModelForCausalLM, AutoTokenizer


class Llama:
    model_name = "Vikhrmodels/Vikhr-Llama-3.2-1B-instruct"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    async def get_response(self, question: types.Message):
        input_ids = self.tokenizer.encode(question.text, return_tensors="pt")
        output = self.model.generate(
            input_ids,
            max_length=1512,
            temperature=0.3,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
