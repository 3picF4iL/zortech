CREATE TABLE brands
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE colors
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE customers
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT NOT NULL
);

CREATE TABLE models
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brands (id)
);

CREATE TABLE tickets
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_creation TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    customer_id INTEGER,
    car_id INTEGER,
    notes TEXT,
    status INTEGER,
    FOREIGN KEY (car_id) REFERENCES cars (id),
    FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE VIEW view_get_color AS
SELECT name
FROM colors
/* view_get_color(name) */;

CREATE VIEW view_get_brand AS
SELECT name
FROM brands
/* view_get_brand(name) */;

CREATE TABLE IF NOT EXISTS "cars" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    brand_id INTEGER,
    model_id INTEGER,
    color_id INTEGER,
    year INTEGER,
    vin TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers (id),
    FOREIGN KEY (brand_id) REFERENCES brands (id),
    FOREIGN KEY (model_id) REFERENCES models (id),
    FOREIGN KEY (model_id) REFERENCES models (id),
    FOREIGN KEY (color_id) REFERENCES colors (id)
);

-- Insert colors lowercase
INSERT INTO colors (name) VALUES ('black');
INSERT INTO colors (name) VALUES ('white');
INSERT INTO colors (name) VALUES ('red');
INSERT INTO colors (name) VALUES ('blue');
INSERT INTO colors (name) VALUES ('green');
INSERT INTO colors (name) VALUES ('yellow');
INSERT INTO colors (name) VALUES ('orange');
INSERT INTO colors (name) VALUES ('purple');
INSERT INTO colors (name) VALUES ('pink');
INSERT INTO colors (name) VALUES ('brown');
INSERT INTO colors (name) VALUES ('gray');
INSERT INTO colors (name) VALUES ('silver');
INSERT INTO colors (name) VALUES ('gold');
INSERT INTO colors (name) VALUES ('beige');
INSERT INTO colors (name) VALUES ('bronze');
INSERT INTO colors (name) VALUES ('copper');
INSERT INTO colors (name) VALUES ('tan');
INSERT INTO colors (name) VALUES ('maroon');
INSERT INTO colors (name) VALUES ('teal');
INSERT INTO colors (name) VALUES ('turquoise');
INSERT INTO colors (name) VALUES ('lavender');
INSERT INTO colors (name) VALUES ('other');

-- Insert brands lowercase
INSERT INTO brands (name) VALUES ('acura');
INSERT INTO brands (name) VALUES ('alfa romeo');
INSERT INTO brands (name) VALUES ('audi');
INSERT INTO brands (name) VALUES ('bmw');
INSERT INTO brands (name) VALUES ('buick');
INSERT INTO brands (name) VALUES ('cadillac');
INSERT INTO brands (name) VALUES ('chevrolet');
INSERT INTO brands (name) VALUES ('chrysler');
INSERT INTO brands (name) VALUES ('dodge');
INSERT INTO brands (name) VALUES ('fiat');
INSERT INTO brands (name) VALUES ('ford');
INSERT INTO brands (name) VALUES ('gmc');
INSERT INTO brands (name) VALUES ('honda');
INSERT INTO brands (name) VALUES ('hyundai');
INSERT INTO brands (name) VALUES ('infiniti');
INSERT INTO brands (name) VALUES ('jaguar');
INSERT INTO brands (name) VALUES ('jeep');
INSERT INTO brands (name) VALUES ('kia');
INSERT INTO brands (name) VALUES ('land rover');
INSERT INTO brands (name) VALUES ('lexus');
INSERT INTO brands (name) VALUES ('lincoln');
INSERT INTO brands (name) VALUES ('mazda');
INSERT INTO brands (name) VALUES ('mercedes-benz');
INSERT INTO brands (name) VALUES ('mini');
INSERT INTO brands (name) VALUES ('mitsubishi');
INSERT INTO brands (name) VALUES ('nissan');
INSERT INTO brands (name) VALUES ('porsche');
INSERT INTO brands (name) VALUES ('ram');
INSERT INTO brands (name) VALUES ('subaru');
INSERT INTO brands (name) VALUES ('tesla');
INSERT INTO brands (name) VALUES ('toyota');
INSERT INTO brands (name) VALUES ('volkswagen');
INSERT INTO brands (name) VALUES ('volvo');

