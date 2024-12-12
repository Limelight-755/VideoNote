**Task:** Generate a detailed and comprehensive summary with timestamps from a YouTube video transcript based on the transcript. Also, add corresponding keyframe images to each summary and generate a word cloud if appropriate.
**Instructions:**
1. **Parse the transcript** to identify key content transitions. Each segment should capture significant content blocks or major shifts in the video, while avoiding overly short intervals or minor transitions.
2. **Format timestamps as [hh:mm:ss]-[hh:mm:ss]**, ensuring the minimum length of each segment is proportional to the total video range specified by the user. For example, if the video range is 5 minutes, the segment length should be at least 30 seconds, unless there is a significant content shift that warrants a shorter segment.
3. Provide **4 sentence summaries** for each segment. Summarize the key points, insights, and transitions discussed in that part of the video. Each summary should focus on capturing the most important aspects of the segment and avoid repetition, ensuring clarity and conciseness.
4. In the JSON format, for each segment, include the corresponding **direct_show_img** keyframe file names (e.g., `keyframe_xxxxx.jpg`). These keyframes should visually reflect the overall content of that specific video segment and can be displayed as they are.
5. For **segment_img**, select keyframes from each segment that contain important objects or details related to the specific segment. These images are associated with key elements in the video but will not be displayed directly and may undergo further image processing to highlight relevant elements.
6. If it helps explain the segment's content, generate a word cloud with 10-15 keywords for this segment(eg:for [00:03:00]-[00:08:40]). Word clouds should only be applied when necessary, not for every segment.But at least 1-2 word cloud is needed for whole note.
7. You must obey:
   + If the segment part have wordcloud, then the sum of segment_img and direct_show_img must be 2.
   + If the segment part don‘t have wordcloud, then the sum of segment_img and direct_show_img must be 4.
   + Be careful not to return images that don't exist! Don't reuse images. 
8. Ensure the number of segments aligns with the user-specified video range and follows the natural flow of the content. Transitions between segments should be logical, reflecting shifts in the video’s narrative or structure. 
9. The final segment should match the exact end time of the user-specified video range. For example, if the specified range ends at 00:24:31, the final segment’s timestamp must be [00:00:00]-[00:24:31]. 
10. The division of time segments should be based on the user-specified video range, maintaining coherence between the content and its timing.
11. Provide the output in the following format sample,please don't conclude "```json```":

{
  "all_title": "Vision Pro",
  "notes": [
    {
      "start_time": "00:00:00",
      "end_time": "00:04:20",
      "title": "Introduction",
      "text": [
        "The presenter introduces the Vision Pro and explains its uniqueness compared to other Apple products.",
        "The video highlights key innovations and expectations for this first-generation device.",
        "This segment sets the foundation for further discussions on Vision Pro's impact and features."
      ],
      "direct_show_img": ["keyframe_1003.jpg", "keyframe_3304.jpg"],
      "segment_img": ["keyframe_5015.jpg", "keyframe_34987.jpg"],
      "wordcloud_word": []
    },
    {
      "start_time": "00:04:20",
      "end_time": "00:07:20",
      "title": "Vision Pro Key Features",
      "text": [
        "The presenter details the hand-tracking technology, immersive high-resolution display, and spatial audio.",
        "These features aim to deliver an unparalleled VR experience.",
        "Vision Pro is positioned as a leader in the market with its cutting-edge technology."
      ],
      "direct_show_img": ["keyframe_1003.jpg", "keyframe_3304.jpg"],
      "segment_img": ["keyframe_39884.jpg", "keyframe_31683.jpg"],
      "wordcloud_word": []
    },
    {
      "start_time": "00:07:20",
      "end_time": "00:10:00",
      "title": "Design and Build Quality",
      "text": [
        "The presenter praises Vision Pro’s premium materials and sleek design.",
        "The ergonomics make it comfortable to wear for long periods.",
        "However, the device's weight may pose challenges for extended use."
      ],
      "direct_show_img": ["keyframe_2097.jpg"],
      "segment_img": ["keyframe_54829.jpg"],
      "wordcloud_word": []
    },
    {
      "start_time": "00:10:00",
      "end_time": "00:15:30",
      "title": "App Ecosystem and Limitations",
      "text": [
        "The presenter critiques the limited app ecosystem for Vision Pro.",
        "Current apps are limited, but there's hope for future developer engagement.",
        "The platform's success may depend on expanding the app ecosystem with immersive applications."
      ],
      "direct_show_img": ["keyframe_57382.jpg","keyframe_34987,"keyframe_25607","keyframe_11918"],
      "segment_img": [],
      "wordcloud_word": []
    },
    {
      "start_time": "00:15:30",
      "end_time": "00:20:00",
      "title": "Practical Use and User Experience",
      "text": [
        "This segment explores the battery life and overall comfort during long use.",
        "Users may face challenges with the device’s weight and battery for extended sessions.",
        "Short sessions are adequate, but longer VR experiences may require improvements."
      ],
      "direct_show_img": ["keyframe_35090.jpg", "keyframe_39884.jpg"],
      "segment_img": ["keyframe_63487.jpg"],
      "wordcloud_word": []
    },
    {
      "start_time": "00:20:00",
      "end_time": "00:24:31",
      "title": "Conclusion and Future Outlook",
      "text": [
        "The presenter wraps up with final thoughts on Vision Pro’s potential.",
        "There is optimism for future iterations with improved apps and pricing.",
        "Vision Pro could become a key product for Apple, shaping the future of VR/AR technology."
      ],
      "direct_show_img": ["keyframe_23809.jpg", "keyframe_29677.jpg"],
      "segment_img": ["keyframe_71234.jpg"],
      "wordcloud_word": []
    }
  ]
}


**Demand:**
Output only the results by json format, without commentary or unnecessary information or your thinking process.

The time period for which we are going to generate our notes is based on the **specified video range** provided by the user: