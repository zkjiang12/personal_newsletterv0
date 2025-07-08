from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
import os
import time
from supabase import create_client, Client
import re

load_dotenv()
#FLASK INITIALIZATION
app = Flask(__name__)
CORS(app)

#GEMINI INITALIZATION
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
grounding_tool = types.Tool( # declare tool use
    google_search=types.GoogleSearch()
)
config = types.GenerateContentConfig( # Configure generation settings
    tools=[grounding_tool]
)

#SUPABASE INITALIZATION
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def uploadToSupabase(response):
    try:
        """Extract paper titles from Gemini response using the ### format"""
        
        #Regex is just a python library for pattern identifcation
        # Find all occurrences of ### [title] ###
        pattern = r'### (.*?) ###'
        matches = re.findall(pattern, response)
        
        for match in matches:
            title = match.strip()
            print(f"Found title: {title}")

            (#upload the title to supabase
                supabase.table("titles")
                .insert({"title": title})
                .execute()
            )

        # now run code to upload the entire contents to Supabase!!
        (
            supabase.table("responses")
            .insert({"content": response})
            .execute()
        )
        print('added everything to supabase')

    except:
        print('error. i fucked up the code lmao')
    

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "service": "newsletter-backend"})

@app.route("/")
def main():
    print('called by front end.')
    print('searching for most recent updates')
    start = time.time()

    #gets the titles from Supabase
    titlesResponse = supabase.table('titles').select('*').execute()
    titles = [title['title'] for title in titlesResponse.data]
    print('titles', titles)
    
    # search with Gemini
    response = client.models.generate_content(
        model = 'gemini-2.5-flash',
        contents= [
            f"""
           CONTEXT:
            I'm an incoming Penn M&T student studying MechE with deep interest in AI, robotics, and startups. I'm currently working at a startup building AI glasses and am excited about how systems/AIs communicate in a fully agentic world, retrieval algorithms/knowledge graphs, and super memory. 
            I want to stay updated with research and learn the cutting edge concepts being explored. 

            TASK:
            Search for 5 of the most impactful papers from arXiv published in the last 30 days in these fields:
            - Multimodal AI
            - Spatial intelligence
            - Robotics and embodied AI
            - Agent to agent communication
            - Proof of human
            - Super memory, knowledge graphs, retrieval algorithms, RAG.
            - Mechanistic Interpretability, AI alignment

            OUTPUT FORMAT:
            Return 5 papers. For each paper, provide exactly this structure:

            **Why It Matters:**
            [How it advances the field, commercial potential, relevance to AI glasses/robotics.]

            **Technical Innovation (if relevant):**
            [Key technical contributions, what it builds upon. Be specific and be concrete.]

            **Future Opportunities:**
            [What can be improved, startup/business opportunities]

            **Key Terms**
            [***key terms from the paper that beginners may not understand explained simply]

            ### [Paper Title] ###

            **Link:** [arXiv link]
            **Publication Date:** [Date]

            **Description:**
            [2-3 sentence summary of what the paper does]

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
    print(type(response.text))
    #now upload stuff to Supabase
    uploadToSupabase(response.text)
    return jsonify({"content": response.text})

@app.route('/supabase')
def getAllSupabaseDocs():
    contents = (
        supabase.table("responses")
        .select('*')
        .execute()
    )
    contents = [content['content'] for content in contents.data]
    print('contents', contents)
    return jsonify({"data": contents})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)

# interesting notes
# so, I changed the gemini api call from 5 papers returned to just 1. time stayed mostly the same. 
# this means that most the time is actually from just searching through Arxiv and not deciding on the paper and generating the info for each paper. 
# thus changed back to 5 papers.

# takeaway
# the most important thing is a quick feedback loop. so if I'm coding something like adding the supabase, it'd be helpful if I didn't have to wait 3 fucking minutes for the gemini to load.
# thus test in diff code where it approximates the complete backend, i.e in this case with gemini 2.5 but no tool use, and when it works, add back into the actual file.

# instead of making the extracting title code complex, just change the response format LMAO to make it easier to find where the title is. I just boxed the title in on both sides with this ###. 