-- Insert models lowercase
INSERT INTO models (brand_id, name) VALUES (1, 'ilx');
INSERT INTO models (brand_id, name) VALUES (1, 'mdx');
INSERT INTO models (brand_id, name) VALUES (1, 'nsx');
INSERT INTO models (brand_id, name) VALUES (1, 'rdx');
INSERT INTO models (brand_id, name) VALUES (1, 'rlx');
INSERT INTO models (brand_id, name) VALUES (1, 'tlx');

-- Alfa Romeo (brand_id: 2)
INSERT INTO models (brand_id, name) VALUES (2, 'giulia');
INSERT INTO models (brand_id, name) VALUES (2, 'stelvio');
INSERT INTO models (brand_id, name) VALUES (2, '4c');
INSERT INTO models (brand_id, name) VALUES (2, '4c spider');
INSERT INTO models (brand_id, name) VALUES (2, 'gtv');
INSERT INTO models (brand_id, name) VALUES (2, 'spider');
INSERT INTO models (brand_id, name) VALUES (2, 'brera');
INSERT INTO models (brand_id, name) VALUES (2, 'mito');
INSERT INTO models (brand_id, name) VALUES (2, '156');
INSERT INTO models (brand_id, name) VALUES (2, '159');
INSERT INTO models (brand_id, name) VALUES (2, 'giulietta');

INSERT INTO models (brand_id, name) VALUES (3, 'a3');
INSERT INTO models (brand_id, name) VALUES (3, 'a4');
INSERT INTO models (brand_id, name) VALUES (3, 'a5');
INSERT INTO models (brand_id, name) VALUES (3, 'a6');
INSERT INTO models (brand_id, name) VALUES (3, 'a7');
INSERT INTO models (brand_id, name) VALUES (3, 'a8');
INSERT INTO models (brand_id, name) VALUES (3, 'q3');
INSERT INTO models (brand_id, name) VALUES (3, 'q5');
INSERT INTO models (brand_id, name) VALUES (3, 'q7');
INSERT INTO models (brand_id, name) VALUES (3, 'q8');
INSERT INTO models (brand_id, name) VALUES (3, 'rs3');
INSERT INTO models (brand_id, name) VALUES (3, 'rs5');
INSERT INTO models (brand_id, name) VALUES (3, 'rs7');
INSERT INTO models (brand_id, name) VALUES (3, 's3');
INSERT INTO models (brand_id, name) VALUES (3, 's4');
INSERT INTO models (brand_id, name) VALUES (3, 's5');
INSERT INTO models (brand_id, name) VALUES (3, 's6');
INSERT INTO models (brand_id, name) VALUES (3, 's7');
INSERT INTO models (brand_id, name) VALUES (3, 's8');
INSERT INTO models (brand_id, name) VALUES (3, 'tt');

INSERT INTO models (brand_id, name) VALUES (4, '1 series');
INSERT INTO models (brand_id, name) VALUES (4, '2 series');
INSERT INTO models (brand_id, name) VALUES (4, '3 series');
INSERT INTO models (brand_id, name) VALUES (4, '4 series');
INSERT INTO models (brand_id, name) VALUES (4, '5 series');
INSERT INTO models (brand_id, name) VALUES (4, '6 series');
INSERT INTO models (brand_id, name) VALUES (4, '7 series');
INSERT INTO models (brand_id, name) VALUES (4, '8 series');
INSERT INTO models (brand_id, name) VALUES (4, 'i3');
INSERT INTO models (brand_id, name) VALUES (4, 'i8');
INSERT INTO models (brand_id, name) VALUES (4, 'm2');
INSERT INTO models (brand_id, name) VALUES (4, 'm3');
INSERT INTO models (brand_id, name) VALUES (4, 'm4');
INSERT INTO models (brand_id, name) VALUES (4, 'm5');
INSERT INTO models (brand_id, name) VALUES (4, 'm6');
INSERT INTO models (brand_id, name) VALUES (4, 'x1');
INSERT INTO models (brand_id, name) VALUES (4, 'x2');
INSERT INTO models (brand_id, name) VALUES (4, 'x3');
INSERT INTO models (brand_id, name) VALUES (4, 'x4');
INSERT INTO models (brand_id, name) VALUES (4, 'x5');
INSERT INTO models (brand_id, name) VALUES (4, 'x6');
INSERT INTO models (brand_id, name) VALUES (4, 'x7');
INSERT INTO models (brand_id, name) VALUES (4, 'z4');

