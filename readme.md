This project is about solving a hilbert's hotel and optimize algorithm

--! also in node class <left --> previous>, <right --> next>



Now I created function to handle the **inf buses that contains inf guests**
which handle by calculate primes number:
1. move all existing guest into 2^n rooms no.
2. move the guests in 1st bus in to 3^n rooms no.
    move the guests in 2nd bus in to 5^n rooms no.
    and so on...

in this way guest will never goes to the same room of each other
hotel.py not handled
_hotel.py using Sieve of Eratosthenes to calculate 1 to n primes
_hotel_2.py using normal prime calculate

### How to predict upper bound of prime 
Theorem 3 in Rosser and Schoenfeld 1962
(3.13)
