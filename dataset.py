from tkinter import ttk
from tkinter import *
import tkinter
import sqlite3

class cadastro:
    # connection dir property----------------------------------------------------
    # propriedade do dir de conexão------------------------------------------------
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations ----------------------------------------------  
        #Inicializações --------------------------------------------------
        self.wind = window
        self.wind.title('cadastro DataSet')

        # Creating a Frame Container ------------------------------------------------  
        #Criando um Contêiner de Quadro-------------------------------------------
        frame = LabelFrame(self.wind, text = 'Registrar novo cadastro')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)        
        
        # Name Input------------------------------------------------------
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Text(frame,width=20,height=3)
        self.name.focus()
        self.name.grid(row = 1, column = 1)


        Label(frame, text = 'Description: ').grid(row = 2, column = 0)
        self.description = Text(frame, width=20,height=3)
        self.description.focus()
        self.description.grid(row = 2, column = 1)

        Label(frame, text = 'Local: ').grid(row = 3, column = 0)
        self.local = Text(frame,width=20,height=3)
        self.local.focus()
        self.local.grid(row = 3, column = 1)
          
      
        
        self.tree = ttk.Treeview(frame, columns=("Name", "Description",))
        self.tree.heading("#0", text="Name", anchor= CENTER)
        self.tree.heading("#1", text="Description", anchor= CENTER)
        self.tree.heading("#2", text="Local", anchor= CENTER)
        self.tree.grid(row = 4, column = 0, columnspan = 5)

        
        


        # Button Add cadastro --------------------------------------------------
        ttk.Button(frame, text = 'Inserir', command = self.add_cadastro).grid(row = 5, column = 1, sticky = W + E)
        #Botão para excluir cadastro--------------------------------------------
        ttk.Button(frame, text = 'DELETE', command = self.delete_cadastro).grid(row = 5, column = 2, sticky = W + E)
        #Botão para atualizar cadastro------------------------------------------
        #ttk.Button(frame, text = 'EDIT', command = self.edit_cadastro).grid(row = 5, column = 3, sticky = W + E)

        # Output Messages ------------------------------------------------------
        # Mensagens de Saída ---------------------------------------------------
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 7, column = 0, columnspan = 3, sticky = W + E)

       
        # Filling the Rows-------------------------------------------------------
        # Preenchendo as filas----------------------------------------------------
        self.get_cadastro()

    # Function to Execute Database Querys----------------------------------------------
    # Função para executar bancos de dados --------------------------------------------
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (id INTEGER PRIMARY KEY , name TEXT, description TEXT, local TEXT)")
            result = cursor.execute(query, parameters)
            conn.commit()
        return result



    def get_cadastro(self):
        # cleaning Table ----------------------------------------------------------------
        # mesa de limpeza------------------------------------------------------------------
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element) 

        query = 'SELECT * FROM cadastro ORDER BY name DESC'
        db_rows = self.run_query(query)


        for row in db_rows:
   
            self.tree.insert('', 0, text = row[1], values = (row[2],row[3]))




  
    # Validação De Entrada De Usuário -----------------------------------------------------
    def validation(self):
        return (self.name.get(1.0, END)),(self.description.get(1.0, END), (self.local.get(1.0, END)))

    def add_cadastro(self):
        if self.validation():
            query = 'INSERT INTO cadastro VALUES(NULL, ?, ?, ?)'
            parameters =  (self.name.get(1.0, END), self.description.get(1.0, END), self.local.get(1.0, END))
            self.run_query(query, parameters)
            self.message['text'] = 'cadastro {} added Successfully'.format(self.name.get(1.0, END))
            self.name.delete(1.0, END)
            self.description.delete(1.0, END)
            self.local.delete(1.0, END)
        else:
            self.message['text'] = 'Name and Data is Required'
        self.get_cadastro()

    def delete_cadastro(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM cadastro WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_cadastro()

   
   

if __name__ == '__main__':
    window = Tk()
    application = cadastro(window)
    window.mainloop()
