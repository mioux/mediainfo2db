CREATE TABLE media_file 
(
    media_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    media_filename VARCHAR(2048)
);

CREATE TABLE ref_media_track_type
(
    track_type_id INT UNSIGNED PRIMARY KEY,
    track_type_label VARCHAR(50) NOT NULL
);

INSERT INTO ref_media_track_type
(
    track_type_id,
    track_type_label
)
VALUES
(1, 'Video'),
(2, 'Audio'),
(3, 'Text'),
(4, 'Menu'),
(5, 'General');

CREATE TABLE media_track
(
    media_track INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    track_type_id INT UNSIGNED NOT NULL,
    media_id INT UNSIGNED NOT NULL,
    media_key VARCHAR(100) NOT NULL,
    media_value VARCHAR(512),
    CONSTRAINT fk_media_track_track_type FOREIGN KEY (track_type_id) REFERENCES mediainfo.ref_media_track_type(track_type_id),
    UNIQUE INDEX idx_media_type_key (media_id, track_type_id, media_key)
);