INSERT INTO models (brand_id, name) VALUES (5, 'cascada');
INSERT INTO models (brand_id, name) VALUES (5, 'encore');
INSERT INTO models (brand_id, name) VALUES (5, 'enclave');
INSERT INTO models (brand_id, name) VALUES (5, 'envision');
INSERT INTO models (brand_id, name) VALUES (5, 'lacrosse');
INSERT INTO models (brand_id, name) VALUES (5, 'regal');
INSERT INTO models (brand_id, name) VALUES (5, 'verano');

INSERT INTO models (brand_id, name) VALUES (6, 'at4');
INSERT INTO models (brand_id, name) VALUES (6, 'ct4');
INSERT INTO models (brand_id, name) VALUES (6, 'ct5');
INSERT INTO models (brand_id, name) VALUES (6, 'ct6');
INSERT INTO models (brand_id, name) VALUES (6, 'ct6-v');
INSERT INTO models (brand_id, name) VALUES (6, 'escalade');
INSERT INTO models (brand_id, name) VALUES (6, 'xt4');
INSERT INTO models (brand_id, name) VALUES (6, 'xt5');
INSERT INTO models (brand_id, name) VALUES (6, 'xt6');
INSERT INTO models (brand_id, name) VALUES (6, 'xts');

INSERT INTO models (brand_id, name) VALUES (7, 'blazer');
INSERT INTO models (brand_id, name) VALUES (7, 'camaro');
INSERT INTO models (brand_id, name) VALUES (7, 'colorado');
INSERT INTO models (brand_id, name) VALUES (7, 'corvette');
INSERT INTO models (brand_id, name) VALUES (7, 'equinox');
INSERT INTO models (brand_id, name) VALUES (7, 'express');
INSERT INTO models (brand_id, name) VALUES (7, 'impala');
INSERT INTO models (brand_id, name) VALUES (7, 'malibu');
INSERT INTO models (brand_id, name) VALUES (7, 'silverado');
INSERT INTO models (brand_id, name) VALUES (7, 'sonic');
INSERT INTO models (brand_id, name) VALUES (7, 'spark');
INSERT INTO models (brand_id, name) VALUES (7, 'suburban');
INSERT INTO models (brand_id, name) VALUES (7, 'tahoe');
INSERT INTO models (brand_id, name) VALUES (7, 'trailblazer');
INSERT INTO models (brand_id, name) VALUES (7, 'traverse');
INSERT INTO models (brand_id, name) VALUES (7, 'trax');
INSERT INTO models (brand_id, name) VALUES (7, 'volt');

INSERT INTO models (brand_id, name) VALUES (8, '300');
INSERT INTO models (brand_id, name) VALUES (8, 'pacifica');
INSERT INTO models (brand_id, name) VALUES (8, 'voyager');

INSERT INTO models (brand_id, name) VALUES (9, 'charger');
INSERT INTO models (brand_id, name) VALUES (9, 'challenger');
INSERT INTO models (brand_id, name) VALUES (9, 'durango');
INSERT INTO models (brand_id, name) VALUES (9, 'journey');

INSERT INTO models (brand_id, name) VALUES (10, '124 spider');
INSERT INTO models (brand_id, name) VALUES (10, '500');
INSERT INTO models (brand_id, name) VALUES (10, '500l');
INSERT INTO models (brand_id, name) VALUES (10, '500x');
INSERT INTO models (brand_id, name) VALUES (10, '500c');
INSERT INTO models (brand_id, name) VALUES (10, '500 abarth');
INSERT INTO models (brand_id, name) VALUES (10, '500 abarth cabrio');
INSERT INTO models (brand_id, name) VALUES (10, '500e');

