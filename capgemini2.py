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
        
        # Configurações das palavras-chave por categoria
        self.palavras_chave = {
            "excelente": ["SAP", "PP", "PM", "QM", "Mapeamento"],
            "bom": ["Integração", "ERP", "TOTVS"],
            "medio": ["Oracle", "Excel"]
        }
        
        # Configurações de e-mail
        self.email_destino = None
        self.quantidade_minima = 2
        
        # CONFIGURAÇÃO GMAIL
        self.email_remetente = "lucaslmonteiro68@gmail.com"
        self.senha_app = "hbix rxyg ceby ajrx"
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
    
    def contar_palavras_chave(self, texto: str) -> Dict[str, Dict]:
        """
        Conta quantas palavras-chave de cada categoria aparecem no texto
        Retorna: {categoria: {"contador": int, "palavras_encontradas": [str]}}
        """
        texto_lower = texto.lower()
        resultado = {}
        
        for categoria, palavras in self.palavras_chave.items():
            contador = 0
            palavras_encontradas = []
            
            for palavra in palavras:
                padrao = r'\b' + re.escape(palavra.lower()) + r'\b'
                matches = re.findall(padrao, texto_lower)
                if matches:
                    contador += len(matches)
                    palavras_encontradas.append(palavra)
            
            resultado[categoria] = {
                "contador": contador,
                "palavras_encontradas": palavras_encontradas
            }
            
        return resultado
    
    def classificar_candidato(self, contadores: Dict[str, Dict]) -> Tuple[str, str]:
        """
        Classifica o candidato baseado nos contadores de palavras-chave
        """
        categorias_atingidas = {}
        for categoria, dados in contadores.items():
            if dados["contador"] >= self.quantidade_minima:
                categorias_atingidas[categoria] = dados
        
        if "excelente" in categorias_atingidas:
            return "excelente", f"Excelente! Encontramos {categorias_atingidas['excelente']['contador']} palavras-chave da categoria mais alta."
        elif "bom" in categorias_atingidas:
            return "bom", f"Bom! Encontramos {categorias_atingidas['bom']['contador']} palavras-chave da categoria boa."
        elif "medio" in categorias_atingidas:
            return "medio", f"Medio. Encontramos {categorias_atingidas['medio']['contador']} palavras-chave da categoria media."
        else:
            return "ruim", "Nao atingiu as expectativas iniciais. Nenhuma categoria foi atingida com a quantidade minima de palavras-chave."
    
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

Estamos muito felizes com sua candidatura. Seu perfil apresentou excelente compatibilidade e, por isso, você já está avançando diretamente para a terceira fase do processo seletivo.

Em breve informaremos os detalhes.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        elif categoria == "bom":
            corpo = f"""Prezado(a) {self.nome_candidato},

Após avaliação de seu perfil, verificamos uma boa compatibilidade com a posição em aberto. Por isso, você está convidado(a) a participar da segunda fase do processo seletivo.

Em breve compartilharemos os próximos passos.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        elif categoria == "medio":
            corpo = f"""Prezado(a) {self.nome_candidato},

Obrigado por participar do processo seletivo. Embora seu perfil apresente apenas uma compatibilidade parcial com a vaga, você foi selecionado(a) para seguir para a segunda fase.

Em breve entraremos em contato com as próximas instruções.

Atenciosamente,
{self.nome_recrutador}
Capgemini"""
        
        else:  # categoria == "ruim"
            corpo = f"""Prezado(a) {self.nome_candidato},

Agradecemos sua participação em nosso processo seletivo. Após análise, identificamos que seu perfil não apresenta compatibilidade suficiente com a vaga no momento.

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
        if categoria != "ruim":
            dados_categoria = contadores[categoria]
            if dados_categoria['palavras_encontradas']:
                print(f"Caracteristicas: {', '.join(dados_categoria['palavras_encontradas'])}")
        else:
            # Para candidatos ruins, mostra o que foi encontrado em cada categoria
            encontradas = []
            for cat, dados in contadores.items():
                if dados['palavras_encontradas']:
                    encontradas.append(f"{cat}: {', '.join(dados['palavras_encontradas'])}")
            if encontradas:
                print(f"Encontrado: {' | '.join(encontradas)}")
        
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
    print("ANALISADOR DE CURRICULOS PDF")
    print("=" * 40)
    print("VERSAO GMAIL - ENVIO AUTOMATICO")
    print("=" * 40)
    
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
        print(f"{nome_candidato} ({categoria}) - {arquivo}")
    
    # Mostra resumo final
    total_analisados = len(resultados_analise)
    total_emails = sum(1 for r in resultados_analise if r['email_enviado'])
    print(f"\nProcesso finalizado: {total_analisados} curriculos analisados e {total_emails} emails enviados")

if __name__ == "__main__":
    main()
