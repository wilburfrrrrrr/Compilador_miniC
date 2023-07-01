/*******************************************************************
 * foo_lib.c
 * Compiladores 20231
 * Ingenieria de Sistemas y Computacion - UTP
 *
 * Contiene funciones/variables libreria externa para foo.c
 *******************************************************************
*/

// Prueba varible global.
int stuff_count;

/* 
    Prueba de definición de función estática, se asegura
    de que no entre en conflicto con fib() definido en foo.c.  
*/
static int fib() {
  return stuff_count += 1;
}

// Incremento variable global.
int increment_stuff_count() {
  fib();
  return 0;
}
