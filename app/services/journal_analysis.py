import json

from openai import OpenAI

from app.settings import settings

PROMPT_VERSION = 'journal_analysis_v1'

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url='https://api.groq.com/openai/v1',
)


def analyze_journal_entry(content: str) -> dict:
    response = client.chat.completions.create(
        model=settings.GROQ_LLM_MODEL,
        messages=[
            {
                'role': 'system',
                'content': (
                    'Você é um assistente de apoio clínico para psicólogos.'
                    'Sua função é estruturar relatos de pacientes sem diagnosticar,'
                    'sem prescrever tratamento e sem substituir o profissional.'
                    'Responda apenas em JSON válido.'
                ),
            },
            {
                'role': 'user',
                'content': f"""
Analise o relato abaixo e retorne apenas um JSON com estes campos:

{{
    "summary": "resumo breve do relato",
    "main_emotion": "emoção principal percebida",
    "trigger": "possível gatilho ou situação",
    "intensity": "baixa, média ou alta",
    "cognitive_patterns": "possíveis padrões cognitivos/emocionais observados",
    "behavior": "comportamento ou reação descrita",
    "clinical_notes": "observações úteis para o psicólogo",
    "suggested_focus": "possíveis pontos para explorar na sessão"
}}

Para o campo "cognitive_patterns", identifique padrões como:
- ruminação
- pensamento catastrófico
- autocobrança
- perfeccionismo
- medo de julgamento
- necessidade de aprovação
- culpa
- insegurança
- evitação
- ansiedade antecipatória

Se não houver informação suficiente, use null.
Os campos summary e main_emotion são obrigatórios.
Se não houver emoção clara, use "neutra" ou "não identificada".

Não faça diagnóstico.
Não prescreva tratamento.
Não substitua a avaliação do psicólogo.

Relato:
{content}
""",
            },
        ],
        temperature=0.2,
        response_format={'type': 'json_object'},
    )

    result = response.choices[0].message.content

    if result is None:
        raise ValueError('Empty AI response')

    return json.loads(result)
