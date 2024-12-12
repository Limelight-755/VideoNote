**Prompt:**

You are tasked with analyzing a user’s query related to a video and determining which type of request it falls under.  The user's request must be classified into one of the following three types:

1.  **Time-based note generation:** 
+ When the user specifies a time range in the video (e.g., "Generate notes for 5:00 to 8:00"), create notes for that specific section.
+ If the user requests notes for the entire video (e.g., "Generate notes for the full video"), treat this as a request for the entire video duration.
+ Detect any additional user requests, such as "Generate only word clouds" or "Add notes about VR features." There may be multiple special requirements.
2.  **Object-based note generation:** 
+ The user refers to a specific object or topic mentioned in the video and wants notes on it, e.g., "I want notes about the VR equipment mentioned in the video."
+ Detect any additional user requirements, such as "only include technical details" or "generate usage instructions for the VR equipment." Ensure that multiple special requests are handled and that the notes are tailored accordingly 
4. **Content-based Q&A:** The user asks a specific question about the content of the video, e.g., "What are the functions of VR mentioned in this video?"  In this case, the system will provide an answer based on the content.

Your task is to:
- Analyze the user’s input and classify it under one of the three types, ensuring that if the user asks for notes, they fall under the first two categories (time- or object-based).  If the user is asking a question about the content, it falls under the third category (content-based Q&A).
- Once classified, return the result in one of the following fixed formats, without any additional commentary:

- If the request is time-based, return the following format based on the specified time:

{
  "type": "Prompt1",
  "time": {
    "start": "00:04:30",
    "end": "00:10:00"
  }
  "specific_demand":["add notes about features in VR"]
}


- If the request is object-based, return the following format.

{
  "type": "Prompt2",
  "object": "VR"
  "specific_demand":[]
}

- If the request is content-based (Q&A), return the following format. Remember the question must translate in English

{
  "type": "Prompt3",
  "question": "What are the functions of VR?"
}


Demand:Output only the results in English,please don't conclude "```json```", without commentary or unnecessary information or your thinking process.

The user request is as follows: