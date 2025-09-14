import pywhatkit as kit
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class WhatsAppSender:
    def __init__(self, root):
        self.root = root
        self.root.title("Enviador de Mensagens WhatsApp")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansão
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Enviar Mensagens WhatsApp", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Contatos
        ttk.Label(main_frame, text="Contatos (um por linha, com código país):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.contacts_text = scrolledtext.ScrolledText(main_frame, width=40, height=6)
        self.contacts_text.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        self.contacts_text.insert(tk.END, "+5521997715254\n+5511999999999")
        
        # Mensagem
        ttk.Label(main_frame, text="Mensagem:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        self.message_text = scrolledtext.ScrolledText(main_frame, width=40, height=8)
        self.message_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        self.message_text.insert(tk.END, "Olá! Esta é uma mensagem automática.")
        
        # Intervalo entre envios
        ttk.Label(main_frame, text="Intervalo entre envios (segundos):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.IntVar(value=15)
        ttk.Spinbox(main_frame, from_=5, to=60, textvariable=self.interval_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Botão de envio
        self.send_button = ttk.Button(main_frame, text="Enviar Mensagens", command=self.send_messages)
        self.send_button.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Área de log
        ttk.Label(main_frame, text="Log de execução:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.log_text = scrolledtext.ScrolledText(main_frame, width=40, height=10)
        self.log_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para enviar")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=6, column=0, columnspan=2, pady=5)
        
    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def send_messages(self):
        contacts = self.contacts_text.get("1.0", tk.END).strip().split('\n')
        message = self.message_text.get("1.0", tk.END).strip()
        interval = self.interval_var.get()
        
        if not contacts or not message:
            messagebox.showerror("Erro", "Por favor, preencha os contatos e a mensagem.")
            return
            
        self.send_button.config(state=tk.DISABLED)
        self.status_var.set("Enviando mensagens...")
        
        try:
            for i, contact in enumerate(contacts):
                if not contact:
                    continue
                    
                self.log_message(f"Enviando para {contact}...")
                
                try:
                    kit.sendwhatmsg_instantly(contact, message, 15, True, 5)
                    self.log_message(f"Mensagem enviada para {contact} com sucesso!")
                except Exception as e:
                    self.log_message(f"Erro ao enviar para {contact}: {str(e)}")
                
                # Se não for o último contato, aguarda o intervalo
                if i < len(contacts) - 1:
                    self.log_message(f"Aguardando {interval} segundos antes do próximo envio...")
                    for j in range(interval, 0, -1):
                        self.status_var.set(f"Aguardando {j} segundos...")
                        time.sleep(1)
                        self.root.update()
            
            self.status_var.set("Todos os envios concluídos!")
            messagebox.showinfo("Sucesso", "Todas as mensagens foram processadas!")
            
        except Exception as e:
            self.log_message(f"Erro inesperado: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
        
        finally:
            self.send_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppSender(root)
    root.mainloop()