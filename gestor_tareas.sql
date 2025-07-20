create table tareas
(
    id            int auto_increment
        primary key,
    titulo        varchar(100)                                                        null,
    resumen       text                                                                null,
    estado        enum ('Por hacer', 'En revisión', 'Finalizado') default 'Por hacer' null,
    fecha_inicio  date                                                                null,
    fecha_entrega date                                                                null,
    hora_entrega  time                                                                null,
    detalles      text                                                                NULL,
    color         varchar(7) DEFAULT '#2196F3'
);


