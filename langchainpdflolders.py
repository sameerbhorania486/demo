from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path='books',
    glob='*.txt',
    loader_cls=PyPDFLoader
)

docs = loader.load()

print(docs[0].metadata)

# for document in docs:
#     print(document.metadata)