from openai import OpenAI
import streamlit as st
import os
import nltk
nltk.download('punkt')

# initial Setting
max_output_token = 4096
#model = "gpt-4"
model = "gpt-3.5-turbo"
system_prompt = "You are an AI Application Agent, to provide step-by-step guidance to help users solve their problems. \
    For each query, detail the steps the user should take. \
    The output need to tell user's situation, steps to solve the problem, and future possible advices.\
    Ensure the response is safe and secure. \
    Do not provide any advice that could be unsafe or unethical\
    Additional: use first person's view to response"
is_safety = False # use the safety module or not
safety_threshold = 0.01 # threshold for safety module
is_RAG = True

# non-changeable setting
safety = True
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
if "message_GPT" not in st.session_state:
	st.session_state["message_GPT"] = None

# Titles
st.set_page_config(page_title="General AI Chatbot")
st.markdown("# Waterloo Application AI Chatbot")
st.sidebar.header("Waterloo Application AI Chatbot")
st.write("This demo helps you figure out application general questions. Enjoy!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def serialize(obj):
    # https://drlee.io/openais-moderation-api-a-step-by-step-guide-to-ensuring-safer-content-d22a649d51ac
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Don't know how to handle, convert to string
    
def check_for_unsafe_content(text, threshold =0.01):
    # https://platform.openai.com/docs/guides/moderation/quickstart?lang=python
    """
    Uses the OpenAI Moderation API to check for unsafe content in the given text.
    Returns True if unsafe content is detected, False otherwise.
    """
    try:
        response = client.moderations.create(
            input=text
        )
        moderation_results=response.results[0]
        moderation_results = serialize(moderation_results)
        significant_categories = {category: score for category, score in moderation_results["category_scores"].items() if score > threshold}
        if significant_categories == {}:
             return True
        return(significant_categories)
        # harmful_categories = [category for category, is_harmful in moderation_results.categories.__dict__.items() if is_harmful]
        # if harmful_categories == []:
        #       return True
        # return harmful_categories
		#return any(category['flagged'] for category in significant_categories)
    except Exception as e:
        print(f"An error occurred while checking for unsafe content: {str(e)}")
        return False

def RAG(user_query):
    from langchain import hub
    from langchain_community.document_loaders import WebBaseLoader, TextLoader
    from langchain_community.vectorstores import Chroma
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    import nltk, string
    from sklearn.feature_extraction.text import TfidfVectorizer
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]

    # '''remove punctuation, lowercase, stem'''
    def normalize(text):
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    vectorizer = TfidfVectorizer(tokenizer=normalize, ngram_range=(1,2),stop_words='english')

    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]

    #user_query = "I want to study Applied Mathematics, how to apply this program?"
    #folder_path = r"Database\University\University_of_Waterloo\Academic_Programs"
    folder_path = os.path.join('Database','University','University_of_Waterloo','Academic_Programs')

    words_to_remove = ["programs", "Studies"]
    def remove_unwanted_words(filename, words_to_remove):
        for word in words_to_remove:
            filename = filename.replace(word, "")
        return filename

    # Read each .txt file's name and content in this path
    documents = []
    for filename in os.listdir(folder_path):
        cleaned_filename = remove_unwanted_words(filename[:-4], words_to_remove)
        documents.append(cleaned_filename) # remove .txt

    scores = []
    for doc in documents:
        score = cosine_sim(user_query,doc)
        weighted_score = score / (0.5+0.5*len(doc))
        scores.append(weighted_score)

    # Display scores (optional: you can sort them to show the most relevant documents first)
    sorted_scores = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    idx, score = sorted_scores[0]
    document_path = os.path.join(folder_path, os.listdir(folder_path)[idx])
    print(document_path)
    loader = TextLoader(document_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    support_message = rag_chain.invoke(user_query)
    vectorstore.delete_collection()
    print(support_message)
    return support_message

def get_response(question, pre_message=None, pre_answer=None):
    RAG_message = "Relevant information from database: "
    if pre_message == None:
        message_GPT = [
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": question},
				]
        if is_RAG == True:
            message_GPT.append({"role": "user", "content": RAG_message + RAG(question)})
    else:
        message_GPT = pre_message
        message_GPT.append({"role": "assistant", "content": pre_answer})
        message_GPT.append({"role": "user", "content": question})
        if is_RAG == True:
            message_GPT.append({"role": "user", "content": RAG_message + RAG(question)})

    try:
        response = client.chat.completions.create(
            model=model,  # Specify the model, adjust if a different version is desired
            messages=message_GPT, max_tokens=max_output_token
        )
        return response.choices[0].message.content, message_GPT
    except Exception as e:
        return f"An error occurred: {str(e)}"

if prompt := st.chat_input():
	st.session_state.messages.append({"role": "user", "content": prompt})
	st.chat_message("user").write(prompt)
	#print(st.session_state.messages)
	if st.session_state["message_GPT"] == None:
		msg, message_GPT = get_response(st.session_state.messages[-1]['content'])
	else:
		msg, message_GPT = get_response(st.session_state.messages[-1]['content'], st.session_state["message_GPT"], st.session_state.messages[-2]['content'])
	st.session_state["message_GPT"] = message_GPT
	if is_safety == True:
		safety = check_for_unsafe_content(msg, safety_threshold)
	if safety == True:
		st.session_state.messages.append({"role": "assistant", "content": msg})
		st.chat_message("assistant").write(msg)
	else:
		st.chat_message("assistant").write(f"Not safety message: {str(safety)}")

