#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisador de Currículos PDF
Analisa currículos baseado em palavras-chave e envia resultado por e-mail
"""

import pdfplumber
import smtplib
from email.message import EmailMessage
import os
from typing import Dict, Tuple
import re

def validar_email(email: str) -> bool:
    """
    Valida se o formato do e-mail está correto
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(padrao, email) is not None

def extrair_email_do_texto(texto: str) -> str:
    """
    Extrai o primeiro e-mail encontrado no texto do currículo
    """
    padrao_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(padrao_email, texto)
    
    if matches:
        return matches[0]  # Retorna o primeiro e-mail encontrado
    return None

def extrair_nome_candidato(texto: str) -> str:
    """
    Extrai o nome do candidato da primeira linha do currículo
    Retorna apenas o primeiro nome (primeira palavra até o primeiro espaço)
    """
    linhas = texto.strip().split('\n')
    if linhas:
        primeira_linha = linhas[0].strip()
        # Remove caracteres especiais e pega apenas a primeira palavra
        nome_limpo = re.sub(r'[^\w\s]', '', primeira_linha)
        palavras = nome_limpo.split()
        if palavras:
            return palavras[0]  # Retorna apenas o primeiro nome
    return "Candidato"

class AnalisadorCurriculo:
    def __init__(self, nome_recrutador: str):
        # Informações do recrutador
        self.nome_recrutador = nome_recrutador
        
        # Configurações das palavras-chave unificadas (português e inglês)
        self.palavras_chave = [
            # Tecnologias Core
            "Python", "Backend", "APIs", "REST", "GraphQL", 
            "LLM", "Large Language Models", "Language Models",
            
            # IA e LLM
            "Agentes LLM", "LLM Agents", "orquestração", "orchestration",
            "Pipelines de busca", "Search Pipelines", "Recuperação de documentos", "Document Retrieval",
            "Embeddings", "vetorização", "vectorization", "vector embeddings",
            
            # Git e Versionamento
            "Git", "branching", "pull requests", "revisão de código", "code review",
            "merge", "commit", "repository", "repositório",
            
            # Metodologias e Ferramentas
            "Jira", "Scrum", "Kanban", "metodologias ágeis", "agile methodologies",
            "sprint", "standup", "daily standup", "retrospective", "retrospectiva",
            
            # Idiomas
            "Inglês avançado", "Advanced English", "Inglês fluente", "Fluent English", 
            "Inglês", "English", "Inglês técnico", "Technical English",
            
            # Frontend e DevOps
            "React", "Next.js", "DevOps", "Containers", "Docker", "Kubernetes",
            "CI/CD", "Continuous Integration", "Continuous Deployment", "Cloud", "AWS", "Azure", "GCP",
            
            # Ferramentas LLM
            "LangChain", "LlamaIndex", "Multi-agente", "Multi-agent",
            "Processamento de documentos", "Document Processing", "Document Processing",
            "Busca multilíngue", "Multilingual Search", "Cross-language Search",
            "Webhooks", "Prompts", "prompt engineering", "outputs estruturados", "structured outputs",
            "chamadas de função", "function calling", "function calls"
        ]
        
        # Configurações de e-mail
        self.email_destino = None
        self.quantidade_minima = 2
        
        # CONFIGURAÇÃO GMAIL
        self.email_remetente = "capgeminitalentforge@gmail.com"
        self.senha_app = "hxdr aeov ufsu sxau"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
        # Informações do candidato atual
        self.nome_candidato = None
        
    def extrair_texto_pdf(self, caminho_pdf: str) -> str:
        """
        Extrai texto de um arquivo PDF usando pdfplumber
        """
        try:
            with pdfplumber.open(caminho_pdf) as pdf:
                texto_completo = ""
                for pagina in pdf.pages:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina:
                        texto_completo += texto_pagina + " "
                return texto_completo.strip()
        except Exception as e:
            raise Exception(f"Erro ao ler PDF {caminho_pdf}: {str(e)}")
    
    def contar_palavras_chave(self, texto: str) -> Dict[str, any]:
        """
        Conta quantas palavras-chave aparecem no texto, agrupando sinônimos
        Retorna: {"contador": int, "palavras_encontradas": [str]}
        """
        texto_lower = texto.lower()
        
        # Grupos de sinônimos (português e inglês)
        grupos_sinonimos = {
            # Tecnologias Core
            "Python": ["python"],
            "Backend": ["backend", "back-end"],
            "APIs": ["apis", "api", "rest", "graphql"],
            "LLM": ["llm", "large language models", "language models"],
            
            # IA e LLM
            "Agentes LLM": ["agentes llm", "llm agents"],
            "Orquestração": ["orquestração", "orchestration"],
            "Pipelines de busca": ["pipelines de busca", "search pipelines"],
            "Recuperação de documentos": ["recuperação de documentos", "document retrieval"],
            "Embeddings": ["embeddings", "vetorização", "vectorization", "vector embeddings"],
            
            # Git e Versionamento
            "Git": ["git", "branching", "pull requests", "revisão de código", "code review", "merge", "commit"],
            "Repository": ["repository", "repositório"],
            
            # Metodologias e Ferramentas
            "Jira": ["jira"],
            "Scrum": ["scrum", "sprint", "standup", "daily standup"],
            "Kanban": ["kanban"],
            "Metodologias ágeis": ["metodologias ágeis", "agile methodologies", "retrospective", "retrospectiva"],
            
            # Idiomas
            "Inglês": ["inglês", "english", "inglês avançado", "advanced english", "inglês fluente", "fluent english", "inglês técnico", "technical english"],
            
            # Frontend e DevOps
            "React": ["react"],
            "Next.js": ["next.js", "nextjs"],
            "DevOps": ["devops"],
            "Containers": ["containers", "docker", "kubernetes"],
            "CI/CD": ["ci/cd", "continuous integration", "continuous deployment"],
            "Cloud": ["cloud", "aws", "azure", "gcp"],
            
            # Ferramentas LLM
            "LangChain": ["langchain"],
            "LlamaIndex": ["llamaindex"],
            "Multi-agente": ["multi-agente", "multi-agent"],
            "Processamento de documentos": ["processamento de documentos", "document processing"],
            "Busca multilíngue": ["busca multilíngue", "multilingual search", "cross-language search"],
            "Webhooks": ["webhooks"],
            "Prompts": ["prompts", "prompt engineering"],
            "Outputs estruturados": ["outputs estruturados", "structured outputs"],
            "Chamadas de função": ["chamadas de função", "function calling", "function calls"]
        }
        
        caracteristicas_encontradas = set()  # Usa set para evitar duplicatas
        contador_total = 0
        
        for caracteristica_principal, sinonimos in grupos_sinonimos.items():
            encontrou = False
            for sinonimo in sinonimos:
                padrao = r'\b' + re.escape(sinonimo.lower()) + r'\b'
                if re.search(padrao, texto_lower):
                    encontrou = True
                    break
            
            if encontrou:
                caracteristicas_encontradas.add(caracteristica_principal)
                contador_total += 1
        
        return {
            "contador": contador_total,
            "palavras_encontradas": list(caracteristicas_encontradas)
        }
    
    def classificar_candidato(self, contadores: Dict[str, any]) -> Tuple[str, str]:
        """
        Classifica o candidato baseado na quantidade total de características encontradas
        """
        total_caracteristicas = contadores["contador"]
        
        if total_caracteristicas > 8:
            return "excelente", f"Excelente! Encontramos {total_caracteristicas} características compatíveis com a vaga. Você está no nível mais alto da hierarquia."
        elif total_caracteristicas >= 6:
            return "bom", f"Bom! Encontramos {total_caracteristicas} características compatíveis com a vaga. Você está no segundo nível da hierarquia."
        elif total_caracteristicas >= 3:
            return "medio", f"Médio. Encontramos {total_caracteristicas} características compatíveis com a vaga. Você está no terceiro nível da hierarquia."
        else:
            return "ruim", f"Encontramos apenas {total_caracteristicas} características compatíveis. Você está no nível mais baixo da hierarquia."
    
    def criar_mensagem_email(self, categoria: str, descricao: str, nome_arquivo: str) -> EmailMessage:
        """
        Cria a mensagem de e-mail com o resultado da análise
        """
        msg = EmailMessage()
        msg['Subject'] = f"Resultado da analise do seu curriculo - {self.nome_recrutador}"
        msg['From'] = self.email_remetente
        msg['To'] = self.email_destino
        
        # Mensagens personalizadas por categoria
        if categoria == "excelente":
            corpo = f"""Prezado(a) {self.nome_candidato},

PARABÉNS! Você está no NÍVEL EXCELENTE da hierarquia de candidatos!

Seu perfil apresentou excelente compatibilidade com nossa vaga de desenvolvimento com foco em LLM e IA.

Você está avançando diretamente para a terceira fase do processo seletivo.

Em breve nossa equipe entrará em contato.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        elif categoria == "bom":
            corpo = f"""Prezado(a) {self.nome_candidato},

