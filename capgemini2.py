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
        
    def configurar_email_destino(self):
        """
        Permite ao usuário configurar o e-mail de destino
        """
        print("\n" + "="*50)
        print("CONFIGURAÇÃO DO E-MAIL DE DESTINO")
        print("="*50)
        
        while True:
            print("\nPara qual e-mail você quer enviar o resultado da análise?")
            print("1. E-mail padrão (lucaslmonteiro68@gmail.com)")
            print("2. Outro e-mail personalizado")
            
            try:
                opcao = input("\nEscolha uma opção (1-2): ").strip()
                
                if opcao == "1":
                    self.email_destino = "lucaslmonteiro68@gmail.com"
                    print(f"✓ E-mail de destino configurado: {self.email_destino}")
                    break
                elif opcao == "2":
                    while True:
                        email = input("\nDigite o e-mail de destino: ").strip()
                        if validar_email(email):
                            self.email_destino = email
                            print(f"✓ E-mail de destino configurado: {self.email_destino}")
                            break
                        else:
                            print("❌ Formato de e-mail inválido! Digite um e-mail válido.")
                    break
                else:
                    print("❌ Opção inválida. Digite 1 ou 2.")
                    
            except KeyboardInterrupt:
                print("\n\nOperação cancelada pelo usuário.")
                exit(0)
            except Exception as e:
                print(f"❌ Erro: {e}")
    
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
    
    def contar_palavras_chave(self, texto: str) -> Dict[str, int]:
        """
        Conta quantas palavras-chave de cada categoria aparecem no texto
        """
        texto_lower = texto.lower()
        contadores = {}
        
        for categoria, palavras in self.palavras_chave.items():
            contador = 0
            for palavra in palavras:
                padrao = r'\b' + re.escape(palavra.lower()) + r'\b'
                matches = re.findall(padrao, texto_lower)
                contador += len(matches)
            contadores[categoria] = contador
            
        return contadores
    
    def classificar_candidato(self, contadores: Dict[str, int]) -> Tuple[str, str]:
        """
        Classifica o candidato baseado nos contadores de palavras-chave
        """
        categorias_atingidas = {}
        for categoria, contador in contadores.items():
            if contador >= self.quantidade_minima:
                categorias_atingidas[categoria] = contador
        
        if "excelente" in categorias_atingidas:
            return "excelente", f"Excelente! Encontramos {categorias_atingidas['excelente']} palavras-chave da categoria mais alta."
        elif "bom" in categorias_atingidas:
            return "bom", f"Bom! Encontramos {categorias_atingidas['bom']} palavras-chave da categoria boa."
        elif "medio" in categorias_atingidas:
            return "medio", f"Médio. Encontramos {categorias_atingidas['medio']} palavras-chave da categoria média."
        else:
            return "ruim", "Não atingiu as expectativas iniciais. Nenhuma categoria foi atingida com a quantidade mínima de palavras-chave."
    
    def criar_mensagem_email(self, categoria: str, descricao: str, nome_arquivo: str) -> EmailMessage:
        """
        Cria a mensagem de e-mail com o resultado da análise
        """
        msg = EmailMessage()
        msg['Subject'] = "Resultado da análise do seu currículo"
        msg['From'] = self.email_remetente
        msg['To'] = self.email_destino
        
        corpo = f"""
        Análise do currículo: {nome_arquivo}
        
        Resultado: {categoria.upper()}
        
        {descricao}
        
        Este e-mail foi enviado automaticamente pelo sistema de análise de currículos.
        """
        
        msg.set_content(corpo)
        return msg
    
    def enviar_email(self, mensagem: EmailMessage) -> bool:
        """
        Envia o e-mail usando Gmail SMTP
        """
        if not self.email_destino:
            print("⚠️  E-mail de destino não configurado - pulando envio")
            return False
        
        try:
            print(f"📤 Enviando e-mail via {self.smtp_server}:{self.smtp_port}...")
            print(f"📧 De: {self.email_remetente}")
            print(f"📧 Para: {self.email_destino}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_remetente, self.senha_app)
                server.send_message(mensagem)
            
            print(f"✅ E-mail enviado com sucesso para {self.email_destino}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar e-mail: {str(e)}")
            return False
    
    def analisar_curriculo(self, caminho_pdf: str) -> Dict:
        """
        Analisa um currículo completo: extrai texto, classifica e envia e-mail
        """
        print(f"\n🔍 Analisando currículo: {caminho_pdf}")
        
        texto = self.extrair_texto_pdf(caminho_pdf)
        print(f"📄 Texto extraído: {len(texto)} caracteres")
        
        contadores = self.contar_palavras_chave(texto)
        print("\n📊 Contadores de palavras-chave:")
        for categoria, contador in contadores.items():
            print(f"  🏷️  {categoria}: {contador}")
        
        categoria, descricao = self.classificar_candidato(contadores)
        print(f"\n🏆 Classificação: {categoria.upper()}")
        print(f"📝 Descrição: {descricao}")
        
        nome_arquivo = os.path.basename(caminho_pdf)
        mensagem = self.criar_mensagem_email(categoria, descricao, nome_arquivo)
        
        if self.enviar_email(mensagem):
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
    print("🚀 ANALISADOR DE CURRÍCULOS PDF")
    print("=" * 50)
    print("📧 VERSÃO GMAIL - ENVIO REAL")
    print("=" * 50)
    print("💡 Durante a apresentação, alguém pode fornecer seu e-mail")
    print("💡 O programa enviará o e-mail REALMENTE via Gmail")
    print("=" * 50)
    
    analisador = AnalisadorCurriculo()
    analisador.configurar_email_destino()
    
    print("\n" + "="*50)
    print("SELECIONAR ARQUIVO PDF")
    print("="*50)
    
    while True:
        caminho_curriculo = input("\nDigite o caminho do arquivo PDF: ").strip()
        caminho_curriculo = caminho_curriculo.strip('"\'')
        
        if os.path.exists(caminho_curriculo):
            break
        else:
            print(f"❌ Arquivo não encontrado: {caminho_curriculo}")
            print("💡 Dica: Você pode arrastar o arquivo PDF para esta janela")
    
    resultado = analisador.analisar_curriculo(caminho_curriculo)
    
    print("\n" + "="*50)
    print("RESULTADO FINAL DA ANÁLISE")
    print("="*50)
    print(f"📁 Arquivo: {resultado['arquivo']}")
    print(f"🏆 Categoria: {resultado['categoria'].upper()}")
    print(f"📝 Descrição: {resultado['descricao']}")
    print(f"📧 E-mail enviado: {'Sim' if resultado['email_enviado'] else 'Não'}")
    
    if resultado['email_enviado']:
        print(f"📤 De: {analisador.email_remetente}")
        print(f"📥 Para: {analisador.email_destino}")
        print("\n🎉 E-mail enviado com sucesso!")
    else:
        print("\n💡 O e-mail não foi enviado, mas a análise foi concluída.")

if __name__ == "__main__":
    main()
