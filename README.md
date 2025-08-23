# Analisador de Currículos PDF

Este programa analisa currículos em PDF baseado em palavras-chave específicas e envia o resultado por e-mail automaticamente.

## Funcionalidades

- **Extração de texto**: Lê PDFs e extrai todo o conteúdo textual
- **Análise por palavras-chave**: Classifica candidatos baseado em listas de palavras específicas
- **Sistema de pontuação**: Requer mínimo de 2 palavras-chave para classificar em uma categoria
- **Envio automático de e-mail**: Envia resultado da análise para e-mail configurado
- **Classificação automática**: Excelente → Bom → Médio → Ruim
- **Seleção interativa de e-mail**: Escolha qual conta usar na hora de executar

## Categorias de Classificação

### 🏆 Excelente
- **Palavras-chave**: "SAP", "PP", "PM", "QM", "Mapeamento"
- **Critério**: 2 ou mais palavras encontradas

### 👍 Bom  
- **Palavras-chave**: "Integração", "ERP", "TOTVS"
- **Critério**: 2 ou mais palavras encontradas

### ⚖️ Médio
- **Palavras-chave**: "Oracle", "Excel"
- **Critério**: 2 ou mais palavras encontradas

### ❌ Ruim
- **Critério**: Não atinge 2 palavras em nenhuma categoria acima

## Instalação

### 1. Instalar Python
Certifique-se de ter Python 3.7+ instalado.

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar e-mail (se necessário)
Para usar o Gmail, você precisa:

1. **Ativar autenticação de 2 fatores** na sua conta Google
2. **Gerar uma senha de app**:
   - Vá em "Gerenciar sua Conta Google" → "Segurança"
   - "Verificação em duas etapas" → "Senhas de app"
   - Gere uma senha para "Email"

## Como Usar

### 1. Executar o programa
```bash
python capgemini2.py
```

### 2. Selecionar e-mail remetente
O programa oferece 5 opções:
- **Gmail**: Configuração automática para Gmail
- **Outlook/Hotmail**: Configuração automática para Outlook
- **Yahoo**: Configuração automática para Yahoo
- **Outro**: Configuração manual de servidor SMTP
- **Não enviar**: Apenas analisa o currículo sem enviar e-mail

### 3. Inserir credenciais
- **E-mail**: Sua conta de e-mail
- **Senha**: Para Gmail, use senha de app; para outros, senha normal

### 4. Selecionar arquivo PDF
- Digite o caminho completo do arquivo
- Ou arraste o arquivo para a janela do terminal

### 5. Verificar resultado
O programa mostrará:
- Texto extraído do PDF
- Contadores de palavras-chave por categoria
- Classificação final do candidato
- Status do envio do e-mail

## Exemplo de Uso

```
🚀 ANALISADOR DE CURRÍCULOS PDF
==================================================

==================================================
CONFIGURAÇÃO DO E-MAIL REMETENTE
==================================================

Opções de e-mail:
1. Gmail
2. Outlook/Hotmail
3. Yahoo
4. Outro (configuração manual)
5. Não enviar e-mail (apenas analisar)

Escolha uma opção (1-5): 1

📧 Configurando Gmail
IMPORTANTE: Use uma senha de app, não sua senha normal!
Para gerar: Google → Gerenciar Conta → Segurança → Senhas de app
Digite seu e-mail Gmail: seu_email@gmail.com
Digite sua senha de app: ********
✓ Gmail configurado!

==================================================
SELECIONAR ARQUIVO PDF
==================================================

Digite o caminho do arquivo PDF: C:\Users\Usuario\Documents\curriculo.pdf

🔍 Analisando currículo: C:\Users\Usuario\Documents\curriculo.pdf
📄 Texto extraído: 15420 caracteres

📊 Contadores de palavras-chave:
  🏷️  excelente: 3
  🏷️  bom: 1
  🏷️  medio: 2

🏆 Classificação: EXCELENTE
📝 Descrição: Excelente! Encontramos 3 palavras-chave da categoria mais alta.

📤 Enviando e-mail via smtp.gmail.com:587...
✓ E-mail enviado com sucesso para lucaslmonteiro68@gmail.com

==================================================
RESULTADO FINAL DA ANÁLISE
==================================================
📁 Arquivo: curriculo.pdf
🏆 Categoria: EXCELENTE
📝 Descrição: Excelente! Encontramos 3 palavras-chave da categoria mais alta.
📧 E-mail enviado: Sim
```

## Personalização

No arquivo `capgemini2.py`, você pode alterar:

- **E-mail de destino**: `self.email_destino = "lucaslmonteiro68@gmail.com"`
- **Quantidade mínima**: `self.quantidade_minima = 2`
- **Palavras-chave**: Edite o dicionário `self.palavras_chave`

## Estrutura do Código

- **`AnalisadorCurriculo`**: Classe principal com toda a lógica
- **`selecionar_email()`**: Menu interativo para escolher conta de e-mail
- **`extrair_texto_pdf()`**: Extrai texto do PDF usando pdfplumber
- **`contar_palavras_chave()`**: Conta ocorrências de palavras-chave
- **`classificar_candidato()`**: Aplica regras de classificação
- **`enviar_email()`**: Envia resultado por e-mail via SMTP
- **`analisar_curriculo()`**: Função principal que coordena todo o processo

## Personalização Avançada

### Adicionar Novas Categorias
```python
self.palavras_chave = {
    "excelente": ["SAP", "PP", "PM", "QM", "Mapeamento"],
    "bom": ["Integração", "ERP", "TOTVS"],
    "medio": ["Oracle", "Excel"],
    "nova_categoria": ["palavra1", "palavra2", "palavra3"]  # Nova categoria
}
```

### Alterar Critérios de Classificação
```python
def classificar_candidato(self, contadores):
    # Sua lógica personalizada aqui
    pass
```

### Modificar Template de E-mail
```python
def criar_mensagem_email(self, categoria, descricao, nome_arquivo):
    # Personalize o corpo do e-mail aqui
    pass
```

## Solução de Problemas

### Erro de Autenticação Gmail
- Verifique se a autenticação de 2 fatores está ativada
- Use senha de app, não sua senha normal
- Confirme se o e-mail e senha estão corretos

### PDF não lido
- Certifique-se de que o arquivo existe no caminho especificado
- Verifique se o PDF não está corrompido
- Alguns PDFs com imagens podem não ter texto extraível

### E-mail não enviado
- Verifique se selecionou uma opção de e-mail válida
- Confirme se as credenciais estão corretas
- Verifique se o e-mail de destino é válido
- Para Gmail, certifique-se de usar senha de app

### Problemas de Conexão
- Verifique sua conexão com a internet
- Alguns provedores podem bloquear portas SMTP
- Tente usar outra rede ou VPN se necessário

## Vantagens da Nova Versão

✅ **Sem variáveis de ambiente** - Configure na hora de usar
✅ **Múltiplos provedores** - Gmail, Outlook, Yahoo, personalizado
✅ **Interface interativa** - Menu fácil de usar
✅ **Modo apenas análise** - Não precisa configurar e-mail se não quiser
✅ **Configuração automática** - Servidores SMTP pré-configurados
✅ **Segurança** - Senha não aparece na tela ao digitar

## Licença

Este projeto é de uso livre para fins educacionais e comerciais.
