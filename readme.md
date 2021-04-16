# Computer Science HL Final-IA
This Django web application takes a set of students (between 200-216) and distributes them into 8 classes. It does so while making sure gender, islamic and native arabic students are distributed equally between classes.

## Installation

Requires [Django](https://www.djangoproject.com/) to work.

```sh
$ git clone https://github.com/dajkatal/CS-FinalIA.git
$ cd CS-FinalIA
$ pip install -r requirements.txt
$ python manage.py runserver
```

## Database

This app uses MySQL to store the data. For the application to work, the credentials of your own MySQL database need to be put in the [settings.py](https://github.com/dajkatal/CS-FinalIA/blob/master/MiniIA/settings.py#L79) folder.

## Format of DATA
The following data is all fake but has the required structure.

| Powerschool ID | First Name  | Last Name  | Grade 5 | Gender | Social Grouping | ARABIC NATIVE/NON NATIVE | ISLAMIC NATIVE/NON NATIVE | Nationality                            | ELL | SEND | Behavior | HMP | H/L | Friends                                                                                   | Avoid | Additional Notes |
|----------------|-------------|------------|---------|--------|-----------------|--------------------------|---------------------------|----------------------------------------|-----|------|----------|-----|-----|-------------------------------------------------------------------------------------------|-------|------------------|
| 38501308183732 | Carrie      | Scott      | 5GW     | M      | 1               | NN                       | None                      | Armenia                                |     |      |          |     |     | Justin Clowers    Jennifer Dawson    Johnny Brown    Richard Chau    Matthew Sharp        |       |                  |
| 52576046759401 | William     | Castro     | 5NV     | M      | 4               | NN                       | N                         | Equatorial Guinea                      |     |      |          |     |     | Christopher Booth    Kymberly Jones    Mary Caron    Margaret Curry    Christopher Pettis |       |                  |
| 18975338209040 | Kyle        | Gallaway   | 5SZ     | F      | 4               | N                        | None                      | Iraq                                   |     |      |          |     |     | Diana Paulding    Bonnie Beekman    William Gaier    Brian Barrett    Henry Lowery        |       |                  |
| 37783253869087 | Diana       | Erwin      | 5WN     | M      | 5               | N                        | N                         | Jersey                                 |     |      |          |     |     | Jean Oneal    Christopher Richey    Lawrence Baca    Nan Smith    Joy Schroeder           |       |                  |
| 93979322378209 | Daniel      | Anderson   | 5CC     | F      | 1               | N                        | None                      | Tunisia                                |     |      |          |     |     | Harrison Mcwhirter    Magaly Drumheller    Aaron Shields    Elmer Pollard    David Ross   |       |                  |
| 43045588093925 | Gina        | Hunt       | 5QJ     | M      | 5               | NN                       | None                      | Congo (the Democratic Republic of the) |     |      |          |     |     | Joy Schroeder    Harrison Mcwhirter    Gladys Young    Gladys Young    Amy Plummer        |       |                  |
| 10745104369777 | Bobbi       | Kukauskas  | 5PI     | M      | 2               | NN                       | None                      | Moldova (the Republic of)              |     |      |          |     |     | Dennis Hohlstein    Martin Ashe    Jody Young    Genevieve Tomes    Joe Martel            |       |                  |
| 69022339103281 | Nan         | Smith      | 5ZJ     | F      | 1               | NN                       | None                      | Grenada                                |     |      |          |     |     | Wilda Millerd    Linda Robinson    Scotty Foor    Harrison Mcwhirter    Teresa Tolman     |       |                  |
| 78454741425812 | Laverne     | Barton     | 5BE     | F      | 2               | NN                       | None                      | Sao Tome and Principe                  |     |      |          |     |     | Leland Fisher    Thomas Suggs    Genevieve Tomes    Lisa Mosier    Kelly Anderson         |       |                  |
| 83277005661465 | Magaly      | Drumheller | 5GF     | M      | 1               | NN                       | None                      | Hungary                                |     |      |          |     |     | Megan Curtis    Kay Roland    William Dunn    Jean Mejorado    Dominque Lewis             |       |                  |
| 99579922032182 | Laila       | Donnelly   | 5YK     | M      | 3               | NN                       | None                      | Virgin Islands (U.S.)                  |     |      |          |     |     | Billy Nevill    Alexander Johnson    Cassandra Shirk    Scotty Foor    Thelma Foster      |       |                  |
| 81462836614748 | Christopher | Richey     | 5SQ     | M      | 1               | NN                       | None                      | Virgin Islands (British)               |     |      |          |     |     | Robert Wright    William Waterhouse    James Reynolds    Lawrence Baca    Kyle Gallaway   |       |                  |
| 62639474241336 | Silvia      | Kempker    | 5RV     | M      | 4               | NN                       | None                      | Gibraltar                              |     |      |          |     |     | Angelia Morris    Johnny Brown    Nancy Diaz    Louise Trammel    James Numbers           |       |                  |
| 12497891798954 | Jennifer    | Dawson     | 5ZO     | F      | 2               | NN                       | None                      | Canada                                 |     |      |          |     |     | Karen Hurst    Silvia Kempker    Nan Smith    Laila Donnelly    Margaret Curry            |       |                  |
| 58906276968411 | Christopher | Pettis     | 5QD     | M      | 1               | NN                       | None                      | Tanzania, United Republic of           |     |      |          |     |     | Dominque Lewis    Yoshiko Burnside    Jerry Wright    Patrick Travis    Carol Diaz        |       |                  |

  


