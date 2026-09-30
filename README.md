# PARCIAL CORTE 2 MICROS SAMUEL CASTRO - OSCAR JUNCO - NICOLAS ROZO

En este escrito se resumirá el funcionamiento general del proyecto el cual incluye:
- Maqueta funcional 3d en pybullet
- diagrama de bloques que resume el funcionamiento generla del sistema
- Bosquejo del esquema eléctrico
- App en streamlit vinculada con esp32

El esquema general de como funcionará la maqueta se puede observar en el siguiente video: https://drive.google.com/file/d/1PH5Jgtv4FQs_7Nv_Evh7C5i0IYT5XCkd/view?usp=sharing
en él se puede observar el modelado 3D y una simulación del funcionamiento por medio de Pybullet, en él se evidencia como el sistema clasificara las monedas dependiendo de su denominación, además este sistema cuenta con una combinación de teclas que permite ingresar monedas adicionales a las que se ven al inicio las cuales son predeterminadas. Este video también simula de forma practica el movimiento del carro transportador, el cual se desplaza por medio de algunos obstaculos.
Esta maqueta 3D se vincula con un app en stream lit la cual contiene una vinculación por wifi a la ESP-32 la cual se encarga de procesar los datos que el archivo urdf extrae del funcionamiento de la maqueta en formato .json . csv, los cuales contienen el conteo de las monedas por denominacion, recorriedo del carro y demas funciones que se pueden evidenciar en las siguientes imagenes y en el archivo cargado en el repositorio llamado app.py. 
<img width="1817" height="963" alt="Captura de pantalla 2026-09-29 233025" src="https://github.com/user-attachments/assets/6ff584d2-93cd-4ef8-9b22-5bc6651d98af" />
<img width="1841" height="916" alt="image" src="https://github.com/user-attachments/assets/17096242-d62b-4b87-b7de-35233e4fb638" />

Finalmente podemos evidenciar en la siguiente imagen el diagrama de bloques que resume el funcionamiento generla del proyecto:
<img width="1062" height="570" alt="Captura de pantalla 2026-09-29 231457" src="https://github.com/user-attachments/assets/4406793a-455f-4b69-861c-1afa5f2f4193" />
Y el boceto primitivo del modelo CAD del proyecto:
<img width="775" height="446" alt="Captura de pantalla 2026-09-29 231019" src="https://github.com/user-attachments/assets/9e57b9c9-148c-41c5-9122-9d81f32a6b8f" />

En este repositorio se incluyen los archivos del proyecto, el urdf de la maqueta 3d, el app.py de la aplicación en streamlit y el codigo cargado a la ESP-32

