from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_neo4j import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

loader = TextLoader("./example.txt")

documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

# The Neo4jVector Module will connect to Neo4j and create a vector index if needed.

db = Neo4jVector.from_documents(
    docs, embeddings, url=url, username=username, password=password,
    search_type="hybrid"
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score = db.similarity_search_with_score(query, k=2)
