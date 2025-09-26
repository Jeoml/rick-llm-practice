🚀 What is Rick LLM?
Rick LLM is a fun and educational project where you fine-tune Llama 3.1 8B to speak in Rick Sanchez’s chaotic, sarcastic style. You'll:

Create a custom dataset from Rick and Morty transcripts (in ShareGPT format)

Finetune Llama using LoRA with Unsloth

Deploy and chat with your Rickified model using Ollama

"Sometimes science is more art than science, Morty."

🧠 How It Works
1. Dataset Creation
Transcripts are cleaned and formatted as instruction-style data

Optionally pushed to Hugging Face for reusability

Script: src/dataset.py

2. Model Finetuning
Performed using Unsloth and LoRA

Hosted on GPU via Lambda Labs

Code: src/rick_llm/

3. Deployment via Ollama
Finetuned model is converted to GGUF + Modelfile

Loaded into Ollama for local chat experience

⚙️ Setup
Create a .env file with:

bash
Copy
Edit
OPENAI_API_KEY="your_openai_api_key"
HUGGINGFACE_TOKEN="your_huggingface_token"
LAMBDA_API_KEY="your_lambda_api_key"
🛠️ Run the Project (Summary)
bash
Copy
Edit
# Optional: Generate dataset
make create-dataset

# Set up cloud instance
make generate-ssh-key
make launch-lambda-instance
make get-lambda-ip
rsync files + ssh into instance

# Inside instance
make lambda-setup
make finetune
make terminate-instance

# Back locally: Download and run in Ollama
make download-model
ollama create rick-llm -f ollama_files/Modelfile
ollama run rick-llm
🤝 Contributing
Fork the repo

Create a new branch

Commit and push your changes

Open a pull request

