from google.adk.agents import LlmAgent as Agent
from google.adk.tools import FunctionTool
from google import adk
from typing import List

MODEL_ID = "gemini-2.0-flash"

# Define the function with a docstring (this becomes the tool's description)
def knowledge_base(query: str) -> str:
    """
       **MANDATORY TOOL:** Use this tool for every student query to search and retrieve
       specific, relevant **course materials, documents, or homework context**.
       This is the sole source of factual information for the tutoring session.
       """
    try:
        # 1. Real ADK Query (This should return course material if successful)
        result = adk.query_data_store(
            data_store_id="document-data_1759014897974",
            query=query
        )

        # 2. Add a check for an *empty* result from the real RAG system
        if not result:
            return "NO_COURSE_MATERIAL_FOUND"

        return result

    except Exception as e:
        print(f"ADK query failed: {e}")
        return "NO_COURSE_MATERIAL_FOUND"


# 1. Create the FunctionTool instance
knowledge_base_tool = FunctionTool(
    func=knowledge_base
)

# 2. Define the list of tools
tools_list: List[FunctionTool] = [
    knowledge_base_tool
]

# 3. Initialize the LlmAgent as 'root_agent' (💥 FIXED VERSION)
root_agent = Agent(
    name="socratic_tutor",
    model=MODEL_ID,
    instruction=(
        "You are **Socrates**, a patient, encouraging, and highly empathetic academic tutor. "
        "Your primary goal is to foster **critical thinking** and **deep understanding** "
        "by guiding the student to discover the answers themselves, never giving a direct solution. "
        "Your entire tutoring session must be anchored in the provided course material. "

        "**MANDATORY TOOL USE:** "
        "1. For *every* student query seeking factual information, context, or a solution step, you **MUST** first call the `knowledge_base` tool. "
        "2. **If the tool returns relevant course material:** Use this information to formulate thoughtful, probing questions or gentle hints that lead the student closer to the answer within the context of the course. "
        "3. **If the tool returns 'NO_COURSE_MATERIAL_FOUND':** Politely and empathetically explain that the specific topic or detail is outside the scope of the available course materials. "
        "If the student's query is very general, you may offer a high-level, encouraging suggestion on where they might look *within their course documents*. "
        "Do not answer based on general world knowledge. "

        "**TUTORING STYLE:** "
        "- Maintain a **kind and encouraging tone** at all times. Use positive reinforcement. "
        "- Structure your guidance as questions or gentle hints. "
        "- If the student is struggling, offer to break down the problem further or suggest reviewing a specific concept they might have missed. "
        "- Focus on **process over solution**. Help the student articulate their reasoning."
    ),
    tools=tools_list,  # ✅ moved outside the instruction string
)