BOA NOTÍCIA! Você está no NÍVEL BOM da hierarquia de candidatos!

Seu perfil apresentou boa compatibilidade com nossa vaga de desenvolvimento.

Você está convidado(a) para a segunda fase do processo seletivo.

Em breve compartilharemos os próximos passos.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        elif categoria == "medio":
            corpo = f"""Prezado(a) {self.nome_candidato},

INFORMAÇÃO IMPORTANTE! Você está no NÍVEL MÉDIO da hierarquia de candidatos!

Seu perfil apresentou compatibilidade parcial com nossa vaga de desenvolvimento com IA.

Você foi selecionado(a) para a segunda fase do processo seletivo.

Em breve entraremos em contato.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        else:  # categoria == "ruim"
            corpo = f"""Prezado(a) {self.nome_candidato},

INFORMAÇÃO IMPORTANTE! Você está no NÍVEL RUIM da hierarquia de candidatos!

Agradecemos sua participação em nosso processo seletivo para a vaga de desenvolvimento com foco em LLM e IA.

Seu perfil não apresentou compatibilidade suficiente com os requisitos técnicos da posição.

Desejamos sucesso em sua trajetória profissional.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        msg.set_content(corpo)
        return msg
    
    def enviar_email(self, mensagem: EmailMessage) -> bool:
        """
        Envia o e-mail usando Gmail SMTP
        """
        if not self.email_destino:
            print("AVISO: E-mail de destino nao configurado - pulando envio")
            return False
        
        try:
            print(f"Enviando e-mail via {self.smtp_server}:{self.smtp_port}...")
            print(f"De: {self.email_remetente}")
            print(f"Para: {self.email_destino}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_remetente, self.senha_app)
                server.send_message(mensagem)
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar e-mail: {str(e)}")
            return False
    
    def analisar_curriculo(self, caminho_pdf: str) -> Dict:
        """
        Analisa um currículo completo: extrai texto, classifica e envia e-mail
        """
        print(f"\n{'='*50}")
        print(f"ANALISANDO: {os.path.basename(caminho_pdf)}")
        print(f"{'='*50}")
        
        # Extrai texto do PDF
        texto = self.extrair_texto_pdf(caminho_pdf)
        
        # Extrai nome do candidato
        self.nome_candidato = extrair_nome_candidato(texto)
        print(f"Candidato: {self.nome_candidato}")
        
        # Extrai e-mail automaticamente do currículo
        email_encontrado = extrair_email_do_texto(texto)
        if email_encontrado:
            self.email_destino = email_encontrado
            print(f"E-mail: {self.email_destino}")
        else:
            print("AVISO: E-mail nao encontrado")
            self.email_destino = None
        
        # Conta palavras-chave
        contadores = self.contar_palavras_chave(texto)
        
        # Classifica o candidato
        categoria, descricao = self.classificar_candidato(contadores)
        print(f"Classificacao: {categoria.upper()}")
        
        # Mostra características encontradas
        if contadores['palavras_encontradas']:
            print(f"Caracteristicas encontradas: {', '.join(contadores['palavras_encontradas'])}")
        print(f"Total de caracteristicas unicas: {contadores['contador']}")
        print(f"Nota: Sinonimos em portugues e ingles sao contados como uma unica caracteristica")
        
        # Cria e envia e-mail (se e-mail foi encontrado)
        nome_arquivo = os.path.basename(caminho_pdf)
        mensagem = self.criar_mensagem_email(categoria, descricao, nome_arquivo)
        
        if self.email_destino and self.enviar_email(mensagem):
            resultado = {
                "arquivo": caminho_pdf,
                "categoria": categoria,
                "descricao": descricao,
                "contadores": contadores,
                "email_enviado": True,
                "nome_candidato": self.nome_candidato
            }
        else:
            resultado = {
                "arquivo": caminho_pdf,
                "categoria": categoria,
                "descricao": descricao,
                "contadores": contadores,
                "email_enviado": False,
                "nome_candidato": self.nome_candidato
            }
        
        return resultado

def main():
    """
    Função principal
    """
    print("ANALISADOR DE CURRICULOS PDF - VAGA DE DESENVOLVIMENTO IA")
    print("=" * 60)
    print("VERSAO GMAIL - ENVIO AUTOMATICO")
    print("=" * 60)
    
    # Captura nome do recrutador
    print("\n" + "="*40)
    print("IDENTIFICACAO")
    print("="*40)
    nome_recrutador = input("Nome do recrutador: ").strip()
    if not nome_recrutador:
        nome_recrutador = "Recrutador"
    
    # Captura pasta de currículos
    print("\n" + "="*40)
    print("SELECIONAR PASTA")
    print("="*40)
    while True:
        pasta_curriculos = input("Caminho da pasta com curriculos: ").strip()
        pasta_curriculos = pasta_curriculos.strip('"\'')
        
        if os.path.exists(pasta_curriculos) and os.path.isdir(pasta_curriculos):
            break
        else:
            print("ERRO: Pasta nao encontrada ou nao e uma pasta valida")
    
    # Busca todos os arquivos PDF na pasta
    pdfs_encontrados = []
    for arquivo in os.listdir(pasta_curriculos):
        if arquivo.lower().endswith('.pdf'):
            caminho_completo = os.path.join(pasta_curriculos, arquivo)
            pdfs_encontrados.append(caminho_completo)
    
    if not pdfs_encontrados:
        print("ERRO: Nenhum arquivo PDF encontrado na pasta")
        return
    
    print(f"Encontrados {len(pdfs_encontrados)} curriculos PDF")
    
    # Cria o analisador
    analisador = AnalisadorCurriculo(nome_recrutador)
    
    # Lista para armazenar resultados
    resultados_analise = []
    
    # Loop para analisar todos os currículos da pasta
    for i, caminho_pdf in enumerate(pdfs_encontrados, 1):
        print(f"\n{'='*50}")
        print(f"CURRICULO {i} DE {len(pdfs_encontrados)}")
        print(f"{'='*50}")
        
        # Analisa o currículo
        resultado = analisador.analisar_curriculo(caminho_pdf)
        resultados_analise.append(resultado)
        
        # Mostra resultado individual
        print(f"Status: {'E-mail enviado' if resultado['email_enviado'] else 'E-mail nao enviado'}")
    
    # Mostra lista de todos os candidatos com classificações
    print(f"\n{'='*60}")
    print("LISTA DE CANDIDATOS ANALISADOS")
    print(f"{'='*60}")
    
    for resultado in resultados_analise:
        nome_candidato = resultado['nome_candidato']
        categoria = resultado['categoria'].upper()
        arquivo = os.path.basename(resultado['arquivo'])
        total_caracteristicas = resultado['contadores']['contador']
        print(f"{nome_candidato} ({categoria}) - {total_caracteristicas} caracteristicas unicas - {arquivo}")
    
    # Mostra resumo final
    total_analisados = len(resultados_analise)
    total_emails = sum(1 for r in resultados_analise if r['email_enviado'])
    print(f"\nProcesso finalizado: {total_analisados} curriculos analisados e {total_emails} emails enviados")

if __name__ == "__main__":
    main()
