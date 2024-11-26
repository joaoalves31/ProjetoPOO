DROP TABLE IF EXISTS transacoes;
DROP TABLE IF EXISTS contas;
DROP TABLE IF EXISTS titulares;
DROP TABLE IF EXISTS pessoas;

CREATE TABLE pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Adiciona AUTO_INCREMENT para gerar ids automaticamente
    nome VARCHAR(100) NOT NULL DEFAULT '',
    idade INT NOT NULL DEFAULT 18,
    cpf VARCHAR(11) NOT NULL UNIQUE
);


CREATE TABLE titulares (
    id INT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,  -- Login não pode ser NULL e é único
    senha VARCHAR(255) NOT NULL,        -- Senha não pode ser NULL
    pessoa_id INT,                      -- Pessoa_id pode ser NULL, permitindo que nem todos os titulares estejam associados a uma pessoa
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);

CREATE TABLE contas (
    numero_conta INT PRIMARY KEY,
    saldo DECIMAL(10, 2) NOT NULL DEFAULT 0.0,  -- Saldo com valor padrão 0.0
    tipo VARCHAR(20) NOT NULL,  -- Tipo de conta, pode ser 'ContaCorrente' ou 'ContaPoupanca'
    titular_id INT NOT NULL,    -- Titular da conta, não pode ser NULL
    limite DECIMAL(10, 2) DEFAULT 0.0,  -- Limite de crédito com valor padrão 0.0 (para contas correntes)
    juros DECIMAL(5, 2) DEFAULT 0.0,    -- Juros com valor padrão 0.0 (para contas poupança)
    FOREIGN KEY (titular_id) REFERENCES titulares(id)
);

CREATE TABLE transacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_transacao VARCHAR(50) NOT NULL,  -- Tipo de transação, como 'depósito', 'transferência', etc.
    valor DECIMAL(10, 2) NOT NULL,        -- Valor da transação, não pode ser NULL
    conta_origem INT NOT NULL,            -- Conta de origem, não pode ser NULL
    conta_destino INT NOT NULL,           -- Conta de destino, não pode ser NULL
    data_transacao DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data da transação, com timestamp default
    FOREIGN KEY (conta_origem) REFERENCES contas(numero_conta),
    FOREIGN KEY (conta_destino) REFERENCES contas(numero_conta)
);