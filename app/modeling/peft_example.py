import torch
from transformers import AutoModel, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

model_name = "BAAI/bge-small-en-v1.5"
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

peft_config = LoraConfig(
    task_type=TaskType.FEATURE_EXTRACTION,
    inference_mode=False,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
)

peft_model = get_peft_model(model, peft_config)

print(peft_model.print_trainable_parameters())

# Example input text
input_text = "Hugging Face models are amazing!"
inputs = tokenizer(input_text, return_tensors="pt")

# Forward pass through the PEFT model
with torch.no_grad():  # No gradients required for inference
    outputs = peft_model(**inputs)

print("last_hidden_state")
print(outputs.last_hidden_state.shape)
print("pooler_output")
print(outputs.pooler_output.shape)
print("lol")
#
# # Forward pass
# outputs = peft_model(**inputs)

# Example of how to fine-tune
# Assume we have some labeled dataset with input_ids and labels
# optimizer = torch.optim.AdamW(peft_model.parameters(), lr=1e-4)
# for epoch in range(num_epochs):
#     for batch in dataloader:
#         input_ids, labels = batch
#         optimizer.zero_grad()
#         outputs = peft_model(input_ids=input_ids)
#         loss = compute_loss(outputs, labels)
#         loss.backward()
#         optimizer.step()

# Save the fine-tuned model

