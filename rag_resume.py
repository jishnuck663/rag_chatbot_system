
from pathlib import Path
from config import db, llm
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


files = list(Path("resumes").glob("*.pdf"))

for i, file in enumerate(files):
    print(i + 1, file.name)

choice = int(input("Select resume: ")) - 1
file = files[choice]


docs = PyPDFLoader(str(file)).load()
chunks = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)


db.add_documents(chunks)
print("Resume stored successfully!")


while True:
    question = input("\nAsk (exit to stop): ")

    if question.lower() == "exit":
        break

    results = db.similarity_search(question, k=3)
    context = "\n".join(d.page_content for d in results)

    prompt = f"""
    Answer using only this resume context.
    If not found, say "Not found in resume".

    Context: {context}
    Question: {question}
    """

    answer = llm.invoke(prompt)
    print("\nAnswer:", answer.content)
