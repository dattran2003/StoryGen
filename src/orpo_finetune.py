import torch, multiprocessing
from datasets import load_dataset
from pert import LoraConfig, PertModel, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from trl import ORPOTrainer, ORPOConfig

model_name = 'Qwen/Qwen2-7B-Instruct'
tokenizer = AutoTokenizer.from_pretrained(model_name)
