# 🚀 Talent Forge - Analisador Inteligente de Currículos

## 📋 Descrição

O **Talent Forge** é um sistema automatizado de análise de currículos PDF desenvolvido especificamente para vagas de **Desenvolvimento com foco em LLM e IA**. O sistema utiliza inteligência artificial para classificar candidatos baseado em características técnicas e enviar e-mails personalizados automaticamente.

## ✨ Funcionalidades Principais

### 🔍 **Análise Inteligente de Currículos**

- **Extração automática** de texto de arquivos PDF
- **Reconhecimento de características técnicas** em português e inglês
- **Sistema de sinônimos** para evitar duplicação de conceitos
- **Classificação hierárquica** baseada na quantidade de características encontradas

### 📧 **Sistema de E-mail Automático**

- **Envio automático** via Gmail SMTP
- **Mensagens personalizadas** por nível de classificação
- **Extração automática** de e-mail do currículo
- **Identificação automática** do nome do candidato

### 🎯 **Classificação Hierárquica Inteligente**

- **🏆 EXCELENTE**: Mais de 8 características → 3ª fase direta
- **🥈 BOM**: 6 a 8 características → 2ª fase
- **🥉 MÉDIO**: 3 a 5 características → 2ª fase
- **❌ RUIM**: 0 a 2 características → Não selecionado

## 🛠️ Tecnologias Utilizadas

- **Python 3.7+**
- **pdfplumber** - Extração de texto de PDFs
- **smtplib** - Envio de e-mails
- **email.message** - Criação de mensagens
- **re** - Expressões regulares para busca
- **os** - Operações de sistema de arquivos

## 📦 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- Conta Gmail com senha de aplicativo configurada

### Passos de Instalação

1. **Clone o repositório:**

