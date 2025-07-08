from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import os

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
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents= [
            """
            CONTEXT:
            I'm an incoming Penn M&T student studying MechE with deep interest in AI, robotics, and startups. I'm currently working at a startup building AI glasses and plan to found my own company in the future.

            TASK:
            Search for one of the most impactful AI/Robotics papers from arXiv published in the last 30 days. Focus on papers relevant to:
            - Computer vision and multimodal AI
            - Spatial intelligence
            - Robotics and embodied AI
            - Edge AI and on-device inference
            - Human-computer interaction (specifically, neuroscience/neuro computing)

            OUTPUT FORMAT:
            For the paper, provide exactly this structure:

            ### [Paper Title]

            **Link:** [arXiv link]
            **Publication Date:** [Date]

            **Description:**
            [2-3 sentence summary of what the paper does]

            **Why It Matters:**
            [How it advances the field, commercial potential, relevance to AI glasses/robotics]

            **Technical Innovation (if relevant):**
            [Key technical contributions, what it builds upon]

            **Future Opportunities:**
            [What can be improved, startup/business opportunities]

            ---

            REQUIREMENTS:
            - Only include papers with actual arXiv links
            - Focus on recent breakthrough results
            """
        ],
        config=config
    )
    print(response.text)
    return jsonify({"content": response.text})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)