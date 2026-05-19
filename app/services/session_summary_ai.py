from openai import OpenAI

from app.settings import settings

client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url='https://api.groq.com/openai/v1',
)


def generate_session_summary(entries: list[dict]) -> str:
    formatted_entries = '\n\n'.join([
        f"""
Data: {entry['date_created']}
Resumo: {entry['summary']}
Emoção principal: {entry['main_emotion']}
Gatilho: {entry['trigger']}
Padrões cognitivos: {entry['cognitive_patterns']}
Comportamento: {entry['behavior']}
"""
        for entry in entries
    ])

    response = client.chat.completions.create(
        model=settings.GROQ_LLM_MODEL,
        messages=[
            {
                'role': 'system',
                'content': (
                    'Você é um assistente de apoio clínico para psicólogos. '
                    'Sua função é gerar um resumo narrativo pré-sessão '
                    'baseado em relatos estruturados de pacientes. '
                    'Não faça diagnóstico. '
                    'Não prescreva tratamento. '
                    'Apenas organize padrões emocionais e comportamentais.'
                ),
            },
            {
                'role': 'user',
                'content': f"""
Gere um resumo clínico narrativo objetivo e conciso para auxiliar a psicóloga antes da sessão.

Objetivo:
- identificar padrões emocionais recorrentes
- identificar gatilhos frequentes
- identificar padrões cognitivos
- resumir comportamentos observados
- sugerir possíveis focos terapêuticos

Regras:
- produza uma visão consolidada do período
- não reescreva cada relato individualmente
- seja objetivo e profissional
- utilize linguagem clínica neutra
- refira-se apenas como "paciente"
- não assuma gênero
- não faça diagnóstico
- não prescreva tratamento
- não invente informações
- evite inferências causais sem evidência explícita
- evite repetições excessivas
- não utilize markdown
- não utilize títulos
- limite a resposta a no máximo 4 parágrafos

Relatos estruturados:

{formatted_entries}
""",
            },
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError('Empty AI response')

    return content
