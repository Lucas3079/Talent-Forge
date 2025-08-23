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

class AnalisadorCurriculo:
    def __init__(self):
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
        msg['Subject'] = "Resultado da analise do seu curriculo"
        msg['From'] = self.email_remetente
        msg['To'] = self.email_destino
        
        corpo = f"""
        Analise do curriculo: {nome_arquivo}
        
        Resultado: {categoria.upper()}
        
        {descricao}
        
        Este e-mail foi enviado automaticamente pelo sistema de analise de curriculos.
        """
        
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
        print(f"Analisando curriculo: {caminho_pdf}")
        
        # Extrai texto do PDF
        texto = self.extrair_texto_pdf(caminho_pdf)
        print(f"Texto extraido: {len(texto)} caracteres")
        
        # Extrai e-mail automaticamente do currículo
        email_encontrado = extrair_email_do_texto(texto)
        if email_encontrado:
            self.email_destino = email_encontrado
            print(f"E-mail encontrado no curriculo: {self.email_destino}")
        else:
            print("AVISO: Nenhum e-mail encontrado no curriculo")
            print("DICA: O resultado da analise sera apenas exibido no terminal")
        
        # Conta palavras-chave
        contadores = self.contar_palavras_chave(texto)
        print("\nANALISE DETALHADA DAS PALAVRAS-CHAVE:")
        print("=" * 60)
        
        for categoria, dados in contadores.items():
            print(f"\nCATEGORIA: {categoria.upper()}")
            print(f"  Contador: {dados['contador']}")
            if dados['palavras_encontradas']:
                print(f"  CARACTERISTICAS ENCONTRADAS: {', '.join(dados['palavras_encontradas'])}")
            else:
                print(f"  CARACTERISTICAS ENCONTRADAS: Nenhuma")
        
        # Classifica o candidato
        categoria, descricao = self.classificar_candidato(contadores)
        print(f"\nCLASSIFICACAO FINAL: {categoria.upper()}")
        print(f"Descricao: {descricao}")
        
        # Mostra resumo das características que determinaram a classificação
        print(f"\nRESUMO DA CLASSIFICACAO:")
        print("-" * 40)
        if categoria != "ruim":
            dados_categoria = contadores[categoria]
            if dados_categoria['palavras_encontradas']:
                print(f"As seguintes caracteristicas foram encontradas:")
                for palavra in dados_categoria['palavras_encontradas']:
                    print(f"  - {palavra}")
            else:
                print("Nenhuma caracteristica especifica foi encontrada.")
        else:
            print("Nenhuma categoria atingiu o minimo de 2 caracteristicas.")
            print("Caracteristicas encontradas em cada categoria:")
            for cat, dados in contadores.items():
                if dados['palavras_encontradas']:
                    print(f"  {cat}: {', '.join(dados['palavras_encontradas'])}")
                else:
                    print(f"  {cat}: Nenhuma")
        
        # Cria e envia e-mail (se e-mail foi encontrado)
        nome_arquivo = os.path.basename(caminho_pdf)
        mensagem = self.criar_mensagem_email(categoria, descricao, nome_arquivo)
        
        if self.email_destino and self.enviar_email(mensagem):
            resultado = {
                "arquivo": caminho_pdf,
                "categoria": categoria,
                "descricao": descricao,
                "contadores": contadores,
                "email_enviado": True
            }
        else:
            resultado = {
                "arquivo": caminho_pdf,
                "categoria": categoria,
                "descricao": descricao,
                "contadores": contadores,
                "email_enviado": False
            }
        
        return resultado

def main():
    """
    Função principal
    """
    print("ANALISADOR DE CURRICULOS PDF")
    print("=" * 50)
    print("VERSAO GMAIL - ENVIO AUTOMATICO")
    print("=" * 50)
    print("DICA: O programa analisa o curriculo e extrai o e-mail automaticamente")
    print("DICA: O resultado e enviado para o e-mail encontrado no curriculo")
    print("=" * 50)
    
    # Seleciona arquivo PDF primeiro
    print("\n" + "="*50)
    print("SELECIONAR ARQUIVO PDF")
    print("="*50)
    
    while True:
        caminho_curriculo = input("\nDigite o caminho do curriculo PDF: ").strip()
        caminho_curriculo = caminho_curriculo.strip('"\'')
        
        if os.path.exists(caminho_curriculo):
            break
        else:
            print(f"ERRO: Arquivo nao encontrado: {caminho_curriculo}")
            print("DICA: Voce pode arrastar o arquivo PDF para esta janela")
    
    # Cria o analisador e analisa o currículo
    analisador = AnalisadorCurriculo()
    resultado = analisador.analisar_curriculo(caminho_curriculo)
    
    # Mostra resultado final
    print("\n" + "="*50)
    print("RESULTADO FINAL DA ANALISE")
    print("="*50)
    print(f"Arquivo: {resultado['arquivo']}")
    print(f"Categoria: {resultado['categoria'].upper()}")
    print(f"Descricao: {resultado['descricao']}")
    print(f"E-mail enviado: {'Sim' if resultado['email_enviado'] else 'Nao'}")
    
    if resultado['email_enviado']:
        print(f"De: {analisador.email_remetente}")
        print(f"Para: {analisador.email_destino}")
        print("\nE-mail enviado com sucesso!")
    else:
        print("\nDICA: O e-mail nao foi enviado, mas a analise foi concluida.")

if __name__ == "__main__":
    main()
