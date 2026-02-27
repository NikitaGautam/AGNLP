import pandas as pd
# names = ["Nigeria"]
# for name in names:
# filename = name
# keyword = filename +" AND (Nutrient OR Fertilization OR Fertilizer OR Rates OR Doses OR Nitrogen OR Phosphorus OR Potassium OR Sulfur OR Sulphur) AND Yield"

names = [
        "nitrogendilution",
        "multispectral",
        "nyield",
        "corn"
    ]
keywords = [
    "Nitrogen dilution curve AND Nitrogen nutrition index AND Critical nitrogen concentration AND (annual ryegrass OR broomcorn millet OR cotton OR fodder beet OR hybrid ryegrass OR maize OR oat OR perennial ryegrass OR potato OR rescue grass OR rice OR sorghum OR sugarcane OR sunflower OR sweet potato OR tall fescue OR timothy grass OR wheat OR white cabbage)",
    "(multispectral airborne images OR drone OR UAV oR UAS OR unmanned aerial vehicle OR remotely piloted aircraft system) AND nitrogen AND yield",
    "yield AND (nitrogen fixation OR N fixation OR nitrogen from the atmosphere OR Ndfa OR nitrogen uptake OR N uptake OR seed nitrogen OR nitrogen harvest index OR NHI) AND (chickpea OR common bean OR cowpea OR faba bean OR field pea OR groundnut OR lentil OR lupins)",
    "corn OR maize AND (grain quality OR grain composition) AND (nitrogen fertilization OR water stress OR drought stress)"
]
for index, name in enumerate(names):
    filename = name
    keyword = keywords[index]
    
    final = ""
   
    # df1 = pd.read_csv(file1, sep='\t')
    # df2 = pd.read_csv(file2, sep='\t')

    # merged_1_2 = pd.concat([df1, df2], ignore_index=True)
    # merged_1_2.drop_duplicates(subset='scopus_id', inplace=True)

    # print(merged_1_2.columns)

    # df3 = pd.read_csv(file3, sep='\t')
    # df3.rename(columns={'Item Title': 'title'}, inplace=True)
    # df3.rename(columns={'Abstract': 'abstract'}, inplace=True)
    # df3.rename(columns={'DOI': 'doi'}, inplace=True)

    # final_merge = pd.concat([merged_1_2, df3], ignore_index=True)
    # final_merge['title'] = final_merge['title'].str.lower()
    # final_merge.drop_duplicates(subset='title', inplace=True)

    # columns = ['title', 'abstract', 'doi', 'authors', 'count']
    # final_df = final_merge[columns]

    # final_df.to_csv(final, sep='\t', index=False)

    # print(final_df)


    # -- in bash export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

    # import pandas as pd
    # import transformers
    # import torch
    # import os

    # df = pd.read_csv(final, sep='\t')

    # # Check if 'abstract' exists, else use 'title'
    # df['text_to_classify'] = df['abstract'].fillna(df['title'])

    # # Initialize the model pipeline
    # model_id = "meta-llama/Llama-2-7b-chat-hf"
    # os.environ["CUDA_VISIBLE_DEVICES"] =  "3"
    # # "0"
    # device = "cuda" if torch.cuda.is_available() else "cpu"

    # pipeline = transformers.pipeline(
    #     "text-generation",
    #     model=model_id,
    #     model_kwargs={"torch_dtype": torch.float16}, 
    #     device=device,
    # )

    # # Define the system and user prompt
    # def create_prompt(text):
    #     messages = [
    #         {"role": "system", "content": "You are an expert in agriculture and an excellent text classifier."},
    #         {"role": "user", "content": f'''You are given a search equation and a text. Your task is to determine if the text contains information relevant to the search equation.
    #         Focus on finding as many keywords from the search equation as possible in the text. 
    #         If the text contains multiple relevant keywords, respond with RELATED. If it does not contain relevant keywords or only a few, respond with UNRELATED.
    #         Only respond with RELATED or UNRELATED no other text required.
    #         Search Equation: {keyword}
    #         Text: {text}
    #         Result:'''}
    #     ]
        
    #     prompt = pipeline.tokenizer.apply_chat_template(
    #         messages,
    #         tokenize=False,
    #         add_generation_prompt=True
    #     )
    #     return prompt

    # terminators = [
    #     pipeline.tokenizer.eos_token_id,
    #     pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    # ]

    # def classify_text(text):
    #     prompt = create_prompt(text)
    #     outputs = pipeline(
    #         prompt,
    #         max_new_tokens=32,
    #         eos_token_id=terminators,
    #         do_sample=True,
    #         temperature=0.6,
    #         top_p=0.9,
    #     )
    #     result_text = outputs[0]["generated_text"][len(prompt):]
    #     # print(result_text)
    #     return result_text.strip()

    # for index, row in df.iterrows():
    #     result = classify_text(row['text_to_classify'])
    #     df.at[index, 'classification_result'] = result
    #     # print(f"Processed row {index}: Classification = {result}")

    # df.drop(columns=['text_to_classify'], inplace=True)
    # updated_csv_file = ""
    # df.to_csv(updated_csv_file, sep='\t', index=False)

    # print(f"Updated CSV saved to: {updated_csv_file}")
