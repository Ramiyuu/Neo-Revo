import os
import shutil
import platform
import subprocess
import ctypes
import glob
import webbrowser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                             QProgressBar, QLabel, QTextEdit, QMessageBox, QInputDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class AppCleanerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NeoRevo')
        self.setWindowIcon(QIcon('ramiyuuico.ico'))
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()

        self.label = QLabel("Escolha uma ação:", self)
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.clean_button = QPushButton('Iniciar Limpeza', self)
        self.clean_button.setStyleSheet("background-color: green; color: white;")
        self.clean_button.clicked.connect(self.start_cleaning)
        layout.addWidget(self.clean_button)

        self.uninstall_button = QPushButton('Desinstalar Aplicativo', self)
        self.uninstall_button.setStyleSheet("background-color: green; color: white;")
        self.uninstall_button.clicked.connect(self.uninstall_application)
        layout.addWidget(self.uninstall_button)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        self.instagram_button = QPushButton(self)
        self.instagram_button.setIcon(QIcon('instagram_logo.png'))
        self.instagram_button.setIconSize(QSize(64, 64))
        self.instagram_button.clicked.connect(self.open_instagram)
        layout.addWidget(self.instagram_button)

        self.instagram_label = QLabel("Créditos no botão acima", self)
        layout.addWidget(self.instagram_label)

        self.close_button = QPushButton('Fechar', self)
        self.close_button.setStyleSheet("background-color: red; color: white;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        widget.setLayout(layout)

    def append_text(self, message):
        self.text_edit.append(message)

    def ask_confirmation(self, question_text):
        reply = QMessageBox.question(self, 'Confirmação', question_text,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def get_input(self, prompt_text):
        text, ok = QInputDialog.getText(self, 'Entrada Necessária', prompt_text)
        if ok and text:
            return text
        return None

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            self.append_text(f"Comando executado: {command}")
            self.append_text(result.stdout)
        except subprocess.CalledProcessError as e:
            self.append_text(f"Erro ao executar comando {command}: {e}")
            self.append_text(e.output)

    def clear_browser_data(self):
        if platform.system() != "Windows":
            QMessageBox.critical(None, "Erro", "Este script é compatível apenas com sistemas Windows.")
            return

        self.run_command("taskkill /F /IM chrome.exe")
        self.run_command("taskkill /F /IM msedge.exe")

        chrome_user_data_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
        edge_user_data_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data')

        self.delete_directory(chrome_user_data_path)
        self.delete_directory(edge_user_data_path)

        self.append_text("Todos os dados dos navegadores foram apagados com sucesso.")

    def delete_directory(self, path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                self.append_text(f"Diretório excluído: {path}")
            else:
                self.append_text(f"Diretório não encontrado: {path}")
        except Exception as e:
            self.append_text(f"Erro ao excluir {path}: {e}")

    def delete_all_in_directory(self, path):
        try:
            if os.path.exists(path):
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                        self.append_text(f"Excluído: {file_path}")
                    except Exception as e:
                        self.append_text(f"Erro ao excluir {file_path}: {e}")
            else:
                self.append_text(f"Diretório não encontrado: {path}")
        except Exception as e:
            self.append_text(f"Erro ao acessar {path}: {e}")

    def clear_thumbnail_cache(self):
        thumbnail_cache_path = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer')
        try:
            for item in os.listdir(thumbnail_cache_path):
                if item.startswith("thumbcache"):
                    item_path = os.path.join(thumbnail_cache_path, item)
                    os.remove(item_path)
                    self.append_text(f"Excluído cache de miniatura: {item_path}")
        except Exception as e:
            self.append_text(f"Erro ao limpar cache de miniaturas: {e}")

    def run_chkdsk_cleanup(self):
        self.run_command("chkdsk /f /scan")

    def delete_memory_dump_files(self):
        dump_files_path = os.path.expandvars(r'%SystemRoot%\Minidump')
        self.delete_directory(dump_files_path)

    def delete_temp_files(self):
        temp_path = os.path.expandvars(r'%TEMP%')
        self.delete_all_in_directory(temp_path)

        windows_temp_path = r'C:\Windows\Temp'
        self.delete_all_in_directory(windows_temp_path)

    def clear_clipboard(self):
        self.run_command("echo off | clip")
        self.append_text("Área de transferência esvaziada.")

    def clear_start_menu_records(self):
        start_menu_path = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs')
        self.delete_directory(start_menu_path)

    def clear_recent_folders_history(self):
        recent_folders_path = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations')
        self.delete_directory(recent_folders_path)

    def clear_open_save_history(self):
        open_save_path = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent')
        self.delete_directory(open_save_path)

    def clear_regedit_history(self):
        self.run_command(r'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Applets\Regedit" /v LastKey /f')

    def clear_notepad_recent_files(self):
        self.run_command(r'reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Applets\Notepad" /v "Recent File List" /f')

    def clear_recent_documents(self):
        recent_documents_path = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent')
        self.delete_directory(recent_documents_path)

    def empty_recycle_bin(self):
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 3)
            self.append_text("Lixeira esvaziada.")
        except Exception as e:
            self.append_text(f"Erro ao esvaziar a lixeira: {e}")

    def clear_downloads_folder(self):
        downloads_path = os.path.expandvars(r'%USERPROFILE%\Downloads')
        self.delete_all_in_directory(downloads_path)

    def clear_documents_folder(self):
        documents_path = os.path.expandvars(r'%USERPROFILE%\Documents')
        self.delete_all_in_directory(documents_path)

    def clear_videos_folder(self):
        videos_path = os.path.expandvars(r'%USERPROFILE%\Videos')
        self.delete_all_in_directory(videos_path)

    def clear_pictures_folder(self):
        pictures_path = os.path.expandvars(r'%USERPROFILE%\Pictures')
        self.delete_all_in_directory(pictures_path)

    def clear_music_folder(self):
        music_path = os.path.expandvars(r'%USERPROFILE%\Music')
        self.delete_all_in_directory(music_path)

    def perform_all_cleanups(self):
        if not self.ask_confirmation("Você tem certeza de que deseja realizar todas as operações de limpeza?"):
            self.append_text("Operação de limpeza cancelada pelo usuário.")
            return

        self.clear_browser_data()
        self.clear_thumbnail_cache()
        self.run_chkdsk_cleanup()
        self.delete_memory_dump_files()
        self.delete_temp_files()
        self.clear_clipboard()
        self.clear_start_menu_records()
        self.clear_recent_folders_history()
        self.clear_open_save_history()
        self.clear_regedit_history()
        self.clear_notepad_recent_files()
        self.clear_recent_documents()
        self.empty_recycle_bin()
        self.clear_downloads_folder()
        self.clear_documents_folder()
        self.clear_videos_folder()
        self.clear_pictures_folder()
        self.clear_music_folder()

        self.append_text("Todas as operações de limpeza foram concluídas com sucesso.")

    def start_cleaning(self):
        self.progress_bar.setValue(0)
        self.perform_all_cleanups()
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Concluído", "Limpeza concluída com sucesso!")

    def uninstall_application(self):
        app_name = self.get_input('Digite o nome do aplicativo:')
        if app_name:
            self.progress_bar.setValue(0)
            if uninstall_application(app_name):
                remove_application_files(app_name)
                remove_similar_files(app_name)
                QMessageBox.information(self, "Concluído", f"Desinstalação e remoção de arquivos para {app_name} concluídas com sucesso!")
            else:
                QMessageBox.warning(self, "Falha", f"Não foi possível desinstalar {app_name}.")
            self.progress_bar.setValue(100)

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/f3r.in4k/")

def uninstall_application(app_name):
    try:
        subprocess.run(f"wmic product where name='{app_name}' call uninstall", shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def remove_application_files(app_name):
    paths = [
        os.path.expandvars(f'%PROGRAMFILES%\\{app_name}'),
        os.path.expandvars(f'%PROGRAMFILES(X86)%\\{app_name}'),
        os.path.expandvars(f'%LOCALAPPDATA%\\{app_name}')
    ]
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

def remove_similar_files(app_name):
    paths = glob.glob(f"C:\\*{app_name}*")
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)

if __name__ == '__main__':
    app = QApplication([])
    window = AppCleanerWindow()
    window.show()
    app.exec_()
