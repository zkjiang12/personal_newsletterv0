#test with gemini
import asyncio
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import os
import time

load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

interests = ["Computer vision, spatial intelligence and multimodal AI","Robotics and embodied AI", "Edge AI and on-device inference", "Human-computer interaction (specifically, neuroscience/neuro computing)"]

async def call_gemini(interest):
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents= [
            f"""
            CONTEXT:
            I'm an incoming Penn M&T student studying MechE with deep interest in AI, robotics, and startups. I'm currently working at a startup building AI glasses and plan to found my own company in the future.

            TASK:
            Search for most impactful AI/Robotics papers from arXiv published in the last 30 days in the field of {interest}
           
            OUTPUT FORMAT:
            For the paper, provide exactly this structure:

            ### [Paper Title]

            **Link:** [arXiv link]
            **Authors:** [First 3-5 authors, institutions]
            **Publication Date:** [Date]

            **Description:**
            [2-3 sentence summary of what the paper does]

            **Why It Matters:**
            [How it advances the field, commercial potential, relevance to AI glasses/robotics]

            **Technical Innovation (if relevant):**
            [Key technical contributions, what it builds upon]

            **Future Opportunities:**
            [What can be improved, startup/business opportunities]

            **Relevance Score:** [1-10 for AI glasses/robotics startup]
            ---

            REQUIREMENTS:
            - Only include papers with actual arXiv links
            - Focus on recent breakthrough results
            """
        ],
        config=config
    )
    print("response",response)
    return response

async def main_concurrent():
    results = await asyncio.gather(*[call_gemini(interest) for interest in interests])
    return results

async def call_gemini_all_interests():
    interests_str = "\n".join([f"- {interest}" for interest in interests])
    
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents= [
            f"""
            CONTEXT:
            I'm an incoming Penn M&T student studying MechE with deep interest in AI, robotics, and startups. I'm currently working at a startup building AI glasses and plan to found my own company in the future.

            TASK:
            Search for the most impactful AI/Robotics papers from arXiv published in the last 30 days across these fields:
            {interests_str}
           
            Find 1-2 top papers per field (total 4-8 papers).
           
            OUTPUT FORMAT:
            For each paper, provide exactly this structure:

            ### [Paper Title]

            **Field:** [Which of the 4 fields this belongs to]
            **Link:** [arXiv link]
            **Authors:** [First 3-5 authors, institutions]
            **Publication Date:** [Date]

            **Description:**
            [2-3 sentence summary of what the paper does]

            **Why It Matters:**
            [How it advances the field, commercial potential, relevance to AI glasses/robotics]

            **Technical Innovation (if relevant):**
            [Key technical contributions, what it builds upon]

            **Future Opportunities:**
            [What can be improved, startup/business opportunities]

            **Relevance Score:** [1-10 for AI glasses/robotics startup]
            ---

            REQUIREMENTS:
            - Only include papers with actual arXiv links
            - Focus on recent breakthrough results
            - Cover all 4 fields mentioned above
            """
        ],
        config=config
    )
    print("response", response)
    return response

async def main_single_call():
    result = await call_gemini_all_interests()
    return result

# FASTEST VERSION - Remove grounding tool (major bottleneck), minimal prompt
async def call_gemini_fast(interest):
    # No grounding tool = much faster
    response = client.models.generate_content(
        model = 'gemini-1.5-flash',  # Fastest model
        contents= [
            f"""Find 1 recent AI paper in {interest}. 

FORMAT:
**{interest}**
Title: [title]
Link: arxiv.org/abs/[id] 
Summary: [1 sentence]
Relevance: [1-10]
---"""
        ]
        # No config = no tools = much faster
    )
    print(response.text)
    return response

async def main_ultra_fast():
    # Concurrent calls with minimal processing
    results = await asyncio.gather(*[call_gemini_fast(interest) for interest in interests])
    return results

print("="*50)
print("SPEED COMPARISON TEST")
print("="*50)

# # Test the slow version with grounding
# print("Testing SLOW version (with Google Search)...")
# start_slow = time.time()
# asyncio.run(main_single_call())
# end_slow = time.time()
# print("SLOW time: ", (end_slow - start_slow))

# Test the fast version  
print("\nTesting FAST version (no tools)...")
start_fast = time.time()
asyncio.run(main_ultra_fast())
end_fast = time.time()
print("FAST time: ", (end_fast - start_fast))

# print(f"\nSPEEDUP: {(end_slow - start_slow) / (end_fast - start_fast):.1f}x faster!") 