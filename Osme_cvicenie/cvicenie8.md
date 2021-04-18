## Cvičenie 8 - Synchrónne vs asynchrónne programovanie

### Popis aplikácie

- aplikácia simuluje pripojenie do existujúcej PostgresSQL databázy a 
  číta synchrónne a asynchrónne dáta z danej databázy pomocou niekoľkých
  SELECT príkazov
- počas behu aplikácie v ľubovoľnom režime sa spočítavajú počet riadkov, 
, ktoré sa vrátia z databázy a takisto aj čas behu aplikácie
    
- databáza bola vytvorená špeciálne pre danú úlohu, čiže po uplynutí 10 dni
bude vymazaná
  
#### Synchrónna verzia

 - aplikácia začne svoj beh vytvorením pripojenia k databáze pomocou 
   prihlasovacích údajov, ktoré sú zadane ručne v kóde.
 - ďalej vytvorime pole SQL Select príkazov, ktoré budu posielané do databázy 

- následne pošleme každý prikáž do databázy a spočítame, vypíšeme 
  jednotlive pola z databázy.
- po odosielaniu všetkých príkazov vypíšeme počet vrátených poli z databázy a 
vypočítame dobu trvania behu programu
  

 Výstup synchrónnej aplikácie:
 ```text
Database opened successfully
-------------------------------
(1, 'Lord of Rings 1', 2)
(3, 'Typescript quickly', 2)
(7, 'Pro Angular 9', 2)
(4, 'Java from EPAM', 4)
(5, 'Java 9 Dependency Injection', 5)
(6, 'Mastering Java 11', 7)
(8, 'Effective Typescript', 11)
(9, 'Angular In Action', 4)
(10, 'Learning Angular', 9)
(4, 'Java from EPAM', 4)
(9, 'Angular In Action', 4)
(5, 'Java 9 Dependency Injection', 5)
(6, 'Mastering Java 11', 7)
(10, 'Learning Angular', 9)
(8, 'Effective Typescript', 11)
(1, 'Lord of Rings 1', 2)
(3, 'Typescript quickly', 2)
(7, 'Pro Angular 9', 2)
(8, 'Effective Typescript', 11)
(1, 'Lord of Rings 1', 2)
(3, 'Typescript quickly', 2)
(7, 'Pro Angular 9', 2)
(4, 'Java from EPAM', 4)
(5, 'Java 9 Dependency Injection', 5)
(6, 'Mastering Java 11', 7)
(8, 'Effective Typescript', 11)
(9, 'Angular In Action', 4)
(10, 'Learning Angular', 9)
(4, 'Java from EPAM', 4)
(9, 'Angular In Action', 4)
(5, 'Java 9 Dependency Injection', 5)
(6, 'Mastering Java 11', 7)
(10, 'Learning Angular', 9)
(8, 'Effective Typescript', 11)
(1, 'Lord of Rings 1', 2)
(3, 'Typescript quickly', 2)
(7, 'Pro Angular 9', 2)
(8, 'Effective Typescript', 11)
Rows count:  38

Total elapsed time for sync_program: 1.01

```

#### Asynchrónna verzia

 - používa taky istý princíp fungovania, ako aj synchrónna verzia
 - všetky volania sa vykonávajú asynchrónne
     
 Výstup asynchrónnej aplikácie:
 ```
Database opened successfully
-------------------------------
<Record id=1 name='Lord of Rings 1' count=2>
<Record id=3 name='Typescript quickly' count=2>
<Record id=7 name='Pro Angular 9' count=2>
<Record id=4 name='Java from EPAM' count=4>
<Record id=5 name='Java 9 Dependency Injection' count=5>
<Record id=6 name='Mastering Java 11' count=7>
<Record id=8 name='Effective Typescript' count=11>
<Record id=9 name='Angular In Action' count=4>
<Record id=10 name='Learning Angular' count=9>
<Record id=4 name='Java from EPAM' count=4>
<Record id=9 name='Angular In Action' count=4>
<Record id=5 name='Java 9 Dependency Injection' count=5>
<Record id=6 name='Mastering Java 11' count=7>
<Record id=10 name='Learning Angular' count=9>
<Record id=8 name='Effective Typescript' count=11>
<Record id=1 name='Lord of Rings 1' count=2>
<Record id=3 name='Typescript quickly' count=2>
<Record id=7 name='Pro Angular 9' count=2>
<Record id=8 name='Effective Typescript' count=11>
<Record id=1 name='Lord of Rings 1' count=2>
<Record id=3 name='Typescript quickly' count=2>
<Record id=7 name='Pro Angular 9' count=2>
<Record id=4 name='Java from EPAM' count=4>
<Record id=5 name='Java 9 Dependency Injection' count=5>
<Record id=6 name='Mastering Java 11' count=7>
<Record id=8 name='Effective Typescript' count=11>
<Record id=9 name='Angular In Action' count=4>
<Record id=10 name='Learning Angular' count=9>
<Record id=4 name='Java from EPAM' count=4>
<Record id=9 name='Angular In Action' count=4>
<Record id=5 name='Java 9 Dependency Injection' count=5>
<Record id=6 name='Mastering Java 11' count=7>
<Record id=10 name='Learning Angular' count=9>
<Record id=8 name='Effective Typescript' count=11>
<Record id=1 name='Lord of Rings 1' count=2>
<Record id=3 name='Typescript quickly' count=2>
<Record id=7 name='Pro Angular 9' count=2>
<Record id=8 name='Effective Typescript' count=11>
Rows count:  38

Total elapsed time for async_program: 1.20
```

#### Záver
 - z ukážky je vidieť ze asynchrónny program je o trosku pomalší, 
 ako synchrónny, pretože čítanie z databázy pri malom množstve dat nie
   je dlho vykonávajúca sa operácia, okrem toho, čítanie dat nie je možne 
   kým sa neotvorí spojenie z databázou, čiže pri asynchrónnom programe
   strácame čas na prepínanie úloh, ktoré sú aj tak zablokované pripojením 
   do databázy
 - samozrejme pri veľmi rozsiahlej databáze a pri vykonaní zložitých operácii
   asynchrónny program by sa vykonal oveľa rýchlejšie ak by sa to tykalo 
   vyberania údajov, ktoré nepotrebuje synchronizácie databázy
 - pri asynchrónnom programe, ktorý by menil dáta v databáze 
   (Insert, Update Delete) by sme nezískali veľku časovú výhodu v porovnaní zo
   synchrónnym pretože pri vytvorení transakcie ostatne príkazy by museli 
   čakať na dokončenie tejto transakcie, preto pri prací z databázami 
   asynchrónne programovanie sa vyskytuje nie veľmi často.