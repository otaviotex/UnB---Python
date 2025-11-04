from datetime import datetime, date
import os
from banco import criar_banco, Medico, Paciente, Consulta, session

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

horarios_disponiveis = ["8:00","9:00","10:00","14:00","15:00","16:00","17:00","18:00"]

criar_banco()

def main():
  print("""
    
  ___                       _  ___        _   
 / _ \                     | |/ _ \      | |  
/ /_\ \ __ _  ___ _ __   __| / /_\ \_   _| |_ 
|  _  |/ _` |/ _ \ '_ \ / _` |  _  | | | | __|
| | | | (_| |  __/ | | | (_| | | | | |_| | |_ 
\_| |_/\__, |\___|_| |_|\__,_\_| |_/\__,_|\__|
        __/ |                                 
       |___/                                  
                                              
                                                                               
    
    """)
  while True:
    
    print("\n[1] Marcar Consulta")
    print("[2] Área do Médico")
    print("[3] Sair")
    
    try:
      opc = int(input("Escolha uma opcao: "))
    except ValueError:
      print("Digite um numero valido")
      continue
        
    if opc < 1 or opc > 3:
      print("Escolha o numero 1 ao 3!")
      continue
    
    clear()
    
    match opc:
      case 1:
        print("\n --------- Cadastro do Paciente ---------\n")
        while True:
          nome = input("Primeiro nome: ")
          if nome.isalpha():
            break
          else:
            print("Insira um nome valido")

        while True:
          sobrenome = input("Ultimo sobrenome: ")
          if sobrenome.isalpha():
            break
          else:
            print("Insira um sobrenome valido")
          
        while True:
            try:
              idade = int(input("Idade: "))
              break
            except ValueError:
              print("Insira apenas numeros")

        while True:
          numero = input("ddd + numero: ").replace(" ", "")
          if numero.isdigit() and len(numero) == 11:
            break
          else:
            print("Insira um numero de celular correto!")
          
        while True:
          genero = input("Genero: ")
          if genero.isalpha():
            break
          else:
            print("Insira apenas letras")
                  
        while True:
          convenio = input("Convenio: ")
          if convenio.isalpha():
            break
          else:
            print("Insira apenas letras")
          
        while True:
          email = input("E-mail: ").strip()
          if "@" in email and "." in email:
            break
          else:
            print("E-mail inválido. Tente novamente.")
        
        paciente = Paciente(nome, sobrenome, idade, genero, numero, convenio, email)  
        
        clear()
        print("Agora você esta pronto(a) para marcar sua consulta!\n")
        
        while True:
          data_input = input("Digite a data da consulta (DD/MM/AAAA): ").strip()
          try:
            data_consulta = datetime.strptime(data_input, "%d/%m/%Y").date()
        
            if data_consulta < date.today():
              print("Essa data ja passou! Insira uma data futura!")
              continue
            break
        
          except ValueError:
            print("Data Invalida, tente novamente!")


        while True:
            hora = input(""" 
---------------

8:00       
9:00        
10:00      
14:00      
15:00     
16:00      
17:00      
18:00      
                
---------------        
Digite a opcao  de horario escolhida(HH:MM): 
""").strip()
            if hora in horarios_disponiveis:
                break
            else:
                print("Insira um horario valido!")

        print("\nMedicos disponíveis: ")
        medicos = session.query(Medico).all()
        if not medicos:
          print("Nenhum medico cadastrado. Cadastre um na area do medico")
          continue
        for i, med in enumerate(medicos, start=1):
          print(f"[{i}] {med.nome} {med.sobrenome} - {med.especialidade}")
        
        while True: 
          try:
            escolha = int(input("Escolha o medico responsavel: "))
            if 1 <= escolha <= len(medicos):
              medico = medicos [escolha -1]
              break
            else:
              print("Digite um numero valido!")
          except ValueError:
            print("Digite um numero valido!")
            
        consulta = Consulta(data=data_consulta, hora=hora, medico=medico, paciente=paciente)

        session.add_all([paciente, consulta])
        session.commit()

        print(f"\nConsulta marcada com {medico.nome} em {data_consulta} às {hora}.")
        
        input("\nPressione ENTER para voltar ao menu.")
        clear()
        
      case 2:
        
        while True:
          print("\n --------- Sistema de Medicos ---------")
          print("[1] Cadastrar Medico")
          print("[2] Login Medico")
          print("[3] Sair")
    
          try:
            opc = int(input("Escolha uma opcao: "))
          except ValueError:
            print("Digite um numero valido")
            continue
    
          if opc < 1 or opc > 3:
            print("Digite um numero entre 1 e 3")
            continue
    
          clear()
    
          match opc:
            case 1:
              print("\n --------- Cadastro de Medicos ---------")
              while True:
                nome = input("Nome: ")
                if nome.isalpha():
                  break
                else:
                  print("Insira um nome valido")
            
              while True:
                sobrenome = input("Ultimo nome: ")
                if sobrenome.isalpha():
                  break
                else:
                  print("Insira um sobrenome valido")
                    
              while True:
                try:
                  idade = int(input("Idade: "))
                  break
                except ValueError:
                  print("Insira apenas numeros")
                    
              while True:
                genero = input("Genero: ")
                if genero.isalpha():
                  break
                else:
                  print("Insira apenas letras")
        
                    
              crm = input("Crm: ")
                    
              while True:
                especialidade = input("Especialidade: ")
                if especialidade.isalpha():
                  break
                else:
                  print("Insira apenas letras")
            
              while True:        
                senha = input("Senha: ")
                confirm_senha = input("Confirme a senha: ")
        
                if senha != confirm_senha:
                  print("Senhas nao conferem. Tente novamente!")
                  continue
                else:
                  medico = Medico(nome, sobrenome, idade, genero, crm, especialidade, senha)
                  session.add(medico)
                  session.commit()
                  print(f"Médico {nome} cadastrado com sucesso!")
                  input("Pressione ENTER para voltar.")
                  clear()
                  break
        
            case 2:
              print("\n --------- Login Medico ---------")
              crm = input("CRM: ")
              senha = input("Senha: ")
              
              medico = session.query(Medico).filter_by(crm=crm).first()
              
              if not medico or not medico.verific_senha(senha):
                print("CRM ou senha incorretos!")
                continue
              
              print(f"\nBem-vindo, Dr(a). {medico.nome}!")
              print("Consultas marcadas:")
              
              consultas = session.query(Consulta).filter_by(id_medico=medico.id).all()
              if not consultas:
                print("Nenhuma consulta marcada.")
              else:
                for c in consultas:
                  data_formatada = c.data.strftime("%d/%m/%Y")
                  print(f"- {data_formatada} as {c.hora} | Paciente: {c.paciente.nome}")
                  
                input("\nPressione ENTER para voltar ao menu principal.")
                clear()
            
            case 3: 
              print("Saindo do Sistema...\n")
              break
      case 3:
        print("Saindo do Sistema...\n")
        break      
main()
