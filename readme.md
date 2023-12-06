# Proyecto Final Flujo en Redes

## Requerimientos
- Python 3.0 en adelante.
- Gurobi Optimizer version 10.0.3 en adelante

## Uso del programa
Las diferentes versiones del programa estan divididas en por entregas, la entrega final del programa esta 
ubicada en el repositorio bajo el nombre de "Entregable5_j.mejia17-d.ricaurte.ipynb", este programa lee los
datos que se encuentran en los archivos txt, de la carpeta "Sistemas_test" los cuales tienen la información 
del sistema de red de energía electrica que se desea suministrar al modelo. Para correr el programa, primero
se debe de indicar en el atributo file_path, la ruta del archivo local, luego de especifcarlo se deben 
de correr todas las instancias presentadas en el archivo de Jupiter Notebook (.ipynb), este entragara la 
solución de la reconfiguración de la red y en archivos alternos el .lp da las instancias que tomaron lugar al
correr el modelo y el .sol entrega la solución del modelo. Si el modelo es clasificado como infactible, los 
detalles del problema aprecen en un archivo finalizado con .ilp.

Autores: Daniela Ricaurte Echeverry y Juana Mejía Botero
