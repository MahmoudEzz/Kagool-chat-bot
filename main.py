import os
from fastapi import FastAPI
from openai import AzureOpenAI
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

dataset = pd.read_csv('dataset/uae_real_estate_2024.csv')

dataset.dropna(inplace=True) # For simplicity, we'll drop rows with missing values

dataset["combined"] = "address: " + dataset["displayAddress"] + ", bedrooms = " + dataset["bedrooms"] + ", type : " + dataset["type"] + ", price: " + str(dataset["price"].iloc[0]) + ", size: " + dataset["sizeMin"] + ", furnishing: " +  dataset["furnishing"] + ", bathrooms = " + dataset["bathrooms"] 
small_dataset= dataset[["combined", "description"]].iloc[:1000]

app = FastAPI()


@app.get("/chat")
async def chat(query: str = ''):

    client = AzureOpenAI(
        azure_endpoint = os.getenv("OPENAI_AZURE_END_POINT"), 
        api_key= os.getenv("OPENAI_API_KEY"),  
        api_version= os.getenv("OPENAI_API_VERSION"),
    )

    data_set_vectors = client.embeddings.create(
        model="text-embedding-ada-002",
        input=small_dataset["combined"].values.tolist(),
    )

    pure_data_set_vectors = []
    for data_set_vector in data_set_vectors.data:
        pure_data_set_vectors.append(data_set_vector.embedding)

    user_vector = client.embeddings.create(
        model="text-embedding-ada-002",
        input=query
        )
    
    user_vector = user_vector.data[0].embedding
    # Normalize the user_vector
    user_vector_norm = user_vector / np.linalg.norm(user_vector)

    # Normalize each vector in pure_data_set_vectors
    pure_embeds_norm = pure_data_set_vectors / np.linalg.norm(pure_data_set_vectors, axis=1, keepdims=True)

    # Calculate the cosine similarity for each pair of the user_vector and the vectors in pure_data_set_vectors
    cosine_similarity_scores = np.dot(user_vector_norm, pure_embeds_norm.T)

    # Get the indices of the scores sorted in descending order
    sorted_indices = np.argsort(1-cosine_similarity_scores)

    # Now create a prioritized list of real state based on the sorted indices
    prioritized_choices = [small_dataset['combined'].iloc[index] for index in sorted_indices]

    # get top 5 posssibilites
    training_DS= prioritized_choices[:30]

    print("---------------------", training_DS)
    # Join the list into a single string with each item on a new line
    embeds_res = "\n".join(training_DS)

    messages = [{"role": "system", "content": """I want you to act as a real estate agent. Your name is "My Super Assistant". You will provide me with one answer from the given info."""}]
    messages.append({"role": "assistant", "content": embeds_res})
    # messages.append({"role": "user", "content": "Give me answer in suitable to render in streamlit chat app"})
    messages.append({"role": "user", "content": query})

    chat_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.9,
        max_tokens=300,
    )

    return chat_response.choices[0].message.content