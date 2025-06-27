create table usuarios
(
    id       int auto_increment
        primary key,
    nombre   varchar(50)  null,
    apellido varchar(50)  null,
    telefono varchar(20)  null,
    correo   varchar(100) null
);

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
    detalles      text                                                                null,
    usuario_id    int                                                                 null,
    constraint tareas_ibfk_1
        foreign key (usuario_id) references usuarios (id)
);

create index usuario_id
    on tareas (usuario_id);


