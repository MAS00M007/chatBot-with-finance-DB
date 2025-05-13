import os
from dotenv import load_dotenv
import pymongo
from huggingface_hub import InferenceClient

load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")
client = InferenceClient(
    provider="novita",
    api_key=api_key,
)

# Connect to your MongoDB instance
mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['test']
transactions_col = db['transactions']

def get_financial_summary():
    total_saving = transactions_col.aggregate([
        {"$match": {"type": "saving"}},
        {"$group": {"_id": None, "sum": {"$sum": "$amount"}}}
    ])
    total_expense = transactions_col.aggregate([
        {"$match": {"type": "expense"}},
        {"$group": {"_id": None, "sum": {"$sum": "$amount"}}}
    ])
    total_income = transactions_col.aggregate([
        {"$match": {"type": "income"}},
        {"$group": {"_id": None, "sum": {"$sum": "$amount"}}}
    ])
    def get_sum(cursor):
        for doc in cursor:
            return doc.get("sum", 0)
        return 0
    return get_sum(total_income), get_sum(total_expense), get_sum(total_saving)

def get_transaction_details():
    txns = list(transactions_col.find())
    if not txns:
        return "No transactions found."
    details = "Here are your transactions:\n"
    for txn in txns:
        details += f"- {txn.get('date', '')}: {txn.get('description', '')} ({txn.get('type', '')}) {txn.get('amount', 0)}\n"
    return details

def ask_bot(domain, user_input):
    db_info = ""
    if domain == "finance":
        system_prompt = "You are a financial expert. Use the user's transaction data to provide personalized financial advice."
        if any(word in user_input.lower() for word in ["save", "saving", "money", "balance", "income", "expense"]):
            income, expense, saving = get_financial_summary()
            db_info = f"Your total income is {income}, total expenses are {expense}, and total savings are {saving}. "
        if "transaction" in user_input.lower():
            db_info += get_transaction_details() + "\n"
    elif domain == "programming":
        system_prompt = "You are a programming expert. Only answer questions about software development, coding, and computer science."
    elif domain == "space":
        system_prompt = "You are a space science expert. Only answer questions about astronomy, astrophysics, and the universe."
    else:
        system_prompt = "You are a helpful assistant."

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": db_info + user_input}
        ],
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    domain = input("Choose domain (finance/programming/space): ")
    question = input("Ask your question: ")
    reply = ask_bot(domain, question)
    print("\n🤖 AI Reply:\n", reply)