INSERT INTO models (brand_id, name) VALUES (11, 'bronco');
INSERT INTO models (brand_id, name) VALUES (11, 'c-max');
INSERT INTO models (brand_id, name) VALUES (11, 'e-series');
INSERT INTO models (brand_id, name) VALUES (11, 'e-series cutaway');
INSERT INTO models (brand_id, name) VALUES (11, 'e-series stripped chassis');
INSERT INTO models (brand_id, name) VALUES (11, 'edge');
INSERT INTO models (brand_id, name) VALUES (11, 'escape');
INSERT INTO models (brand_id, name) VALUES (11, 'expedition');
INSERT INTO models (brand_id, name) VALUES (11, 'explorer');
INSERT INTO models (brand_id, name) VALUES (11, 'f-150');
INSERT INTO models (brand_id, name) VALUES (11, 'f-250');
INSERT INTO models (brand_id, name) VALUES (11, 'f-350');
INSERT INTO models (brand_id, name) VALUES (11, 'f-450');
INSERT INTO models (brand_id, name) VALUES (11, 'f-550');
INSERT INTO models (brand_id, name) VALUES (11, 'fiesta');
INSERT INTO models (brand_id, name) VALUES (11, 'flex');
INSERT INTO models (brand_id, name) VALUES (11, 'focus');
INSERT INTO models (brand_id, name) VALUES (11, 'fusion');
INSERT INTO models (brand_id, name) VALUES (11, 'mustang');
INSERT INTO models (brand_id, name) VALUES (11, 'ranger');

INSERT INTO models (brand_id, name) VALUES (12, 'acadia');
INSERT INTO models (brand_id, name) VALUES (12, 'canyon');
INSERT INTO models (brand_id, name) VALUES (12, 'sierra');
INSERT INTO models (brand_id, name) VALUES (12, 'terrain');
INSERT INTO models (brand_id, name) VALUES (12, 'yukon');
INSERT INTO models (brand_id, name) VALUES (12, 'yukon xl');

INSERT INTO models (brand_id, name) VALUES (13, 'accord');
INSERT INTO models (brand_id, name) VALUES (13, 'civic');
INSERT INTO models (brand_id, name) VALUES (13, 'clarity');
INSERT INTO models (brand_id, name) VALUES (13, 'cr-v');
INSERT INTO models (brand_id, name) VALUES (13, 'fit');
INSERT INTO models (brand_id, name) VALUES (13, 'hr-v');
INSERT INTO models (brand_id, name) VALUES (13, 'insight');
INSERT INTO models (brand_id, name) VALUES (13, 'passport');
INSERT INTO models (brand_id, name) VALUES (13, 'pilot');
INSERT INTO models (brand_id, name) VALUES (13, 'ridgeline');

INSERT INTO models (brand_id, name) VALUES (14, 'accent');
INSERT INTO models (brand_id, name) VALUES (14, 'ioniq');
INSERT INTO models (brand_id, name) VALUES (14, 'kona');
INSERT INTO models (brand_id, name) VALUES (14, 'nexo');
INSERT INTO models (brand_id, name) VALUES (14, 'palisade');
INSERT INTO models (brand_id, name) VALUES (14, 'santa fe');
INSERT INTO models (brand_id, name) VALUES (14, 'sonata');
INSERT INTO models (brand_id, name) VALUES (14, 'tucson');
INSERT INTO models (brand_id, name) VALUES (14, 'veloster');

INSERT INTO models (brand_id, name) VALUES (15, 'qx30');
INSERT INTO models (brand_id, name) VALUES (15, 'qx50');
INSERT INTO models (brand_id, name) VALUES (15, 'qx60');
INSERT INTO models (brand_id, name) VALUES (15, 'qx80');

INSERT INTO models (brand_id, name) VALUES (16, 'e-pace');
INSERT INTO models (brand_id, name) VALUES (16, 'f-pace');
INSERT INTO models (brand_id, name) VALUES (16, 'i-pace');
INSERT INTO models (brand_id, name) VALUES (16, 'xe');
INSERT INTO models (brand_id, name) VALUES (16, 'xf');
INSERT INTO models (brand_id, name) VALUES (16, 'xj');

