import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pyzabbix import ZabbixAPI
import subprocess
import ipaddress
import socket
from datetime import datetime
import threading
import time

# === VARIÁVEIS GLOBAIS ===
parar_varredura = False
zapi = None
ZABBIX_SERVER = ''
ZABBIX_USER = ''
ZABBIX_PASSWORD = ''

# === FUNÇÃO PRINCIPAL ===
def iniciar_varredura():
    global parar_varredura
    parar_varredura = False

    ip_inicio = ip_entry_inicio.get()
    ip_fim = ip_entry_fim.get()
    grupo_nome = group_var.get().strip()
    template_nome = template_var.get().strip()
    log_area.delete(1.0, tk.END)

    if not ip_inicio or not ip_fim or not grupo_nome or not template_nome:
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    try:
        start_ip = int(ipaddress.IPv4Address(ip_inicio))
        end_ip = int(ipaddress.IPv4Address(ip_fim))
    except ValueError:
        messagebox.showerror("Erro", "IP inicial ou final inválido.")
        return

    log_file = f"log_zabbix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    def run():
        templates = zapi.template.get(output="extend")
        encontrados = [t for t in templates if template_nome.lower() in t['host'].lower()]
        if not encontrados:
            log(f"❌ Template contendo '{template_nome}' não encontrado.")
            return
        template_id = encontrados[0]['templateid']

        group = zapi.hostgroup.get(filter={"name": grupo_nome})
        if not group:
            log(f"📁 Grupo '{grupo_nome}' não existe. Criando...")
            group = zapi.hostgroup.create(name=grupo_nome)
            group_id = group['groupids'][0]
        else:
            group_id = group[0]['groupid']

        with open(log_file, "w") as log_file_handle:
            for ip_int in range(start_ip, end_ip + 1):
                if parar_varredura:
                    log("⏸️ Varredura pausada pelo usuário.")
                    return
                ip_str = str(ipaddress.IPv4Address(ip_int))
                log(f"🔍 Verificando {ip_str}...")
                if is_host_up(ip_str):
                    hostname = get_hostname(ip_str)
                    existing = zapi.host.get(filter={"host": hostname})
                    if existing:
                        hostname = ip_str
                    existing = zapi.host.get(filter={"host": hostname})
                    if existing:
                        log(f"⚠️ {hostname} ({ip_str}) já existe.")
                        log_file_handle.write(f"{ip_str} - já existe\n")
                        continue
                    try:
                        zapi.host.create(
                            host=hostname,
                            interfaces=[{
                                "type": 1,
                                "main": 1,
                                "useip": 1,
                                "ip": ip_str,
                                "dns": "",
                                "port": "10050"
                            }],
                            groups=[{"groupid": group_id}],
                            templates=[{"templateid": template_id}]
                        )
                        log(f"✅ {hostname} ({ip_str}) adicionado.")
                        log_file_handle.write(f"{ip_str} - adicionado como {hostname}\n")
                    except Exception as e:
                        log(f"❌ Erro com {ip_str}: {e}")
                        log_file_handle.write(f"{ip_str} - erro: {e}\n")
                else:
                    log(f"⛔ {ip_str} sem resposta.")
                    log_file_handle.write(f"{ip_str} - sem resposta\n")
        log("📄 Fim da varredura. Verifique o log gerado.")

    threading.Thread(target=run).start()

def conectar_zabbix():
    global zapi, ZABBIX_SERVER, ZABBIX_USER, ZABBIX_PASSWORD
    ZABBIX_SERVER = url_var.get().strip()
    ZABBIX_USER = user_var.get().strip()
    ZABBIX_PASSWORD = pass_var.get().strip()

    try:
        zapi = ZabbixAPI(ZABBIX_SERVER)
        zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)
        messagebox.showinfo("Conectado", "✅ Conexão com o Zabbix realizada com sucesso!")
        atualizar_autocomplete()
        habilitar_campos()
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"❌ Falha ao conectar: {e}")

