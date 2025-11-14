from PySide6.QtWidgets import (
    QApplication, QMainWindow,  QTextEdit,
    QToolBar, QMenuBar, QStatusBar, QLabel, QFileDialog, QColorDialog, QFontDialog, QMessageBox, QInputDialog,
    QStatusBar, QDockWidget, QLineEdit, QPushButton, QVBoxLayout, QWidget
)
from PySide6.QtGui import QAction, QIcon, QKeySequence, QTextCursor, QTextImageFormat
from PySide6.QtCore import QSize, Qt
import sys
import os

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Word")

        self.texto_dock = QTextEdit()
        self.setCentralWidget(self.texto_dock)

        self.configurar_menu()

        self.configurar_barra_estado()

        self.configurar_barra_herramientas()

        self.configurar_dock_busqueda()

        self.texto_dock.textChanged.connect(self.actualizar_contador)

    def configurar_menu(self):
        # <-- Barra de Menu -->
        barra_menu = QMenuBar(self)
        Archivo = barra_menu.addMenu("&Archivo")
        Editar = barra_menu.addMenu("&Editar")
        Search_Replace = barra_menu.addMenu("&Buscar y Reemplazar")
        Personalizar = barra_menu.addMenu("Personalizar")
        self.setMenuBar(barra_menu)

        # <-- Acciones para el menu Archivo-->
        accion_Nuevo = QAction(QIcon.fromTheme("document-new"), "Nuevo", self)
        accion_Nuevo.setStatusTip("Crea un nuevo documento.")
        accion_Nuevo.setShortcut(QKeySequence("Ctrl+n"))
        accion_Nuevo.triggered.connect(self.nuevo_documento)
        Archivo.addAction(accion_Nuevo)

        accion_Abrir = QAction(QIcon.fromTheme("document-open"), "Abrir", self)
        accion_Abrir.setStatusTip("Abre un documento existente.")
        accion_Abrir.setShortcut(QKeySequence("Ctrl+o"))
        accion_Abrir.triggered.connect(self.abrir_documento)
        Archivo.addAction(accion_Abrir)

        accion_Guardar = QAction(QIcon.fromTheme("document-save"), "Guardar", self)
        accion_Guardar.setStatusTip("Guarda el documento actual.")
        accion_Guardar.setShortcut(QKeySequence("Ctrl+s"))
        accion_Guardar.triggered.connect(self.guardar_documento)
        Archivo.addAction(accion_Guardar)

        accion_salir = QAction(QIcon.fromTheme("application-exit"), "salir", self)
        accion_salir.setStatusTip("salir de la aplicacion.")
        accion_salir.setShortcut(QKeySequence("Ctrl+q"))
        accion_salir.triggered.connect(self.close)
        Archivo.addAction(accion_salir)

        # <-- Acciones para el menu Editar -->
        accion_Deshacer = QAction(QIcon.fromTheme("edit-undo"), "Deshacer", self)
        accion_Deshacer.setStatusTip("Deshace la última acción.")
        accion_Deshacer.setShortcut(QKeySequence("Ctrl+z"))
        accion_Deshacer.triggered.connect(self.texto_dock.undo)
        Editar.addAction(accion_Deshacer)

        accion_Rehacer = QAction(QIcon.fromTheme("edit-redo"), "Rehacer", self)
        accion_Rehacer.setStatusTip("Rehace la última acción deshecha.")
        accion_Rehacer.setShortcut(QKeySequence("Ctrl+y"))
        accion_Rehacer.triggered.connect(self.texto_dock.redo)
        Editar.addAction(accion_Rehacer)

        accion_pegar = QAction(QIcon.fromTheme("edit-paste"), "Pegar", self)
        accion_pegar.setStatusTip("Pega el contenido del portapapeles.")
        accion_pegar.setShortcut(QKeySequence("Ctrl+v"))
        accion_pegar.triggered.connect(self.texto_dock.paste)
        Editar.addAction(accion_pegar)

        accion_copiar = QAction(QIcon.fromTheme("edit-copy"), "Copiar", self)
        accion_copiar.setStatusTip("Copia el contenido seleccionado al portapapeles.")
        accion_copiar.setShortcut(QKeySequence("Ctrl+c"))
        accion_copiar.triggered.connect(self.texto_dock.copy)
        Editar.addAction(accion_copiar)

        accion_cortar = QAction(QIcon.fromTheme("edit-cut"), "Cortar", self)
        accion_cortar.setStatusTip("Corta el contenido seleccionado al portapapeles.")
        accion_cortar.setShortcut(QKeySequence("Ctrl+x"))
        accion_cortar.triggered.connect(self.texto_dock.cut)
        Editar.addAction(accion_cortar)

        accion_buscar = QAction(QIcon.fromTheme("edit-find"), "Buscar", self)
        accion_buscar.setStatusTip("Buscar texto en el documento.")
        accion_buscar.setShortcut(QKeySequence("Ctrl+f"))
        accion_buscar.triggered.connect(self.buscar_texto)
        Search_Replace.addAction(accion_buscar)

        accion_reemplazar = QAction(QIcon.fromTheme("edit-find-replace"), "Reemplazar", self)
        accion_reemplazar.setStatusTip("Reemplazar texto en el documento.")
        accion_reemplazar.setShortcut(QKeySequence("Ctrl+h"))
        accion_reemplazar.triggered.connect(self.reemplazar_texto)
        Search_Replace.addAction(accion_reemplazar)

        # <-- Acciones para el menu personalizar --> 
        accion_color = QAction("Cambiar color de las letras", self)
        accion_color.triggered.connect(self.cambiar_color_letra)

        accion_letra = QAction("Cambiar tipo de letra", self)
        accion_letra.triggered.connect(self.cambiar_letra)

        accion_fondo = QAction("Cambiar color del fondo", self)
        accion_fondo.triggered.connect(self.cambiar_color_fondo)

        accion_insertar_imagen = QAction("Insertar imagen", self)
        accion_insertar_imagen.setStatusTip("Insertar una imagen en el documento.")
        accion_insertar_imagen.triggered.connect(self.insertar_imagen)

        Personalizar.addAction(accion_color)
        Personalizar.addAction(accion_letra)
        Personalizar.addAction(accion_fondo)
        Personalizar.addAction(accion_insertar_imagen)

        self.acciones = {
            "nuevo": accion_Nuevo,
            "abrir": accion_Abrir,
            "guardar": accion_Guardar,
            "salir": accion_salir,
            "deshacer": accion_Deshacer,
            "rehacer": accion_Rehacer,
            "pegar": accion_pegar,
            "copiar": accion_copiar,
            "cortar": accion_cortar,
            "buscar": accion_buscar,
            "reemplazar": accion_reemplazar,
            "insertar_imagen": accion_insertar_imagen
        }



    def configurar_barra_estado(self):
        # <-- Barra de Estado -->
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        self.barra_estado.showMessage("Listo")
        self.Contar_palabras = QLabel("Palabras: 0")
        self.barra_estado.addPermanentWidget(self.Contar_palabras)



    def configurar_barra_herramientas(self):
        # <-- Barra de Herramientas -->
        barra_herramientas = QToolBar("Barra principal", self)
        barra_herramientas.setIconSize(QSize(32, 32))
        self.addToolBar(barra_herramientas)

        for accion in self.acciones.values():
            barra_herramientas.addAction(accion)



    def configurar_dock_busqueda(self):
        # <-- Panel lateral de búsqueda/reemplazo -->
        self.dock_busqueda = QDockWidget("Buscar/Reemplazar", self)
        self.widget_busqueda = QWidget()
        layout_busqueda = QVBoxLayout(self.widget_busqueda)

        self.caja_buscar = QLineEdit()
        self.caja_buscar.setPlaceholderText("Texto a buscar...")
        self.caja_reemplazar = QLineEdit()
        self.caja_reemplazar.setPlaceholderText("Reemplazar con...")

        boton_buscar = QPushButton("Buscar siguiente")
        boton_reemplazar = QPushButton("Reemplazar")
        boton_todo = QPushButton("Reemplazar todo")

        layout_busqueda.addWidget(self.caja_buscar)
        layout_busqueda.addWidget(self.caja_reemplazar)
        layout_busqueda.addWidget(boton_buscar)
        layout_busqueda.addWidget(boton_reemplazar)
        layout_busqueda.addWidget(boton_todo)

        self.dock_busqueda.setWidget(self.widget_busqueda)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_busqueda)
        self.dock_busqueda.hide()

        boton_buscar.clicked.connect(self.buscar_siguiente)
        boton_reemplazar.clicked.connect(self.reemplazar_una)
        boton_todo.clicked.connect(self.reemplazar_todo)


    def nuevo_documento(self):
        self.texto_dock.clear()
        self.barra_estado.showMessage("Nuevo documento creado", 2000)

    def abrir_documento(self):
        archivo = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivo de text (*.txt);;Todos los archivos (*)")
        if archivo[0]:
            with open(archivo[0], "r", encoding="utf-8") as f:
                self.texto_dock.setText(f.read())
                self.barra_estado.showMessage("Archivo abierto con exito", 3000)

    def guardar_documento(self):
        ruta = QFileDialog.getSaveFileName(self, "Guardad archivo", "", "Archivo de textp (*.txt);;Todos los archivos (*)")
        if ruta[0]:
            with open(ruta[0], "w") as archivo:
                archivo.write(self.texto_dock.toPlainText())
                QMessageBox.information(self, "Guardar archivo", f"Archivo guardado en:\n{ruta}")
                self.barra_estado.showMessage("Archivo guardado con exito", 3000)

    def cambiar_color_letra(self):
        color = QColorDialog.getColor()
        if (color.isValid()):
            self.texto_dock.setTextColor(color)
            self.barra_estado.showMessage(f"color de texto cambiado {color.name()}", 3000)

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.texto_dock.setStyleSheet(f"QTextEdit {{ background-color: {color.name()}; }}")
            self.barra_estado.showMessage(f"Color de fondo del editor cambiado a {color.name()}", 3000)

    def cambiar_letra(self):
        letra_actual = self.texto_dock.currentFont() 
        ok, nueva_letra = QFontDialog.getFont(letra_actual, self)
        if ok:
            self.texto_dock.setFont(nueva_letra)
            self.barra_estado.showMessage(f"Letra cambiada {nueva_letra.family()}", 3000)

    def actualizar_contador(self):
        cursor = self.texto_dock.toPlainText().strip().split()
        cantidad = len(cursor)
        self.Contar_palabras.setText(f"palabras: {cantidad}")

    def buscar_texto(self):
        self.dock_busqueda.show()
        self.barra_estado.showMessage("Panel de búsqueda abierto", 2000)

    def reemplazar_texto(self):
        self.dock_busqueda.show()
        self.barra_estado.showMessage("Panel de reemplazo abierto", 2000)

    def insertar_imagen(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.bmp *.gif)")
        if ruta and os.path.exists(ruta):
            cursor = self.texto_dock.textCursor()
            formato = QTextImageFormat()
            formato.setName(ruta)
            cursor.insertImage(formato)
            self.barra_estado.showMessage("Imagen insertada con exito. ", 3000)

    def buscar_siguiente(self):
        texto = self.caja_buscar.text()
        if not texto:
            return
        if not self.texto_dock.find(texto):
            self.texto_dock.moveCursor(QTextCursor.Start)
            if not self.texto_dock.find(texto):
                QMessageBox.information(self, "Buscar", "No se encontró el texto.")

    def reemplazar_una(self):
        texto = self.caja_buscar.text()
        nuevo = self.caja_reemplazar.text()
        if not texto:
            return
        cursor = self.texto_dock.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == texto:
            cursor.insertText(nuevo)
            self.buscar_siguiente()

    def reemplazar_todo(self):
        texto = self.caja_buscar.text()
        nuevo = self.caja_reemplazar.text()
        if not texto:
            return
        contenido = self.texto_dock.toPlainText()
        ocurrencias = contenido.count(texto)
        self.texto_dock.setPlainText(contenido.replace(texto, nuevo))
        QMessageBox.information(self, "Reemplazar todo", f"Reemplazadas {ocurrencias} ocurrencias.")


if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.resize(800, 600)
    ventana1.show()
    app.exec()