INSERT INTO models (brand_id, name) VALUES (17, 'cherokee');
INSERT INTO models (brand_id, name) VALUES (17, 'compass');
INSERT INTO models (brand_id, name) VALUES (17, 'gladiator');
INSERT INTO models (brand_id, name) VALUES (17, 'grand cherokee');
INSERT INTO models (brand_id, name) VALUES (17, 'renegade');
INSERT INTO models (brand_id, name) VALUES (17, 'wrangler');

INSERT INTO models (brand_id, name) VALUES (18, 'carens');
INSERT INTO models (brand_id, name) VALUES (18, 'forte');
INSERT INTO models (brand_id, name) VALUES (18, 'k5');
INSERT INTO models (brand_id, name) VALUES (18, 'k900');
INSERT INTO models (brand_id, name) VALUES (18, 'niro');
INSERT INTO models (brand_id, name) VALUES (18, 'rio');
INSERT INTO models (brand_id, name) VALUES (18, 'seltos');
INSERT INTO models (brand_id, name) VALUES (18, 'sorento');
INSERT INTO models (brand_id, name) VALUES (18, 'soul');
INSERT INTO models (brand_id, name) VALUES (18, 'sportage');
INSERT INTO models (brand_id, name) VALUES (18, 'stinger');
INSERT INTO models (brand_id, name) VALUES (18, 'telluride');

-- Land Rover (brand_id: 19)
INSERT INTO models (brand_id, name) VALUES (19, 'defender');
INSERT INTO models (brand_id, name) VALUES (19, 'discovery');
INSERT INTO models (brand_id, name) VALUES (19, 'discovery sport');
INSERT INTO models (brand_id, name) VALUES (19, 'freelander');
INSERT INTO models (brand_id, name) VALUES (19, 'range rover');
INSERT INTO models (brand_id, name) VALUES (19, 'range rover evoque');
INSERT INTO models (brand_id, name) VALUES (19, 'range rover sport');
INSERT INTO models (brand_id, name) VALUES (19, 'range rover velar');

-- Lexus (brand_id: 20)
INSERT INTO models (brand_id, name) VALUES (20, 'ct');
INSERT INTO models (brand_id, name) VALUES (20, 'es');
INSERT INTO models (brand_id, name) VALUES (20, 'gs');
INSERT INTO models (brand_id, name) VALUES (20, 'gx');
INSERT INTO models (brand_id, name) VALUES (20, 'is');
INSERT INTO models (brand_id, name) VALUES (20, 'lc');
INSERT INTO models (brand_id, name) VALUES (20, 'ls');
INSERT INTO models (brand_id, name) VALUES (20, 'lx');
INSERT INTO models (brand_id, name) VALUES (20, 'nx');
INSERT INTO models (brand_id, name) VALUES (20, 'rc');
INSERT INTO models (brand_id, name) VALUES (20, 'rx');
INSERT INTO models (brand_id, name) VALUES (20, 'ux');

-- Lincoln (brand_id: 21)
INSERT INTO models (brand_id, name) VALUES (21, 'aviator');
INSERT INTO models (brand_id, name) VALUES (21, 'continental');
INSERT INTO models (brand_id, name) VALUES (21, 'corsair');
INSERT INTO models (brand_id, name) VALUES (21, 'mkc');
INSERT INTO models (brand_id, name) VALUES (21, 'mkt');
INSERT INTO models (brand_id, name) VALUES (21, 'mkz');
INSERT INTO models (brand_id, name) VALUES (21, 'nautilus');
INSERT INTO models (brand_id, name) VALUES (21, 'navigator');

-- Mazda (brand_id: 22)
INSERT INTO models (brand_id, name) VALUES (22, 'cx-3');
INSERT INTO models (brand_id, name) VALUES (22, 'cx-30');
INSERT INTO models (brand_id, name) VALUES (22, 'cx-5');
INSERT INTO models (brand_id, name) VALUES (22, 'cx-8');
INSERT INTO models (brand_id, name) VALUES (22, 'cx-9');
INSERT INTO models (brand_id, name) VALUES (22, 'mazda2');
INSERT INTO models (brand_id, name) VALUES (22, 'mazda3');
INSERT INTO models (brand_id, name) VALUES (22, 'mazda6');
INSERT INTO models (brand_id, name) VALUES (22, 'mx-30');
INSERT INTO models (brand_id, name) VALUES (22, 'mx-5 miata');

