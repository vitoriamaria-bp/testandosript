from pathlib import Path


ARQUIVO_INSERTS = Path(__file__).with_name("inserts_dados.sql")
TOTAL_ESPERADO_INSERTS = 129


def contar_inserts(conteudo):
    return sum(1 for linha in conteudo.splitlines() if linha.startswith("INSERT INTO"))


def main():
    if not ARQUIVO_INSERTS.exists():
        print("Arquivo inserts_dados.sql nao encontrado.")
        print("Esse arquivo deve ficar junto deste script para popular uma maquina nova.")
        return

    conteudo = ARQUIVO_INSERTS.read_text(encoding="utf-8")
    total_inserts = contar_inserts(conteudo)

    if total_inserts == 0:
        print("O arquivo inserts_dados.sql esta vazio ou sem INSERTs.")
        print("Use a versao fixa com os dados iniciais do projeto.")
        return

    print("Arquivo de carga inicial encontrado: inserts_dados.sql")
    print(f"Total de INSERTs encontrados: {total_inserts}")

    if total_inserts != TOTAL_ESPERADO_INSERTS:
        print(f"Atencao: eram esperados {TOTAL_ESPERADO_INSERTS} INSERTs.")

    print("\nPara carregar em uma maquina nova, rode primeiro a criacao automatica do projeto, se necessario.")
    print("Depois execute:")
    print("mysql -u root -p db_core_study1 < inserts_dados.sql")
    print("\nEste script nao consulta o MySQL para evitar sobrescrever os dados fixos quando o banco estiver vazio.")


if __name__ == "__main__":
    main()
