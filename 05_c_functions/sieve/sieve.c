// sieve.c
#include <stdlib.h>
#include <string.h>
#include <math.h>

int sieve(int n, int *out) {
    char *prime = (char*)malloc(n+1);
    memset(prime, 1, n+1);
    prime[0] = prime[1] = 0;

    int limit = (int)sqrt((double)n);
    for (int p = 2; p <= limit; p++) {
        if (prime[p]) {
            for (int multiple = p*p; multiple <= n; multiple += p) {
                prime[multiple] = 0;
            }
        }
    }

    int count = 0;
    for (int i = 2; i <= n; i++) {
        if (prime[i]) out[count++] = i;
    }

    free(prime);
    return count;
}
