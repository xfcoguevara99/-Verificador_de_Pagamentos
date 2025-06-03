# -Verificador_de_Pagamento

💡 Projeto: Automatização da Conferência de Pagamentos Comunitários
Este projeto surgiu em 2020, quando ainda residia na Venezuela. Na comunidade onde morava, uma pessoa era responsável por receber pagamentos de produtos destinados à população. Como os bancos não ofereciam ferramentas automatizadas para conferir as transferências recebidas, todo o processo era feito manualmente.

Durante um curso de Python, identifiquei a oportunidade de aplicar os conhecimentos adquiridos para resolver esse problema real. Criei uma ferramenta simples que automatizava a conferência dos pagamentos, comparando transferências recebidas com uma lista de devedores, valores esperados e datas de pagamento.

⚙️ Funcionalidades
Leitura de arquivos do banco e da lista de usuários em formato .xlsx.

Verificação de referências bancárias cruzadas com os dados dos usuários.

Detecção de referências repetidas.

Classificação dos pagamentos:

✅ Pagamento correto

⚠️ Pagamento com valor incorreto (faltando ou sobrando)

❌ Pagamento não encontrado

🔁 Referência duplicada

📤 Exportação de um arquivo resumo com os dados verificados de todos os usuários.

🧠 Motivação
Esse foi meu primeiro projeto prático com Python. Surgiu a partir de uma necessidade real da minha comunidade na Venezuela, onde o controle de pagamentos era feito manualmente. A ferramenta facilitou o trabalho da pessoa encarregada e demonstrou o valor da automação com programação.

🚀 Melhorias Futuras
Melhorar tratamento de erros de entrada e leitura de arquivos.
Adicionar uma interface gráfica (GUI).
Suporte a múltiplos formatos de entrada (CSV, TXT).

