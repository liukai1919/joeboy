from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class ChatModel:
    def __init__(self):
        self.device = settings.MODEL_DEVICE
        self.model_name = settings.MODEL_NAME
        self.max_length = settings.MAX_LENGTH
        self.temperature = settings.TEMPERATURE
        self.top_p = settings.TOP_P
        self.top_k = settings.TOP_K
        
        logger.info(f"Loading model {self.model_name} on {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        
        # 检查CUDA是否可用
        if torch.cuda.is_available():
            logger.info(f"CUDA is available. Loading model in 8-bit quantized mode to reduce memory consumption.")
            # 使用 8-bit 量化和自动设备映射
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                load_in_8bit=True,
                device_map="auto",
                trust_remote_code=True
            )
        else:
            logger.warning("CUDA is not available, falling back to CPU with full weights")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
        
        logger.info("Model loaded successfully")

    def generate_response(self, prompt: str, max_new_tokens: int = 512) -> str:
        """
        生成聊天回复
        """
        try:
            logger.debug(prompt)
            # 构建输入
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = inputs.to("cuda:0")
            
            # 生成回复
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    top_k=self.top_k,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True
                )
            
            # 仅保留模型新生成的 token 部分
            generated_ids = outputs[0][inputs["input_ids"].size(1):]
            reply = self.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
            # 如果模型继续生成了下一轮 "User:" 等标记，则截断
            stop_phrases = ["\nUser:", "\n用户：", "\nHuman:"]
            for s in stop_phrases:
                if s in reply:
                    reply = reply.split(s)[0].strip()
                    break
            return reply
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"

    def format_prompt(self, user_input: str, chat_history: list = None) -> str:
        """
        格式化提示词，只返回最终答案，不输出推理过程
        """
        if chat_history is None:
            chat_history = []
        
        # 系统指令：只回答最终答案，不包含推理
        prompt = "System: You are a helpful AI assistant. Provide only the final answer to the user's question. Do NOT include any reasoning, analysis, or chain-of-thought.\n\n"
        
        # 添加历史对话
        for message in chat_history:
            if message["role"] == "user":
                prompt += f"User: {message['content']}\n"
            else:
                prompt += f"Assistant: {message['content']}\n"
        # 添加当前用户输入
        prompt += f"User: {user_input}\nAssistant:"
        
        return prompt