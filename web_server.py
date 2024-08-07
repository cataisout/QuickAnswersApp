import streamlit as st
import requests

API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

headers = {"Authorization": f"Bearer {st.secrets['API_TOKEN']}"}

st.set_page_config(page_title="QuickAnswers", layout="centered")

if 'ans' not in st.session_state:
    st.session_state['ans'] = ''



@st.cache_resource(show_spinner=False)

def load_model():
   
    requests.post(API_URL, headers=headers)

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def execute_query(context, question):

    output = query({
	"inputs": {
	"question": question,
	"context": context
            },
                })

    answer = output['answer']

    st.session_state['ans'] = answer


header = st.container()
input = st.container()
output = st.container()

with st.spinner('Initiating app...'):
    load_model()

with header:
    st.title('QuickAnswers - Perguntas e respostas ágeis com IA')
    st.header('Otimize sua leitura')
    st.write('<div style="text-align:justify">' +
             '''Utilize a caixa contexto para inserir algum texto no qual busque uma informação rápida, e sua pergunta na caixa de perguntas.''' + '<div>', unsafe_allow_html=True)

with input:
    st.write('')
    context = st.text_area('Insira texto para busca:')
    question = st.text_input('Sua pergunta:')
    st.button('Resposta', on_click=execute_query,
              args=(context, question))

with output:
    st.write('')
    st.code(st.session_state['ans'])