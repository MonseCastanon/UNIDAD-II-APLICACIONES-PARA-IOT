# INSTRUMENTO DE EVALUACIÓN UNIDAD II APLICACIONES PARA IOT
---

## 📌 Información General  
| **🔹 Campo**           | **📝 Información**                                  |
|----------------------|-------------------------------------------------|
| **👤 Nombre**        | Monserrat Guadalupe Castañon Sánchez           |
| **📝 Grupo**        | GDS0653                                         |
| **📚 Materia**      | Aplicaciones para IoT                         |
| **📖 Unidad**       | 2                          |

---

## 🎯 **Objetivo**  
✍️ *El objetivo de este repositorio es mostrar la funcionalidad y la creación del código en pyhton para la realización de videos
de evidencia para los conocimientos necesarios para acreditar la mataria de Aplicaciones para IoT*

---

## 🖼️ **Multimedia**  
### 🎥 Video Explicativo  
📌 *(Coloca aquí un enlace o incrusta un video explicativo.)*  
| **🎥 Video**           | **📝 Información**                           | **🖼️ Imagen circuito** |
|----------------------|-------------------------------------------------|-------------------------|
| **👤 Nombre**        | Monserrat Guadalupe Castañon Sánchez           |      |
| **📝 Grupo**        | GDS0653                                         |      |
| **📚 Materia**      | Aplicaciones para IoT                           |      |
| **📖 Unidad**       | 2                                               |      |


| #  | Imagen                               | Sensor                                   | Sesión |
|----|--------------------------------------|------------------------------------------|-----|
| 1  | ![KY-003]("https://uelectronics.com/wp-content/uploads/2017/06/AR0024-Modulo-KY-004-Sensor-Push-Boton_v2-min-768x768") | KY-003 Sensor de Efecto Hall             | 4   |
| 2  | ![image](<img src="..." width=100>) | KY-004 Módulo Push Botón                 | 3   |
| 3  | ![image](https://github.com/user-attachments/assets/52cdaf6b-7dd8-4c6e-952e-3fafe42e2049) | KY-005 Sensor Infrarrojo                 | 4   |
| 4  | ![image](<img src="..." width=100>) | KY-008 Módulo LED Láser                  | 3   |
| 5  | ![image](https://github.com/user-attachments/assets/035856d3-291c-4253-956e-621778495b0d) | KY-012 Módulo Buzzer Activo              | 4   |
| 6  | ![image](https://github.com/user-attachments/assets/87bd83f8-38e3-4186-a92f-96f8566b4be9) | KY-010 Módulo Foto Interruptor           | 5   |
| 7  | ![image](<img src="..." width=100>) | KY-019 Módulo de 1 Relevador             | 5   |
| 8  | ![image](https://github.com/user-attachments/assets/0d2c5534-034d-45bd-8e5b-9456a08be7ed) | KY-021 Módulo Mini Interruptor Magnético | 6   |
| 9  | ![image](<img src="..." width=100>) | KY-022 Módulo LED Infrarrojo Receptor    | 6   |
| 10 | ![image](<img src="..." width=100>) | KY-024 Sensor de Campo Magnético         | 6   |
| 11 | ![image](<img src="..." width=100>) | KY-026 Sensor de Flama                   | 7   |
| 12 | ![image](https://github.com/user-attachments/assets/025d9232-326f-461c-91f8-f10f3808ac07) | KY-027 Módulo Luminoso de Inclinación    | 1   |
| 13 | ![image](https://github.com/user-attachments/assets/f973be90-dd24-4441-ab0b-07d8f0a62d00) | KY-028 Sensor de Temperatura Digital     | 2   |
| 14 | ![image](<img src="..." width=100>) | KY-033 Sensor de Línea                   | 8   |
| 15 | ![image](<img src="..." width=100>) | KY-035 Sensor Efecto Hall Análogo        | 8   |
| 16 | ![image](https://github.com/user-attachments/assets/fdd991cc-e561-4697-8c3a-7a99da213b51) | KY-037 Módulo Micrófono Sensible         | 1   |
| 17 | ![image](<img src="..." width=100>) | KY-040 Módulo Encoder                    | 9   |
| 18 | ![image](<img src="..." width=100>) | HC-SR04                                  | 9   |
| 19 | ![image](<img src="..." width=100>) | Motor vibración                          | 9   |

| #  | Imagen                               | Sensor                                   | Sesión |
|----|--------------------------------------|------------------------------------------|-----|
| 1 | ![image](<img src="..." width=100>) | MQ-2                          | 9   |
| 2 | ![image](<img src="..." width=100>) | MQ-3                          | 9   |
| 3 | ![image](<img src="..." width=100>) | MQ-4                          | 9   |
| 4 | ![image](<img src="..." width=100>) | MQ-5                          | 9   |
| 5 | ![image](<img src="..." width=100>) | MQ-6                          | 9   |
| 6 | ![image](<img src="..." width=100>) | MQ-8                          | 9   |
| 7 | ![image](https://github.com/user-attachments/assets/defc9c2d-77eb-48b3-8a88-5609182723e6) | MQ-9                          | 9   |
| 8 | ![image](<img src="..." width=100>) | MQ-135                          | 9   |

### 🖼️ Imágenes  
📌 *(Coloca aquí capturas o imágenes relevantes del proyecto.)*  

---

## 🐍 **Código en Python**  
```python
# Ejemplo de código en Python
import time

def cuenta_regresiva(n):
    while n > 0:
        print(f"⏳ Tiempo restante: {n} segundos")
        time.sleep(1)
        n -= 1
    print("🚀 ¡Despegue!")

# Llamada a la función
cuenta_regresiva(5)
```

---

## 📝 **Conclusión**  
✍️ *El trabajo en sí estuvo un poco complicado porque algunos sensores no funcionaban correctamente pero también es culpa de los estudiantes que los utilizaban porque algunos no cuidaban en cómo los conectaba o en como los desconectaban. Con mi compañera me acomodé muy bien ya que logramos tener todos los sensores a excepción de un MQ de Zinc porque ninguna de las dos consiguió a esperanza de que alguién trajera una barra de Zinc pero por lo visto todos los demás estudiantes pensaron igual y nadie llegó con Zinc. Pero mi compañera hizo muy bien su trabajo y aunque se le complicó un poco logró a echar a andar todos los sensores que le tocaban. Mi desarrollo fue bueno ya que stuve al pendiente de que todo estuviera en orden y llevar control de todos los sensores que tocaban y que llevábamos. Fue muy interesante esta unidad*  

---

✨ *¡Gracias por leer este repositorio! Espero que sea de utilidad.* 😊