-- Mercedes-Benz (brand_id: 23)
INSERT INTO models (brand_id, name) VALUES (23, 'a-class');
INSERT INTO models (brand_id, name) VALUES (23, 'b-class');
INSERT INTO models (brand_id, name) VALUES (23, 'c-class');
INSERT INTO models (brand_id, name) VALUES (23, 'cla');
INSERT INTO models (brand_id, name) VALUES (23, 'cls');
INSERT INTO models (brand_id, name) VALUES (23, 'e-class');
INSERT INTO models (brand_id, name) VALUES (23, 'g-class');
INSERT INTO models (brand_id, name) VALUES (23, 'gl-class');
INSERT INTO models (brand_id, name) VALUES (23, 'gla');
INSERT INTO models (brand_id, name) VALUES (23, 'glb');
INSERT INTO models (brand_id, name) VALUES (23, 'glc');
INSERT INTO models (brand_id, name) VALUES (23, 'gle');
INSERT INTO models (brand_id, name) VALUES (23, 'glk');
INSERT INTO models (brand_id, name) VALUES (23, 'gls');
INSERT INTO models (brand_id, name) VALUES (23, 'gt');
INSERT INTO models (brand_id, name) VALUES (23, 's-class');
INSERT INTO models (brand_id, name) VALUES (23, 'sl');
INSERT INTO models (brand_id, name) VALUES (23, 'slc');
INSERT INTO models (brand_id, name) VALUES (23, 'slk');

-- Mini (brand_id: 24)
INSERT INTO models (brand_id, name) VALUES (24, 'cooper');
INSERT INTO models (brand_id, name) VALUES (24, 'cooper clubman');
INSERT INTO models (brand_id, name) VALUES (24, 'cooper countryman');
INSERT INTO models (brand_id, name) VALUES (24, 'cooper s');
INSERT INTO models (brand_id, name) VALUES (24, 'cooper se');
INSERT INTO models (brand_id, name) VALUES (24, 'john cooper works');

-- Mitsubishi (brand_id: 25)
INSERT INTO models (brand_id, name) VALUES (25, 'eclipse cross');
INSERT INTO models (brand_id, name) VALUES (25, 'lancer');
INSERT INTO models (brand_id, name) VALUES (25, 'mirage');
INSERT INTO models (brand_id, name) VALUES (25, 'outlander');
INSERT INTO models (brand_id, name) VALUES (25, 'outlander sport');
INSERT INTO models (brand_id, name) VALUES (25, 'pajero');

-- Nissan (brand_id: 26)
INSERT INTO models (brand_id, name) VALUES (26, 'altima');
INSERT INTO models (brand_id, name) VALUES (26, 'armada');
INSERT INTO models (brand_id, name) VALUES (26, 'frontier');
INSERT INTO models (brand_id, name) VALUES (26, 'gt-r');
INSERT INTO models (brand_id, name) VALUES (26, 'juke');
INSERT INTO models (brand_id, name) VALUES (26, 'leaf');
INSERT INTO models (brand_id, name) VALUES (26, 'maxima');
INSERT INTO models (brand_id, name) VALUES (26, 'murano');
INSERT INTO models (brand_id, name) VALUES (26, 'pathfinder');
INSERT INTO models (brand_id, name) VALUES (26, 'rogue');
INSERT INTO models (brand_id, name) VALUES (26, 'sentra');
INSERT INTO models (brand_id, name) VALUES (26, 'titan');
INSERT INTO models (brand_id, name) VALUES (26, 'versa');
INSERT INTO models (brand_id, name) VALUES (26, 'x-trail');

