-- CONFIGURACIÓN
PRAGMA foreign_keys = ON;

-- CREACIÓN DE TABLAS
CREATE TABLE Miembro (
    id_miembro INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_completo TEXT NOT NULL,
    telefono TEXT NOT NULL
);

CREATE TABLE Clase (
    id_clase INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_clase TEXT NOT NULL,
    dia_semana TEXT NOT NULL,
    horario TEXT NOT NULL
);

CREATE TABLE Inscripcion (
    miembro_id INTEGER NOT NULL,
    clase_id INTEGER NOT NULL,
    PRIMARY KEY (miembro_id, clase_id),
    FOREIGN KEY (miembro_id) REFERENCES Miembro(id_miembro),
    FOREIGN KEY (clase_id) REFERENCES Clase(id_clase)
);

-- INSERCIÓN DE DATOS
INSERT INTO Miembro (nombre_completo, telefono) VALUES 
('Ana Perez', '809-555-0101'), ('Jose Luis', '809-555-0102'),
('Maria Garcia', '809-555-0103'), ('Carlos Diaz', '809-555-0104'),
('Lucia Gomez', '809-555-0105');

INSERT INTO Clase (nombre_clase, dia_semana, horario) VALUES 
('Yoga', 'Lunes', '08:00 AM'), ('Zumba', 'Martes', '06:00 PM'),
('Spinning', 'Miercoles', '07:00 PM'), ('Boxeo', 'Jueves', '05:00 PM'),
('Pilates', 'Viernes', '09:00 AM');

INSERT INTO Inscripcion (miembro_id, clase_id) VALUES (1,1), (2,2), (3,3), (4,4), (5,5);