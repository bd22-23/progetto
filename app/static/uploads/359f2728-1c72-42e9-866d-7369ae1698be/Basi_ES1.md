## Query Prima esercitazione Basi

1. Trovare il nome della nazione che ha come capitale 'Baku':

   ```sql
   SELECT country.name FROM country JOIN city ON city.id = country.capital AND city.name = 'Baku';
   ```

   Azerbaijan

2. Anno di indipendenza della nazione in cui si trova la città 'Taizz':

   ```sql
   SELECT country.indepyear FROM city JOIN country ON city.countrycode = country.code WHERE city.name = 'Taizz';
   ```

   **Risultato:** 1918

3. Nome della capitale della nazione in cui si trova la città 'Samarkand':

   ```sql
   SELECT city.name FROM city JOIN country ON country.code = city.countrycode WHERE city.id IN (SELECT country.capital FROM city JOIN country ON city.countrycode = country.code WHERE city.name = 'Samarkand');
   ```

   **Risultato:** 

4. Numero di nazioni per cui non si conosce la data di indipendenza

   ```sql
   SELECT COUNT(*) FROM country WHERE country.indepyear IS NULL;
   ```

   **Risultato:** 47

5. Trovare il numero di lingue ufficiali che sono parlate nella regione Southeast Asia

   ```sql
   SELECT COUNT(DISTINCT countrylanguage.language) FROM countrylanguage JOIN country ON country.code = countrylanguage.countrycode WHERE country.region = 'Southeast Asia' AND isofficial;
   ```

   **Risultato:** 10

6. Contare le forme di governo in cui compare la parola Republic

   ```sql
   SELECT COUNT(DISTINCT governmentform) FROM country WHERE country.governmentform ~ 'Republic';
   ```

   **Risultato:** 5

7. Numero delle nazioni in cui tutte le lingue parlate sono non ufficiali

   ```sql
   SELECT COUNT(*) FROM country WHERE country.code NOT IN (SELECT DISTINCT country.code FROM country JOIN countrylanguage ON country.code = countrylanguage.countrycode WHERE countrylanguage.isofficial);
   ```

   **Risultato:** 49

8. Trovare due citta' con lo stesso nome di cui una e' capitale di una nazione e appartengono allo stesso continente. Restituire il nome comune di tali citta' e il nome della/delle nazione/i a cui appartengono

   ```sql
   ```

   

9. Trovare la media dei massimi prodotti interni lordi nei vari continenti

   ```sql
   SELECT AVG(prodottiInterni) FROM(SELECT MAX(gnp) AS prodottiInterni FROM country GROUP BY continent) AS t;
   ```

   **Risultato:** 2239394.142857142857





## Esame di prova 28 Gennaio 2021

1. Nome pizze in cui almeno un ingrediente ha quantità magazzino uguale a 0

   ```sql
   SELECT Pizze.nome FROM Pizze 
   NATURAL JOIN Ricette 
    JOIN Ingredienti ON Ricette.codIngrediente = Ingredienti.codIngrediente 
   WHERE Ingredienti.quantitaMagazzino = 0;
   ```

2. Nome e prezzo pizze che contengono sia ricuola che pom. freschi

   ```sql
   SELECT Pizze.nome, Pizze.prezzo FROM Pizze 
   JOIN Ricette r1 USING(codPizza) 
   JOIN Ricette r2 USING(codPizza)
   JOIN Ingredienti i1 ON r1.codIngrediente = i1.codIngrediente
   JOIN Ingredienti i2 ON r2.codIngrediente = i2.codIngrediente
   WHERE i1.nome = 'Rucola' AND i2.nome = "Pom. Freschi";
   ```

3. Per ogni pizza trovare nome e quante volte sono state ordinate da leo ortolani.

   ```sql
   SELECT Pizze.nome,
   FROM Pizze COUNT(Ordine.codOrdini)
   FROM Pizze RIGHT JOIN Ordini USING(codPizza)
   GROUP BY Pizza.codPizza, Pizza.nome
   ```



Per ogni area, trovare il nome e il numero dei progetti del manager (o dei manager) che coordina il numero massimo di dipendenti. Se un dipendente occorre in piu` progetti deve essere contato una sola volta e il manager non coordina se stesso.

```sql
SELECT M.Area, P.nome, COUNT(P.cod) FROM Progetti P
JOIN Manager M ON P.Responsabile = M.Cod
JOIN Staff S USING(Cod)
JOIN Dipendenti D ON S.Id = D.Id
GROUP BY M.area, P.nome
HAVING COUNT(D.id) = (SELECT MAX(y.num) 
					FROM (SELECT Progetti.name, COUNT(*) c FROM Dipendenti DP
					JOIN Staff SP ON SP.Id = DP.Id
					WHERE M.Cod <> DP.Id
					GROUP BY Progetti.name) y)
```