-- Porsche (brand_id: 27)
INSERT INTO models (brand_id, name) VALUES (27, '911');
INSERT INTO models (brand_id, name) VALUES (27, 'boxster');
INSERT INTO models (brand_id, name) VALUES (27, 'cayenne');
INSERT INTO models (brand_id, name) VALUES (27, 'cayman');
INSERT INTO models (brand_id, name) VALUES (27, 'macan');
INSERT INTO models (brand_id, name) VALUES (27, 'panamera');
INSERT INTO models (brand_id, name) VALUES (27, 'taycan');

-- Ram (brand_id: 28)
INSERT INTO models (brand_id, name) VALUES (28, '1500');
INSERT INTO models (brand_id, name) VALUES (28, '2500');
INSERT INTO models (brand_id, name) VALUES (28, '3500');
INSERT INTO models (brand_id, name) VALUES (28, 'promaster');
INSERT INTO models (brand_id, name) VALUES (28, 'promaster city');

-- Subaru (brand_id: 29)
INSERT INTO models (brand_id, name) VALUES (29, 'ascent');
INSERT INTO models (brand_id, name) VALUES (29, 'brz');
INSERT INTO models (brand_id, name) VALUES (29, 'crosstrek');
INSERT INTO models (brand_id, name) VALUES (29, 'forester');
INSERT INTO models (brand_id, name) VALUES (29, 'impreza');
INSERT INTO models (brand_id, name) VALUES (29, 'legacy');
INSERT INTO models (brand_id, name) VALUES (29, 'outback');
INSERT INTO models (brand_id, name) VALUES (29, 'wrx');

-- Tesla (brand_id: 30)
INSERT INTO models (brand_id, name) VALUES (30, 'model s');
INSERT INTO models (brand_id, name) VALUES (30, 'model 3');
INSERT INTO models (brand_id, name) VALUES (30, 'model x');
INSERT INTO models (brand_id, name) VALUES (30, 'model y');
INSERT INTO models (brand_id, name) VALUES (30, 'roadster');
INSERT INTO models (brand_id, name) VALUES (30, 'cybertruck');

-- Toyota (brand_id: 31)
INSERT INTO models (brand_id, name) VALUES (31, '4runner');
INSERT INTO models (brand_id, name) VALUES (31, 'avalon');
INSERT INTO models (brand_id, name) VALUES (31, 'camry');
INSERT INTO models (brand_id, name) VALUES (31, 'corolla');
INSERT INTO models (brand_id, name) VALUES (31, 'highlander');
INSERT INTO models (brand_id, name) VALUES (31, 'land cruiser');
INSERT INTO models (brand_id, name) VALUES (31, 'prius');
INSERT INTO models (brand_id, name) VALUES (31, 'rav4');
INSERT INTO models (brand_id, name) VALUES (31, 'sienna');
INSERT INTO models (brand_id, name) VALUES (31, 'supra');
INSERT INTO models (brand_id, name) VALUES (31, 'tacoma');
INSERT INTO models (brand_id, name) VALUES (31, 'tundra');
INSERT INTO models (brand_id, name) VALUES (31, 'yaris');

-- Volkswagen (brand_id: 32)
INSERT INTO models (brand_id, name) VALUES (32, 'atlas');
INSERT INTO models (brand_id, name) VALUES (32, 'beetle');
INSERT INTO models (brand_id, name) VALUES (32, 'golf');
INSERT INTO models (brand_id, name) VALUES (32, 'jetta');
INSERT INTO models (brand_id, name) VALUES (32, 'passat');
INSERT INTO models (brand_id, name) VALUES (32, 'tiguan');
INSERT INTO models (brand_id, name) VALUES (32, 'touareg');
INSERT INTO models (brand_id, name) VALUES (32, 'transporter');


-- Volvo (brand_id: 33)
INSERT INTO models (brand_id, name) VALUES (33, 's60');
INSERT INTO models (brand_id, name) VALUES (33, 's90');
INSERT INTO models (brand_id, name) VALUES (33, 'v60');
INSERT INTO models (brand_id, name) VALUES (33, 'v90');
INSERT INTO models (brand_id, name) VALUES (33, 'xc40');
INSERT INTO models (brand_id, name) VALUES (33, 'xc60');
INSERT INTO models (brand_id, name) VALUES (33, 'xc90');