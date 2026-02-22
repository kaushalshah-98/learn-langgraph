1. user will send message
   1. Checks node
      1. if contain any offensive words
      2. if has some proper length or any other validations
      3. check timer if its up, we directly reply time is up!
      4. possible paths are [patient_node]
   2. (child of 1) Patient node
      1. prompt to say that you are patient and give the context
      2. do not reveal your diagnose
      3. do not reply to questions that are out of context
      4. do not reply in very big texts and have max token length
      5. mimic like a human conversation
      6. Give some few shot examples in prompt
      7. possible paths are [extra node, examiner node]
   3. (child of 2) Extra node
      1. Check if it contain diagnose name, revert back to patient node
      2. End and reply to user
      3. possible paths are [end]
   4. (child of 2) Examiner node
      1. when state is examiner, we push examiner questions to user
      2. user reply backs
      3. Here its not AI
      4. possible paths are [markschemenode, end]
   5. (child of 4) Markscheme node
      1. when state is markscheme, mark the markschemes using AI
      2. save in db/redis 
      3. possible paths are [aummary, end]
   6. (child of 5) Summary node
      1. when state is result, generate summary using markscheme, conversations
      2. brief, markscheme (related), examiner related (good, bad, improvements) 
      3. possible paths are [end]

2. There will be token of streams send to user via websocket
   
3. State will ve 
   1. messages array
   2. llm call count -> to exit if we need to restrict for free users
   3. token count -> to exit if we need to restrict for free users
   4. timer or endedAt
   5. summary -> if we need to generate or update summary till now
   6. max_message_window
   7. How to save this data in redis or DB per user session
   8. route -> actor | examiner | markscheme | summary

4. Router ->
   1. based on state route to patient, or examiner or markscheme or summary
   2. patient will have further child to check if response is okay or else loopback
   3. similar for markscheme and summary if needed

5. How to have concurrent chats with this setup and how much concurrency?
6. See latency of LLMS
7. check which LLM could be best for actor, markscheme and summary
8. Whether FE can communicate directly with AI service or via BE ?
9.  Examiner questions are harcoded in FE, how to fetch it from state or redis or DB?
10. Fault taulerance if patient take too much time? than redirect to fast one?
11. If free session, we can use faster or cheap llms?
12. How to create prod ready app and deploy it using env and routes?
13. For a average session how much token counts happen or how much llm calls happen at each level
    1.  Patient => token counts and llm calls and latency per query
    2.  Examiner => its all hardcoded
    3.  Markscheme => token counts and latency per query
        1.  how to improve this and what context?
        2.  how to get same structure response back using llm.with strcuture?
    4.  Summary => token counts and latency per query
        1.  how to improve this and what context?
        2.  how to get some structure response back using llm.with strcuture?
14. How much in-memory state?