def pausar_varredura():
    global parar_varredura
    parar_varredura = True

def is_host_up(ip, tentativas=1, intervalo=0.5):
    for _ in range(tentativas):
        result = subprocess.run(["ping", "-n", "1", "-w", "1000", ip],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode == 0:
            return True
        time.sleep(intervalo)
    return False

def get_hostname(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except Exception:
        return ip

def log(msg):
    log_area.insert(tk.END, msg + "\n")
    log_area.see(tk.END)
    root.update()

def filtrar_combobox(event, combo, full_list):
    texto = combo.get().lower()
    filtrado = [item for item in full_list if texto in item.lower()]
    if not filtrado:
        filtrado = full_list
    combo['values'] = filtrado

def atualizar_autocomplete():
    try:
        grupos = [g['name'] for g in zapi.hostgroup.get()]
        templates = [t['host'] for t in zapi.template.get()]

        group_combo['values'] = grupos
        template_combo['values'] = templates

        group_combo.bind('<KeyRelease>', lambda e: filtrar_combobox(e, group_combo, grupos))
        template_combo.bind('<KeyRelease>', lambda e: filtrar_combobox(e, template_combo, templates))
    except Exception as e:
        log(f"Erro ao carregar autocomplete: {e}")

def habilitar_campos():
    ip_entry_inicio.config(state='normal')
    ip_entry_fim.config(state='normal')
    group_combo.config(state='normal')
    template_combo.config(state='normal')
    btn_iniciar.config(state='normal')
    btn_pausar.config(state='normal')

# === INTERFACE ===
root = tk.Tk()
root.title("Zabbix automatic host registration V1.0")

frame_login = tk.Frame(root)
frame_login.pack(pady=10)

tk.Label(frame_login, text="Zabbix URL:").grid(row=0, column=0)
url_var = tk.StringVar(value="http://")
tk.Entry(frame_login, textvariable=url_var, width=35).grid(row=0, column=1, padx=5)

tk.Label(frame_login, text="Usuário:").grid(row=1, column=0)
user_var = tk.StringVar()
tk.Entry(frame_login, textvariable=user_var, width=20).grid(row=1, column=1, padx=5)

tk.Label(frame_login, text="Senha:").grid(row=2, column=0)
pass_var = tk.StringVar()
tk.Entry(frame_login, textvariable=pass_var, width=20, show='*').grid(row=2, column=1, padx=5)

btn_conectar = tk.Button(frame_login, text="Conectar", command=conectar_zabbix)
btn_conectar.grid(row=3, column=0, columnspan=2, pady=5)

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="IP Inicial:").grid(row=0, column=0)
ip_entry_inicio = tk.Entry(frame_top, width=15, state='disabled')
ip_entry_inicio.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="IP Final:").grid(row=0, column=2)
ip_entry_fim = tk.Entry(frame_top, width=15, state='disabled')
ip_entry_fim.grid(row=0, column=3, padx=5)

tk.Label(root, text="Grupo de Host (Zabbix)").pack()
group_var = tk.StringVar()
group_combo = ttk.Combobox(root, textvariable=group_var, state='disabled')
group_combo.pack(pady=5)

tk.Label(root, text="Template (Zabbix)").pack()
template_var = tk.StringVar()
template_combo = ttk.Combobox(root, textvariable=template_var, state='disabled')
template_combo.pack(pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_iniciar = tk.Button(frame_buttons, text="Iniciar Varredura", command=iniciar_varredura, state='disabled')
btn_iniciar.pack(side=tk.LEFT, padx=5)
btn_pausar = tk.Button(frame_buttons, text="Pausar", command=pausar_varredura, state='disabled')
btn_pausar.pack(side=tk.LEFT, padx=5)

log_area = scrolledtext.ScrolledText(root, width=70, height=20)
log_area.pack(padx=10, pady=10)

footer = tk.Label(root, text="Desenvolvido por Nilson Jandre", font=("Arial", 8), fg="gray")
footer.pack(pady=(0, 5))

root.mainloop()
