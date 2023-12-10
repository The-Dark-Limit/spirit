import asyncio
import uuid
from functools import partial

from loguru import logger
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.infra.utils.typings import DictStrStr


class DialogGPT:
    def __init__(self):
        self._memory = ''
        self._max_memory_size = 1000
        self._request_mapper: DictStrStr = {}
        self._response_mapper: DictStrStr = {}
        # TODO Snapshots
        self._model = AutoModelForCausalLM.from_pretrained(
            'tinkoff-ai/ruDialoGPT-medium',
        )
        self._tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-medium')

    async def serve(self) -> None:
        if len(self._request_mapper.keys()):
            item = self._request_mapper.popitem()
            result = await self._process(item[1])
            self._response_mapper.update({item[0]: result})
        await asyncio.sleep(1)

    async def put_request(self, request: str) -> str:
        uid = str(uuid.uuid4())
        self._request_mapper.update({uid: request})
        if len(self._request_mapper.keys()):
            logger.info(f'[MODEL][REQUEST_QUEUE]: {self._request_mapper}')
        return uid

    async def get_response(self, uid: str) -> str:
        response = None
        while response is None:
            await self.serve()
            response = self._response_mapper.pop(uid, None)
            await asyncio.sleep(0.5)
        logger.info(f'[MODEL][RESPONSE_QUEUE]: {self._response_mapper}')
        return response

    async def _process(self, question: str) -> str:
        memory = self._memory + f'@@ПЕРВЫЙ@@ {question} @@ВТОРОЙ@@'
        inputs = self._tokenizer(memory, return_tensors='pt')

        kwargs = dict(
            **inputs,
            top_k=10,
            top_p=0.95,
            num_beams=3,
            num_return_sequences=1,
            do_sample=True,
            no_repeat_ngram_size=2,
            temperature=1.2,
            repetition_penalty=1.2,
            length_penalty=1.0,
            eos_token_id=50257,
            max_new_tokens=64,
        )
        new_generate = partial(self._model.generate, **kwargs)
        generated_token_ids = new_generate()

        context_with_response = [self._tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
        result = context_with_response[0].replace(self._memory, '').replace('@@ПЕРВЫЙ@@', '').replace('@@ВТОРОЙ@@', '')

        self._memory = self._memory + result
        logger.info(f'Context: {self._memory}')
        logger.info(f'Context len: {len(self._memory)}')
        if len(self._memory) > self._max_memory_size:
            self._memory = ''
        return result.replace(question, '')
