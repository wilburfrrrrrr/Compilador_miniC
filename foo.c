/********************************************************
 * foo.c
 * Compiladores 20231
 * Ingenieria de Sistemas y Computacion - UTP
 *
 * Este es un simple archivo en C que debe ser compilado
 * con el compilador de MiniC.
 ********************************************************
*/

/*
    Prototipos para algunas librerias estandar de C
    (el codigo las llama directamente)
*/
extern int printf(char *str, ...);
extern char *malloc(int size);
extern int free(char *ptr);

/*
    Prueba a variable externa. Cuantas veces llamamos a
    la funcion printf()
*/
extern int stuff_count;

// Incremente esta variable global
extern int increment_stuff_count();

/*
    Prueba a variable global. Cuantas veces hemos llamado
    a la funcion fib()
*/
int fib_count;

// Funcion fibonacci: Prueba una bifurcacion simple y recursion
static int fib(int n) {
    fib_count += 1;
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}

/*
    Solo un envolvimiento para mostrar facilmente el
    funcionamiento de la funcion fib()
*/
static int show_fib(int n) {
    printf("fin(%d) es %d.\n", n, fib(n));
    return 0;
}

// Prueba de puntero y tipo char
static int set_a(char *c) {
    *c = 'a';
    return 0;
}

// Prueba de literal String y devolucion de char *.
static char *get_literal() {
    return "blah bla blah\n";
}

// Programa principal que ejecuta las pruebas
int main(int argc, char **argv) {
    char c;
    int i;

    c = 'h';

    // Prueba asignaciones multiples
    fib_count = stuff_count = 0;

    /*
        Prueba el paso de argumentos de linea de comandos,
        punteros/arreglos, para bucles.
    */
    printf("Mi noimbre de ejecucion es %s.\n", *argv);
    for (i = 0; i < argc; i += 1) {
        printf("  argv[%d] es: %s   "
               "argv[%d][0] es: %c\n", i, argv[i], argv[i][0]);
        increment_stuff_count();
    }

    // Prueba de bucle while con break/continue
    i = 0;
    while (1) {
        show_fib();
        i += 1;
        if (i > 5) break;
        else continue;
    }
    stuff_count = stuff_count * 2;

    printf("fib_count es %d.\n", fib_count);
    printf("stuff_count es %d.\n", stuff_count);

    printf("antes set_a(&c), c == '%c'\n", c);

    // Prueba de direccion operador (&)
    set_a(&c);

    {
        // Prueba de coercion de tipos char-int e int-char
        int a;
        char b;
        int c;

        /*
            Note que es aritmetica en complemento de dos, es un
            int de 32-bit consistente de todo 1s.

            (Esto tambien es una prueba del '-' unario)
        */
        a = -1;

        /*
            La siguiente linea levanta un warning del compilador, ya
            que un int de 32-bit con signo esta siendo truncado a un 
            char de 8-bits
        */
        b = a;

        c = b;

        printf("  a = %d\n", a);
        printf("  b = %d\n", b);
        printf("  c = %d\n", c);
    }

    /*
        Tenga en cuenta ahora que el alcance de c está en el alcance principal de la función, 
        no en el alcance de la declaración compuesta anterior.
        Esta prueba asegura que la dirección y el contenido de c no cambiaron durante la 
        ejecución de la instrucción compuesta.
    */
    printf("despues set_a(&c), c == '%c'\n", c);

    printf("get_literal() = %s\n", get_literal());

    // Ejemplo de indexación de puntero a través de matriz.
    printf("get_literal()[3] = %c\n", get_literal()[3]);

    {
        /*
            Prueba de construccion de un string usando asignacion
            via indice de arreglo de un puntero char. El buffer
            es dinamicamente localizado.
        */
        char *c;

        c = malloc(30);
        c[0] = 'h';
        c[1] = 'i';
        c[2] = 0;
        printf("string es: %s\n", c);
        free(c);
    }
    return 0;
}