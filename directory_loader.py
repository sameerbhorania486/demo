from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader
)

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
import os


# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()

api_key = os.getenv("api_key")


# =========================
# TXT LOADER
# =========================

text_loader = DirectoryLoader(
    path="File_Loader",
    glob="*.txt",
    loader_cls=TextLoader
)

text_docs = text_loader.load()

print("TXT files loaded:", len(text_docs))


# =========================
# TEXT TOOL
# =========================

@tool
def search_text(que: str):
    """Search relevant information from Text documents.
    Use this tool when the user asks about Git or GitHub commands.
    """

    result = []

    for i in text_docs:
        if que.lower() in i.page_content.lower():
            result.append(i.page_content)

    if result:
        return "\n".join(result)

    return "Text information not found."


# =========================
# LLM
# =========================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=api_key
)


# =========================
# BIND TOOL
# =========================

llm_tool = llm.bind_tools([
    search_text
])


# =========================
# USER QUESTION
# =========================

que = input("How can I help you today? ")

message = [
    HumanMessage(content=que)
]


# =========================
# FIRST LLM CALL
# =========================

response = llm_tool.invoke(message)

print("\nLLM Decided:")
print(response.tool_calls)

message.append(response)


# =========================
# TOOL MAPPING
# =========================

all_tools = {
    "search_text": search_text
}


# =========================
# EXECUTE TOOL
# =========================

for tool_call in response.tool_calls:

    tool_name = tool_call["name"]

    tool_result = all_tools[tool_name].invoke(
        tool_call["args"]
    )

    print("\nTool Result:")
    print(tool_result)

    message.append(
        ToolMessage(
            content=tool_result,
            tool_call_id=tool_call["id"]
        )
    )


# =========================
# FINAL LLM RESPONSE
# =========================

final_response = llm.invoke(message)

print("\nFinal Answer:")
print(final_response.content)