from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import os
import time

load_dotenv()
app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "service": "newsletter-backend"})

@app.route("/")
def main():
    print('called by front end.')
    print('searching for most recent updates')
    start = time.time()
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents= [
            """
            CONTEXT:
            I'm an incoming Penn M&T student studying MechE with deep interest in AI, robotics, and startups. I'm currently working at a startup building AI glasses and am excited about how systems/AIs communicate in a fully agentic world, retrieval algorithms/knowledge graphs, and super memory. 
            I want to stay updated with research and learn the cutting edge concepts being explored. 

            TASK:
            Search for 5 of the most impactful papers from arXiv published in the last 30 days in these fields:
            - Computer vision and multimodal AI
            - Spatial intelligence
            - Robotics and embodied AI
            - Edge AI and on-device inference
            - Agent to agent communication
            - Proof of human
            - Super memory, knowledge graphs, retrieval algorithms, RAG.
            - Mechanistic Interpretability, AI alignment
            - Human-computer interaction (specifically, neuroscience/neuro computing)

            OUTPUT FORMAT:
            Return 5 papers. For each paper, provide exactly this structure:

            ### [Paper Title]

            **Link:** [arXiv link]
            **Publication Date:** [Date]

            **Description:**
            [2-3 sentence summary of what the paper does]

            **Why It Matters:**
            [How it advances the field, commercial potential, relevance to AI glasses/robotics.]

            **Technical Innovation (if relevant):**
            [Key technical contributions, what it builds upon. Be specific and be concrete.]

            **Future Opportunities:**
            [What can be improved, startup/business opportunities]

            **Key Terms**
            [***key terms from the paper that beginners may not understand explained simply]

            ---

            REQUIREMENTS:
            - Only include papers with actual arXiv links
            - Focus on recent breakthrough results
            - Make sure to dive into the details of each paper. Don't abstract it away. 
            """
        ],
        config=config
    )
    print(response.text)
    end = time.time()
    print(f"time spent {end-start}")
    return jsonify({"content": response.text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)

# interesting notes
# so, I changed the gemini api call from 5 papers returned to just 1. time stayed mostly the same. 
# this means that most the time is actually from just searching through Arxiv and not deciding on the paper and generating the info for each paper. 
# thus changed back to 5 papers.
