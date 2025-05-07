from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import GenerationConfig
import torch

class LyricGenerator:
    SYSTEM_TEMPLATE = (
        "You are a professional {genre} songwriter.\n"
        "Your task is to write original lyrics in the style of {genre} music.\n"
        "- Use themes, rhythm, and vocabulary that are typical of {genre} songs.\n"
        "- The song should convey a strong sense of {emotion}.\n"
        "- The central theme or topic of the lyrics is: {topic}.\n"
        "- Target length: around {length} words.\n"
        "\n### LYRICS START BELOW ###\n"
    )

    DEFAULT_SLOTS = {
        "genre": "pop",
        "emotion": "joy",
        "topic": "love",
        "length": 200
    }

    def __init__(self, model_path):
        # pick the best device
        self.device = (
            torch.device("cuda")
            if torch.cuda.is_available()
            else torch.device("mps")
            if torch.backends.mps.is_available()
            else torch.device("cpu")
        )
                # load tokenizer
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True,
            local_files_only=True
        )

        
        # load model *then* move it to the device
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,
            local_files_only=True,
            low_cpu_mem_usage=False  # optional
        ).to(self.device)
        self.model.eval()

    def build_prompt(self, slots: dict) -> str:
        merged = {**self.DEFAULT_SLOTS, **slots}
        return self.SYSTEM_TEMPLATE.format(**merged)

    def _extract_lyrics_only(self, full_text: str, prompt: str) -> str:
        if "### LYRICS START BELOW ###" in full_text:
            return full_text.split("### LYRICS START BELOW ###", 1)[1].strip()
        elif full_text.startswith(prompt):
            return full_text[len(prompt):].strip()
        return full_text.strip()

    def generate(self, slots: dict) -> str:
        # 1. 解析并限制目标字数
        target_word_count = slots.get("length", 200)
        target_word_count = max(200, min(target_word_count, 1200))
        target_tokens = int(target_word_count * 1.4)

        # 2. 构建 prompt 并 tokenize
        prompt = self.build_prompt(slots)
        enc = self.tokenizer(prompt, return_tensors="pt", truncation=True)
        input_ids = enc["input_ids"].to(self.device)
        attention_mask = enc["attention_mask"].to(self.device)

        # 3. 生成文本
        output_ids = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=target_tokens,
            do_sample=True,
            top_p=0.9,
            top_k=40,
            temperature=1.1,
            repetition_penalty=1.0,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        # 4. 解码并抽取歌词部分
        full_text = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
        return self._extract_lyrics_only(full_text, prompt)
