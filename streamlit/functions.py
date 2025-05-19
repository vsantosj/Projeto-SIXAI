import boto3
import json
import uuid
from datetime import date
import os

PROFILE_NAME = os.environ.get("AWS_PROFILE", "sixai")


def get_boto3_client(service_name, region_name='us-east-1', profile_name='sixai'):
    """
    Retorna um cliente do serviço AWS especificado.
    
    Tenta usar o perfil especificado para desenvolvimento local primeiro.
    Se falhar, assume que está em uma instância EC2 e usa as credenciais do IAM role.
    """
    try:
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        client = session.client(service_name)
        if service_name == 'sts':
            caller_identity = client.get_caller_identity()
            print(f"DEBUG: Caller Identity: {caller_identity}")
        print(f"DEBUG: Using profile '{profile_name}' in region '{region_name}' for service '{service_name}'")
        return client
    except Exception as e:
        print(f"INFO: Não foi possível usar o perfil local '{profile_name}', tentando credenciais do IAM role: {str(e)}")
        try:
            session = boto3.Session(region_name=region_name)
            client = session.client(service_name)
            caller_identity = client.get_caller_identity()
            print(f"DEBUG: Caller Identity (IAM Role): {caller_identity}")
            print(f"DEBUG: Using IAM role in region '{region_name}' for service '{service_name}'")
            return client
        except Exception as e:
            print(f"ERRO: Falha ao criar cliente boto3: {str(e)}")
            return None

# ALTERAR
def generate_chat_prompt(user_message, conversation_history=None, context=""):
    current_date = date.today()
    """
    Gera um prompt de chat completo com histórico de conversa e contexto opcional.
    """
    system_prompt = f"""
Hoje é dia {current_date.strftime('%d-%m-%y')} - você é atendente da empresa SIX AI.Objetivo: Sua responsabilidade é atender os usuários e orientar para que tenha
 - informações - meteorológicas de acordo com o seu histórico de base de dados. (Não acesse a internet, quero dados históricos).Formato: respostas diretas em tópicos 
 e frases com máximo em 2 linhas.GUARDRAIL: Invente um nome, responda de forma coloquial e dinâmica. Caso o usuário solicite algo que seja fora do assunto, informe-o educadamente sobre
  o seu objetivo. FEW-SHOT: O nosso objetivo é ínformar a possibilidade de alagamentos em cidades. Queremos que o usuário informe a cidade dele. Pergunte uma pergunta de cada vez, 
  seja sucinto.FACT-CHECKING: baseie-se em fontes como inmet e instituições similares, se for o caso, use a API fornecidas por eles.
    """

    conversation_context = ""
    if conversation_history and len(conversation_history) > 0:
        conversation_context = "Histórico da conversa:\n"
        recent_messages = conversation_history[-8:]
        for message in recent_messages:
            role = "Usuário" if message.get('role') == 'user' else "Assistente"
            conversation_context += f"{role}: {message.get('content')}\n"
        conversation_context += "\n"

    full_prompt = f"{system_prompt}\n\n{conversation_context}{context}Usuário: {user_message}\n\nAssistente:"

    return full_prompt


# ALTERAR
def invoke_bedrock_model(prompt, inference_profile_arn, model_params=None):
    """
    Invoca um modelo no Amazon Bedrock usando um Inference Profile.
    """
    if model_params is None:
        model_params = {
            "temperature": 0.6,
            "top_p": 0.7,
            "top_k": 50,
            "max_tokens": 2048
        }

    bedrock_runtime = get_boto3_client('bedrock-runtime')

    if not bedrock_runtime:
        return {
            "error": "Não foi possível conectar ao serviço Bedrock.",
            "answer": "Erro de conexão com o modelo.",
            "sessionId": str(uuid.uuid4())
        }

    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": model_params["max_tokens"],
            "temperature": model_params["temperature"],
            "top_p": model_params["top_p"],
            "top_k": model_params["top_k"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        })

        response = bedrock_runtime.invoke_model(
            modelId=inference_profile_arn,  # Usando o ARN do Inference Profile
            body=body,
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response['body'].read())
        answer = response_body['content'][0]['text']

        return {
            "answer": answer,
            "sessionId": str(uuid.uuid4())
        }

    except Exception as e:
        print(f"ERRO: Falha na invocação do modelo Bedrock: {str(e)}")
        print(f"ERRO: Exception details: {e}")
        return {
            "error": str(e),
            "answer": f"Ocorreu um erro ao processar sua solicitação: {str(e)}. Por favor, tente novamente.",
            "sessionId": str(uuid.uuid4())
        }
