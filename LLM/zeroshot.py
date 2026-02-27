import transformers
import torch
import os
# model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
model_id = "meta-llama/Llama-2-7b-chat-hf"
os.environ["CUDA_VISIBLE_DEVICES"]="0"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(device)

pipeline = transformers.pipeline(
"text-generation",
model=model_id,
model_kwargs={"torch_dtype": torch.bfloat16},
device=device,
)

messages = [
{"role": "system", "content": "You a expert in agriculture and an excellent text classifier."},
{"role": "user", "content": '''Given the text and keywords, determine whether the text contains information relevant to the keyword. 
            Return response of either unrelated = 0 or related = 1, only return the number.
            KEYWORDS: Niger AND (Nutrient OR Fertilization OR Fertilizer OR Rates OR Doses OR Nitrogen OR Phosphorus OR Potassium OR Sulfur OR Sulphur) AND Yield
            Text: From the last several years, in serious consideration of the worldwide economic and environmental pollution issues there has been increasing research interest in the value of bio-sourced lignocellulosic biomass. Agro-industrial biomass comprised on lignocellulosic waste is an inexpensive, renewable, abundant and provides a unique natural resource for large-scale and cost-effective bio-energy collection.
             To expand the range of natural bio-resources the rapidly evolving tools of biotechnology can lower the conversion costs and also enhance target yield of the product of interest. In this background green biotechnology presents a promising approach to convert most of the solid agricultural wastes particularly lignocellulosic materials into liquid bio based energy-fuels. In fact, major advances have already been achieved to competitively position cellulosic ethanol with corn ethanol. The present summarized review work begins with an overview on the physico-chemical features and composition of agro-industrial biomass. The information is also given on the multi-step processing technologies of agro-industrial biomass to fuel ethanol followed by a brief summary of future considerations. Copyright (C) 2014, The Egyptian Society of Radiation Sciences and Applications. Production and hosting by Elsevier B.V. All rights reserved.}
            Result:'''},
]

prompt = pipeline.tokenizer.apply_chat_template(
messages,
tokenize=False,
add_generation_prompt=True
)

terminators = [
pipeline.tokenizer.eos_token_id,
pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = pipeline(
prompt,
max_new_tokens=128,
eos_token_id=terminators,
do_sample=True,
temperature=0.6,
top_p=0.9,
)
print(outputs[0]["generated_text"][len(prompt):])