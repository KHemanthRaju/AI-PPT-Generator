import json
import uuid
import boto3
import streamlit as st
from botocore.exceptions import ClientError
from botocore.eventstream import EventStreamError

agent_id = "XXXXXXXXXX" # Paste your agent ID here
agent_alias_id = "XXXXXXXXXX" # Paste your alias ID here

def initialize_session():
    """Initialize session settings"""
    if "client" not in st.session_state:
        st.session_state.client = boto3.client("bedrock-agent-runtime")
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = None
    
    return st.session_state.client, st.session_state.session_id, st.session_state.messages

def display_chat_history(messages):
    """Display chat history"""
    st.title("PowerPoint Creator and Emailer")
    st.text("I'll search the web, create slides, and email them to you!")
    
    for message in messages:
        with st.chat_message(message['role']):
            st.markdown(message['text'])

def handle_trace_event(event):
    """Process trace events"""
    if "orchestrationTrace" not in event["trace"]["trace"]:
        return
    
    trace = event["trace"]["trace"]["orchestrationTrace"]
    
    # Display "Model Input" trace
    if "modelInvocationInput" in trace:
        with st.expander("🤔 Thinking...", expanded=False):
            input_trace = trace["modelInvocationInput"]["text"]
            try:
                st.json(json.loads(input_trace))
            except:
                st.write(input_trace)
    
    # Display "Model Output" trace
    if "modelInvocationOutput" in trace:
        output_trace = trace["modelInvocationOutput"]["rawResponse"]["content"]
        with st.expander("💡 Thoughts organized", expanded=False):
            try:
                thinking = json.loads(output_trace)["content"][0]["text"]
                if thinking:
                    st.write(thinking)
                else:
                    st.write(json.loads(output_trace)["content"][0])
            except:
                st.write(output_trace)
    
    # Display "Rationale" trace
    if "rationale" in trace:
        with st.expander("✅ Decided on next action", expanded=True):
            st.write(trace["rationale"]["text"])
    
    # Display "Tool Invocation" trace
    if "invocationInput" in trace:
        invocation_type = trace["invocationInput"]["invocationType"]
                
        if invocation_type == "ACTION_GROUP":
            with st.expander("💻 Executing Lambda...", expanded=False):
                st.write(trace['invocationInput']['actionGroupInvocationInput'])
    
    # Display "Observation" trace
    if "observation" in trace:
        obs_type = trace["observation"]["type"]
        
        if obs_type == "ACTION_GROUP":
            with st.expander(f"💻 Retrieved Lambda execution results", expanded=False):
                st.write(trace["observation"]["actionGroupInvocationOutput"]["text"])
                
def invoke_bedrock_agent(client, session_id, prompt):
    """Invoke Bedrock agent"""
    return client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        enableTrace=True,
        inputText=prompt,
    )

def handle_agent_response(response, messages):
    """Process agent responses"""
    with st.chat_message("assistant"):
        for event in response.get("completion"):
            if "trace" in event:
                handle_trace_event(event)
            
            if "chunk" in event:
                answer = event["chunk"]["bytes"].decode()
                st.write(answer)
                messages.append({"role": "assistant", "text": answer})

def show_error_popup(exeption):
    """Display error popup"""
    if exeption == "throttlingException":
        error_message = "【ERROR】Bedrock model load seems high. Please wait about a minute, reload the browser, and try again 🙏 (If issues persist, consider changing models or [requesting a service quota increase](https://aws.amazon.com/jp/blogs/news/generative-ai-amazon-bedrock-handling-quota-problems/))"
    st.error(error_message)

def main():
    """Main application processing"""
    client, session_id, messages = initialize_session()
    display_chat_history(messages)
    
    if prompt := st.chat_input("Example: Research the latest Bedrock use cases in Japan"):
        messages.append({"role": "human", "text": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            response = invoke_bedrock_agent(client, session_id, prompt)
            handle_agent_response(response, messages)
            
        except (EventStreamError, ClientError) as e:
            if "throttlingException" in str(e):
                show_error_popup("throttlingException")
            else:
                raise e

if __name__ == "__main__":
    main()