```bash
git clone <url-do-repositorio>
cd Talent-Forge
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Configure as credenciais Gmail** no arquivo `capgemini2.py`:

```python
self.email_remetente = "seu-email@gmail.com"
self.senha_app = "sua-senha-de-app"
```

## 🚀 Como Usar

### 1. **Execução do Sistema**

```bash
python capgemini2.py
```

### 2. **Configuração Inicial**

- **Nome do recrutador**: Digite seu nome ou identificação
- **Pasta de currículos**: Cole o caminho completo da pasta com os PDFs

### 3. **Processo Automático**

O sistema irá:

- ✅ Analisar todos os PDFs da pasta
- ✅ Extrair texto e características técnicas
- ✅ Classificar candidatos por hierarquia
- ✅ Enviar e-mails personalizados
- ✅ Gerar relatório completo

## 🎯 Sistema de Características Técnicas

### **Tecnologias Core (40+ características)**

- **Python, Backend, APIs (REST/GraphQL)**
- **LLM, Large Language Models, Agentes LLM**
- **Git, Jira, Scrum, Kanban, Metodologias ágeis**
- **React, Next.js, DevOps, Containers, CI/CD, Cloud**
- **LangChain, LlamaIndex, Multi-agente**
- **Embeddings, Vetorização, Processamento de documentos**

### **Sistema de Sinônimos Inteligente**

O sistema reconhece automaticamente variações em português e inglês:

- **"Git"** = "git", "branching", "pull requests", "code review"
- **"Inglês"** = "english", "inglês avançado", "advanced english", "fluent english"
- **"LLM"** = "large language models", "language models"
- **"DevOps"** = "containers", "docker", "kubernetes", "ci/cd"

## 📊 Estrutura de Classificação

### **🏆 NÍVEL EXCELENTE (>8 características)**

- **Perfil ideal** para a vaga
- **Avança direto** para 3ª fase (entrevista técnica)
- **Domínio completo** das tecnologias essenciais

### **🥈 NÍVEL BOM (6-8 características)**

- **Base sólida** em desenvolvimento
- **Conhecimentos** em frontend e DevOps
- **2ª fase** para avaliação de experiência com LLMs

### **🥉 NÍVEL MÉDIO (3-5 características)**

- **Compatibilidade parcial** com a vaga
- **Conhecimentos** em ferramentas específicas de LLM
- **2ª fase** para avaliação técnica geral

### **❌ NÍVEL RUIM (0-2 características)**

- **Compatibilidade insuficiente** com os requisitos
- **Não selecionado** para próximas fases
- **Feedback construtivo** para desenvolvimento

## 📧 Sistema de E-mails

### **Configuração Gmail**

- **SMTP Server**: smtp.gmail.com
- **Porta**: 587
- **Autenticação**: TLS com senha de aplicativo

### **Mensagens Personalizadas**

- **Nível hierárquico** claramente identificado
- **Próximos passos** específicos por categoria
- **Tom profissional** e motivacional
- **Informações essenciais** de forma concisa

## 📁 Estrutura de Arquivos

```
Talent-Forge/
├── capgemini2.py          # Sistema principal
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
└── pasta_curriculos/      # Pasta com PDFs para análise
```

## 🔧 Configurações Personalizáveis

### **Palavras-chave**

- Edite a lista `self.palavras_chave` para adicionar/remover características
- Configure grupos de sinônimos para novos conceitos

### **Limites de Classificação**

- Modifique os valores na função `classificar_candidato`:

```python
if total_caracteristicas > 8:      # Excelente
elif total_caracteristicas >= 6:   # Bom
elif total_caracteristicas >= 3:   # Médio
else:                              # Ruim
```

### **Configurações de E-mail**

- Altere credenciais Gmail
- Personalize mensagens por categoria
- Modifique assinatura e informações da empresa

## 📈 Relatórios e Saída

### **Console em Tempo Real**

- Progresso da análise por currículo
- Características encontradas em cada candidato
- Total de características únicas
- Status de envio de e-mails

### **Resumo Final**

- Lista completa de candidatos analisados
- Classificação e quantidade de características
- Total de e-mails enviados
- Estatísticas do processo

## 🚨 Tratamento de Erros

### **Validações Implementadas**

- ✅ Verificação de existência de pasta
- ✅ Validação de arquivos PDF
- ✅ Tratamento de erros de leitura de PDF
- ✅ Validação de formato de e-mail
- ✅ Tratamento de falhas no envio de e-mails

### **Logs e Feedback**

- Mensagens de erro descritivas
- Avisos para situações não críticas
- Confirmação de operações bem-sucedidas

## 🔒 Segurança e Privacidade

### **Credenciais**

- **Senha de aplicativo** Gmail (não senha principal)
- **Configuração local** (não compartilhada)
- **Validação de e-mails** antes do envio

### **Dados**

- **Processamento local** (não enviado para servidores externos)
- **Temporário** (não armazenado permanentemente)
- **Conformidade** com LGPD para dados pessoais

## 🚀 Casos de Uso

### **Recrutamento em Massa**

- Análise de **centenas de currículos** automaticamente
- **Classificação objetiva** baseada em critérios técnicos
- **Comunicação automática** com todos os candidatos

### **Seleção Especializada**

- **Foco em tecnologias específicas** (LLM, IA, Backend)
- **Reconhecimento de habilidades** em múltiplos idiomas
- **Avaliação consistente** de perfis técnicos

### **Processo Seletivo Estruturado**

- **Hierarquia clara** de candidatos
- **Fases definidas** por nível de compatibilidade
- **Feedback personalizado** para cada categoria

## 🔮 Funcionalidades Futuras

### **Melhorias Planejadas**

- [ ] Interface gráfica (GUI)
- [ ] Análise de currículos em outros idiomas
- [ ] Integração com ATS (Applicant Tracking System)
- [ ] Relatórios em PDF/Excel
- [ ] Dashboard web para acompanhamento
- [ ] Machine Learning para classificação mais precisa

### **Expansões Técnicas**

- [ ] Suporte a mais formatos de arquivo
- [ ] Análise de portfólios online
- [ ] Integração com LinkedIn e GitHub
- [ ] Avaliação de projetos open source

## 🤝 Contribuição

### **Como Contribuir**

1. **Fork** do repositório
2. **Crie uma branch** para sua feature
3. **Commit** suas mudanças
4. **Push** para a branch
5. **Abra um Pull Request**

### **Áreas de Contribuição**

- **Novas características técnicas** para análise
- **Melhorias no sistema de sinônimos**
- **Otimizações de performance**
- **Novos formatos de saída**
- **Testes e validações**

## 📞 Suporte

### **Documentação**

- Este README contém todas as informações essenciais
- Código comentado para fácil compreensão
- Exemplos de uso e configuração

### **Issues e Bugs**

- Reporte problemas via GitHub Issues
- Inclua detalhes do erro e ambiente
- Anexe logs e arquivos de exemplo

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

## 👨‍💻 Autor

Desenvolvido para otimizar processos de recrutamento técnico com foco em desenvolvimento e inteligência artificial.

---

**⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!**
